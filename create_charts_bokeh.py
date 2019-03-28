# min python>=3.6
# pip install bokeh pandas

import json

from datetime import datetime, timedelta

import pandas as pd
import pytz

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, Range1d, DatetimeTickFormatter
from bokeh.transform import factor_cmap
from bokeh.embed import json_item


SITES = ['reddit', 'ard']

def create_chart(server):

    with open(f'{server}.log') as csv_file:
        speed_data = pd.read_csv(csv_file, sep=' ', header=None, names=['site', 'timestamp', 'speed'], parse_dates=['timestamp'])
    
    speed_data.loc[speed_data.site == 'tagesschau', 'site'] = 'ard'

    timeindexed = speed_data.set_index(pd.DatetimeIndex(speed_data['timestamp']))
    grouped = timeindexed.groupby(['site', pd.Grouper(freq='2h')])
    grouped = grouped.describe().reset_index()

    # Offset to actually have the timestamp in the middle of the 2h timewindow
    grouped['timestamp'] = grouped['timestamp'] + pd.DateOffset(hours=1)
    reddit_grouped = grouped[grouped['site'] == 'reddit']
    ard_grouped = grouped[grouped['site'] == 'ard']

    output_file(f"{server}.html")

    raw_data_source = ColumnDataSource(speed_data)
    avg_data_source_reddit = ColumnDataSource(reddit_grouped)
    avg_data_source_ard = ColumnDataSource(ard_grouped)

    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    week_ago = now - timedelta(days=7)

    chart = figure(
        title=f'Download Speed from {server}', x_axis_type="datetime", height=500, width=800, tools="pan,wheel_zoom,box_zoom,reset",
        y_range=Range1d(0, int(speed_data['speed'].max() * 1.1), bounds=(0,int(speed_data['speed'].max() * 1.1))),
        x_range=Range1d(week_ago, now, bounds=(speed_data['timestamp'].min(), now)),
        sizing_mode='scale_width'
    )

    chart.yaxis[0].formatter = NumeralTickFormatter(format="0.000b")
    chart.yaxis.axis_label = "downloaded per second"

    chart.xaxis[0].formatter = DatetimeTickFormatter(days=['%Y-%m-%d'])
    chart.xaxis.axis_label = "date (UTC)"

    scatter = chart.scatter(x='timestamp', y='speed', source=raw_data_source, color=factor_cmap('site', ['red', 'blue'], SITES), legend="site", fill_alpha=0.1, line_alpha=0)
    line_reddit = chart.line(x='timestamp_', y='speed_mean', source=avg_data_source_reddit, line_color='red', legend="reddit average", line_dash='dotted', line_width=3)
    line_ard = chart.line(x='timestamp_', y='speed_mean', source=avg_data_source_ard, line_color='blue', legend="ard average", line_dash='dashed', line_width=3)

    chart.add_tools(HoverTool(
        tooltips=[
            ( 'date',   '@timestamp{%Y-%m-%d %H:%M}' ),
            ( 'speed', '@speed{0.000b}/s' )
        ],

        formatters={
            'timestamp': 'datetime'
        },
        renderers=[scatter],
        toggleable= False
    ))

    chart.add_tools(HoverTool(
        tooltips=[
            ( 'date',   '@timestamp_{%Y-%m-%d %H:%M}' ),
            ( 'speed', '@speed_mean{0.000b}/s' )
        ],

        formatters={
            'timestamp_': 'datetime'
        },
        renderers=[line_reddit, line_ard],
        toggleable= False
    ))

    chart.legend.location = 'top_center'
    chart.legend.orientation = 'horizontal'
    new_legend = chart.legend[0]
    chart.legend[0].plot = None
    chart.add_layout(new_legend, 'below')

    chart.legend.click_policy = 'hide'

    save(chart)
    with open(f'{server}.json', 'w') as json_file:
        json.dump(json_item(chart), json_file)


create_chart('hetzner')
create_chart('home')
# min python>=3.6
# pip install bokeh pandas

import json

import pandas as pd

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, Range1d, DatetimeTickFormatter
from bokeh.transform import factor_cmap
from bokeh.embed import json_item


SITES = ['reddit', 'tagesschau']

def create_chart(server):

    with open(f'{server}.log') as csv_file:
        speed_data = pd.read_csv(csv_file, sep=' ', header=None, names=['site', 'timestamp', 'speed'], parse_dates=['timestamp'])

    timeindexed = speed_data.set_index(pd.DatetimeIndex(speed_data['timestamp']))
    grouped = timeindexed.groupby(['site', pd.Grouper(freq='2h')])
    grouped = grouped.describe().reset_index()

    # Offset to actually have the timestamp in the middle of the 2h timewindow
    grouped['timestamp'] = grouped['timestamp'] + pd.DateOffset(hours=1)
    reddit_grouped = grouped[grouped['site'] == 'reddit']
    tagesschau_grouped = grouped[grouped['site'] == 'tagesschau']

    output_file(f"{server}.html")

    raw_data_source = ColumnDataSource(speed_data)
    avg_data_source_reddit = ColumnDataSource(reddit_grouped)
    avg_data_source_tagesschau = ColumnDataSource(tagesschau_grouped)

    chart = figure(
        title=f'Download Speed from {server}', x_axis_type="datetime", height=500, width=800, tools="pan,wheel_zoom,box_zoom,reset",
        y_range=Range1d(0, int(speed_data['speed'].max() * 1.1), bounds=(0,int(speed_data['speed'].max() * 1.1))),
        sizing_mode='scale_width'
    )

    chart.yaxis[0].formatter = NumeralTickFormatter(format="0.000b")
    chart.yaxis.axis_label = "downloaded per second"

    chart.xaxis[0].formatter = DatetimeTickFormatter(days=['%Y-%m-%d'])
    chart.xaxis.axis_label = "date"

    scatter = chart.scatter(x='timestamp', y='speed', source=raw_data_source, color=factor_cmap('site', ['red', 'blue'], SITES), legend="site", fill_alpha=0.2, line_alpha=0.2)
    line_reddit = chart.line(x='timestamp_', y='speed_mean', source=avg_data_source_reddit, line_color='red', legend="reddit average", line_dash='dotted', line_width=3)
    line_tagesschau = chart.line(x='timestamp_', y='speed_mean', source=avg_data_source_tagesschau, line_color='blue', legend="tagesschau average", line_dash='dashed', line_width=3)

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
        renderers=[line_reddit, line_tagesschau],
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
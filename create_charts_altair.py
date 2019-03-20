# python >= 3.6
# pip install pandas altair selenium
# also make chromedriver available in PATH: https://sites.google.com/a/chromium.org/chromedriver/home


import altair as alt
import pandas as pd

def create_chart(site):

    with open(f'{site}.log') as csv_file:
        speed_data = pd.read_csv(csv_file, sep=' ', header=None, names=['site', 'timestamp', 'speed'], parse_dates=['timestamp'])

    base = alt.Chart(speed_data, width=800)

    brush = alt.selection(type='interval', encodings=['x'])

    scatter = base.mark_point(size=15).encode(
        x=alt.X('timestamp:T', axis=alt.Axis(title='date'), timeUnit='yearmonthdatehoursminutes'),
        y=alt.Y('speed:Q', axis=alt.Axis(format='~s', title='download speed (bytes/s)')),
        color=alt.Color('site', scale=alt.Scale(domain=['reddit', 'tagesschau'], range=['red', 'blue'])),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7))
    ).add_selection(
        brush
    )

    reddit_line = base.mark_rule(color='red').encode(
        y='mean(speed):Q',
        size=alt.SizeValue(2)
    ).transform_filter(
        alt.FieldEqualPredicate(field='site', equal='reddit')
    ).transform_filter(
        brush
    )

    tagesschau_line = base.mark_rule(color='blue').encode(
        y='mean(speed):Q',
        size=alt.SizeValue(2)
    ).transform_filter(
        alt.FieldEqualPredicate(field='site', equal='tagesschau')
    ).transform_filter(
        brush
    )
    
    chart = alt.layer(scatter, reddit_line, tagesschau_line, data=speed_data)
    chart.configure(numberFormat='~s').save(f'{site}.html')

create_chart('hetzner')
create_chart('home')
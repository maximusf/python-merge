import pandas as pd

# lists to hold column names and year labels
precips = []
yearnames = []

for i in range(2009, 2027, 1):
    filename = 'noaa' + str(i) + '.csv'
    yearcol = 'y' + str(i)
    precipcol = 'precip' + str(i)
    highcol = 'high' + str(i)
    lowcol = 'low' + str(i)

    df = pd.read_csv(filename, header=0,
                     names=['station','name','elevation','lat','long',yearcol,
                            'mmdd',precipcol,highcol,lowcol])

    # filter out bad precipitation readings
    df = df[df[precipcol] != -9999]

    # limit to summer months (June, July, August)
    df = df[df['mmdd'].str.contains('06/|07/|08/')]

    # drop unused columns
    df.drop(['station','name','elevation','lat','long'], axis=1, inplace=True)

    if i == 2009:
        allweather = df
        precips = [precipcol]
    else:
        allweather = allweather.merge(df, on='mmdd', how='outer')
        precips.append(precipcol)

    yearnames.append(str(i))

import plotly.express as px

fig = px.imshow(allweather[precips], y=allweather['mmdd'], x=yearnames,
                color_continuous_scale='blues',
                labels=dict(x='Year', y='Month/Day', color='Precipitation (inches)'))

fig.update_layout(title='')

# get just the plotly div/script (not a full HTML page)
chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

# build the final HTML with descriptive text and NOAA link
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Summer Storms in Columbia</title>
</head>
<body>
    <h1>Summer Storms in Columbia, SC</h1>
    <p>
        The visualization below shows the amount of precipitation recorded at the USC station by the
        <a href="https://www.ncdc.noaa.gov/" target="_blank">National Oceanic and Atmospheric Administration</a>
        during June, July, and August of each year from 2009 to 2026.
    </p>
    <p>
        Summer thunderstorms are a defining feature of Columbia's climate. The heatmap reveals that
        rainfall is often concentrated in short, intense bursts rather than spread evenly across the season.
        Some years, like 2015, saw notably heavy downpours during certain stretches of summer.
    </p>
    {chart_html}
</body>
</html>
"""

with open('precip_heatmap.html', 'w') as f:
    f.write(html_content)

print('Done! Written to precip_heatmap.html')

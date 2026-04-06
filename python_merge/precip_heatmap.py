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

fig.write_html('precip_heatmap.html')
print('Done! Written to precip_heatmap.html')

import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output


#Inserting dataset
energy_data = pd.read_csv('E:/ModifiedDownloads/owid-energy-data.csv' )

#Isolating all the countries we might need alongside other usefull columns (year,iso,etc). Also choosing only 1 continent column since there are more. 
energy_data_country = energy_data[energy_data['country'].isin([
    'Rwanda', 'Panama', 'Zimbabwe', 'Chile', 'Greece', 'Sao Tome and Principe', 'Switzerland', 'Sierra Leone', 
    'Croatia', 'Senegal', 'North Korea', 'Syria', 'Tanzania', 'Chad', 'Dominica', 'Yemen', 'Kiribati', 'Russia', 
    'Botswana', 'Burkina Faso', 'Niue', 'Bulgaria', 'Bermuda', 'Saint Pierre and Miquelon', 'Solomon Islands', 
    'Sudan', 'Belarus', 'Australia', 'Kyrgyzstan', 'Martinique', 'Turkmenistan', 'Samoa', 'South Sudan', 
    'Trinidad and Tobago', 'Bhutan', 'Greenland', 'United States', 'Guadeloupe', 'Hong Kong', 'Kenya', 
    'Azerbaijan', 'Liberia', 'Tajikistan', 'Niger', 'Nicaragua', 'Gibraltar', 'Austria', 'Iran', 'Congo', 
    'Guam', 'Zambia', 'Djibouti', 'El Salvador', 'Indonesia', 'West Germany', 'Turks and Caicos Islands', 
    'Guyana', 'Spain', 'Angola', 'Hungary', 'India', 'Haiti', 'China', 'Mali', 'Singapore', 'Lithuania', 
    'Faroe Islands', 'Mauritania', 'Bolivia', 'Iceland', 'Argentina', 'Bahrain', 'Western Sahara', 'Uruguay', 
    'Guatemala', 'Mauritius', 'Guinea', 'Montenegro', 'Namibia', 'Poland', 'Ukraine', 'Sweden', 'South Korea', 
    'Jordan', 'Bahamas', 'Maldives', 'Vietnam', 'Dominican Republic', 'Saudi Arabia', 'Burundi', 'Jamaica', 
    'Wake Island (EIA)', 'Honduras', 'Cuba', 'Egypt', 'Pakistan', 'Tuvalu', 'Madagascar', 'Turkey', 'East Germany', 
    'Ghana', 'Lebanon', 'French Guiana', 'Vanuatu', 'Gabon', 'American Samoa', 'Kazakhstan', 'Saint Vincent and the Grenadines', 
    'Myanmar', 'Czechia', 'Albania', 'Equatorial Guinea', 'Mexico', 'Democratic Republic of Congo', 'Falkland Islands', 
    'Norway', 'Papua New Guinea', 'Eswatini', 'Antigua and Barbuda', 'Brunei', 'Ethiopia', 'Guinea-Bissau', 
    'New Caledonia', 'Puerto Rico', 'Mongolia', 'Cameroon', 'Oman', 'Romania', 'Palestine', 'New Zealand', 
    'Netherlands Antilles', 'Qatar', 'Cayman Islands', 'Serbia', 'Moldova', 'Georgia', 'Kuwait', 'Saint Kitts and Nevis', 
    'Malta', 'Saint Lucia', 'Benin', 'Suriname', 'Kosovo', 'Estonia', 'Armenia', 'Aruba', 
    'Cook Islands', 'French Polynesia', 'United Arab Emirates', 'Venezuela', 'Malawi', 
    'British Virgin Islands', 'Fiji', 'Macao', 'Italy', 'Nigeria', 'Cambodia', 'Nepal', 'Libya', 'Peru', 
    'Grenada', 'Barbados', 'Canada', 'Netherlands', 'Sri Lanka', 'Northern Mariana Islands', 'Eritrea', 
    'Belize', 'USSR', 'Somalia', 'Uzbekistan', 'Ireland', 'Algeria', 
    'North Macedonia', 'Denmark', 'Latvia', 'United Kingdom', 'Costa Rica', 
    'Comoros', 'Japan', 'Finland', 'Luxembourg', 'Yugoslavia', 'Philippines', 'United States Virgin Islands', 
    "Cote d'Ivoire", 'Ecuador', 'Tonga', 'Israel', 'Malaysia', 'Germany', 'East Timor', 'Iraq', 'Paraguay', 
    'Portugal', 'Tunisia', 'Montserrat', 'Nauru', 'Bangladesh', 'Togo', 'Seychelles', 'Morocco', 'Serbia and Montenegro', 
    'Thailand', 'Slovakia', 'Brazil', 'Cyprus', 'Gambia', 'Lesotho', 'Taiwan', 'Colombia', 'Belgium', 
    'Bosnia and Herzegovina', 'Laos', 'Mozambique', 'Czechoslovakia', 'Uganda', 'Cape Verde', 'Curacao', 
    'Saint Helena', 'Slovenia', 'Afghanistan', 'France', 'Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'World'
])]

#Restricting the dataset to the years 2003 to 2022(I had seen in the previous paper that was when fewer missing values appeared)
energy_data_country_year = energy_data_country[(energy_data_country['year'] >= 2003) & (energy_data_country['year'] <= 2022)]

#Leftover of data preprocessing
continents_and_world = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'South America',"Australia" 'Oceania', 'World']
continents_and_world
only_countries = energy_data_country_year[~energy_data_country_year['country'].isin(continents_and_world)]

app = dash.Dash(__name__)

#Layout of linechart. We make it so it appears with the chosen countries of Greece, Albania, Bulgaria, North Macedonia and Turkey
line_chart_layout = html.Div([
    html.H2("Primary Energy Consumption Over Time"),
    html.Label("Select Country:"),
    dcc.Dropdown(
        id='line-chart-country-dropdown',
        options=[{'label': country, 'value': country} for country in only_countries['country'].unique()],
        value=['Greece','Albania', 'Bulgaria', 'North Macedonia', 'Turkey'],
        multi=True
    ),
    html.Label("Select Year Range:"),
    dcc.RangeSlider(
        id='line-chart-year-slider',
        min=2003,
        max=2022,
        value=[2003, 2022],
        marks={str(year): str(year) for year in range(2003, 2023)}
    ),
    dcc.Graph(id='line-chart')
])

#Callback for line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('line-chart-country-dropdown', 'value'),
     Input('line-chart-year-slider', 'value')]
)
def update_line_chart(selected_countries, selected_years):
    filtered_data = only_countries[(only_countries['country'].isin(selected_countries)) &
                                   (only_countries['year'] >= selected_years[0]) &
                                   (only_countries['year'] <= selected_years[1])]
    line_chart = px.line(filtered_data, x='year', y='primary_energy_consumption', color='country',
                         title='Primary Energy Consumption Over Time')
    return line_chart

#Layout for pie char. It has a year dropdown and a country dropdown so we can choose the data we need.
pie_chart_layout = html.Div([
    html.H2("Energy Consumption by Source"),
    html.Label("Select Country:"),
    dcc.Dropdown(
        id='pie-chart-country-dropdown',
        options=[{'label': country, 'value': country} for country in only_countries['country'].unique()],
        value='Greece'
    ),
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='pie-chart-year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2003, 2023)],
        value=2022
    ),
    dcc.Graph(id='pie-chart')
])

#Callback for pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-chart-country-dropdown', 'value'),
     Input('pie-chart-year-dropdown', 'value')]
)
def update_pie_chart(selected_country, selected_year):
    filtered_data = energy_data_country_year[(energy_data_country_year['country'] == selected_country) &
                                             (energy_data_country_year['year'] == selected_year)]
    
    energy_sources = {
        'Electricity': filtered_data['electricity_share_energy'].values[0],
        'Solar': filtered_data['solar_share_energy'].values[0],
        'Hydro': filtered_data['hydro_share_energy'].values[0],
        'Wind': filtered_data['wind_share_energy'].values[0],
        'Biofuel': filtered_data['biofuel_share_energy'].values[0],
        'Other Renewables': filtered_data['other_renewables_share_energy'].values[0]
    }
    
    pie_data = pd.DataFrame(list(energy_sources.items()), columns=['Energy Source', 'Percentage'])
    
    pie_chart = px.pie(pie_data, names='Energy Source', values='Percentage',
                       title=f'Energy Consumption by Source in {selected_country} for {selected_year}')
    return pie_chart

#Layout for bubble chart. The bubble size corresponds to population and the x and y axes are gpd and greenhouse gass emmisions.Limited to the countried mentioned above
bubble_chart_layout = html.Div([
    html.H2("Greenhouse Gas Emissions vs. GDP per Capita"),
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2003, 2023)],
        value=2022
    ),
    dcc.Graph(id='bubble-chart')
])

#Callback for bubble chart
@app.callback(
    Output('bubble-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_bubble_chart(selected_year):
    filtered_data = only_countries[only_countries['year'] == selected_year].dropna(subset=['gdp', 'greenhouse_gas_emissions', 'population'])

    fig = px.scatter(
        filtered_data,
        x='gdp',
        y='greenhouse_gas_emissions',
        size='population',
        color='country',
        hover_name='country',
        size_max=60,
        title=f'Greenhouse Gas Emissions vs. GDP per Capita, {selected_year}',
        labels={'gdp': 'GDP per capita (USD)', 'greenhouse_gas_emissions': 'Greenhouse Gas Emissions (MtCO2e)'},
        log_x=True
    )
    
    return fig

#Layout for bar chart. A simple double bar chart showing energy generation vs green gass emmisions
bar_chart_layout = html.Div([
    html.H2("Greenhouse Gas Emissions vs. Electricity Generation"),
    html.Label("Select Countries:"),
    dcc.Dropdown(
        id='bar-chart-country-dropdown',
        options=[{'label': country, 'value': country} for country in energy_data_country_year['country'].unique()],
        value=['Greece','Albania', 'Bulgaria', 'North Macedonia', 'Turkey'],  
        multi=True
    ),
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='bar-chart-year-dropdown',
        options=[{'label': str(year), 'value': year} for year in sorted(energy_data_country_year['year'].unique())],
        value=2022 
    ),
    dcc.Graph(id='bar-chart')
])

#Callback for bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('bar-chart-country-dropdown', 'value'),
     Input('bar-chart-year-dropdown', 'value')]
)
def update_bar_chart(selected_countries, selected_year):
    filtered_data = energy_data_country_year[(energy_data_country_year['country'].isin(selected_countries)) &
                                             (energy_data_country_year['year'] == selected_year)]
    
    melted_data = filtered_data.melt(id_vars=['country'], value_vars=['greenhouse_gas_emissions', 'electricity_generation'],
                                     var_name='Metric', value_name='Value')
    
    fig = px.bar(
        melted_data,
        x='country',
        y='Value',
        color='Metric',
        barmode='group',
        title=f'Greenhouse Gas Emissions vs. Electricity Generation in {selected_year}',
        labels={'Value': 'MtCO2e / TWh', 'Metric': 'Metric'}
    )
    return fig


app.layout = html.Div([
    html.H1("Energy Data Dashboard", style={'text-align': 'center'}),
    
    html.Div([
        html.P("This dashboard presents energy data on Greece and neighbouring countries from 2003 to 2022.", style={'text-align': 'center'}),
        
    ]),

    line_chart_layout,
    pie_chart_layout,
    bubble_chart_layout,
    bar_chart_layout,
])

if __name__ == '__main__':
    app.run_server(debug=True)





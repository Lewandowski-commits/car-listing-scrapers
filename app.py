import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd

df = pd.read_csv('data/data.csv')

external_stylesheets = [dbc.themes.MINTY]

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col, style={"scope": "col"}) for col in dataframe.columns], style={"class": "table-active"})
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={"class": "table table-hover"})

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Row(
        dbc.Col([
            html.H1("Car Listing Agreggator"),
            html.H2("Scrape listings from otomoto.pl and olx.pl and compare!"),
            html.P('This Dash web app allows you to visualise the underlying data pulled using <a href="https://github.com/Lewandowski-commits">my Github repo</a>.'),
            html.Br(),
            html.H3("Filters pane")
        ])
    ),

    dbc.Row([
        dbc.Col([html.Label("model year"),
                 dcc.RangeSlider(id="slct-year",
                                 min=df["year"].min(),
                                 max=df["year"].max(),
                                 step=1,
                                 value=[df["year"].median(), df["year"].max()]),
                 html.P(id="year-slicer-val")], width=2),

        dbc.Col([
            html.Label("engine displacement"),
            dcc.RangeSlider(id="slct-disp",
                            min=df["disp (cm3)"].min(),
                            max=df["disp (cm3)"].max(),
                            step=100,
                            value=[df["disp (cm3)"].min(), df["disp (cm3)"].median()]),
            html.P(id="disp-slicer-val")], width=2)
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("Data visualisation"),
            html.Label("X axis"),
            dcc.Dropdown(options=[
                {'label': 'Displacement', 'value': 'disp (cm3)'},
                {'label': 'Price', 'value': 'price'},
                {'label': 'Mileage', 'value': 'mileage (km)'},
                {'label': 'Year', 'value': 'year'}
            ],
            id="fig1-x-dropdown",
            value="price"),

            html.Br(),
            html.Label("Y axis"),
            dcc.Dropdown(options=[
                {'label': 'Displacement', 'value': 'disp (cm3)'},
                {'label': 'Price', 'value': 'price'},
                {'label': 'Mileage', 'value': 'mileage (km)'},
                {'label': 'Year', 'value': 'year'}
            ],
            id="fig1-y-dropdown",
            value = "mileage (km)"
            ),

            html.Br(),
            html.Label("Colors"),
            dcc.Dropdown(options=[
                {'label': 'Fuel type', 'value': 'fuel type'},
                {'label': 'City', 'value': 'city'},
                {'label': 'Year', 'value': 'year'}
            ],
            id="fig1-colors-dropdown",
            value = "fuel type"
            )
        ], width=3),

        dbc.Col([
            dcc.Graph(id="fig1")
        ], width=9)
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("Data"),
            html.Div(id="table-id")
        ])
    ])
])


@app.callback(
    Output('table-id', 'children'),
    Output("disp-slicer-val", "children"),
    Output("year-slicer-val", "children"),
    Output("fig1", "figure"),
    Input('slct-year', 'value'),
    Input("slct-disp", "value"),
    Input('fig1-x-dropdown', 'value'),
    Input('fig1-y-dropdown', 'value'),
    Input('fig1-colors-dropdown', 'value'))
def update_figure(selected_year, selected_disp, selected_x_fig1, selected_y_fig1, selected_colors_fig1):
    dff = df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])].dropna()
    dff = dff[(dff["disp (cm3)"] >= selected_disp[0]) & (dff["disp (cm3)"] <= selected_disp[1])]

    table = generate_table(dff, max_rows=20)
    disp_slicer_text = f"Chosen range: {selected_disp} (cm3)"
    year_slicer_text = f"Chosen range: {selected_year}"
    
    fig1 = px.scatter(dff,
                      x=selected_x_fig1,
                      y=selected_y_fig1,
                      color=selected_colors_fig1,
                      marginal_y="violin",
                      marginal_x="box",
                      template="simple_white")

    fig1.update_layout(transition_duration=500)

    return table, disp_slicer_text, year_slicer_text, fig1


if __name__ == '__main__':
    app.run_server(debug=True)
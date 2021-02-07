import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('data/D07-02-2021 T15-32-44.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id="slct-year",
                 options=[{"label": str(int(item)), "value": int(item)} for item in df["year"].dropna().sort_values().unique()],
                 multi=False,
                 value=df["year"].max()),

    html.Div(id="table-id")
])


@app.callback(
    Output('table-id', 'children'),
    Input('slct-year', 'value'))
def update_figure(selected_year):
    dff = df[df["year"] == selected_year]
    
    table = generate_table(dff)

    return table


if __name__ == '__main__':
    app.run_server(debug=True)
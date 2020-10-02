import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import psycopg2
import os
from sqlalchemy import create_engine

# # ------------------------------------------------------------------------------
# # Import data from postgreSQL using psycopg2
# conn = psycopg2.connect(dbname="my_db", user=os.environ['psql_username'],\
#  password=os.environ['psql_pw'], host="localhost", port=5431) # connection string
# cur = conn.cursor() # cursor object
#
# cur.execute('''SELECT * FROM event_count''')
# for row in cur.fetchall():
#     print (row)

# Import data from postgreSQL using sqlalchemy
engine = create_engine("postgresql://user:password@localhost:5431/wow_db")

df1 = pd.read_sql_table("auctions", engine)
df2 = pd.read_sql_table("auctions_items", engine)

# dash Application
app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_item",
                 options=dropdown_op,
                 multi=False,
                 value=min(views_ts.keys()),
                 style={'width': "40%"}
                 ),
html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='views_timeseries', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='views_timeseries', component_property='figure')],
    [Input(component_id='slct_item', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The item id chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["product_id"] == option_slctd]
    s = pd.to_numeric(dff['time_period'])
    dff = dff.drop(columns=['time_period'])
    dff = dff.merge(s.to_frame(), left_index=True, right_index=True)

    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x = 'time_period',
        y = 'view_cnt',
        color = 'product_id',
        labels={'view_cnt': 'view counts',
        'time_period':'time since start (minutes)'},
        template='plotly_dark'
    )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host="10.0.0.6")
                                                             

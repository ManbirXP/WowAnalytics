import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State, MATCH, ALL

import dash  # (version 1.12.0) pip install dash
import dash_daq as daq

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import psycopg2
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

# Import data from postgreSQL using sqlalchemy
engine = create_engine("postgresql://user@password@localhost:5431/wow_db")
#df1 = pd.read_sql_table("table_auctions_info", engine)
#g1 = df1.filter(df1['name']=="Face Smasher")
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class allauctions(Base):
   __tablename__ = 'table_auctions_f1'

   auc = Column(Integer, primary_key = True)
   item = Column(Integer , ForeignKey('allitems.id'))
   bid = Column(Integer)
   buyout = Column(Integer)
   ownerRealm = Column(String)
   owner = Column(String)
#relationships
   intelligence = relationship("allitems")
class allitems(Base):
    __tablename__ = 'table_info_new_f1'

   id = Column(Integer,primary_key = True)
   name = Column(String)
   itemLevel = Column(Integer)
   requiredLevel = Column(Integer)
   itemClass = Column(Integer)
   itemSubClass = Column(Integer)
   stat = Column(Integer)
   amount = Column(Integer)
   inventoryType = Column(Integer)


#----To get all of the auctions, each auc`:tion must be assigned a unique integer ID#, which will be made the new Primary Key.
#----...for now, some auctions are eliminated from the database if they have the same owner as another auction in the DB. 

#-----We need to load two databases to work with; one from all-time to view historical data, and this second one...:
#-----...The most recent scan for every server. 
#class mostrecentauctions(Base):

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
def join():
    records = session.query(allauctions).\
        join(allitems, allitems.id == allauctions.item).all()
    for record in records:
        recordObject = {
            'name': record.intelligence.name,
            'bid': record.bid,
            'buyout': record.buyout,
            'ownerrealm': record.ownerRealm,
            'owner': record.owner,
            'auc': record.auc,
            'subclass': record.intelligence.itemSubClass,
        }
    return recordObject
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([

    html.Label('Select character level'),
    daq.NumericInput(
    min=0,
    max=110,
    value=20
    ),


    html.Label('Select character class'),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
        {'label': 'Mage', 'value': 'Mage'},
            {'label': 'Warlock', 'value': 'Warlock'},
            {'label': 'Rogue', 'value': 'Rogue'},
            {'label': 'Demon Hunter', 'value': 'Demon Hunter'},
            {'label': 'Hunter', 'value': 'Hunter'},
            {'label': 'Warrior', 'value': 'Warrior'},
            {'label': 'Paladin', 'value': 'Paladin'},
            {'label': 'Death Knight', 'value': 'Death Knight'},

            ],
        value='Mage'
    ),
html.Label('Select Realm'),
    dcc.Dropdown(
        id='serverdropdown',
        options=[
            {'label': 'BlackRock', 'value': 'BlackRock'},
            {'label': 'Antoniodas', 'value': 'Antoniodas'},
            {'label': 'Draenor', 'value': 'Draenor'},
            {'label': 'Ragnaros', 'value': 'Ragnaros'},
            ],
        value='BlackRock'
    ),

    html.Div(id='numeric-input-output'),
    html.Div(id='dd-output-container'),
    html.Div(id='ds-output-container')
])


#@app.callback(
#    dash.dependencies.Output('numeric-input-output', 'children'),
 #   dash.dependencies.Output('dd-output-container', 'children'),
  #  [dash.dependencies.Input('my-numeric-input', 'value'),
   #  dash.dependencies.Input('demo-dropdown', 'value')])

@app.callback(
        Output("ds-output-container","children"),
        Input("serverdropdown","value"))

def showresults(value):
    #playerClass = 
    result = "Best Weapon for you on {} ".format(value)
    return result

server = app.server

if __name__ == '__main__':
   server.run(debug=True, host = '0.0.0.0' )
                                                                                                                                                          145,0-1       Bot

   
    

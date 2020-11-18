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
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import psycopg2
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import join
from sqlalchemy import and_

# Stat Names
statnames = ["","","","Agility","","Intellect","","Stamina"]

# Import data from postgreSQL using sqlalchemy
engine = create_engine("postgresql://manbir:m4nb!r1123@172.31.64.131:5431/wow_db")
df1 = pd.read_sql_table("table_auctions_f1",engine)
df2 = pd.read_sql_table("table_info_new_f1",engine)
pd.set_option('display.float_format', '{:.2f}'.format)



from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class allauction(Base):
   __tablename__ = 'table_auctions_f1'

   auc = Column(Integer, primary_key = True)
   #was "item"
   item = Column(Integer, ForeignKey('table_info_new_f1.id'))
   bid = Column(Integer)
   buyout = Column(Integer)
   ownerRealm = Column(String)
   owner = Column(String)
   def __repr__(self):
        return "<User(auc='%d', item='%d', buyout='%d', ownerRealm=%s, owner=%s)>" % (
                                self.auc, self.item, self.buyout, self.ownerRealm, self.owner)
 #relationships
   intelligence = relationship("allitems" )
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

#tableofauctions = pd.read_csv('allauctions')
#tableofitems = pd.read_csv('allitems')

#Left_join = pd.merge(df1,df2,on ='id',how='left')
#Left_join

def join():
    records = session.query(allauction).\
    	join(allitems, allitems.id == allauction.item).all()
    for record in records:
        recordObject = {
            'name': record.intelligence.name,
            'bid': record.bid,
            'buyout': record.buyout,
            'ownerrealm': record.ownerRealm,
            'owner': record.owner,
            'auc': record.auc,
            'class': record.intelligence.itemClass,
            'subclass': record.intelligence.itemSubClass,
        }
records = session.query(allauction).\
        join(allitems, allitems.id == allauction.item).distinct(allauction.ownerRealm)
options = []
for col in records:
    options.append({'label':'{}'.format(col.ownerRealm), 'value':col.ownerRealm})

distinct_class = session.query(allauction).\
        join(allitems, allitems.id == allauction.item).distinct(allitems.itemClass)

options_class = []
for col in distinct_class:
    options_class.append({'label':'{}'.format(col.intelligence.itemClass), 'value':col.intelligence.itemClass})



#result = session.query(allauctions).all()
#result = session.query(allauctions).filter(allauctions.name == "Face Smasher")
#result = session.query(allweapons).filter(allweapons.name == "Face Smasher")
#for row in result:
#     print(row.bid)
#----The following section plots historical trends for a given input item.----
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#c7465d'
}
app.layout = html.Div(children=[
    html.H1(
        children='WoW Auction Intelligence',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Label('Select character level'),
    daq.NumericInput(
    id = 'levelselection',
    min=0,
    max=110,
    value=20
    ),


    html.Label('Select Item Class'),
    dcc.Dropdown(
        id='demodropdown',
        options=options_class,
        value=2
    ),

     html.Label('Select Your Realm'),
     dcc.Dropdown(
        id='serverdropdown',
        options= options, 
        value='Hellfire'
    ),

     html.Label('Select Your Class'),
dcc.Dropdown(
        id='classselection',
        options=[
            {'label': 'Mage', 'value': 'Mage'},
            {'label': 'Priest', 'value': 'Priest'},
            {'label': 'Warlock', 'value': 'Warlock'},
            {'label': 'Monk', 'value': 'Monk'},
            {'label': 'Rogue', 'value': 'Rogue'},
            {'label': 'Druid', 'value': 'Druid'},
            {'label': 'Shaman', 'value': 'Shaman'},
            {'label': 'Hunter', 'value': 'Hunter'},
            {'label': 'Demon Hunter', 'value': 'Demon Hunter'},
            {'label': 'Warrior', 'value': 'Warrior'},
            {'label': 'Paladin', 'value': 'Paladin'},
            {'label': 'Death Knight', 'value': 'Death Knight'}
        ],
        value='Mage'
    ),

    html.Div(id='numeric-input-output'),
    html.Div(id='dd-output-container'),
    html.Div(id='ds-output-container', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={})

])#, style={'marginBottom': 50, 'marginTop': 25})


@app.callback(
        Output("dd-output-container","children"),
        Input("demodropdown","value")
        )
def classvariable(demodropdown):
        itemclass = demodropdown 
        #classdisplay = "You {}".format(userclass)
        if itemclass==0:
            itemname="Consumable"
            message = "You have selected [{}] item class".format(itemname)
        elif itemclass==2:
            itemname="Weapon"
            message = "You have selected [{}] item class".format(itemname)
        elif itemclass==4:
            itemname="Armor"
            message = "You have selected [{}] item class".format(itemname)
        elif itemclass==7:
            itemname="Tradeskill"
            message = "You have selected [{}] item class".format(itemname)
        elif itemclass==9:
            itemname="Recipe"
            message = "You have selected [{}] item class".format(itemname)
        elif itemclass==15:
            itemname="Miscellaneous"
            message = "You have selected [{}] item class".format(itemname)
        return message

@app.callback(
        Output("ds-output-container","children"),
        Output("my_bee_map","figure"),
        [Input("serverdropdown","value"),
        Input("demodropdown","value"),
        #Input("classselection","value"),
        Input("levelselection","value")]
        )
def showresults(serverdropdown, demodropdown, levelselection):
    server_name = serverdropdown
    #userclass = classselection
    level = levelselection
    
    best_gear = session.query(allauction).\
        join(allitems, allitems.id == allauction.item).filter(and_(allitems.itemClass==demodropdown,allauction.ownerRealm==serverdropdown, allitems.requiredLevel<=levelselection)).first()
    #best_gear = gear.first()
    gear_info = {'Name': best_gear.intelligence.name,
            'MP': best_gear.bid,
            'SP': best_gear.buyout,
            'Seller': best_gear.owner,
            'Item Level': best_gear.intelligence.itemLevel}

    #Provides a display advising best choices for the selected class:
#    desiredStats = goodstats
#    if classSelection == "Mage":
#    goodStats = [1, 2]

    #if len(goodStats == 2):
    #goodStatsDisplay = "As a [{}], you care most about [{}], and [{}].".format(classSelection, statNames[goodStats[0]], statNames[goodStats[1]])
    #result = "As a [{}], you care most about [{}], and [{}].".format(classSelection, statNames[goodStats[0]], statNames[goodStats[1]])

    df_avg = df1.copy()
    df_avg= df_avg.groupby(['item'])[['buyout']].mean()
    df_avg.reset_index(inplace=True)
    df_avg = df_avg[df_avg['item']==best_gear.item]
    result = "The best item for a level [{}] on [{}] is [{}] with average asking price of [{}].".format(level, server_name, gear_info, (df_avg['buyout']).to_string(index=False)) 
     
    dff = df1.copy() 
    dff = dff.groupby(['item', 'buyout', 'ownerRealm'], sort=False).count()
    dff.reset_index(inplace=True)

    #dff = dff[dff['ownerRealm'] == serverdropdown]
    dff = dff[dff['item'] == best_gear.item]
    # Plotly Express
    hist_data = [dff['buyout']]
    group_labels= ['SP']
    fig = px.line(dff, y="buyout" ,labels={
                     "buyout": "Selling Price (in Game Currency)",
                     "sepal_width": "Time index",
                 },
                title="Selling Price Trend")    #fig = ff.create_distplot(hist_data,group_labels, bin_size = 350000)
    return result, fig 

server = app.server

if __name__ == '__main__':
   server.run(debug=True, host = '0.0.0.0' )





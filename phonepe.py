import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import mysql.connector
import plotly.express as px
import json
import requests 


#Creating Dataframe For Visualisation:
#Sql connecting code.
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

#Aggregated Transaction Dataframe:
cursor.execute("select * from aggregated_transaction")
table1=cursor.fetchall()
Aggregated_transaction=pd.DataFrame(table1, columns=("States","Years","Quarter",
                                                     "Transaction_type",
                                                     "Transaction_count",
                                                     "Transaction_amount"))

#Aggregated User Dataframe:
cursor.execute("select * from aggregated_user")
table2=cursor.fetchall()
Aggregated_user=pd.DataFrame(table2, columns=("States","Years","Quarter",
                                                     "Brands",
                                                     "Transaction_count",
                                                     "Percentage"))

#Map Transaction Dataframe:
cursor.execute("select * from map_transaction")
table3=cursor.fetchall()
Map_transaction=pd.DataFrame(table3, columns=("States","Years","Quarter",
                                                     "Districts",
                                                     "Transaction_count",
                                                     "Transaction_amount"))

#Map User Dataframe:
cursor.execute("select * from map_user")
table4=cursor.fetchall()
Map_user=pd.DataFrame(table4, columns=("States","Years","Quarter",
                                                     "Districts",
                                                     "RegisterdUsers",
                                                     "AppOpens"))


#Top Transaction Dataframe:
cursor.execute("select * from top_transaction")
table5=cursor.fetchall()
Top_transaction=pd.DataFrame(table5, columns=("States","Years","Quarter",
                                                     "Pincodes",
                                                     "Transaction_count",
                                                     "Transaction_amount"))

#Top User Dataframe:
cursor.execute("select * from top_user")
table6=cursor.fetchall()
Top_user=pd.DataFrame(table6, columns=("States","Years","Quarter",
                                                     "Pincodes",
                                                     "RegisteredUsers"
                                                     ))
#Aggregated Transaction:
def trans_amt_ct(df,year):
    trans_amt_cnt=df[df["Years"]==year]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="Transaction_amount",
                        title=f"Transaction Amount of {year}",
                        color_discrete_sequence=px.colors.sequential.algae_r,
                        height=650, width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(trans_amt_cnt1,x="States",y="Transaction_count",
                        title=f"Transaction Count of {year}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r,
                        height=650, width=600)
        st.plotly_chart(fig_count)
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    col1,col2=st.columns(2)
    with col1:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_amount"].min(),trans_amt_cnt1["Transaction_amount"].max()),
                                hover_name="States",title=f"Transaction Amount of {year}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    with col2:
        India_map_2=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"Transaction Count of {year}",fitbounds="locations",
                                height=600,width=600)
        India_map_2.update_geos(visible=False)
        st.plotly_chart(India_map_2)
    return trans_amt_cnt

def trans_amt_ct_Q(df,quarter):
    
    trans_amt_cnt=df[df["Quarter"]==quarter]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="Transaction_amount",
                        title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(trans_amt_cnt1,x="States",y="Transaction_count",
                        title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r
                        )
        st.plotly_chart(fig_count)
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    col1,col2=st.columns(2)

    with col1:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_amount"].min(),trans_amt_cnt1["Transaction_amount"].max()),
                                hover_name="States",title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    with col2:
        India_map_2=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",fitbounds="locations",
                                height=600,width=600)
        India_map_2.update_geos(visible=False)
        st.plotly_chart(India_map_2)
    return trans_amt_cnt

def trans_amt_ct_Tt(df,trans_type):
    
    trans_amt_cnt=df[df["Transaction_type"]==trans_type]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="Transaction_amount",
                        title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} for {trans_type}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(trans_amt_cnt1,x="States",y="Transaction_count",
                        title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} for {trans_type}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r
                        )
        st.plotly_chart(fig_count)
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    col1,col2=st.columns(2)

    with col1:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_amount"].min(),trans_amt_cnt1["Transaction_amount"].max()),
                                hover_name="States",title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} for {trans_type}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)

    with col2:
        India_map_2=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} for {trans_type}",fitbounds="locations",
                                height=600,width=600)
        India_map_2.update_geos(visible=False)
        st.plotly_chart(India_map_2)

#Aggregated user:
def trans_ct_user(df,year):
    trans_amt_cnt=df[df["Years"]==year]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
 
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="Transaction_count",
                        title=f"Aggregated User Transaction count of {year}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"Aggregated User Transaction count of {year}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt

def trans_user_ct_Q(df,quarter):
    
    trans_amt_cnt=df[df["Quarter"]==quarter]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_count=px.bar(trans_amt_cnt1,x="States",y="Transaction_count",
                        title=f"User Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r
                        )
        st.plotly_chart(fig_count)
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"User Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt

def trans_user_brand(df,brand):
    
    trans_amt_cnt=df[df["Brands"]==brand]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_count=px.bar(trans_amt_cnt1,x="States",y="Transaction_count",
                        title=f"User Brands Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt["Quarter"].min()} for {brand}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r
                        )
        st.plotly_chart(fig_count)
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"User Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt["Quarter"].min()} for {brand}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt

#Districts
def trans_amt_ct_dist(df,state):
    
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amt_cnt1,x="Districts",y="Transaction_amount",
                        title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} for {state}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(trans_amt_cnt1,x="Districts",y="Transaction_count",
                        title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} for {state}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r
                        )
        st.plotly_chart(fig_count)
    return trans_amt_cnt

def trans_amt_ct_dist_M(df,state):
    
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    col1,col2=st.columns(2)
    with col1:

        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_amount"].min(),trans_amt_cnt1["Transaction_amount"].max()),
                                hover_name="States",title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} ",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)

    with col2:
        India_map_2=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["Transaction_count"].min(),trans_amt_cnt1["Transaction_count"].max()),
                                hover_name="States",title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()} ",fitbounds="locations",
                                height=600,width=600)
        India_map_2.update_geos(visible=False)
        st.plotly_chart(India_map_2)
    
#Map User:

def trans_ct_Ruser(df,year):
    trans_amt_cnt=df[df["Years"]==year]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["RegisterdUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="RegisterdUsers",
                        title=f"Registered User count of {year}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="RegisterdUsers",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["RegisterdUsers"].min(),trans_amt_cnt1["RegisterdUsers"].max()),
                                hover_name="States",title=f"Registered User count of {year}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1) 
    return trans_amt_cnt

def trans_ct_Ruser_Q(df,quarter):
    trans_amt_cnt=df[df["Quarter"]==quarter]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["RegisterdUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amt_cnt1,x="States",y="RegisterdUsers",
                        title=f"Registered User count of {trans_amt_cnt["Years"].min()} and Quarter-{quarter}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="RegisterdUsers",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["RegisterdUsers"].min(),trans_amt_cnt1["RegisterdUsers"].max()),
                                hover_name="States",title=f"Registered User count of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt

def trans_ct_Ruser_dist(df,state):
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("Districts")[["RegisterdUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amt_cnt1,x="Districts",y="RegisterdUsers",
                        title=f"Registered User count of {trans_amt_cnt["Years"].min()} and Quarter-{trans_amt_cnt["Quarter"].min()} for {state}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
    return trans_amt_cnt
 
def trans_ct_Ruser_distM(df,state):
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["RegisterdUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()
    col1,col2=st.columns(2)
    with col1:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="RegisterdUsers",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["RegisterdUsers"].min(),trans_amt_cnt1["RegisterdUsers"].max()),
                                hover_name="States",title=f"Registered User count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt["Quarter"].min()}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
def user_App(df,year):
    trans_amt_cnt=df[df["Years"]==year]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["AppOpens"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amt_cnt1,x="States",y="AppOpens",
                        title=f"App open count of {year} ",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
    
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="AppOpens",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["AppOpens"].min(),trans_amt_cnt1["AppOpens"].max()),
                                hover_name="States",title=f"App open count of {year}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt
              
def user_App_Q(df,quarter):
    trans_amt_cnt=df[df["Quarter"]==quarter]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["AppOpens"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="AppOpens",
                        title=f"App User count of {trans_amt_cnt["Years"].min()} and Quarter-{quarter}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st .plotly_chart(fig_amount)
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="AppOpens",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["AppOpens"].min(),trans_amt_cnt1["AppOpens"].max()),
                                hover_name="States",title=f"Registered User count of year-{trans_amt_cnt['Years'].min()} and quarter-{quarter}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt 

def user_App_dist(df,state):
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("Districts")[["AppOpens"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amt_cnt1,x="Districts",y="AppOpens",
                        title=f"User App count of {trans_amt_cnt["Years"].min()} and Quarter-{trans_amt_cnt["Quarter"].min()} for {state}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)

#Top_transaction
        
def top_pin(df,state):
    
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby(str("Pincodes"))[["Transaction_count","Transaction_amount"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="Pincodes",y="Transaction_amount",
                        title=f"Transaction Amount of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        fig_amount.update_layout(xaxis_type='category')
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(trans_amt_cnt1,x="Pincodes",y="Transaction_count",
                        title=f"Transaction Count of year-{trans_amt_cnt['Years'].min()} and quarter-{trans_amt_cnt['Quarter'].min()}",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r
                        )
        fig_count.update_layout(xaxis_type='category')
        st.plotly_chart(fig_count)
    
#Top user:
def top_user_Y(df,year):
    trans_amt_cnt=df[df["Years"]==year]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["RegisteredUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="RegisteredUsers",
                        title=f"RegisteredUsers count of {year}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="RegisteredUsers",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["RegisteredUsers"].min(),trans_amt_cnt1["RegisteredUsers"].max()),
                                hover_name="States",title=f"RegisteredUsers count of {year}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)

    return trans_amt_cnt


def top_user_Q(df,quarter):
    trans_amt_cnt=df[df["Quarter"]==quarter]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("States")[["RegisteredUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amt_cnt1,x="States",y="RegisteredUsers",
                        title=f"RegisteredUsers count of {trans_amt_cnt["Years"].min()} and quarter-{quarter}",
                        color_discrete_sequence=px.colors.sequential.algae_r
                        )
        st.plotly_chart(fig_amount)
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    with col2:
        India_map_1=px.choropleth(trans_amt_cnt1, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="RegisteredUsers",color_continuous_scale="Rainbow",
                                range_color=(trans_amt_cnt1["RegisteredUsers"].min(),trans_amt_cnt1["RegisteredUsers"].max()),
                                hover_name="States",title=f"RegisteredUsers count of {trans_amt_cnt["Years"].min()} and quarter-{quarter}",fitbounds="locations",
                                height=600,width=600)
        India_map_1.update_geos(visible=False)
        st.plotly_chart(India_map_1)
    return trans_amt_cnt

def top_user_pin(df,state):
    trans_amt_cnt=df[df["States"]==state]
    trans_amt_cnt.reset_index(drop=True,inplace=True)

    trans_amt_cnt1=trans_amt_cnt.groupby("Pincodes")[["RegisteredUsers"]].sum()
    trans_amt_cnt1.reset_index(inplace=True)
    

    fig_amount=px.bar(trans_amt_cnt1,x="Pincodes",y="RegisteredUsers",
                    title=f"Registered User count of {trans_amt_cnt["Years"].min()} and Quarter-{trans_amt_cnt["Quarter"].min()} for {state}",
                    color_discrete_sequence=px.colors.sequential.algae_r
                    )
    fig_amount.update_layout(xaxis_type='category')
    st.plotly_chart(fig_amount)
    
    
#code for streamlit 
st.set_page_config(layout='wide',page_icon='🌏')
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
with st.sidebar:
    select=option_menu("Main menu",["HOME","DATA EXPLORATION","TOP CHARTS","INSIGHTS"])
if select=="HOME":
    img=Image.open('C:/Users/ayish/GuviProjects/Intro.png')
    st.image(img,width=1000,channels="RGB")
    st.title('GUIDE:')
    
    img2=Image.open('C:/Users/ayish/GuviProjects/Aggregated.png')
    st.image(img2,width=600,channels='RGB')
    
    img4=Image.open('C:/Users/ayish/GuviProjects/map1pic.png')
    st.image(img4,width=600,channels='RGB')

    img3=Image.open('C:/Users/ayish/GuviProjects/map2pic.png')
    st.image(img3,width=600,channels='RGB')
    
elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

    with tab1:
        method1=st.radio("Select the option",['Aggregated Transaction','Aggregated User'])

        if method1=="Aggregated Transaction":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("choose year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max())
            trans_amt_ct_Y=trans_amt_ct(Aggregated_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("choose Quarter",trans_amt_ct_Y["Quarter"].min(),trans_amt_ct_Y["Quarter"].max())
            trans_amt_ct_Q1=trans_amt_ct_Q(trans_amt_ct_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                trans_types=st.selectbox("Choose Transaction type",("Recharge & bill payments",
                                                                    "Peer-to-peer payments",
                                                                    "Merchant payments",
                                                                    "Financial Services",
                                                                    "Others"))
            trans_amt_ct_Tt(trans_amt_ct_Q1,trans_types)
        elif method1=="Aggregated User":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("choose year",Aggregated_user["Years"].min(),Aggregated_user["Years"].max())
            trans_ct_user1=trans_ct_user(Aggregated_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("choose Quarter",trans_ct_user1["Quarter"].min(),trans_ct_user1["Quarter"].max())
            trans_user_ct_Q1=trans_user_ct_Q(trans_ct_user1,quarters)

            col1,col2=st.columns(2)
            with col1:
                brands=st.selectbox("Choose Brand",(Aggregated_user["Brands"].unique()))
            trans_user_brand(trans_user_ct_Q1,brands)
                



    with tab2:
        method2=st.radio("Select the option",['Map Transaction','Map User'])

        if method2=="Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                M_years=st.slider("select the year",Map_transaction["Years"].min(),Map_transaction["Years"].max())
            trans_amt_ct_Y1=trans_amt_ct(Map_transaction,M_years)

            col1,col2=st.columns(2)
            with col1:
                M_quarters=st.slider("select the Quarter",trans_amt_ct_Y1["Quarter"].min(),trans_amt_ct_Y1["Quarter"].max())
            trans_amt_ct_Q2=trans_amt_ct_Q(trans_amt_ct_Y1,M_quarters)

            col1,col2=st.columns(2)
            with col1:
                districts=st.selectbox("Choose State",(Map_transaction["States"].unique()))
            trans_amt_ct_dist(trans_amt_ct_Q2,districts)
            col1,col2=st.columns(2)
            with col1:
                districts1=st.selectbox("Select State",(Map_transaction["States"].unique()))
            trans_amt_ct_dist_M(trans_amt_ct_Q2,districts1)
            
        elif method2=="Map User":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("choose the Year",Map_user["Years"].min(),Map_user["Years"].max())
            trans_ct_reguser=trans_ct_Ruser(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                M_quarters=st.slider("Select Quarter",trans_ct_reguser["Quarter"].min(),trans_ct_reguser["Quarter"].max())
            trans_ct_user_Q1=trans_ct_Ruser_Q(trans_ct_reguser,M_quarters)

            col1,col2=st.columns(2)
            with col1:
                state=st.selectbox("Choose the State",(Map_transaction["States"].unique()))
            trans_ct_Ruser_dist(trans_ct_user_Q1,state)
            col1,col2=st.columns(2)
            with col1:
                state1=st.selectbox("Select the State",(Map_transaction["States"].unique()))
            trans_ct_Ruser_distM(trans_ct_user_Q1,state1)

            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Year you want",Map_user["Years"].min(),Map_user["Years"].max())
            user_App1=user_App(Map_user,years)
            col1,col2=st.columns(2)
            with col1:
                M_quarters=st.slider("Quarter you want",user_App1["Quarter"].min(),user_App1["Quarter"].max())
            user_App_Q1=user_App_Q(user_App1,M_quarters)
            col1,col2=st.columns(2)
            with col1:
                state=st.selectbox("Enter State",(Map_transaction["States"].unique()))
            user_App_dist(user_App_Q1,state)

    with tab3:
        method3=st.radio("Select the option",['Top Transaction','Top User'])

        if method3=="Top Transaction":
            col1,col2=st.columns(2)
            with col1:
                T_years=st.slider("select year",Top_transaction["Years"].min(),Top_transaction["Years"].max())
            trans_amt_ct_Y2=trans_amt_ct(Top_transaction,T_years)
            col1,col2=st.columns(2)
            with col1:
                T_quarters=st.slider("select Quarter",trans_amt_ct_Y2["Quarter"].min(),trans_amt_ct_Y2["Quarter"].max())
            trans_amt_ct_Q3=trans_amt_ct_Q(trans_amt_ct_Y2,T_quarters)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose pincode",(Top_transaction["States"].unique()))
            top_pin(trans_amt_ct_Q3,states)
            
        elif method3=="Top User":
            col1,col2=st.columns(2)
            with col1:
                T_years=st.slider("choose year here:",Top_user["Years"].min(),Top_user["Years"].max())
            top_user_Y1=top_user_Y(Top_user,T_years)
            col1,col2=st.columns(2)
            with col1:
                T_quarters=st.slider("choose Quarter here:",top_user_Y1["Quarter"].min(),top_user_Y1["Quarter"].max())
            top_user_Q1=top_user_Q(top_user_Y1,T_quarters)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose state here:",(Top_user["States"].unique()))
            top_user_pin(top_user_Q1,states)
            

elif select=="TOP CHARTS":
    Button=st.radio("select the button",["Transaction Amount",
                                         "Transaction Count",
                                         "Registered Users",
                                         "App open"])
    if Button=="Transaction Amount":
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Maximum and Minimum Transaction Amount of Years:")
            A_T=Aggregated_transaction.groupby("Years")["Transaction_amount"].sum().reset_index().sort_values('Transaction_amount')
           # A_T_top10=A_T.nlargest(10,"Transaction_amount")
            ATam_df=pd.DataFrame(A_T)
            ATam_df.reset_index(drop=True,inplace=True)
            st.write(ATam_df)
        with col2:
            fig1=px.pie(A_T,values="Transaction_amount",names="Years",title="Graphical Representation of Years",hole=0.5)
            st.plotly_chart(fig1)
        with col1:
            st.subheader("Maximum and Minimum Transaction Amount of Quarter:")
            A_T=Aggregated_transaction.groupby("Quarter")["Transaction_amount"].sum().reset_index().sort_values('Transaction_amount')
           # A_T_top10=A_T.nlargest(10,"Transaction_amount")
            ATam_df=pd.DataFrame(A_T)
            ATam_df.reset_index(drop=True,inplace=True)
            st.write(ATam_df)
        with col2:
            fig1=px.pie(A_T,values="Transaction_amount",names="Quarter",title="Graphical Representation of Quarters",hole=0.5)
            st.plotly_chart(fig1)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 States Transaction Amount:")
            A_T=Aggregated_transaction.groupby("States")["Transaction_amount"].sum().reset_index().sort_values('Transaction_amount')
            A_T_top10=A_T.nlargest(10,"Transaction_amount")
            ATam_df=pd.DataFrame(A_T_top10)
            ATam_df.reset_index(drop=True,inplace=True)
            st.write(ATam_df)
        with col2:
            fig1=px.pie(A_T_top10,values="Transaction_amount",names="States",title="Graphical Representation of Top_10 states")
            st.plotly_chart(fig1)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Districts Transaction amount:")
            M_T=Map_transaction.groupby("Districts")["Transaction_amount"].sum().reset_index().sort_values('Transaction_amount')
            M_T_top10=M_T.nlargest(10,"Transaction_amount")
            MTam_df=pd.DataFrame(M_T_top10)
            MTam_df.reset_index(drop=True,inplace=True)
            st.write(MTam_df)
        with col2:
            fig2=px.pie(M_T_top10,values="Transaction_amount",names="Districts",title="Graphical Representation of Top_10 districts")
            st.plotly_chart(fig2)
        
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Transaction_type Transaction Amount:")
            A_TT=Aggregated_transaction.groupby("Transaction_type")["Transaction_amount"].sum().reset_index().sort_values('Transaction_amount')
            ATTam_df=pd.DataFrame(A_TT)
            ATTam_df.reset_index(drop=True,inplace=True)
            st.write(ATTam_df)
        with col2:
            fig3=px.pie(A_TT,values="Transaction_amount",names="Transaction_type",title="Graphical Representation of Transaction Type",
                        hole=0.5,color_discrete_sequence=['purple','red', 'blue', 'green','yellow'])
            st.plotly_chart(fig3)   
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Pincodes Transaction amount:")
            T_T=Top_transaction.groupby("Pincodes")["Transaction_amount"].sum().reset_index().sort_values('Transaction_amount')
            T_T_top10=T_T.nlargest(10,"Transaction_amount")
            TTam_df=pd.DataFrame(T_T_top10)
            TTam_df.reset_index(drop=True,inplace=True)
            st.write(TTam_df)
        with col2:
            fig2=px.pie(T_T_top10,values="Transaction_amount",names="Pincodes",title="Graphical Representation of Top_10 pincodes")
            st.plotly_chart(fig2)
    elif Button=="Transaction Count":
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 States Transaction Count:")
            A_T=Aggregated_transaction.groupby("States")["Transaction_count"].sum().reset_index().sort_values('Transaction_count')
            A_T_top10=A_T.nlargest(10,"Transaction_count")
            ATc_df=pd.DataFrame(A_T_top10)
            ATc_df.reset_index(drop=True,inplace=True)
            st.write(ATc_df)
        with col2:
            fig1=px.pie(A_T_top10,values="Transaction_count",names="States",title="Graphical Representation of Top_10 States")
            st.plotly_chart(fig1)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Districts Transaction Count:")
            M_T=Map_transaction.groupby("Districts")["Transaction_count"].sum().reset_index().sort_values('Transaction_count')
            M_T_top10=M_T.nlargest(10,"Transaction_count")
            MTc_df=pd.DataFrame(M_T_top10)
            MTc_df.reset_index(drop=True,inplace=True)
            st.write(MTc_df)
        with col2:
            fig2=px.pie(M_T_top10,values="Transaction_count",names="Districts",title="Graphical Representation of Top_10 districts")
            st.plotly_chart(fig2)
        
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Transaction_type Transaction Count:")
            A_TT=Aggregated_transaction.groupby("Transaction_type")["Transaction_count"].sum().reset_index().sort_values('Transaction_count')
            ATTc_df=pd.DataFrame(A_TT)
            ATTc_df.reset_index(drop=True,inplace=True)
            st.write(ATTc_df)
        with col2:
            fig3=px.pie(A_TT,values="Transaction_count",names="Transaction_type",title="Graphical Representation of Transaction Type",
                        hole=0.5,color_discrete_sequence=['red','purple', 'blue', 'green','yellow'])
            st.plotly_chart(fig3)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Pincodes Transaction count:")
            T_T=Top_transaction.groupby("Pincodes")["Transaction_count"].sum().reset_index().sort_values('Transaction_count')
            T_T_top10=T_T.nlargest(10,"Transaction_count")
            TTc_df=pd.DataFrame(T_T_top10)
            TTc_df.reset_index(drop=True,inplace=True)
            st.write(TTc_df)
        with col2:
            fig2=px.pie(T_T_top10,values="Transaction_count",names="Pincodes",title="Graphical Representation of Top_10 pincodes")
            st.plotly_chart(fig2)
    
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Brands Transaction count:")
            B_T=Aggregated_user.groupby("Brands")["Transaction_count"].sum().reset_index().sort_values('Transaction_count')
            B_T_top10=B_T.nlargest(10,"Transaction_count")
            BTc_df=pd.DataFrame(B_T_top10)
            BTc_df.reset_index(drop=True,inplace=True)
            st.write(BTc_df)
        with col2:
            fig2=px.pie(B_T_top10,values="Transaction_count",names="Brands",title="Graphical Representation of Top_10 brands")
            st.plotly_chart(fig2)
    elif Button=="Registered Users":
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 States Registered Users:")
            R_T=Map_user.groupby("States")["RegisterdUsers"].sum().reset_index().sort_values('RegisterdUsers')
            R_T_top10=R_T.nlargest(10,"RegisterdUsers")
            R_df=pd.DataFrame(R_T_top10)
            R_df.reset_index(drop=True,inplace=True)
            st.write(R_df)
        with col2:
            fig1=px.pie(R_T_top10,values="RegisterdUsers",names="States",title="Graphical Representation of Top_10 States")
            st.plotly_chart(fig1)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Districts Registered Users:")
            Rd_T=Map_user.groupby("Districts")["RegisterdUsers"].sum().reset_index().sort_values('RegisterdUsers')
            Rd_T_top10=Rd_T.nlargest(10,"RegisterdUsers")
            Rd_df=pd.DataFrame(Rd_T_top10)
            Rd_df.reset_index(drop=True,inplace=True)
            st.write(Rd_df)
        with col2:
            fig2=px.pie(Rd_T_top10,values="RegisterdUsers",names="Districts",title="Graphical Representation of Top_10 districts")
            st.plotly_chart(fig2)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Pincodes Registered Users:")
            Rp_T=Top_user.groupby("Pincodes")["RegisteredUsers"].sum().reset_index().sort_values('RegisteredUsers')
            Rp_T_top10=Rp_T.nlargest(10,"RegisteredUsers")
            Rp_df=pd.DataFrame(Rp_T_top10)
            Rp_df.reset_index(drop=True,inplace=True)
            st.write(Rp_df)
        with col2:
            fig2=px.pie(Rp_T_top10,values="RegisteredUsers",names="Pincodes",title="Graphical Representation of Top_10 pincodes")
            st.plotly_chart(fig2)
    elif Button=="App open":
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 States of App Opens:")
            ap_T=Map_user.groupby("States")["AppOpens"].sum().reset_index().sort_values('AppOpens')
            ap_T_top10=ap_T.nlargest(10,"AppOpens")
            ap_df=pd.DataFrame(ap_T_top10)
            ap_df.reset_index(drop=True,inplace=True)
            st.write(ap_df)
        with col2:
            fig1=px.scatter(ap_T_top10,x="States",y="AppOpens",color="AppOpens",title="Graphical Representation of Top_10 States")
            st.plotly_chart(fig1)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Top_10 Districts Of App Opens:")
            app_T=Map_user.groupby("Districts")["AppOpens"].sum().reset_index().sort_values('AppOpens')
            app_T_top10=app_T.nlargest(10,"AppOpens")
            app_df=pd.DataFrame(app_T_top10)
            app_df.reset_index(drop=True,inplace=True)
            st.write(app_df)
        with col2:
            fig2=px.scatter(app_T_top10,x="Districts",y="AppOpens",color="Districts",title="Graphical Representation of Top_10 districts")
            st.plotly_chart(fig2)
        
elif select=="INSIGHTS":
    img=Image.open('C:/Users/ayish/GuviProjects/pic.png')
    st.image(img,width=800,channels="RGB")
    col1,col2=st.columns(2)
    with col1:
        img1=Image.open('C:/Users/ayish/GuviProjects/1.png')
        st.image(img1,width=500,channels="RGB")
        img2=Image.open('C:/Users/ayish/GuviProjects/2.png')
        st.image(img2,width=500,channels="RGB")
        img3=Image.open('C:/Users/ayish/GuviProjects/3.png')
        st.image(img3,width=500,channels="RGB")
        img4=Image.open('C:/Users/ayish/GuviProjects/4.png')
        st.image(img4,width=500,channels="RGB")
        img5=Image.open('C:/Users/ayish/GuviProjects/5.png')
        st.image(img5,width=500,channels="RGB")
        img6=Image.open('C:/Users/ayish/GuviProjects/6.png')
        st.image(img6,width=500,channels="RGB")
    

      
#Needed Libraries
import os
import json
import pandas as pd
import mysql.connector

#Aggregated_Transaction

path1="C:/Users/ayish/GuviProjects/Phonepe/Phonepe pulse/pulse/data/aggregated/transaction/country/india/state/"
agg_trans_list=os.listdir(path1)
columns1={"States":[],"Years":[],"Quarter":[],"Transaction_type":[],"Transaction_count":[],"Transaction_amount":[]}
for state in agg_trans_list:
    cur_states=path1+state+"/"
    agg_year_list=os.listdir(cur_states)
    
    for year in agg_year_list:
        cur_year=cur_states+year+'/'
        agg_file_list=os.listdir(cur_year)

        for file in agg_file_list:
            cur_file=cur_year+file
            data=open(cur_file,'r')

            A=json.load(data)
            for i in A["data"]["transactionData"]:
                name=i["name"]
                count=i["paymentInstruments"][0]["count"]
                amount=i["paymentInstruments"][0]["amount"]
                columns1["Transaction_type"].append(name)
                columns1["Transaction_count"].append(count)
                columns1["Transaction_amount"].append(amount)
                columns1["States"].append(state)
                columns1["Years"].append(year)
                columns1["Quarter"].append(int(file.strip(".json")))
aggregated_transaction=pd.DataFrame(columns1)
aggregated_transaction['States']=aggregated_transaction['States'].str.replace('-',' ')
aggregated_transaction['States']=aggregated_transaction['States'].str.title()
aggregated_transaction['States']=aggregated_transaction['States'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
aggregated_transaction['States']=aggregated_transaction['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

#aggregate_user
path2='C:/Users/ayish/GuviProjects/Phonepe/Phonepe pulse/pulse/data/aggregated/user/country/india/state/'
agg_user_list=os.listdir(path2)
columns2={"States":[],"Years":[],"Quarter":[],"Brands":[],"Transaction_count":[],"Percentage":[]}
for state in agg_user_list:
    cur_states=path2+state+'/'
    agg_year_list=os.listdir(cur_states)
    for year in agg_year_list:
        cur_year=cur_states+year+'/'
        agg_file_list=os.listdir(cur_year)
        for file in agg_file_list:
            cur_file=cur_year+file
            data=open(cur_file,'r')

            B=json.load(data)
            try:
                for item in B['data']['usersByDevice']:
                    brand=item["brand"]
                    count=item['count']
                    percentage=item["percentage"]
                    columns2["Brands"].append(brand)
                    columns2["Transaction_count"].append(count)
                    columns2["Percentage"].append(percentage)
                    columns2["States"].append(state)
                    columns2["Years"].append(year)
                    columns2["Quarter"].append(int(file.strip(".json")))

            except:
                pass
aggregated_user=pd.DataFrame(columns2)

aggregated_user['States']=aggregated_user['States'].str.replace('-',' ')
aggregated_user['States']=aggregated_user['States'].str.title()
aggregated_user['States']=aggregated_user['States'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
aggregated_user['States']=aggregated_user['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

#Map_transaction
path3="C:/Users/ayish/GuviProjects/Phonepe/Phonepe pulse/pulse/data/map/transaction/hover/country/india/state/"
map_trans_list=os.listdir(path3)
columns3={"States":[],"Years":[],"Quarter":[],"Districts":[],"Transaction_count":[],"Transaction_amount":[]}
for state in map_trans_list:
    cur_states=path3+state+'/'
    map_year_list=os.listdir(cur_states)
    for year in map_year_list:
        cur_year=cur_states+year+'/'
        map_file_list=os.listdir(cur_year)
        for file in map_file_list:
            cur_file= cur_year+file
            data=open(cur_file,'r')
            
            C=json.load(data)
            
            for item in C['data']['hoverDataList']:
                name=item['name']
                count=item['metric'][0]['count']
                amount=item['metric'][0]['amount']
                columns3['Districts'].append(name)
                columns3['Transaction_count'].append(count)
                columns3['Transaction_amount'].append(amount)
                columns3["States"].append(state)
                columns3["Years"].append(year)
                columns3["Quarter"].append(int(file.strip(".json")))
map_transaction=pd.DataFrame(columns3)

map_transaction['States']=map_transaction['States'].str.replace('-',' ')
map_transaction['States']=map_transaction['States'].str.title()
map_transaction['States']=map_transaction['States'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
map_transaction['States']=map_transaction['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

#map_user
path4='C:/Users/ayish/GuviProjects/Phonepe/Phonepe pulse/pulse/data/map/user/hover/country/india/state/'
columns4={"States":[],"Years":[],"Quarter":[],"Districts":[],"RegisteredUsers":[],"AppOpens":[]}
map_user_list=os.listdir(path4)
for state in map_user_list:
    cur_states=path4+state+'/'
    map_year_list=os.listdir(cur_states)
    for year in map_year_list:
        cur_year=cur_states+year+'/'
        map_file_list=os.listdir(cur_year)
        for file in map_file_list:
            cur_file=cur_year+file
            data=open(cur_file,'r')

            D=json.load(data)
            for item in D["data"]['hoverData'].items():
                district=item[0]
                registered_user=item[1]['registeredUsers']
                app_open=item[1]['appOpens']
                columns4['Districts'].append(district)
                columns4['RegisteredUsers'].append(registered_user)
                columns4['AppOpens'].append(app_open)
                columns4["States"].append(state)
                columns4["Years"].append(year)
                columns4["Quarter"].append(int(file.strip(".json")))
map_user=pd.DataFrame(columns4)
map_user['States']=map_user['States'].str.replace('-',' ')
map_user['States']=map_user['States'].str.title()
map_user['States']=map_user['States'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
map_user['States']=map_user['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
                
#TOP TRANSACTION
path5='C:/Users/ayish/GuviProjects/Phonepe/Phonepe pulse/pulse/data/top/transaction/country/india/state/'
columns5={"States":[],"Years":[],"Quarter":[],"Pincodes":[],"Transaction_count":[],"Transaction_amount":[]}
top_transaction_list=os.listdir(path5)
for state in top_transaction_list:
    cur_states=path5+state+'/'
    top_year_list=os.listdir(cur_states)
    for year in top_year_list:
        cur_year=cur_states+year+'/'
        top_file_list=os.listdir(cur_year)
        for file in top_file_list:
            cur_file=cur_year+file
            data=open(cur_file,'r')

            E=json.load(data)
            for item in E['data']['pincodes']:
                entityname=item['entityName']
                count=item['metric']['count']
                amount=item['metric']['amount']
                columns5['Pincodes'].append(entityname)
                columns5['Transaction_count'].append(count)
                columns5['Transaction_amount'].append(amount)
                columns5["States"].append(state)
                columns5["Years"].append(year)
                columns5["Quarter"].append(int(file.strip(".json")))
top_transaction=pd.DataFrame(columns5)
top_transaction['States']=top_transaction['States'].str.replace('-',' ')
top_transaction['States']=top_transaction['States'].str.title()
top_transaction['States']=top_transaction['States'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
top_transaction['States']=top_transaction['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

#TOP USER
path6='C:/Users/ayish/GuviProjects/Phonepe/Phonepe pulse/pulse/data/top/user/country/india/state/'
columns6={"States":[],"Years":[],"Quarter":[],"Pincodes":[],"RegisteredUsers":[]}
top_user_list=os.listdir(path6)
for state in top_user_list:
    cur_state=path6+state+'/'
    cur_year_list=os.listdir(cur_state)
    for year in cur_year_list:
        cur_year=cur_state+year+'/'
        cur_file_list=os.listdir(cur_year)
        for file in cur_file_list:
            cur_file=cur_year+file
            data=open(cur_file,'r')

            F=json.load(data)
            for item in F['data']['pincodes']:
                pincodes=item['name']
                registered_user=item['registeredUsers']
                columns6['Pincodes'].append(pincodes)
                columns6['RegisteredUsers'].append(registered_user)
                columns6["States"].append(state)
                columns6["Years"].append(year)
                columns6["Quarter"].append(int(file.strip(".json")))
top_user=pd.DataFrame(columns6)
top_user['States']=top_user['States'].str.replace('-',' ')
top_user['States']=top_user['States'].str.title()
top_user['States']=top_user['States'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
top_user['States']=top_user['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

#creating and inserting query for SQL:

#Connecting to SQL
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

#Aggregated transaction table:
create_query_1='''create table if not exists aggregated_transaction(States varchar(100),
                                                       Years int,
                                                       Quarter int,
                                                       Transaction_type varchar(200),
                                                       Transaction_count bigint,
                                                       Transaction_amount bigint)'''

cursor.execute(create_query_1)
connection.commit()

insert_query_1='''Insert Into aggregated_transaction(States,
                                                    Years,
                                                    Quarter,
                                                    Transaction_type,
                                                    Transaction_count,
                                                    Transaction_amount)
                                                    values(%s,%s,%s,%s,%s,%s)'''
Table_data=aggregated_transaction.values.tolist()
cursor.executemany(insert_query_1,Table_data)
connection.commit()

#Aggregated User table:
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

create_query_2='''create table if not exists aggregated_user(States varchar(100),
                                                       Years int,
                                                       Quarter int,
                                                       Brands varchar(200),
                                                       Transaction_count bigint,
                                                       Percentage float)'''

cursor.execute(create_query_2)
connection.commit()

insert_query_2='''Insert Into aggregated_user(States,
                                            Years,
                                            Quarter,
                                            Brands,
                                            Transaction_count,
                                            Percentage)
                                            values(%s,%s,%s,%s,%s,%s)'''
Table_data=aggregated_user.values.tolist()
cursor.executemany(insert_query_2,Table_data)
connection.commit()

#Map transaction table:
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

create_query_3='''create table if not exists map_transaction(States varchar(100),
                                                       Years int,
                                                       Quarter int,
                                                       Districts varchar(200),
                                                       Transaction_count bigint,
                                                       Transaction_amount bigint)'''

cursor.execute(create_query_3)
connection.commit()

insert_query_3='''Insert Into map_transaction(States,
                                            Years,
                                            Quarter,
                                            Districts,
                                            Transaction_count,
                                            Transaction_amount)
                                            values(%s,%s,%s,%s,%s,%s)'''
Table_data=map_transaction.values.tolist()
cursor.executemany(insert_query_3,Table_data)
connection.commit()

#Map User table:
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

create_query_4='''create table if not exists map_user(States varchar(100),
                                                       Years int,
                                                       Quarter int,
                                                       Districts varchar(200),
                                                       RegisteredUsers bigint,
                                                       AppOpens bigint)'''

cursor.execute(create_query_4)
connection.commit()

insert_query_4='''Insert Into map_user(States,
                                            Years,
                                            Quarter,
                                            Districts,
                                            RegisteredUsers,
                                            AppOpens)
                                            values(%s,%s,%s,%s,%s,%s)'''
Table_data=map_user.values.tolist()
cursor.executemany(insert_query_4,Table_data)
connection.commit()

#TOP transaction table:
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

create_query_5='''create table if not exists top_transaction(States varchar(100),
                                                       Years int,
                                                       Quarter int,
                                                       Pincodes varchar(15),
                                                       Transaction_count bigint,
                                                       Transaction_amount bigint)'''

cursor.execute(create_query_5)
connection.commit()

insert_query_5='''Insert Into top_transaction(States,
                                            Years,
                                            Quarter,
                                            Pincodes,
                                            Transaction_count,
                                            Transaction_amount)
                                            values(%s,%s,%s,%s,%s,%s)'''
Table_data=top_transaction.values.tolist()
cursor.executemany(insert_query_5,Table_data)
connection.commit()

#Map User table:
config={"user":"root",
            "password":"Aspnas@2020",
            "host":'127.0.0.1',
            "database":"phonepedb",
            "port":3306}
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

create_query_6='''create table if not exists top_user(States varchar(100),
                                                       Years int,
                                                       Quarter int,
                                                       Pincodes varchar(15),
                                                       RegisteredUsers bigint
                                                       )'''

cursor.execute(create_query_6)
connection.commit()

insert_query_6='''Insert Into top_user(States,
                                        Years,
                                        Quarter,
                                        Pincodes,
                                        RegisteredUsers
                                        )
                                        values(%s,%s,%s,%s,%s)'''
Table_data=top_user.values.tolist()
cursor.executemany(insert_query_6,Table_data)
connection.commit()
            
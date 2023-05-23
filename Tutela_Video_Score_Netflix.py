import pandas as pd
import numpy as np
import MySQLdb
import math
conn=MySQLdb.connect(host="10.35.105.37", user="user_lulr", password="453a6a8fa4cf3080ec65f0cae7cf29fb2288932e", database="sqa_main_db")
    

sql = "SELECT * FROM tutela_border_mm_kabupaten_nation WHERE yearweek=(SELECT MAX(yearweek) FROM tutela_border_mm_kabupaten_nation)"


df_tutela = pd.read_sql(sql, conn)
df_tutela = df_tutela[['location','region','operator','video_score_netflix','yearweek']]

df_tutela.loc[df_tutela['operator']=="Telkomsel", 'Telkomsel'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="Telkomsel", 'Telkomsel_null'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="XL", 'XL'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="XL", 'XL_null'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="Indosat Ooredoo + 3", 'Indosat Ooredoo + 3'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="Indosat Ooredoo + 3", 'Indosat Ooredoo + 3_null'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="Smartfren", 'Smartfren'] = df_tutela['video_score_netflix']
df_tutela.loc[df_tutela['operator']=="Smartfren", 'Smartfren_null'] = df_tutela['video_score_netflix']
df_tutela = df_tutela.groupby('location').max().reset_index()
df_tutela = df_tutela[["location",'region','Telkomsel','Indosat Ooredoo + 3', 'XL','Smartfren','Telkomsel_null','Indosat Ooredoo + 3_null','XL_null','Smartfren_null','yearweek']]
df_tutela["Telkomsel"].fillna(0, inplace=True)
df_tutela["Smartfren"].fillna(0, inplace=True)
df_tutela["XL"].fillna(0, inplace=True)
df_tutela["Indosat Ooredoo + 3"].fillna(0, inplace=True)
def search_winner(df_tutela):
    if(df_tutela['Telkomsel'] > df_tutela["XL"]) and (df_tutela['Telkomsel'] > df_tutela['Indosat Ooredoo + 3']) and (df_tutela['Telkomsel'] > df_tutela['Smartfren']):
     return 'Telkomsel'
    elif(df_tutela['Indosat Ooredoo + 3'] > df_tutela["Telkomsel"]) and(df_tutela['Indosat Ooredoo + 3'] > df_tutela['XL']) and (df_tutela['Indosat Ooredoo + 3'] > df_tutela['Smartfren']):
     return 'Indosat Ooredoo + 3'
    elif(df_tutela['XL'] > df_tutela["Telkomsel"]) and(df_tutela['XL'] > df_tutela['Indosat Ooredoo + 3']) and (df_tutela['XL'] > df_tutela['Smartfren']):
     return 'XL'
    elif(df_tutela['Smartfren'] > df_tutela["Telkomsel"]) and(df_tutela['Smartfren'] > df_tutela['Indosat Ooredoo + 3']) and (df_tutela['Smartfren'] > df_tutela['XL']):
     return 'Smartfren'
    else:
        return 'No Winner'
df_tutela["Winner"] = df_tutela.apply(search_winner, axis=1)


def tsel_winner(df_tutela):
    if(df_tutela['Winner']=="Telkomsel"):
        return 'Win'
    elif(df_tutela['Winner']=="No Winner"):
        return 'No Winner'
    elif(df_tutela['Winner']!="Telkomsel"):
        return 'Lose'
df_tutela["tsel_winner"] = df_tutela.apply(tsel_winner, axis=1)

df_tutela["Max"] = df_tutela[['Indosat Ooredoo + 3','Smartfren','XL']].max(axis=1)

    

#Confidence Interval 95 Feb
sample_mean = 0
confidence_level_value = 1.96
total_cities = df_tutela["Winner"]!= 'No Winner'
sample_std = np.std(df_tutela.Telkomsel_null)
sample_size = total_cities.values.sum()
upper_ci = (sample_mean + confidence_level_value *(sample_std/math.sqrt(sample_size)))
lower_ci = (sample_mean - confidence_level_value *(sample_std/math.sqrt(sample_size)))
print(sample_size)
print(sample_std)
# df_tutela["Min"] = df_tutela["Telkomsel"]-upper_ci

def tsel_winner_ci_95(df_tutela):
    if(df_tutela["tsel_winner"]=="Win") and ((df_tutela["Telkomsel"]-upper_ci) > df_tutela["Max"]):
        return "Win"
    elif(df_tutela["tsel_winner"]=="Win")and((df_tutela["Telkomsel"]-upper_ci) <= df_tutela["Max"]):
        return "Par"
    elif(df_tutela["tsel_winner"] =="Lose")and((df_tutela["Telkomsel"]+upper_ci) >= df_tutela["Max"]):
        return "Par"
    elif(df_tutela["tsel_winner"]=="No Winner"):
        return "No Winner"
    else:
        return "Lose"
df_tutela["tsel_winner_ci_95"] = df_tutela.apply(tsel_winner_ci_95, axis=1)


def final_status(df_tutela):
    if(df_tutela["tsel_winner_ci_95"]=="No Winner"):
        return "No Winner"
    elif(df_tutela["tsel_winner_ci_95"]=="Lose"):
        return "Lose"
    else:
        return "Win"
df_tutela["final_status"] = df_tutela.apply(final_status, axis=1)

def for_ppt(df_tutela):
    if(df_tutela["final_status"]=="Win"):
        return "Tsel"
    elif(df_tutela["final_status"]!="Win")and(df_tutela["Winner"]=="Indosat Ooredoo + 3"):
        return "ISAT+3"
    elif(df_tutela["final_status"]!="Win")and(df_tutela["Winner"]=="Smartfren"):
        return "Smartfren"
    elif(df_tutela["final_status"]!= "Win")and(df_tutela["Winner"]=="XL"):
        return "XL"
    else:
        return "No Winner"
df_tutela["for_ppt"] = df_tutela.apply(for_ppt, axis=1)
df_tutela["Category"] = "Video Score Netflix"
df_tutela["Upper CI"] = upper_ci
df_tutela["Lower CI"] = lower_ci
print(upper_ci)
print(lower_ci)
df_final = df_tutela[["yearweek","Category","location","region","Indosat Ooredoo + 3_null","Smartfren_null","Telkomsel_null","XL_null","Winner","tsel_winner","tsel_winner_ci_95","final_status","for_ppt","Upper CI","Lower CI"]]
print(df_final)
path_to_csv = "/home/sysadmin/halil/video_score_netflix.csv"
df_final.fillna('\\N', inplace=True)
df_final.to_csv(path_to_csv, index=None)


cursor = conn.cursor()
sql_2 = "LOAD DATA LOCAL INFILE '/home/sysadmin/halil/video_score_netflix.csv' INTO TABLE tutela_border_mm_kabupaten_nation_ci FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
cursor.execute(sql_2)
conn.commit()
cursor.close()
print(cursor.rowcount, "rows was inserted")
print("Upload Done")
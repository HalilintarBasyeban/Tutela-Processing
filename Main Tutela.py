import ftplib
import MySQLdb
conn=MySQLdb.connect(host="", user="", password="", database="", port=4000)
import pandas as pd
import shutil
import os

#mendapatkan nama file otomatis
sql = "SELECT MAX(yearweek) AS yearweek FROM tabel"
df = pd.read_sql(sql, conn)
df["Get"]=df["yearweek"].str[-2:]
df = df.apply(pd.to_numeric)
df = df[["yearweek"]]
df = df.yearweek.item()
df = df+1
nama_file =str(df)
path = '/path to files/'
file_name = "path to files"+nama_file+"_isat3.csv"
download_source = "/path to files"+file_name
move_path = '/path to files'

#download from ftp
print("Start Downloading")
HOSTNAME = ""
USERNAME = ""
PASSWORD = ""

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
ftp_server.encoding = "utf-8"
# ftp_server.dir(path)
ftp_server.cwd(path)
with open(file_name, "wb") as file:
    ftp_server.retrbinary(f"RETR {file_name}", file.write)
ftp_server.close()
print("Download Success")
shutil.move(download_source, move_path)
print("Move File success")




path_raw = 'path to files'+file_name
path_olah = 'path to files/tutela_border_mm_kabupaten_nation.csv'
#read tutela dataframe
tutela_dataframe = pd.read_csv(path_raw)

#filter tutela dataframe
filtered_values = tutela_dataframe[(tutela_dataframe['level']=='kabupaten')&(tutela_dataframe['node']=='4G')]
filtered_values.fillna('\\N', inplace=True)
filtered_values.to_csv(path_olah, index=None)
print("Start Uploading")

#upload dataframe to sql
cursor = conn.cursor()
sql2 = "LOAD DATA LOCAL INFILE 'path to files' INTO TABLE tutela_border_mm_kabupaten_nation FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
# print(sql2)
cursor.execute(sql2)
conn.commit()
cursor.close()
print(cursor.rowcount, "rows was inserted")
print("Upload Done")

if os.path.exists("path to files"+file_name):
   os.remove("path to files"+file_name) 
   print("Delete Old File Success")
else:
    print("File not exist")
print("Run Tutela Game Parameter")
tutela_game_parameter = 'path to files/Tutela_Game_parameter.py'
exec(open(tutela_game_parameter).read())

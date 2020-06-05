import psycopg2
import re

#Соединение с базой данных и методы для получения buildings и hospitals

def connectionDB(database="map",user="postgres",passwd="",host="127.0.0.1",port="5432"):
   conn = psycopg2.connect(
   database="map1",
   user="postgres",
   password="v1999242852",
   host="127.0.0.1",
   port="5432")
   return conn

def getBuildings():
    conn = connectionDB()
    cursor=conn.cursor()
    line="select id,street,number,st_AsText(linestring) from buildings where street is not null and number is not null"
    cursor.execute(line)
    buildings=cursor.fetchall()
    result_buildings=[]
    count_t=0
    for building in buildings:
        coordinates=list(map(float,re.findall(r'\d\d\.\d+',building[-1])))
        building=list(building)
        building.pop()
        if (len(coordinates)==2):
            building.append({"is_Pair":True,"coordinate":(coordinates[1],coordinates[0])})
            count_t+=1
        else:
            X=[coordinate for coordinate in coordinates[::2]]
            Y=[coordinate for coordinate in coordinates[1::2]]
            building.append({"is_Pair": False, "x":X,"y":Y})
        result_buildings.append(building)
    cursor.close()
    conn.close()
    return result_buildings

def getHospitals():
    conn=connectionDB()
    cursor=conn.cursor()
    line="select id,street,number,name,st_AsText(linestring) from hospitals"
    cursor.execute(line)
    hospitals=cursor.fetchall()
    result_hospitals=[]
    count_t=0
    for hospital in hospitals:
        coordinates=list(map(float,re.findall(r'\d\d\.\d+',hospital[-1])))
        hospital=list(hospital)
        hospital.pop()
        if (len(coordinates)==2):
            hospital.append({"is_Pair":True,"coordinates":(coordinates[1],coordinates[0])})
            count_t+=1
        else:
            X=[coordinate for coordinate in coordinates[::2]]
            Y=[coordinate for coordinate in coordinates[1::2]]
            hospital.append({"is_Pair": False, "x":X,"y":Y})
        result_hospitals.append(hospital)
    cursor.close()
    conn.close()
    return result_hospitals
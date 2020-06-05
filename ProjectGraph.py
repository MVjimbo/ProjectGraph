import xml.etree.ElementTree as ET
import psycopg2
from psycopg2 import extensions as ext
import shapely
import re
import struct


def connectionDB():
   conn = psycopg2.connect(
   database="map", 
   user="postgres", 
   password="v1999242852", 
   host="127.0.0.1", 
   port="5432") 
   return conn

def xmlScanNodes(root,conn):
    cursor=conn.cursor()
    columns=("id","lat","lon")
    count=0
    for node in root.findall("node"):
        values=[]
        count+=1
        insert='insert into nodes (id,lat,lon) values (%s,%s,%s)',
        (int(node.get("id")),float(node.get("lat")),float(node.get("lon")))
        cursor.execute('insert into nodes (id,lat,lon) values (%s,%s,%s)',
            (int(node.get("id")),float(node.get("lat")),float(node.get("lon"))))
        conn.commit()
    cursor.close()
    print(count)




def xmlScanStreets(root):
    streets=[]
    for children in root:
        is_Street=0
        street_Name=''
        tags=children.findall('tag')
        if len(tags)!=0:
            for tag in tags:
                if tag.get('k')=="highway" and (tag.get('v') in ('motorway','trunk','primary','secondary','tertiary','unclassified','residential')):
                    is_Street=1
                    break
            if is_Street==1:
                nodes=[]
                for node in children.findall('nd'): 
                    nodes.append(node.get('ref'))
                for tag in tags:
                    if tag.get('k')=="name":
                        street_Name=tag.get('v')
                streets.append([street_Name,nodes])
                #if tag.get('k')=="addr:housenumber":
                 #   is_House=1
                  #  is_Street=0
                   # house_Number=tag.get('v')
    print(streets)

def xmlScanBuildings(root,conn):
    count_buildings=0
    count_nodes=0
    cursor=conn.cursor()
    for children in root:
        building={"name":"","amenity":""}
        is_Building=0
        have_Street=0
        have_Number=0
        street_Name=''
        building_Number=''
        tags=children.findall('tag')
        if len(tags)!=0:
            for tag in tags:
                if tag.get('k')=="building" and (tag.get('v') in ('apartments','detached','dormitory','hotel','house','residential','semidetached_house','commercial','industrial','office','retail','supermarket','cathedral','church','mosque','fire_station','government','hospital','kindergarten','public','school','university','pavilion','clinic')):
                    is_Building=1
                if tag.get('k')=="addr:street":
                    have_Street=1
                    street_Name=tag.get('v')
                if tag.get('k')=="addr:housenumber":
                    have_Number=1
                    building_Number=tag.get('v')
            if is_Building==1 and have_Street==1 and have_Number==1:
                count_buildings+=1
                for tag in tags:
                    if tag.get('k')=="name":
                        building["name"]=tag.get('v')
                    if tag.get('k')=="amenity":
                        building["amenity"]=tag.get('v')
                building["id"]=children.get("id")
                building["street"]=street_Name
                building["number"]=building_Number
                if building["name"]=="" and building["amenity"]=="":
                    cursor.execute('insert into buildings (id,street,number) values (%(id)s , %(street)s, %(number)s)',building)
                elif building["name"]=="" and building["amenity"]!="":
                    cursor.execute('insert into buildings (id,street,number,amenity) values (%(id)s ,%(street)s, %(number)s, %(amenity)s)',building)
                elif building["name"]!="" and building["amenity"]=="":
                    cursor.execute('insert into buildings (id,street,number,name) values (%(id)s ,%(street)s, %(number)s, %(name)s)',building)
                else:
                    cursor.execute('insert into buildings (id,street,number,name,amenity) values (%(id)s ,%(street)s, %(number)s, %(name)s, %(amenity)s)',building)
                for node in children.findall('nd'):
                    count_nodes+=1
                    cursor.execute('insert into nodes_buildings (id_nodes,id_buildings) values (%s,%s)',
                        (int(node.get('ref')),building["id"]))
    conn.commit()
    cursor.close()
    print(count_buildings,count_nodes)
                
def xmlScanHospital(root):
    count=0
    hospitals=[]
    for children in root:
        have_Street=0
        is_Hospital=0
        street=""
        amenity=""
        tags=children.findall('tag')
        if len(tags)!=0:
            for tag in tags:
                if tag.get('k')=="building" and (tag.get("v")=="hospital"):
                    is_Hospital=1
                if tag.get('k')=="addr:street":
                    have_Street=1
            if is_Hospital==1 and have_Street==1:
                hospital=[]
                for tag in tags:
                    if tag.get("k")=="name":
                        hospital.append(tag.get("v"))
                    if tag.get("k")=="addr:street":
                        hospital.append(tag.get("v"))
                hospitals.append(hospital)
    print(hospitals)

def xmlNodeScanRoadRelation(root): 
    relation=[]
    for children in root.findall("relation"):
        is_Street=0
        relation_Name=""
        tags=children.findall("tag")
        for tag in tags:
            if tag.get("k")=="type" and tag.get("v")=="associatedStreet":
                is_Street=1
                break
        if is_Street==1:
            for tag in tags:
                if tag.get("k")=="name":
                    relation_Name=tag.get('v')
            relation.append(relation_Name)
    print (relation)

def getBuildings(conn):
    cursor=conn.cursor()
    line="select id,street,number,name,st_AsText(linestring) from hospitals"
    cursor.execute(line)
    buildings=cursor.fetchall()
    for building in buildings:
        coordinates=list(map(float,re.findall(r'\d\d\.\d+',building[-1])))
        building=list(building)
        building.pop()
        if (len(coordinates)==2):
            building.append([coordinates[0],coordinates[1]])
        else:
            is_Even=0
            building.append([])
            building.append([])
            for coordinate in coordinates:
                building[-2+is_Even].append(coordinate)
                is_Even+=1
                if is_Even==2:
                    is_Even=0
        print(building)
        #for elem in coordinate:
   
    cursor.close()

if __name__=="__main__":
    file_name='planet_65.397,57.075_65.721,57.191.osm'
    tree=ET.parse(file_name)
    root=tree.getroot()
    conn=connectionDB()
    #getBuildings(conn)
    print(struct.calcsize("P") * 8)
    conn.close()
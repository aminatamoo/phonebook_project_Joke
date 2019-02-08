# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:04:37 2019

@author: amina
"""

import sqlite3
import json
import requests

conn=sqlite3.connect('phonebook.db')
c=conn.cursor()


import json

with open('mock_data/mock_data_people.json') as json_file:
   data_people = json.load(json_file)

with open('mock_data/mock_data_business.json') as json_file:
   data_business = json.load(json_file)
    
#CREATE DB TABLE
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS phonebookpeople(First_name TEXT ,Last_name TEXT, Address_line1 TEXT, City TEXT, Postcode TEXT, Telephone REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS phonebookbusiness(Business_name TEXT, Address_line1 TEXT, City TEXT, Postcode TEXT, Telephone REAL, Business_category TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS postcodes(Postcode TEXT, x_coord FLOAT, y_coord FLOAT)')
 
#ENTERING DATA IN TABLE
def dynamic_data_entryPeople():
    for line in data_people:
        First_namekey=list(line.keys())[0]
        First_name =  line[First_namekey]
        
        Last_namekey=list(line.keys())[1]
        Last_name =  line[Last_namekey]
        
        Address_line1key=list(line.keys())[2]
        Address_line1 =  line[Address_line1key]
        
        City_key=list(line.keys())[3]
        City =  line[City_key]
        
        Postcode_key=list(line.keys())[5]
        Postcode =  line[Postcode_key]
        
        Telephone_key=list(line.keys())[7]
        Telephone =  line[Telephone_key]
        c.execute("INSERT INTO phonebookpeople(First_name, Last_name, Address_line1, City, Postcode, Telephone) VALUES (?, ?, ?, ?, ?, ?)", (First_name, Last_name, Address_line1, City, Postcode, Telephone))
    conn.commit()
    
def dynamic_data_entryBusiness():   
    for line in data_business:
    
        Business_namekey=list(line.keys())[0]
        Business_name =  line[Business_namekey]
#        print(Business_name)
     
        Address_line1key=list(line.keys())[1]
        Address_line1 =  line[Address_line1key]
    
        Citykey=list(line.keys())[2]
        City =  line[Citykey]
       
        Postcodekey=list(line.keys())[4]
        Postcode =  line[Postcodekey]
      
        Telephonekey=list(line.keys())[6]
        Telephone =  line[Telephonekey]
      
        Business_categorykey=list(line.keys())[7]
        Business_category =  line[Business_categorykey]
        
        c.execute("INSERT INTO phonebookbusiness(Business_name, Address_line1, City, Postcode, Telephone, Business_category) VALUES (?, ?, ?, ?, ?, ?)", (Business_name, Address_line1, City, Postcode, Telephone, Business_category))
        conn.commit()
        
def call_api(current_postcode):
    print(current_postcode)
    api_postcode = current_postcode.replace(" ","")
    endpoint = "http://api.postcodes.io/postcodes/"
    response = requests.get(endpoint + api_postcode)
    dataapi = response.json()
    if dataapi['status']==200:
        x_coord = dataapi['result']['longitude']
        y_coord = dataapi['result']['latitude']
        c.execute("INSERT INTO postcodes(Postcode, x_coord, y_coord) VALUES (?, ?, ?)", (current_postcode, x_coord, y_coord))
        conn.commit()
    else:
        print("duplicate or doesn't exist")
        
def check_postcodeExists(current_postcode):
    c.execute('SELECT * FROM postcodes WHERE Postcode=?',(current_postcode,))
    results = c.fetchall()
    if not results:
        call_api(current_postcode)
           
    
def dynamic_data_entryPostcodes():
    c.execute('SELECT Postcode FROM phonebookpeople')
    for row in c.fetchall():
        current_postcode = row[0]
        check_postcodeExists(current_postcode)
        
    c.execute('SELECT Postcode FROM phonebookbusiness')
    for row in c.fetchall():
        current_postcode = row[0]
        check_postcodeExists(current_postcode)
        

            
        
            
            
        
dynamic_data_entryPostcodes()
        
         
    



# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:04:37 2019

@author: amina
"""
from math import radians,atan,sin,cos,asin,sqrt
import requests
import string
import sqlite3
import os
db_path = 'phonebook.db'

#MAIN FUNCTION


def main_Phonebook_bus():
    #saves business type or name that user is searching for in a var
    name_bus='Business Name or Business Type'
    sym_bus='&'
    searched_busName=get_name(name_bus,sym_bus)
    
    #gets location that user is searching for
    searched_location=get_userLocation() 
    
    #applies formatting to location input based on whether city/town or postcode was entered
    searched_location=format_location(searched_location)
    
    #selecting from db based on user search
    c=filter_by_search_bus(searched_busName,searched_location)
    
    #retrieve resulting selection from db
    bus_found=retrieve_search(c)
    
    #add distance attribute to business(es) found details
    bus_found_d=add_distance_from_user(bus_found)
    
    #sorts results based on user choice(distance or alphabetically)
    sorted_results=sort_results(bus_found_d)
    
    #presents results in a user friendly way
    make_lookPretty_bus(sorted_results)

def main_Phonebook_people():
    #saves surname that user is searching for in var
    name_people = 'Surname'
    sym_people = '-'
    searched_surname=get_name(name_people,sym_people)
    
    #saves location that user is searching for in var
    searched_location=get_userLocation() 
    
    #applies formatting to location input based on whether city/town or postcode was entered
    searched_location=format_location(searched_location)
    
    #selecting from db based on user search
    c=filter_by_search(searched_surname,searched_location)
    
    #retrieves resulting selection from db
    people_found=retrieve_search(c)
    
    #adds distance attribute to people found details
    people_found_d=add_distance_from_user(people_found)
    
    #sorts results based on user choice(distance or alphabetically)
    sorted_results=sort_results(people_found_d)
    
    #presents results in a user friendly way
    make_lookPretty_people(sorted_results)
       
    
#DATABASE CONN
def check_db():
    if os.path.exists(db_path):
        return True
    else:
        return False

def getdb():
    conn=sqlite3.connect(db_path)
    c=conn.cursor()
    return (c,conn)

#USER SEARCH FUNCTIONALITIES  
 
#------------------VALIDATION----------------------
    
#VALIDATION FUNCTIONS 
def has_numbers(inputStr):
    for char in inputStr:
        if char.isdigit():
            return True
    return False

def has_symbols(inputStr):
    invalidSymbols = set(string.punctuation)
    for char in inputStr:
        if char in invalidSymbols:
            return True
    return False

def has_symbols_exclude(inputStr,symbol):
    invalidSymbols = set(string.punctuation.replace(symbol,''))
    for char in inputStr:
        if char in invalidSymbols:
            return True
    return False

def check_name(func1, func2, inputStr, symbol, name_type):   
    print('Invalid Input')
    if func1(inputStr):
        print('- user\'s response contains numbers. Please re-enter a valid {}.'.format(name_type.lower()))
    elif func2(inputStr,symbol):
        print('- user\'s response contains special characters (only {} accepted). Please re-enter a valid {}.'.format(symbol,name_type.lower()))
    elif inputStr=='':
         print('- You must enter a {}. Please enter a valid {}.'.format(name_type.lower()))
         
def check_userLocation(func1, inputStr):
    print('Invalid Input')
    if func1(inputStr):
        print('- user\'s response contains special characters. Please re-enter a valid location.')
    elif inputStr.isdigit():
        print('- user\'s response is not a valid postcode. Please re-enter a valid location.')
    elif inputStr=='':
        print('- You must enter a location. Please enter a valid location.')

         
def format_location(searched_location):
    if has_numbers(searched_location):
        #POSTCODE
        while len(searched_location)<5:
            print('Invalid Postcode provided. Please enter a full postcode (e.g. AB12 3DB)')
            searched_location=get_userLocation()   
        searched_location=searched_location.upper()
        return searched_location
    else:
        #TOWN/CITY
        searched_location=searched_location.title()
        return searched_location

#GET AND VALIDATING USER INPUT
def get_name(name_type,symbol):
    searched_name=input('Enter {}: '.format(name_type)).title()
    while has_numbers(searched_name) or has_symbols_exclude(searched_name,symbol) or searched_name=='':
        check_name(has_numbers,has_symbols_exclude, searched_name,symbol,name_type)
        searched_name = input('Enter {}: '.format(name_type)).title()
    return searched_name

def get_userLocation():
    searched_location = input('Enter a Town, City or Postcode: ')
    while searched_location.isdigit() or has_symbols(searched_location) or searched_location=='':
        check_userLocation(has_symbols, searched_location)
        searched_location = input('Enter a Town, City or Postcode: ')
    return searched_location

def get_userPostcode():
    user_postcode=input('Enter your Postcode: ').upper()
    while user_postcode.isdigit() or has_symbols(user_postcode) or user_postcode=='':
        check_userLocation(has_symbols, user_postcode)
        user_postcode = input('Enter your postcode: ').upper()    
    user_postcode=inf_loop_postcode(user_postcode)
    return user_postcode 

def inf_loop_postcode(postcode):  
    while len(postcode)<5:
        print('Invalid Postcode provided. Please enter a full postcode (e.g. AB12 3DB)')
        postcode=input('Enter your Postcode: ').upper()
    return postcode

def get_userCoord(postcode):
    postcode=postcode.replace(" ","")
    endpoint = "http://api.postcodes.io/postcodes/"
    response = requests.get(endpoint+postcode)
    dataapi = response.json()
    if dataapi['status']==200:
        x_coord = float(dataapi['result']['longitude'])
        y_coord = float(dataapi['result']['latitude'])
        return x_coord, y_coord
    else:
        print('Postcode entered doesn\'t exist')
        return None

#SORTING FUNCTIONS

def initial_askSort():
    try:
        ask=int(input('How would you like to sort the results? Please enter the number 1 or 2.\n1. Sort by Distance.\n2. Sort by Alphabetical order\n'))        
    except ValueError:
        ask=0  
    return ask  

def askSort():
    ask=initial_askSort()
    while ask < 1 or ask > 2:
        print("Please enter '1' or '2' only!\n")                
        ask=initial_askSort()
    return ask       

def calc_distance_haversine(coord_set1,coord_set2):
    lon1,lat1=coord_set1
    lon2,lat2=coord_set2
    lon1,lat1,lon2,lat2=map(radians,[lon1,lat1,lon2,lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    R=6371
    d=R*c
    return d
        
def add_distance_from_user(results):
    user_postcode=get_userPostcode()
    user_coord=get_userCoord(user_postcode)
    results_d=[]
    for person in results:
        person=list(person)
        result_coord=float(person[7]),float(person[8])
        distance=calc_distance_haversine(user_coord,result_coord)
        person.append(distance)
        person=tuple(person)
        results_d.append(person)
    return results_d

#READ DB FUNCTIONS BUSINESS
def filter_db_bus(cat,name,city,postcode):
    c,conn=getdb()
    c.execute("SELECT * FROM phonebookbusiness INNER JOIN postcodes ON postcodes.Postcode=phonebookbusiness.Postcode WHERE (Business_category=? OR Business_name LIKE ?) AND (City=? OR postcodes.Postcode=?)",(cat,('%'+name[:3]+'%'),city,postcode))
    return c

def generate_bus_catList():
    bus_cat=[]
    c,conn=getdb() 
    c.execute('SELECT DISTINCT Business_category FROM phonebookbusiness') 
    results=c.fetchall()
    for row in results:
        bus_cat.append(row[0])
    return bus_cat
    
def filter_by_search_bus(name,location): 
    bus_cat=generate_bus_catList()
    if name in bus_cat and location.istitle():
        bus_type = name
        city = location
        c=filter_db_bus(bus_type,"''",city,'')
    elif name in bus_cat and location.isupper():
        bus_type = name
        postcode = location
        c=filter_db_bus(bus_type,"''",'',postcode)
    if name not in bus_cat and location.istitle():
        bus_name = name
        city = location
        c=filter_db_bus('',bus_name,city,'')
    elif name not in bus_cat and location.isupper():
        bus_name = name
        postcode = location
        c=filter_db_bus('',bus_name,'',postcode)
    return c

#READ DB FUNCTIONS PEOPLE   
def filter_db_people(surname,city,postcode):
    c,conn=getdb()
    c.execute("SELECT *FROM phonebookpeople INNER JOIN postcodes ON postcodes.Postcode=phonebookpeople.Postcode WHERE Last_name LIKE ? AND (City=? OR postcodes.Postcode=?)",(('%'+surname[:3]+'%'),city,postcode))
    return c
    
def filter_by_search(surname,location):  
    if location.istitle():
        city = location
        c=filter_db_people(surname,city,'')
        return c
    elif location.isupper():
        postcode = location
        c=filter_db_people(surname,'',postcode)
        return c
    
#RETRIEVE FROM DB 
        
def retrieve_search(c):
    response = c.fetchall()
    results = []
    if response:
        for row in response:
            results.append(row)
    return results

#SORTING FUNCTIONS
def sort_list(l,i):
    l.sort(key=lambda t:t[i])
    return l      

def sort_results(results):
    how_toSort = askSort()
    if how_toSort == 1:
        sorted_results=sort_list(results,9)     
    elif how_toSort == 2:
        sorted_results = sort_list(results,1)
    return sorted_results


#DISPLAY RESULTS
def make_lookPretty_bus(results):
    if not results:
        print('No results found. We do not have this person in our database')
    else:
        for item in results:
                print('-'*12)
                print(item[0],'({})'.format(item[5]))
                print('{}, {}, {}'.format(item[1],item[2],item[3]))
                print(item[4])
                print(round(item[9],2),'km')    

def make_lookPretty_people(results):
    if not results:
        print('No results found. We do not have this business in our database')
    else:
        for item in results:
                print('-'*12)
                print(item[0],item[1])
                print('{}, {}, {}'.format(item[2],item[3],item[4]))
                print(item[5])
                print(round(item[9],2),'km')

   
if __name__=='__main__':       
    main_Phonebook_bus()
    #main_Phonebook_people()
    





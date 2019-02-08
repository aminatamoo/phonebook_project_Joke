# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 10:43:17 2019

@author: amina
"""


from phonebook_v2 import *

class test_Phonebook():
    def __init__(self):
        self.t_surname='Lamers'
        self.t_city='London'
        self.t_postcode='EC3M 1AJ'
        pass
    
    def test_get_userSurname(self):
        self.surnameCheck=get_userSurname()
        return self.surnameCheck
    
    def test_get_userLocation(self):
        if self.surnameCheck:
            self.locationCheck=get_userLocation()
            print('Passed test 1')
            return self.locationCheck
        else:
            return 'Not getting a surname'
        
    def test_format_location(self):
        if self.locationCheck:
            self.formatCheck=format_location(self.locationCheck)
            if self.formatCheck:
                print('Passed test 2')
                return self.formatCheck
            else:
                print('Issue with formatting or location')
                return False
        else:
            print('Not getting a location')
            return False
        
    def test_filter_by_search(self):
        if self.formatCheck:
            self.filterCheck=filter_by_search(self.surnameCheck,self.formatCheck)
            if self.filterCheck:
                print('Passed test 3')
                return self.filterCheck
            else:
                print('Issue with formatting or filtering')
        else:
            print('Not getting a location')
            return False
        
    def test_retrieve_search(self):
        if self.filterCheck:
            self.retrieveCheck=retrieve_search(self.filterCheck)
            if self.retrieveCheck:
                print('Passed test 4')
                return self.filterCheck
            else:
                print('Issue with filtering or retrieving from db: Searched entities may not be in db')
        else:
            print('Not getting a filtered result')
            return False
                
        
    def runTests(self):
        self.test_get_userSurname()
        self.test_get_userLocation()
        self.test_format_location()
        self.test_filter_by_search()
        self.test_retrieve_search()
    
            
if __name__ == "__main__":

    newTest=test_Phonebook()     
    newTest.runTests()      
        
    
    

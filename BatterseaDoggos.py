#!/usr/bin/env python
# coding: utf-8



# Import libraries
import requests
from datetime import date
from bs4 import BeautifulSoup
import os.path
import csv




# Request list of dogs
response_dogs = requests.get('https://www.battersea.org.uk/api/animals/dogs')



# Get list of dogs
all_dogs = response_dogs.json()
#print (all_dogs)
animal_list = list(all_dogs['animals'].keys())
# This has all the info we want, except for ideal home location


# Create/open csv file with info
csv_path = './Doggos.csv'
Header = ['NID','Name','Birth_date','Centre','Date_published','Size','Breed','Sex','Child_Suitability','Cat_suitability','Dog_suitability','Reserved','Date_reserved','Rehomed','Date_rehomed','Ideal_location']
if 0 == os.path.isfile(csv_path): #if file does not exist
    with open(csv_path,'w') as csvFile:
        writer = csv.writer(csvFile)

    csvFile.close()




dogtionary = {}
with open(csv_path,'r') as dog_file:
    data = csv.DictReader(dog_file,delimiter=',')
    for row in data:
        # if row[0] == 'NID':
        #     continue
        dogtionary[row['NID']] = row#[1:-1]
dog_file.close()



# Find individual dogs and information about their ideal home location. We find it in the html file
for number in animal_list:
    
    dog = all_dogs['animals'][number]
    # Update rehomed status
    dog_id = dog['nid']

    # If dogtionary contains this dog ---> Update
    if dog_id in dogtionary.keys():
        update_dog = dogtionary.get(dog_id)
        if dog['field_animal_rehomed'] != '':
            #print ('printing update dog:',update_dog)
            #setattr(update_dog, '')
            update_dog['Rehomed'] = dog['field_animal_rehomed']
            update_dog['Date_rehomed'] = date.today()

            #update_dog['Rehomed'] = dog['field_animal_rehomed']
            #update_dog['Date_rehomed'] = date.today()

        if dog['field_animal_reserved'] != '':
            update_dog['Reserved'] = dog['field_animal_reserved']
            update_dog['Date_reserved'] = date.today()

    else :

        url = "https://www.battersea.org.uk" + (dog['path']) + "?&id=" + str(dog['nid'])
        dog_result = requests.get(url)
        dog_html = dog_result.content
        soup = BeautifulSoup(dog_html)
        animal_details = soup.findAll("div",{"class": "animal_details"})
        tag = soup.find("span", text="Ideal home location")
        ideal_home = tag.find_next_sibling("span").text
        dog['Ideal_location'] = ideal_home

        print ('Inserting new dog')

        date_reserved = ''
        date_rehomed = ''
        if dog['field_animal_reserved'] != '':
            date_reserved = date.today()

        if dog['field_animal_rehomed'] != '':
            date_rehomed = date.today()

        dogtionary[dog_id] = {'NID':dog['nid'],'Name':dog['title'],'Birth_date':dog['field_animal_age'],'Centre':dog['field_animal_centre'],'Date_published':dog['field_animal_date_published'],'Size':dog['field_animal_size'],'Breed':dog['field_animal_breed'],'Sex':dog['field_animal_sex'],'Child_Suitability':dog['field_animal_child_suitability'],'Cat_suitability':dog['field_animal_cat_suitability'],'Dog_suitability':dog['field_animal_dog_suitability'],'Reserved':dog['field_animal_reserved'],'Rehomed':dog['field_animal_rehomed'],'Ideal_location':dog['Ideal_location'],'Date_reserved':date_reserved,'Date_rehomed':date_rehomed}



print('Dogtionary:',dogtionary)

print ('Test')
# Insert into csv file
try:
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Header )
        writer.writeheader()
        for data in dogtionary.values():
            writer.writerow(data)
except IOError:
    print("I/O error")





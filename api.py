# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 07:30:47 2022

@author: zbookuser
"""

import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os


class PetFriends:
    """API библиотека к веб приложению Pet Friends"""
    
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        
    def get_api_key(self, email, password):
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем'''
        
        headers = {
            'email': email,
            'password': password
        }
        
        res = requests.get(self.base_url + 'api/key', headers = headers)
        status = res.status_code
        
        results = ""
        if status == 200:            
            try:
                results = res.json()
            except:
                results = res.text()
        
        return status, results
    
        
    
    def get_list_of_pets(self, auth_key, filter):
        
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        
        res = requests.get(self.base_url + 'api/pets', headers = headers, params = filter)
        status = res.status_code
        
        results = ""
        if status == 200:
            try:
                results = res.json()
            except:
                results = res.text()
        
        return status, results
    
    
    def add_new_pet_simple(self, auth_key, name, animal_type, age):
        
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        
        res = requests.post(self.base_url + 'api/create_pet_simple', headers = headers, data = data)
        
        status = res.status_code
        
        results = ""
        if status == 200:
            try:
                results = res.json()
            except:
                results = res.text()
        
        return status, results
    
    
    def add_photo_to_pet(self, auth_key, pet_id, pet_photo):
                
        data = MultipartEncoder(
            fields = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
            )
                        
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        
        
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers = headers, data = data)
        
        status = res.status_code
        results = res
        if status == 200:
            try:
                results = res.json()
            except:
                results = res.text()            
        
        return status, results
    
    
    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
                                
        data = MultipartEncoder(
            fields = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                }
            )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        
        res = requests.post(self.base_url + 'api/pets', headers = headers, data = data)
        status = res.status_code
        
        results = ""
        try:
            results = res.json()
        except:
            results = res.text()
        
        return status, results
    
    
    def delete_pet(self, auth_key, pet_id):
        
        headers = {'auth_key': auth_key['key']}
        
        res = requests.delete(self.base_url + 'api/pets/'+pet_id, headers = headers)
        status = res.status_code
        
        '''results = ""
        try:
            results = res.json()
        except:
            results = res.text()'''
        
        return status
    
    
    def update_pet(self, auth_key, pet_id, name, animal_type, age):
        
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers = headers, data = data)
        status = res.status_code
        
        results = ""
        try:
            results = res.json()
        except:
            results = res.text()
        
        return status, results
        
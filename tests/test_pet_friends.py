# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 07:30:27 2022

@author: zbookuser
"""

from api import PetFriends
from settings import v_email, v_password
import os



pf = PetFriends()

def get_incorrected_value(value: str):
    '''функция для получения некорректного значения путем изменения первого
    символа корректного значения'''
    
    print("Текущее значение: " + value)
    # редактируем значение:
    #l = len(auth_key['key'])
    value = "f" + value[:-1]
    print("Новое значение: " + value)
    return value



def test_get_api_key_corrected(email = v_email, password = v_password):
    '''тест проверяет получение api-ключа при корректных 
        данных почты и пароля'''
    status, results = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in results
    print(type(results))
    print(results)
    
def test_get_api_key_incorrected_without_data(email = "", password = ""):
    '''тест проверяет получение api-ключа без данных'''
    
    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_incorrected_without_email(email = "", password = v_password):
    '''тест проверяет получение api-ключа 
        при корректном пароле и без почты'''
    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_incorrected_without_password(email = v_email, password = ""):
    '''тест проверяет получение api-ключа 
        при корректной почте и без пароля'''
    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_incorrected_password(email = v_email, password = get_incorrected_value(v_password)):
    '''тест проверяет получение api-ключа 
        при корректной почте и некорректном пароле'''
    status, _ = pf.get_api_key(email, password)
    assert status == 403

    
def test_get_api_key_incorrected_email(email = "n"+v_email, password = v_password):
    '''тест проверяет получение api-ключа 
        при некорректной почте'''
    status, _ = pf.get_api_key(email, password)
    assert status == 403
      


def test_get_list_of_all_pets_corrected():
    '''позитивный тест на получение списка всех питомцев'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    filter = ""
        
    status, results = pf.get_list_of_pets(auth_key = auth_key, filter = filter)
    assert status == 200
    assert len(results['pets']) > 0
    print(len(results['pets']))
    

def test_get_list_of_all_pets_incorrected_key():
    '''негативный тест на получение списка всех питомцев 
        при авторизации с неверным ключем'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    auth_key['key'] = get_incorrected_value(auth_key['key'])
    filter = ""
        
    status, results = pf.get_list_of_pets(auth_key = auth_key, filter = filter)
    assert status == 403



def test_get_list_of_my_pets_corrected():
    '''позитивный тест на получение списка только питомцев пользователя.''' 
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    filter = "my_pets"
        
    status, results = pf.get_list_of_pets(auth_key = auth_key, filter = filter)
    assert status == 200
    count_pets = len(results['pets'])
        
    if count_pets != 0:
        print(f"my Pets = {len(results['pets'])}")
        print(results['pets'][0].keys())
        #for i in range(count_pets):
            #assert results['pets'][i]['user_id'] == auth_key['key']
    else:
        Exception("There is not pets")

def test_add_new_pet_simple_corrected():
    '''позитивный тест добавления нового питомца (упрощенный)'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    
    name = 'Sharik'
    animal_type = 'dog'
    age = 5
    
    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    
    assert status == 200
    assert results['name'] == name
    
    
def test_add_new_pet_simple_incorrected_key():
    '''негативный тест добавления питомца (упрощенно) при некорректном ключе'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    auth_key['key'] = get_incorrected_value(auth_key['key'])
    
    name = 'Sharik'
    animal_type = 'dog'
    age = 5
    
    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    
    assert status == 403
    

def test_add_new_pet_simple_incorrected_without_name():
    '''негативный тест добавления питомца (упрощенно) при незаполненном поле "name"'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    
    name = ''
    animal_type = 'dog'
    age = 5
    
    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    
    assert status == 400
    
    
def test_add_new_pet_simple_incorrected_without_animal_type():
    '''негативный тест добавления питомца (упрощенно) при незаполненном поле "animal_type"'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    
    name = 'Bobik'
    animal_type = ''
    age = 5
    
    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    
    assert status == 400
    

def test_add_new_pet_simple_incorrected_without_age():
    '''негативный тест добавления питомца (упрощенно) при незаполненном поле "age"'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    
    name = 'Barsik'
    animal_type = 'cat'
    age = None
    
    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    
    assert status == 400
    

def test_add_new_pet_simple_incorrected_str_format_age():
    '''негативный тест добавления питомца (упрощенно) при стрковом формате данных поля "age"'''
    
    _, auth_key = pf.get_api_key(v_email, v_password)
    
    name = 'Doggy'
    animal_type = 'dog'
    age = '4'
    
    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    
    assert status == 400


"""def test_add_photo_to_pet_corrected():
    '''позитивный тест добавления фото к питомцу'''

    _, auth_key = pf.get_api_key(v_email, v_password)    
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
       
    pet_photo = 'images/dog.jpg'
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        old_pet_photo = my_pets['pets'][0]['pet_photo']
        status, results = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)
        print(type(results))
        print("Results: ")
        print(results)
        
        assert status == 200

        assert results['pet_photo'] != None
        assert results['pet_photo'] != old_pet_photo
    else:
        raise Exception("There is no my pets")"""
    


def test_add_new_pet():
    _, auth_key = pf.get_api_key(v_email, v_password)
    
    name = 'Murka'
    animal_type = 'cat'
    age = '1'
    pet_photo = 'images/cat.jpg'
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    
    status, results = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert results['name'] == name
    print(type(results))
    print(results)
    
    
def test_delete_pet():
    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key = auth_key, filter = 'my_pets')
    
    #проверяем, есть ли списке питомцы
    if len(my_pets['pets']) == 0:
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = 'images/cat.jpg'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        pf.add_new_pet(auth_key, 'Bobik', 'dog', '3', pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key = auth_key, filter = 'my_pets')
    
    #получаем id первого питомца для удаления
    pet_id = my_pets['pets'][0]['id']
    
    status = pf.delete_pet(auth_key, pet_id)
    
    assert status == 200
    
    
def test_update_pet():
    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key = auth_key, filter = 'my_pets')
    
    #проверяем, есть ли списке питомцы
    if len(my_pets['pets']) == 0:
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = 'images/cat.jpg'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        pf.add_new_pet(auth_key, 'Bobik', 'dog', '3', pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key = auth_key, filter = 'my_pets')
    
    #получаем id первого питомца для изменения
    pet_id = my_pets['pets'][0]['id']
    new_name = my_pets['pets'][0]['name'] + '1'
    new_animal_type = my_pets['pets'][0]['animal_type']
    new_age = my_pets['pets'][0]['age']
    
    status, results = pf.update_pet(auth_key, pet_id, new_name, new_animal_type, new_age)
    
    assert status == 200
    _, my_pets = pf.get_list_of_pets(auth_key = auth_key, filter = 'my_pets')
    assert my_pets['pets'][0]['name'] == new_name
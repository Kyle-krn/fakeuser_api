import string
import random
from typing import List, Literal
import random
from faker import Faker
import pytz
import uuid
from datetime import datetime
import hashlib

fake_ru = Faker('ru_RU')
fake_en = Faker('en_US')

PHONE_CODE = {
    'country_code': {
        'ru': '+7',
        'eng': '+1'
    },
    'operator_code': {
        'ru': ['911', '912', '917', '919', '981', '982', 
               '987', '988', '989', '904', '921', '922', 
               '927', '929', '931', '932', '937', '939', 
               '999', '900', '901', '902', '904', '908', 
               '950', '951', '952', '953', '991', '992'],
        'eng': ['205', '251', '256', '334', '480', '520', 
               '602', '623', '928', '209', '213', '310', 
               '323', '408', '415', '424', '510', '530', 
               '559', '562', '619', '626', '650', '661', 
               '707', '714', '760', '805', '239', '305', 
               '321', '352', '386', '407', '561', '727', 
               '754', '772', '786', '813', '850', '863', 
               '904', '941']
    }
}


def generate_password(length: int, easy_to_read: bool = False, characters: List[str] = []) -> str:
    strings = ''

    punctuation = string.punctuation
    punctuation = punctuation.replace("'", "")
    punctuation = punctuation.replace('"', "")
    punctuation = punctuation.replace("\\", "")


    if "uppercase" in characters:
        strings += string.ascii_uppercase
    if "lowercase" in characters:
        strings += string.ascii_lowercase
    if "numbers" in characters:
        strings += string.digits
    if "symbols" in characters:
        strings += punctuation
    if strings == "":
        strings = string.ascii_uppercase + string.ascii_lowercase + string.digits + punctuation

    if easy_to_read:
        strings = strings.replace("l", "")
        strings = strings.replace("1", "")
        strings = strings.replace("o", "")
        strings = strings.replace("O", "")
        strings = strings.replace("0", "")
    
    return ''.join(random.choice(strings) for _ in range(length))

def generate_name(count: int, format: int, sex: Literal['male', 'female']) -> List[str]:
    names = []
    if format <= 5:
        lang = 'ru'
    else:
        lang = 'eng'
    
    if sex == 'any':
        gender = None
    else:
        gender = sex

    for i in range(count):
        if sex == 'any':
            gender = random.choice(['male', 'female'])
        name = {
            'first_name': getattr(fake_ru if lang == 'ru' else fake_en, f'first_name_{gender}')(),
            'last_name': getattr(fake_ru if lang == 'ru' else fake_en, f'last_name_{gender}')(),
            'patronymic': getattr(fake_ru, f'middle_name_{gender}')() if lang == 'ru' else None
        }
        if gender == 'male':
            if lang == 'ru':
                name['title'] = 'Г-н'
            else:
                name['title'] = 'Mr.'
        else:
            if lang == 'female':
                name['title'] = 'Г-жа'
            else:
                name['title'] = 'Mrs.'

        if format == 3:
            name['first_name'] = name['first_name'][0] + "."
            name['patronymic'] = name['patronymic'][0] + "."
        elif format == 4:
            name['last_name'] = name['last_name'][0] + "."
            name['patronymic'] = name['patronymic'][0] + "."
        names.append(name)
    return names

def generate_timezone() -> dict:
    tz_name = random.choice(pytz.all_timezones)
    tz = datetime.now(pytz.timezone(tz_name))
    offset=tz.strftime('%z')
    offset = offset[:3] +':'+ offset[3:]
    return {'offset': offset, 'description': tz_name}

def random_address(localization: Literal['ru', 'eng']) -> dict:
    random_address = {
        'street': fake_ru.street_name() if localization == 'ru' else fake_en.street_name(),
        'house': fake_ru.building_number() if localization == 'ru' else fake_en.building_number(),
        'city': fake_ru.city() if localization == 'ru' else fake_en.city(),
        'state': fake_ru.region() if localization == 'ru' else fake_en.state(),
        'country': 'Russia' if localization == 'ru' else 'USA',
        'postcode': fake_ru.postcode() if localization == 'ru' else fake_en.postcode(),
        'coordinates': {
            'lat': None,
            'long': None
        }
    }
    coord = fake_ru.local_latlng(country_code='RU' if localization == 'ru' else "US")
    random_address['coordinates']['lat'] = coord[0]
    random_address['coordinates']['long'] = coord[1]
    return random_address

def random_login(localization: Literal['ru', 'eng']):
    password = generate_password(length=8)
    return {
        'uuid': uuid.uuid4(),
        'username': fake_ru.user_name() if localization == 'ru' else fake_en.user_name(),
        'password': password,
        'md5': hashlib.md5(password.encode()).hexdigest(),
        'sha1': hashlib.sha1(password.encode()).hexdigest(),
        'sha256': hashlib.sha256(password.encode()).hexdigest()
    }

def random_job(localization: Literal['ru', 'eng']):
    return {
        'job': fake_ru.job() if localization == 'ru' else fake_en.job(),
        'company': fake_ru.company() if localization == 'ru' else fake_en.company()
    }

def random_phone_number(localization: Literal['ru', 'eng']):
    return PHONE_CODE['country_code'][localization] + random.choice(PHONE_CODE['operator_code'][localization]) + ''.join([random.choice(string.digits) for i in range(7)])
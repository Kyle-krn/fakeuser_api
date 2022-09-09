import string
import random
from typing import List, Literal
import random
from faker import Faker
import pytz
import uuid
from datetime import datetime, date, timedelta
import hashlib
from api import models
from django.conf import settings

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
            if lang == 'ru':
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

def generate_timezone(tz_name: str = None) -> dict:
    if not tz_name:
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
    tz_name = coord[4]
    random_address['coordinates']['lat'] = coord[0]
    random_address['coordinates']['long'] = coord[1]
    return tz_name, random_address

def random_login(localization: Literal['ru', 'eng']) -> dict:
    password = generate_password(length=8)
    return {
        'uuid': uuid.uuid4(),
        'username': fake_ru.user_name() if localization == 'ru' else fake_en.user_name(),
        'password': password,
        'md5': hashlib.md5(password.encode()).hexdigest(),
        'sha1': hashlib.sha1(password.encode()).hexdigest(),
        'sha256': hashlib.sha256(password.encode()).hexdigest()
    }

def random_job(localization: Literal['ru', 'eng']) -> dict:
    return {
        'job': fake_ru.job() if localization == 'ru' else fake_en.job(),
        'company': fake_ru.company() if localization == 'ru' else fake_en.company()
    }

def random_phone_number(localization: Literal['ru', 'eng']) -> str:
    return PHONE_CODE['country_code'][localization] + random.choice(PHONE_CODE['operator_code'][localization]) + ''.join([random.choice(string.digits) for i in range(7)])

def random_datetime(min_year=datetime.now().year - 5, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    random_date = start + (end - start) * random.random()
    return {'date': random_date,
            'days': (datetime.now() - random_date).days}

def random_email(localization: Literal['ru', 'eng']) -> str:
    return fake_en.email() if localization == 'ru' else fake_ru.email()

def random_dob(age: int = None) -> dict:
    if not age:
        age = random.randint(18, 60)
    return {
        'date': date.today() - timedelta(days=365*age),
        'age': age
    }

def random_photo(gender: Literal['male', 'female']) -> dict:
    photo_model = random.choice(models.UserPhoto.objects.filter(gender=gender))
    photo = {
        'small': settings.HOST + photo_model.photo_100.url,
        'medium': settings.HOST + photo_model.photo_200.url,
        'original': settings.HOST + photo_model.photo.url
    }
    return photo_model.age, photo

class RandomUser:

    def __init__(self, 
                 gender: Literal['male', 'female'] = None, 
                 localization: Literal['ru', 'eng'] = None) -> None:
        self.gender = gender if gender in ('male', 'female') else random.choice(('male', 'female'))
        self.localization = localization if localization in ('ru', 'eng') else random.choice(('ru', 'eng'))
        self.nat = 'Russian' if localization == 'ru' else 'American'
        self.name = generate_name(count=1, 
                                   format=0 if self.localization == 'ru' else 6,
                                   sex=self.gender)[0]
        self.__init_address()
        self.email = random_email(self.localization)
        self.login = random_login(self.localization)
        self.job = random_job(self.localization)
        self.age = None
        self.__init_photo()
        self.__init_dob()
        self.registered = random_datetime()
        self.phone = random_phone_number(localization=self.localization)

        self.__accept_fields = ['gender', 'name', 'timezone', 'location', 
                                'email', 'login', 'job', 'dob', 
                                'registered','phone','photo','nat']
        
    def __init_address(self) -> None:
        tz_name, self.location = random_address(self.localization)
        self.timezone = generate_timezone(tz_name)

    def __init_photo(self) -> None:
        photo_model = random.choice(models.UserPhoto.objects.filter(gender=self.gender))
        self.age = photo_model.age
        self.photo = {
            'small': settings.HOST + photo_model.photo_100.url,
            'medium': settings.HOST + photo_model.photo_200.url,
            'original': settings.HOST + photo_model.photo.url
        }

    def __init_dob(self) -> None:
        if not self.age:
           self.age = random.randint(18, 60)
        self.dob = {
            'date': date.today() - timedelta(days=365*self.age),
            'age': self.age
        }

    def return_dict(self, 
                    include: List[str] = [], 
                    exclude: List[str] = []) -> dict:
        fields = [i for i in include if i in self.__accept_fields]
        if len(fields) == 0:
            fields = self.__accept_fields
        print(fields)
        fields = [i for i in fields if i not in exclude]
        print(fields)
        return {i: getattr(self, i) for i in fields}
        

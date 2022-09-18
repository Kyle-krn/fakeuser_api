from typing import List, Literal
from faker import Faker
from datetime import datetime, date, timedelta
from api import models
from django.conf import settings
import hashlib
import pytz
import string
import random


common_faker = Faker(['ru_RU', 'en_US'])

NATIONALITY = ['ru', 'us', 'aze', 'bgd', 'cze', 'dnk', 'deu', 'grc', 'chl']

LOCAL_LITERAL = Literal['ru', 'us', 'aze', 'bgd', 'cze', 'dnk', 'deu', 'grc', 'chl']

USER_ACCEPT_FIELDS = ['gender', 'name', 'timezone', 'location', 
                      'email', 'login', 'job', 'dob', 
                      'registered','phone','photo','nat', 'ssn']

PHONE_CODE = {
    'country_code': {
        'ru': '+7',
        'us': '+1',
        'aze': '+994',
        'bgd': '+880',
        'cze': '+420',
        'dnk': '+45',
        'deu': '+49',
        'grc': '+30',
        'chl': '+56'
    },
    'operator_code': {
        'ru': ['911', '912', '917', '919', '981', '982', 
               '987', '988', '989', '904', '921', '922', 
               '927', '929', '931', '932', '937', '939', 
               '999', '900', '901', '902', '904', '908', 
               '950', '951', '952', '953', '991', '992'],
        'us': ['205', '251', '256', '334', '480', '520', 
               '602', '623', '928', '209', '213', '310', 
               '323', '408', '415', '424', '510', '530', 
               '559', '562', '619', '626', '650', '661', 
               '707', '714', '760', '805', '239', '305', 
               '321', '352', '386', '407', '561', '727', 
               '754', '772', '786', '813', '850', '863', 
               '904', '941'],
        'aze': ['12', '123', '124', '125', '20', '88', '192', '193', '113'],
        'bgd': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],
        'cze': ['601', '602', '606', '607', '603', '604', '605', '608', '70', '72', '73', '77', '79', '91'],
        'dnk': ['4281', '4282', '4283', '4284', '4285', '4286', '4287', '4288', '4289', '4290'],
        'deu': ['0151', '0160', '0170', '0171', '0175', '0152', '0162', '0172', '0173', '0174'],
        'grc': ['697', '698', '697', '694', '695', '690', '693', '699'],
        'chl': ['9939', '9929', '9931', '9935', '9941', '9947']
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
    password = ''.join(random.choice(strings) for _ in range(length))
    return password


def generate_name(count: int, 
                  lang: str, 
                  sex: Literal['male', 'female'] = 'any') -> List[str]:
    names = []
    # if format <= 5:
    #     lang = 'ru'
    # else:
    #     lang = 'us'
    
    faker: Faker = common_faker['ru_RU' if lang == 'ru' else 'en_US']
    
    if sex == 'any':
        gender = None
    else:
        gender = sex

    for i in range(count):
        if sex == 'any':
            gender = random.choice(['male', 'female'])
        name = {
            'title': get_title(gender=gender, localization=lang),
            'first_name': getattr(faker, f'first_name_{gender}')(),
            'last_name': getattr(faker, f'last_name_{gender}')(),
            'patronymic': getattr(faker, f'middle_name_{gender}')() if lang == 'ru' else None
        }
        names.append(name)
    return names


def get_title(gender: Literal['male', 'female'], localization: LOCAL_LITERAL):
    if localization == 'ru':
        if gender == 'male':
            return 'Г-н'
        else:
            return 'Г-жа'    
    elif localization == 'us':
        if gender == 'male':
            return 'Mr.'
        else:
            return 'Mrs.'
    return None


def generate_timezone(tz_name: str = None) -> dict:
    if not tz_name:
        tz_name = random.choice(pytz.all_timezones)
    tz = datetime.now(pytz.timezone(tz_name))
    offset=tz.strftime('%z')
    offset = offset[:3] +':'+ offset[3:]
    return {'offset': offset, 'description': tz_name}


def random_address(localization: LOCAL_LITERAL,
                   user_faker: Faker = None) -> dict:
    faker: Faker = (faker["ru_RU" if localization == 'ru' else 'en_US']) if not user_faker else user_faker
    region_name_attr = {
        'ru': 'region',
        'us': 'state',
        'aze': 'administrative_unit',
        'bgd': 'administrative_unit',
        'cze': 'administrative_unit',
        'dnk': 'administrative_unit',
        'deu': 'administrative_unit',
        'grc': 'administrative_unit',
        'chl': 'administrative_unit',
    }
    random_address = {
        'street': faker.street_name(),
        'house': faker.building_number(),
        'city': faker.city(),
        'state': getattr(faker, region_name_attr[localization])(),
        'country': faker.current_country(),
        'postcode': faker.postcode(),
        'coordinates': {
            'lat': None,
            'long': None
        }
    }
    coord = faker.local_latlng(faker.current_country_code())
    if localization == 'grc':
        tz_name = 'Europe/Athens'
    else:
        tz_name = coord[4]
    random_address['coordinates']['lat'] = coord[0]
    random_address['coordinates']['long'] = coord[1]
    return tz_name, random_address    


def random_datetime(min_year=datetime.now().year - 5, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    random_date = start + (end - start) * random.random()
    return {'date': random_date,
            'days': (datetime.now() - random_date).days}


def func_locale(country_name: str):
    if country_name == 'ru':
        return 'ru_RU', 'Russian'
    elif country_name == 'us':
        return 'en_US', 'American'
    elif country_name == 'aze':
        return 'az_AZ', 'Azerbaijani'
    elif country_name == 'bgd':
        return 'bn_BD', 'Bangladeshi',
    elif country_name == 'cze':
        return 'cs_CZ', 'Czech'
    elif country_name == 'dnk':
        return 'da_DK', 'Danish'
    elif country_name == 'deu':
        return 'de_DE', 'German'
    elif country_name == 'grc':
        return 'el_GR', 'Greek'
    elif country_name == 'chl':
        return 'es_CL', 'Chilean'


class RandomUser:
    def __init__(self,
                 user_faker: Faker,
                 photo_models: List,
                 return_fields: List[str],
                 gender: Literal['male', 'female'] = None, 
                 localization: List = None
                 ) -> None:
        self.return_fields = return_fields

        self.gender = gender if gender in ('male', 'female') else random.choice(('male', 'female')) #643ms
        self.localization = localization if localization in NATIONALITY else 'us'
        locale, nat = func_locale(self.localization)
        self.faker = user_faker[locale] #618ms
        self.nat = nat #623ms
        if 'name' in self.return_fields:
            self.__init_name() #978ms
        if 'location' in self.return_fields:
            self.__init_address() #3s
        if 'location' not in self.return_fields and 'timezone' in self.return_fields:
             self.timezone = generate_timezone()
        if 'email' in self.return_fields:
            self.email = self.faker.email() #3s
        if 'login' in self.return_fields:
            self.__init_login() #3.68s
        if 'job' in self.return_fields:
            self.__init_job()
        self.age = None
        if 'photo' in self.return_fields:
            self.__init_photo(photo_models[0 if self.gender == 'male' else 1])
        if 'dob' in self.return_fields:
            self.__init_dob()
        if 'registered' in self.return_fields:
            self.registered = random_datetime()
        if 'phone' in self.return_fields:
            self.__init_phone_number()
        if 'ssn' in self.return_fields:
            self.__init_ssn()
        self.__accept_fields = ['gender', 'name', 'timezone', 'location', 
                                'email', 'login', 'job', 'dob', 
                                'registered','phone','photo','nat', 'ssn']
    
    def __init_name(self):
        self.name = {
            'title': get_title(gender=self.gender, localization=self.localization),
            'first_name': getattr(self.faker, f'first_name_{self.gender}')(),
            'last_name': getattr(self.faker, f'last_name_{self.gender}')(),
            'patronymic': getattr(self.faker, f'middle_name_{self.gender}')() if self.localization == 'ru' else None
        }
        
    def __init_address(self) -> None:
        tz_name, self.location = random_address(self.localization, self.faker) #2.19s
        if self.localization == 'bgd':
            tz_name = 'Asia/Dhaka'
        if 'timezone' in self.return_fields:
            self.timezone = generate_timezone(tz_name)

    def __init_photo(self, photo_models) -> None:
        photo_model = random.choice(photo_models)
        self.age = photo_model.age
        self.photo = {
            'small': settings.HOST + photo_model.photo_100.url,
            'medium': settings.HOST + photo_model.photo_200.url,
            'original': settings.HOST + photo_model.photo.url
        }

    def __init_job(self) -> None:
        self.job = {
            'job': self.faker.job(),
            'company': self.faker.company()
        }

    def __init_dob(self) -> None:
        if not self.age:
            self.age = random.randint(18, 60)
        self.dob = {
            'date': date.today() - timedelta(days=365*self.age),
            'age': self.age
        }

    def __init_login(self) -> None:
        password = generate_password(length=8)
        self.login = {
            'uuid': self.faker.uuid4(),
            'username': self.faker.user_name(),
            'password': password,
            'md5': hashlib.md5(password.encode()).hexdigest(),
            'sha1': hashlib.sha1(password.encode()).hexdigest(),
            'sha256': hashlib.sha256(password.encode()).hexdigest()
        }

    def __init_phone_number(self):
        self.phone = PHONE_CODE['country_code'][self.localization] + random.choice(PHONE_CODE['operator_code'][self.localization]) + ''.join([random.choice(string.digits) for i in range(7)])

    def __init_ssn(self):
        self.ssn = self.faker.ssn() if self.localization != 'dnk' else None

    def return_dict(self) -> dict:
        return {i: getattr(self, i) for i in self.return_fields if i in self.__dict__}
        

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class HotelItem(Item):
    collection = table = 'Hotel'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    price = Field()
    location = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    walk_distance = Field()
    is_bookable = Field()
    pic_array = Field()
    number = Field()


class ServiceItem(Item):
    collection = table = 'Service'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    score = Field()
    service = Field()
    environment = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class ShoppingItem(Item):
    collection = table = 'Shopping'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    quality = Field()
    environment = Field()
    service = Field()
    type = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class FoodItem(Item):
    collection = table = 'Food'

    title = Field()
    url = Field()
    branch = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    taste = Field()
    environment = Field()
    service = Field()
    type = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    recommend = Field()
    number = Field()


class CarItem(Item):
    collection = table = 'Car'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class PetItem(Item):
    collection = table = 'Pet'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    service = Field()
    environment = Field()
    economical = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class FilmItem(Item):
    collection = table = 'Film'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class FilmItem2(Item):
    collection = table = 'Film2'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class HomeItem(Item):
    collection = table = 'Home'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    contract_price = Field()
    type = Field()
    img = Field()
    district = Field()
    location = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    design = Field()
    designer = Field()
    number = Field()


class WeddingItem(Item):
    collection = table = 'Wedding'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    location = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    product_photos = Field()
    number = Field()


class BeautyItem(Item):
    collection = table = 'Beauty'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    effect = Field()
    environment = Field()
    service = Field()
    type = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class BabyItem(Item):
    collection = table = 'Baby'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    location = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    product_photos = Field()
    number = Field()


class LifeItem(Item):
    collection = table = 'Life'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    score = Field()
    environment = Field()
    service = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class EducationItem(Item):
    collection = table = 'Educaton'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    effect = Field()
    teachers = Field()
    environment = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class MedicalItem(Item):
    collection = table = 'Medical'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    effect = Field()
    environment = Field()
    service = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class SportsItem(Item):
    collection = table = 'Sports'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    score = Field()
    environment = Field()
    service = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()


class TourItem(Item):
    collection = table = 'Tour'

    title = Field()
    url = Field()
    star = Field()
    review_num = Field()
    mean_price = Field()
    img = Field()
    type = Field()
    location = Field()
    address = Field()
    score = Field()
    environment = Field()
    service = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    branch = Field()
    number = Field()

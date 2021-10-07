from django.core.checks import messages
from django.db import models
import random
import math
from django.urls import reverse
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import uuid

Type_CHOICES = (
    ('city', 'CITY'),
    ('state', 'STATE'),
    ('locality', 'LOCALITY'),
)
Type_CHOICES_Ad = (
    ('adventure', 'ADVENTURE'),
    ('tour', 'TOUR'),
)



class Destination(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=200, choices=Type_CHOICES, default='', null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    faq = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    covid_status = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    how_to_reach = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    readmore = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)

    def __str__(self):
        return self.name


class AdventureTourTypes(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=200, choices=Type_CHOICES_Ad, default='', null=True, blank=True)
    best_time_visit = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    top_10_places = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    readmore = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    faq = models.CharField(max_length=1000, default="", null=True, blank=True)
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Citie(models.Model):
    city = models.CharField(max_length=300)
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)

    def __str__(self):
        return self.city


class Product(models.Model):
    name = models.CharField(max_length=200, default="", null=True, blank=True)
    description = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    rating = models.CharField(
        max_length=50, default="0", null=True, blank=True)
    regular = models.IntegerField(default=0, null=True, blank=True)
    sale = models.IntegerField(default=0, null=True, blank=True)
    child = models.IntegerField(default=0, null=True, blank=True)
    sale_child = models.IntegerField(default=0, null=True, blank=True)
    days = models.IntegerField(default=0, null=True, blank=True)
    location = models.CharField(
        max_length=50, default="", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    manual_slug = models.SlugField(
        max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, default="", null=True, blank=True)
    country = models.CharField(
        max_length=50, default="", null=True, blank=True)
    highlights = models.CharField(
        max_length=100000, default="", null=True, blank=True)
    overview = models.CharField(
        max_length=100000, default="", null=True, blank=True)
    inclusion = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    a_inclusion = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    overview = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    category = models.CharField(
        max_length=500, default="", null=True, blank=True)
    tag_category = models.CharField(
        max_length=500, default="", null=True, blank=True)
    duration_type = models.CharField(
        max_length=100, default="", null=True, blank=True)
    duration = models.CharField(
        max_length=100, default="", null=True, blank=True)
    loca_city = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    city = models.CharField(max_length=200, default="", null=True, blank=True)
    locality = models.CharField(
        max_length=100, default="", null=True, blank=True)
    start_loc = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    map = models.CharField(max_length=2000, default="", null=True, blank=True)
    adventuretype = models.CharField(
        max_length=50, default="", null=True, blank=True)
    adventurelevel = models.CharField(
        max_length=50, default="", null=True, blank=True)
    adventureloc = models.CharField(
        max_length=50, default="", null=True, blank=True)
    reviews = models.CharField(
        max_length=50, default="", null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    order = models.IntegerField(default=0, null=True, blank=True)
    cashback = models.IntegerField(default=0, null=True, blank=True)
    additional_info = models.CharField(
        max_length=100000, default="", null=True, blank=True)
    ques1 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ques2 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ques3 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ques4 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ques5 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ans1 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ans2 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ans3 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ans4 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    ans5 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    tags = TaggableManager()
    promo_code = models.CharField(max_length=100,default='AU')
    margin = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products", kwargs={"slug": self.slug})


class des(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(
        max_length=1000, default="", blank=True, null=True)


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)


class duration(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Countries(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Erp(models.Model):
    due = models.CharField(max_length=2000, default="", null=True, blank=True)
    dueh1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    dueh2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    dueh3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    duet1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    duet2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    duet3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    net = models.CharField(max_length=2000, default="", null=True, blank=True)
    name = models.CharField(max_length=2000, default="", null=True, blank=True)
    phone = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    email = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    package = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    start_date = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    total_cost = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    agent = models.CharField(max_length=500, default="", null=True, blank=True)
    agent_phone = models.CharField(
        max_length=500, default="", null=True, blank=True)
    reminder_date = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    booking_id = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    booking_date = models.DateField(auto_now=False, auto_now_add=False)
    payment_client1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_date1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1 = models.CharField(max_length=2000, default="", null=True, blank=True)
    comment1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_client2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_date2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2 = models.CharField(max_length=2000, default="", null=True, blank=True)
    comment2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_client3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_date3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3 = models.CharField(max_length=2000, default="", null=True, blank=True)
    comment3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_client4 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment_date4 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4 = models.CharField(max_length=2000, default="", null=True, blank=True)
    comment4 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_name1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_contact1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_phone1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_cost1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_comment1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_name2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_contact2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_phone2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_cost2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_comment2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_name3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_contact3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_phone3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_cost3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    hotel_comment3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment1_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet1_date_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment1_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment2_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet2_date_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment2_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment3_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet3_date_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment3_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment4_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet4_date_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment4_hotel1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment1_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet1_date_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment1_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment2_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet2_date_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment2_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment3_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet3_date_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment3_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment4_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet4_date_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment4_hotel2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment1_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet1_date_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment1_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment2_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet2_date_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment2_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment3_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet3_date_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment3_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment4_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet4_date_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment4_hotel3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_name1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_contact1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_phone1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_cost1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_comment1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_name2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_contact2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_phone2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_cost2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_comment2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_name3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_contact3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_phone3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_cost3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    transport_comment3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment1_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet1_date_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment1_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment2_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet2_date_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment2_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment3_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet3_date_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment3_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment4_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet4_date_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment4_transport1 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment1_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet1_date_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment1_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment2_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet2_date_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment2_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment3_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet3_date_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment3_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment4_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet4_date_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment4_transport2 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment1_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet1_date_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop1_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment1_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment2_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet2_date_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop2_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment2_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment3_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet3_date_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop3_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment3_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    payment4_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    paymet4_date_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    mop4_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    comment4_transport3 = models.CharField(
        max_length=2000, default="", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Emr", kwargs={"slug": self.slug})


class Itinerary(models.Model):
    phone = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    name = models.CharField(max_length=2000, default="", null=True, blank=True)
    location = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    person = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    category = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    hotel_type = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    meal_type = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    vehicle = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    other_inclusion = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    start_loc = models.CharField(
        max_length=2000, default="", null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    end_loc = models.CharField(
        max_length=200, default="", null=True, blank=True)
    days1 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days2 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days3 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days4 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days5 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days5 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days6 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days7 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days8 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days9 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days10 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days11 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    days12 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    textdays1 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays2 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays3 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays4 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays5 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays6 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays7 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays8 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays9 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays10 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays11 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    textdays12 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    hotel_location1 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    hotel_location2 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    hotel_location3 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    hotel_location4 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    meal_type1 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    meal_type2 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    meal_type3 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    meal_type4 = models.CharField(
        max_length=10000, default="", null=True, blank=True)
    hotel_nights1 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_nights2 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_nights3 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_nights4 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_rooms1 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_rooms2 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_rooms3 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_rooms4 = models.CharField(
        max_length=500, default="", null=True, blank=True)
    hotel_name1 = models.CharField(
        max_length=50000, default="", null=True, blank=True)
    hotel_name2 = models.CharField(
        max_length=5000, default="", null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    hotel_name3 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    hotel_name4 = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    payment = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    payment_type = models.CharField(
        max_length=5000, default="", null=True, blank=True)
    agent = models.CharField(max_length=500, default="", null=True, blank=True)
    agent_phone = models.CharField(
        max_length=500, default="", null=True, blank=True)
    payment2 = models.CharField(
        max_length=10000, default="", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("itinerarys", kwargs={"slug": self.slug})


class Blogpost(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length=50)
    head0 = models.CharField(max_length=50, default="")
    chead0 = models.CharField(max_length=5000, default="")
    head1 = models.CharField(max_length=300, default="")
    chead1 = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=300, default="")
    chead2 = models.CharField(max_length=10000, default="")
    slug = models.SlugField(unique=True, null=True, blank=True)
    pub_date = models.DateField()
    thumbnail = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogposts", kwargs={"slug": self.slug})


class states(models.Model):
    Country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(null=False, default="", max_length=50)
    phone = models.CharField(null=False, default="", max_length=10)

    def __str__(self):
        return self.name


class wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(null=True, default=0)
    wallet_id = str(models.AutoField)


Coupon_Type_CHOICES = (
    ('price', 'PRICE'),
    ('percentage', 'PERCENTAGE'),
)
Status_Type_CHOICES = (
    ('active', 'ACTIVE'),
    ('inactive', 'INACTIVE'),
)


class promo(models.Model):
    coupon = models.CharField(null=False, default="", max_length=50)
    email = models.CharField(null=False, default="", max_length=500)
    price = models.IntegerField(null=True, default=0)
    type = models.CharField(
        max_length=200, choices=Coupon_Type_CHOICES, default='', null=False)
    date = models.CharField(null=False, default="", max_length=50)
    status = models.CharField(
        max_length=200, choices=Status_Type_CHOICES, default='', null=False)
    margin = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.coupon



class Affiliate(models.Model):
    coupon = models.CharField(null=False, default="", max_length=50)
    email = models.CharField(null=False, default="", max_length=500)
    total_price = models.IntegerField(null=True, default=0)
    margin_earned = models.CharField(null=False, default="", max_length=50)
    product = models.CharField(null=False, default="", max_length=2000)
    date = models.CharField(null=False, default="", max_length=500)
    coupon_uid = models.CharField(null=False, default="", max_length=500)

    def __str__(self):
        return self.coupon

# =============================== affiliate user link ==============================
def from_100000():
    largest = AffiliateUser.objects.all().order_by('aid').last()
    if not largest:
        return 123456
    return largest.aid + 1

class AffiliateUser(models.Model):
    name = models.CharField(max_length=500,null=True,blank=True)
    email = models.EmailField(max_length=500,null=True,blank=True)
    phone = models.CharField(max_length=16,null=True,blank=True)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    account_number = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    upi_id = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True)
    status = models.CharField(max_length=200, choices=Status_Type_CHOICES, default='inactive', null=True, blank=True)
    photo_copy = models.FileField(upload_to='uploads/affiliate_photo_id',null=True,blank=True)
    aid = models.PositiveBigIntegerField(default=from_100000,null=True,blank=True)

    def __str__(self):
        return str(self.name)

class AffiliateEarning(models.Model):
    aid = models.ForeignKey(AffiliateUser, on_delete=models.CASCADE)
    margin = models.CharField(null=True,max_length=50)
    total_price = models.IntegerField(null=True, default=0)


    def __str__(self):
        return str(self.aid)

class AffiliateLink(models.Model):
    aid = models.ForeignKey(AffiliateUser, on_delete=models.CASCADE)
    link = models.CharField(max_length=50000,null=True,blank=True)
    date = models.DateField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.aid)

Payment_Status_Type_CHOICES = (
    ('done', 'DONE'),
    ('notdone', 'NOTDONE'),
)

class AffiliateWithdraw(models.Model):
    aid = models.ForeignKey(AffiliateUser ,on_delete=models.CASCADE)
    name = models.CharField(max_length=10000,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    amount = models.CharField(max_length=2000,null=True,blank=True)
    payemt_status =  models.CharField(max_length=200, choices=Payment_Status_Type_CHOICES,
     default='notdone', null=True, blank=True)
    

    def __str__(self):
        return str(self.aid)
    


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True)
    date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    days = models.IntegerField(null=True, default=1)
    orderId = models.CharField(null=True, max_length=100)
    orderAmount = models.CharField(null=True, max_length=50)
    referenceId = models.CharField(null=True, max_length=100)
    coupon_uid = models.CharField(null=False, default="", max_length=500)
    aid = models.CharField(max_length=50,null=True,blank=True)
    margin = models.IntegerField(default=0,null=True,blank=True)
    created = models.DateTimeField(
        null=True, auto_now=True, auto_now_add=False, blank=True)

    def __str__(self):
        return self.orderId


class TravelGuide(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=200, choices=Type_CHOICES, default='', null=True, blank=True)
    tag = CharField(max_length=200, null=True, blank=True)
    manual_slug = models.SlugField(
        max_length=100, null=True, blank=True)
    heading = models.CharField(max_length=500, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    blog1 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog2 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog3 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog4 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog5 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog6 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog7 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog8 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog9 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog10 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog11 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog12 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog13 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog14 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog15 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog16 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog17 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog18 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog19 = models.CharField(
        max_length=50000, null=True, blank=True)
    blog20 = models.CharField(
        max_length=50000, null=True, blank=True)
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)


    def __str__(self):
        return self.name


class Populartags(models.Model):
    name = CharField(max_length=100, null=True, blank=True)
    link = CharField(max_length=200, null=True, blank=True)
    tag = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class TopPicksEntryForm(models.Model):
    heading = models.CharField(max_length=200,null=True,blank=True)
    cover_img = models.ImageField(upload_to='uploads/TopPicks/', null=True, blank=True)
    manual_slug = models.SlugField(max_length=100, null=True, blank=True)
    box1_text = models.CharField(max_length=200,null=True,blank=True)
    box1_background = models.ImageField(upload_to='uploads/TopPicks/',null=True,blank = True)
    box1_url = models.URLField(max_length=200,null=True,blank=True)
    box2_text = models.CharField(max_length=200,null=True,blank=True)
    box2_background = models.ImageField(upload_to='uploads/TopPicks/',null=True,blank = True)
    box2_url = models.URLField(max_length=200,null=True,blank=True)
    box3_text = models.CharField(max_length=200,null=True,blank=True)
    box3_background = models.ImageField(upload_to='uploads/TopPicks/',null=True,blank = True)
    box3_url = models.URLField(max_length=200,null=True,blank=True)
    text5 = models.CharField(max_length=200,null=True,blank=True)
    text5_image = models.ImageField(upload_to='uploads/TopPicks/',null=True,blank = True)
    text_1 = models.CharField(max_length=300,null=True,blank=True)
    slug_1 = models.CharField(max_length=300,null=True,blank=True)
    text_2 = models.CharField(max_length=300,null=True,blank=True)
    slug_2 = models.CharField(max_length=300,null=True,blank=True)
    text_3 = models.CharField(max_length=300,null=True,blank=True)
    slug_3 = models.CharField(max_length=300,null=True,blank=True)
    text_4 = models.CharField(max_length=300,null=True,blank=True)
    slug_4 = models.CharField(max_length=300,null=True,blank=True)
    text_5 = models.CharField(max_length=300,null=True,blank=True)
    slug_5 = models.CharField(max_length=300,null=True,blank=True)
    text_6 = models.CharField(max_length=300,null=True,blank=True)
    slug_6 = models.CharField(max_length=300,null=True,blank=True)
    text_7 = models.CharField(max_length=300,null=True,blank=True)
    slug_7 = models.CharField(max_length=300,null=True,blank=True)
    text_8 = models.CharField(max_length=300,null=True,blank=True)
    slug_8 = models.CharField(max_length=300,null=True,blank=True)
    text_9 = models.CharField(max_length=300,null=True,blank=True)
    slug_9 = models.CharField(max_length=300,null=True,blank=True)
    text_10 = models.CharField(max_length=300,null=True,blank=True)
    slug_10 = models.CharField(max_length=300,null=True,blank=True)
    text_11 = models.CharField(max_length=300,null=True,blank=True)
    slug_11 = models.CharField(max_length=300,null=True,blank=True)
    text_12 = models.CharField(max_length=300,null=True,blank=True)
    slug_12 = models.CharField(max_length=300,null=True,blank=True)
    text_13 = models.CharField(max_length=300,null=True,blank=True)
    slug_13 = models.CharField(max_length=300,null=True,blank=True)
    text_14 = models.CharField(max_length=300,null=True,blank=True)
    slug_14 = models.CharField(max_length=300,null=True,blank=True)
    text_15 = models.CharField(max_length=300,null=True,blank=True)
    slug_15 = models.CharField(max_length=300,null=True,blank=True)
    text_16 = models.CharField(max_length=300,null=True,blank=True)
    slug_16 = models.CharField(max_length=300,null=True,blank=True)
    text_17 = models.CharField(max_length=300,null=True,blank=True)
    slug_17 = models.CharField(max_length=300,null=True,blank=True)
    text_18 = models.CharField(max_length=300,null=True,blank=True)
    slug_18 = models.CharField(max_length=300,null=True,blank=True)
    text_19 = models.CharField(max_length=300,null=True,blank=True)
    slug_19 = models.CharField(max_length=300,null=True,blank=True)
    text_20 = models.CharField(max_length=300,null=True,blank=True)
    slug_20 = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.heading

class BestPackage(models.Model):
    top_picks = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    number = models.CharField(max_length=12,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    date_of_travel = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    number_of_people = models.IntegerField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name


class ProductEnquiry(models.Model):
    product_slug = models.CharField(max_length=300,null=True,blank=True)
    name = models.CharField(max_length=300,null=True,blank=True)
    number = models.CharField(max_length=12,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    date_of_travel = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    number_of_people = models.IntegerField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = wallet.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)


def pre_save_post_reciever(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    exists = Product.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" % (slugify(instance.name), instance.id)
    instance.slug = slug


pre_save.connect(pre_save_post_reciever, sender=Product)


def pre_save_post_reciever2(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exists = Product.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" % (slugify(instance.title), instance.id)
    instance.slug = slug


pre_save.connect(pre_save_post_reciever2, sender=Blogpost)


def pre_save_post_reciever3(sender, instance, *args, **kwargs):
    slug = slugify(instance.phone+'-'+instance.name+'-'+instance.location)
    exists = Itinerary.objects.filter(slug=slug).exists()
    instance.slug = slug


pre_save.connect(pre_save_post_reciever3, sender=Itinerary)





# ========================================= course Model =======================================

Type_dur = (
    ('hour','Hour'),
    ('day','Day'),
)

class Course(models.Model):
    state = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    locality = models.CharField(max_length=200,null=True,blank=True)
    course_name = models.CharField(max_length=250,null=True,blank=True)
    course_category = models.CharField(max_length=200,null=True,blank=True)
    course_duration = models.IntegerField(null=True,blank=True)
    course_dur_type = models.CharField(max_length=200,choices=Type_dur ,default="" ,null=True,blank=True)
    course_level = models.CharField(max_length=200,null=True,blank=True)
    popularity = models.IntegerField(null=True,blank=True)

    course_display_name = models.CharField(max_length=300,null=True,blank=True)
    certification = models.CharField(max_length=300,null=True,blank=True)
    trainer_detail = models.CharField(max_length=300,null=True,blank=True)
    manual_slug = models.SlugField(max_length=300,null=True,blank=True)

    summary = models.CharField(max_length=100000,null=True,blank=True)
    achivement = models.CharField(max_length=100000,null=True,blank=True)
    course_details = models.CharField(max_length=100000,null=True,blank=True)
    inclusion = models.CharField(max_length=100000,null=True,blank=True)
    after_course_next_step = models.CharField(max_length=100000,null=True,blank=True)
    regular_price = models.IntegerField(default=0,null=True,blank=True)
    sale_price = models.IntegerField(default=0,null=True,blank=True)
    cover_image = models.ImageField(upload_to='uploads/course',null=True,blank=True)
    image2 = models.ImageField(upload_to='uploads/course',null=True,blank=True)
    image3 = models.ImageField(upload_to='uploads/course',null=True,blank=True)
    image4 = models.ImageField(upload_to='uploads/course',null=True,blank=True)

    def __str__(self):
        return self.course_display_name

    


class StateItineraryData(models.Model):
    state = models.CharField(max_length=150,null=True,blank=True)
    trip_name = models.CharField(max_length=1000,null=True,blank=True)
    trip_category = models.CharField(max_length=500,null=True,blank=True)
    locations = models.CharField(max_length=1000,null=True,blank=True)
    day_schedule_heading = models.CharField(max_length=600,blank=True,null=True)
    day_schedule_itinerary = models.TextField(null=True,blank=True)
    activity_name = models.CharField(max_length=500,null=True,blank=True)
    activity_price = models.IntegerField(null=True,blank=True)
    other_transport_name = models.CharField(max_length=500,null=True,blank=True)
    other_transport_price = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.state
    
    
class CityHotelData(models.Model):
    state = models.CharField(max_length=150,null=True,blank=True)
    city = models.CharField(max_length=150,null=True,blank=True)
    accommodation_category = models.CharField(max_length=200,null=True,blank=True)
    stay_name = models.CharField(max_length=500,null=True,blank=True)
    room_type = models.CharField(max_length=500,null=True,blank=True)
    meal_type = models.CharField(max_length=500,null=True,blank=True)
    room_sharing = models.CharField(max_length=500,null=True,blank=True)
    honeymoon_kit_price = models.IntegerField(blank=True,null=True)
    total_price = models.IntegerField(blank=True,null=True)
    hotel_link = models.URLField(max_length=500,null=True,blank=True)
    image1 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)
    image2 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)
    image3 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)
    image4 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)
    image5 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)
    image6 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)
    image7 = models.ImageField(upload_to='uploads/hotel-img',null=True,blank=True)

    def __str__(self):
        return self.stay_name



class ItineraryData(models.Model):
    name = models.CharField(max_length=1000,null=True , blank=True)
    number = models.CharField(max_length=1000,null=True,blank=True)
    email = models.EmailField(max_length=254 , null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    state = models.CharField(max_length=1000,null=True , blank=True)
    trip_name = models.CharField(max_length=2000,null=True , blank=True)
    package_display_name = models.CharField(max_length=2000,null=True , blank=True)
    date_of_travel = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    trip_category = models.CharField(max_length=2000,null=True , blank=True)
    starting_location = models.CharField(max_length=5000,null=True , blank=True)
    ending_location = models.CharField(max_length=5000,null=True , blank=True)
    no_of_days = models.CharField(max_length=2000,null=True , blank=True)

    trip_highlights = models.CharField(max_length=10000,null=True , blank=True)
    additional_inclusion =  models.CharField(max_length=10000,null=True , blank=True)

    day_1 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_1 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_1 = models.CharField(max_length=20000,null=True , blank=True) 
    day_2 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_2 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_2 = models.CharField(max_length=20000,null=True , blank=True) 
    day_3 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_3 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_3 = models.CharField(max_length=20000,null=True , blank=True) 
    day_4 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_4 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_4 = models.CharField(max_length=20000,null=True , blank=True) 
    day_5 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_5 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_5 = models.CharField(max_length=20000,null=True , blank=True) 
    day_6 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_6 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_6 = models.CharField(max_length=20000,null=True , blank=True) 
    day_7 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_7 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_7 = models.CharField(max_length=20000,null=True , blank=True) 
    day_8 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_8 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_8 = models.CharField(max_length=20000,null=True , blank=True) 
    day_9 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_9 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_9 = models.CharField(max_length=20000,null=True , blank=True) 
    day_10 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_10 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_10 = models.CharField(max_length=20000,null=True , blank=True) 
    day_11 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_11 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_11 = models.CharField(max_length=20000,null=True , blank=True) 
    day_12 = models.CharField(max_length=2000,null=True , blank=True)
    day_heading_12 = models.CharField(max_length=5000,null=True , blank=True)
    day_itinerary_12 = models.CharField(max_length=20000,null=True , blank=True) 
    
    inclusion_exclusion = models.CharField(max_length=20000,null=True , blank=True) 
    activity_1 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_person_1 = models.CharField(max_length=5000,null=True , blank=True)
    activity_price_1 = models.CharField(max_length=5000,null=True , blank=True)
    activity_2 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_person_2 = models.CharField(max_length=5000,null=True , blank=True)
    activity_price_2 = models.CharField(max_length=5000,null=True , blank=True)
    activity_3 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_person_3 = models.CharField(max_length=5000,null=True , blank=True)
    activity_price_3 = models.CharField(max_length=5000,null=True , blank=True)
    activity_4 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_person_4 = models.CharField(max_length=5000,null=True , blank=True)
    activity_price_4 = models.CharField(max_length=5000,null=True , blank=True)
    activity_5 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_person_5 = models.CharField(max_length=5000,null=True , blank=True)
    activity_price_5 = models.CharField(max_length=5000,null=True , blank=True)

    hotel_city_name_1 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_stay_name_1 = models.CharField(max_length=10000,null=True , blank=True)
    meal_type_1 = models.CharField(max_length=5000,null=True , blank=True)
    room_sharing_1  = models.CharField(max_length=5000,null=True , blank=True)
    honeymoon_kit_price_1 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_room_1 = models.IntegerField(null=True , blank=True)
    hotel_nights_1 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_night_1 = models.IntegerField(null=True , blank=True)
    hotel_total_cost_1 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_city_name_2 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_stay_name_2 = models.CharField(max_length=10000,null=True , blank=True)
    meal_type_2 = models.CharField(max_length=5000,null=True , blank=True)
    room_sharing_2  = models.CharField(max_length=5000,null=True , blank=True)
    honeymoon_kit_price_2 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_room_2 = models.IntegerField(null=True , blank=True)
    hotel_nights_2 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_night_2 = models.IntegerField(null=True , blank=True)
    hotel_total_cost_2 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_city_name_3 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_stay_name_3 = models.CharField(max_length=10000,null=True , blank=True)
    meal_type_3 = models.CharField(max_length=5000,null=True , blank=True)
    room_sharing_3  = models.CharField(max_length=5000,null=True , blank=True)
    honeymoon_kit_price_3 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_room_3 = models.IntegerField(null=True , blank=True)
    hotel_nights_3 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_night_3 = models.IntegerField(null=True , blank=True)
    hotel_total_cost_3 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_city_name_4 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_stay_name_4 = models.CharField(max_length=10000,null=True , blank=True)
    meal_type_4 = models.CharField(max_length=5000,null=True , blank=True)
    room_sharing_4  = models.CharField(max_length=5000,null=True , blank=True)
    honeymoon_kit_price_4 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_room_4 = models.IntegerField(null=True , blank=True)
    hotel_nights_4 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_night_4 = models.IntegerField(null=True , blank=True)
    hotel_total_cost_4 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_city_name_5 = models.CharField(max_length=5000,null=True , blank=True)
    hotel_stay_name_5 = models.CharField(max_length=10000,null=True , blank=True)
    meal_type_5 = models.CharField(max_length=5000,null=True , blank=True)
    room_sharing_5  = models.CharField(max_length=5000,null=True , blank=True)
    honeymoon_kit_price_5 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_room_5 = models.IntegerField(null=True , blank=True)
    hotel_nights_5 = models.CharField(max_length=5000,null=True , blank=True)
    number_of_night_5 = models.IntegerField(null=True , blank=True)
    hotel_total_cost_5 = models.CharField(max_length=5000,null=True , blank=True)

    vehicle_type_1 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_unit_1 = models.IntegerField(null=True , blank=True)
    vehicle_total_price_1 = models.CharField(max_length=5000,null=True , blank=True)
    vehicle_type_2 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_unit_2 = models.IntegerField(null=True , blank=True)
    vehicle_total_price_2 = models.CharField(max_length=5000,null=True , blank=True)
    vehicle_type_3 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_unit_3 = models.IntegerField(null=True , blank=True)
    vehicle_total_price_3 = models.CharField(max_length=5000,null=True , blank=True)
    vehicle_type_4 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_unit_4 = models.IntegerField(null=True , blank=True)
    vehicle_total_price_4 = models.CharField(max_length=5000,null=True , blank=True)
    vehicle_type_5 = models.CharField(max_length=5000,null=True , blank=True)
    no_of_unit_5 = models.IntegerField(null=True , blank=True)
    vehicle_total_price_5 = models.CharField(max_length=5000,null=True , blank=True)

    other_vehicle_type_1 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_no_of_unit_1 = models.IntegerField(null=True , blank=True)
    other_vehicle_total_price_1 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_type_2 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_no_of_unit_2 = models.IntegerField(null=True , blank=True)
    other_vehicle_total_price_2 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_type_3 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_no_of_unit_3 = models.IntegerField(null=True , blank=True)
    other_vehicle_total_price_3 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_type_4 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_no_of_unit_4 = models.IntegerField(null=True , blank=True)
    other_vehicle_total_price_4 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_type_5 = models.CharField(max_length=5000,null=True , blank=True)
    other_vehicle_no_of_unit_5 = models.IntegerField(null=True , blank=True)
    other_vehicle_total_price_5 = models.CharField(max_length=5000,null=True , blank=True)

    total_calculated_price = models.CharField(max_length=5000,null=True , blank=True)
    change_in_activity_price = models.CharField(max_length=5000,null=True , blank=True)
    change_in_activity_details = models.CharField(max_length=10000,null=True , blank=True)
    change_in_hotel_price = models.CharField(max_length=5000,null=True , blank=True)
    change_in_hotel_details = models.CharField(max_length=10000,null=True , blank=True)
    change_in_transport_price = models.CharField(max_length=5000,null=True , blank=True)
    change_in_transport_details = models.CharField(max_length=10000,null=True , blank=True)
    change_in_other_price = models.CharField(max_length=5000,null=True , blank=True)
    change_in_other_details = models.CharField(max_length=10000,null=True , blank=True)
    regular_price = models.CharField(max_length=10000,null=True , blank=True)
    total_trip_cost = models.CharField(max_length=5000,null=True , blank=True)

    extra_price_off = models.CharField(max_length=5000,null=True , blank=True)
    end_extra_off = models.CharField(max_length=300,null=True ,blank=True)

    payment_type = models.CharField(max_length=5000,null=True , blank=True)
    number_of_people = models.CharField(max_length=5000,null=True , blank=True)
    each_people_cost = models.CharField(max_length=5000,null=True , blank=True)
    
    agant_name = models.CharField(max_length=5000,null=True , blank=True)
    agant_number = models.CharField(max_length=5000,null=True , blank=True)
    itinerary_date_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ItineraryDatas", kwargs={"slug": self.slug})
    



def pre_save_post_reciever4(sender, instance, *args, **kwargs):
    slug = slugify(instance.number+'-'+instance.name+'-'+instance.state)
    exists = Itinerary.objects.filter(slug=slug).exists()
    instance.slug = slug


pre_save.connect(pre_save_post_reciever4, sender=ItineraryData)


class State(models.Model):
    state = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.state

class Cities(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(str(self.state) +" - "+ self.city)

class Locality(models.Model):
    city = models.ForeignKey(Cities,on_delete=models.CASCADE)
    locality = models.CharField(max_length=200,null=True,blank=True)


    def __str__(self):
        return str(str(self.city) +"-"+ self.locality)



# rentals-form
class Rentals(models.Model):
    state = models.CharField(max_length=122)
    city = models.CharField(max_length=122)
    rentals_type = models.CharField(max_length=122)
    vehicle_gear_type = models.CharField(max_length=122)
    category = models.CharField(max_length=122)
    brand_name = models.CharField(max_length=122)
    product_name = models.CharField(max_length=122)
    product_image = models.ImageField(
        null=True, blank=True, upload_to="uploads/rentals-img")
    product_image_2 = models.ImageField(
        null=True, blank=True, upload_to="uploads/rentals-img")
    specification_1 = models.CharField(max_length=122)
    specification_2 = models.CharField(max_length=122)
    specification_3 = models.CharField(max_length=122)
    popularity_score = models.CharField(max_length=122)
    delivery_option = models.CharField(max_length=122)
    terms_and_conditions = models.TextField()
    price_1_3 = models.CharField(max_length=122)
    price_4_7 = models.CharField(max_length=122)
    price_8_15 = models.CharField(max_length=122)
    price_16_30 = models.CharField(max_length=122)

    def __str__(self):
        return self.product_name
    
    
    






    

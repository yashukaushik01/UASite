from django.db import models
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
    amount = models.IntegerField(null=True, default=2000)
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
    created = models.DateTimeField(
        null=True, auto_now=True, auto_now_add=False, blank=True)

    def __str__(self):
        return self.orderId


class Placetovisit(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=200, choices=Type_CHOICES, default='', null=True, blank=True)
    tag = CharField(max_length=200, null=True, blank=True)
    manual_slug = models.SlugField(
        max_length=100, null=True, blank=True)
    heading = models.CharField(max_length=500, null=True, blank=True)
    summary = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    blog1 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog2 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog3 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog4 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog5 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog6 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog7 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog8 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog9 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog10 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog11 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog12 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog13 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog14 = models.CharField(
        max_length=5000, null=True, blank=True)
    blog15 = models.CharField(
        max_length=5000, null=True, blank=True)
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Populartags(models.Model):
    name = CharField(max_length=100, null=True, blank=True)
    link = CharField(max_length=200, null=True, blank=True)
    tag = CharField(max_length=200, null=True, blank=True)

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

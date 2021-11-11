import hashlib
import uuid
import hmac
import base64
from django.db.models import Q
from django.db.models import query
from django.http import request
from django.http import response
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Affiliate, AffiliateWithdraw, Cities, CityHotelData, Erp, LinkHits, PartialPayment, Populartags, Product, Destination, Images, StateItineraryData, TopPicksEntryForm, duration, phone, Purchase, states, des, promo, AdventureTourTypes, TravelGuide, BestPackage, ProductEnquiry
from .models import Blogpost, wallet
from .models import Itinerary, ItineraryData, Rentals,  Agent, Testimonials, AgentProductBooking, AgentWithdrawHistory, AffiliateUser, AffiliateEarning, AffiliateLink
from .models import State as States, Locality as Localities
from .forms import CityHotelDataForm, ItineraryDataForm, ItineraryForm, ProductEnquiryForm, ProductForm, Addphone, StateItineraryDataForm, purchaseform, UpdateForm, BlogForm, UpdateItineraryForm, ErpForm, UpdateErpForm, TravelGuideEntryForm, PopularTagForm, Top_picks_entryForm, BestPackageForm, CourseEntryForm, AffiliateUserForm
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import datetime
from math import ceil, prod
from taggit.models import Tag
import re
import json
from django.contrib.admin.views.decorators import staff_member_required
from functools import reduce
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.mail import message, send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
import random


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def index(request):
    allprods = []
    allDesti = []

    allDesti.append({
        'name': 'Goa',
        'prod': len(Product.objects.filter(state='Goa'))
    })
    allDesti.append({
        'name': 'Himachal-Pradesh',
        'prod': len(Product.objects.filter(state='Himachal-Pradesh'))
    })
    allDesti.append({
        'name': 'Kedarnath',
        'prod': len(Product.objects.filter(city='Kedarnath'))
    })
    allDesti.append({
        'name': 'Ladakh',
        'prod': len(Product.objects.filter(state='Ladakh'))
    })
    allDesti.append({
        'name': 'Manali',
        'prod': len(Product.objects.filter(city='Manali'))
    })
    allDesti.append({
        'name': 'Kashmir',
        'prod': len(Product.objects.filter(state='Kashmir'))
    })
    allDesti.append({
        'name': 'Dehradun',
        'prod': len(Product.objects.filter(city='Dehradun'))
    })
    allDesti.append({
        'name': 'All',
        'prod': len(Product.objects.all())
    })
    print(len(Product.objects.all()))

    catprods = Product.objects.values("category", "id")
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        ns = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod, range(1, ns), ns])
    if request.user.is_authenticated:
        status = wallet.objects.filter(user=request.user)
    else:
        status = phone.objects.filter(name='aditya')
    context = {
        'products': Product.objects.all(),
        'destinations': Destination.objects.all(),
        'tel': phone.objects.filter(name='aditya'),
        'allprods': allprods,
        'amount': status,
        'populartags': Populartags.objects.filter(tag='Index Tag'),
        'allDesti': allDesti
    }
    return render(request, 'index.html', context)


def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Product.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [{'label': x.name, 'category': "Products"} for x in queryset]
    return JsonResponse(mylist, safe=False)


def more(request):
    Products = Product.objects.all()

    if request.method == 'POST':
        rangef = request.POST.get('range')
        advent = request.POST.get('adventure')
        dur = request.POST.get('duration')
        if rangef == "1":
            if (advent == None or advent == "All") and dur == None:
                Products = Product.objects.all()

            elif advent == None or advent == "All":
                Products = Product.objects.filter(duration_type=dur)

            elif dur == None:
                Products = Product.objects.filter(adventuretype=advent)

            else:
                Products = Product.objects.filter(
                    adventuretype=advent).filter(duration_type=dur)

        else:
            if (advent == None or advent == "All") and dur == None:
                Products = Product.objects.all().filter(sale__range=(0, rangef))

            elif advent == None or advent == "All":
                Products = Product.objects.filter(
                    duration_type=dur).filter(sale__range=(0, rangef))

            elif dur == None:
                Products = Product.objects.filter(
                    adventuretype=advent).filter(sale__range=(0, rangef))

            else:
                Products = Product.objects.filter(adventuretype=advent).filter(
                    duration_type=dur).filter(sale__range=(0, rangef))

    context = {
        'products': Products,

    }
    return render(request, 'more.html', context)


def searchMatch(query, item):
    if query in item.location or query in item.name or query in item.category or query in item.description:
        return True
    else:
        return False


def search(request):
    query = str(request.GET.get('search'))
    allprods = []
    message = 0
    catprods = Product.objects.values("category", "id")
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        ns = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allprods.append([prod, range(1, ns), ns])
    if len(allprods) == 0:
        message = 2

    params = {"allprods": allprods, "message": message}
    return render(request, "search.html", params)


def Tagged(request, tag_slug):

    tag = get_object_or_404(Tag, slug=tag_slug)
    product = Product.objects.filter(tags_in=[tag])
    context = {
        'products': product,
        'query': query
    }
    return render(request, 'more.html', context)


def autocompleteModel(request):

    if request.is_ajax():
        q = request.GET.get('term', '')
        state = states.objects.filter(name__icontains=q)
        results = []
        for pl in state:
            product_json = {}
            product_json = pl.name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def Delete(request, pk):
    cat = get_object_or_404(Itinerary, id=pk)

    if request.method == 'POST':         # If method is POST,
        cat.delete()
        return redirect('/itinerarylist')

    return render(request, 'itinerarylist.html', {'post': cat})


def Delete2(request, pk):
    cat = get_object_or_404(Erp, id=pk)

    if request.method == 'POST':         # If method is POST,
        cat.delete()
        return redirect('/erplist')

    return render(request, 'erplist.html', {'post': cat})


def TourPayment(request, slug):
    post = get_object_or_404(ItineraryData, slug=slug)
    return render(request, 'tour-payment.html', {'post': post})


@staff_member_required
def EditItinerary(request, slug):
    post = get_object_or_404(Itinerary, id=slug)
    if request.method == 'POST':
        form = UpdateItineraryForm(request.POST or None, instance=post)
        print(form.errors)
        form.save()
        messages.success(request, "Changed!")
        return redirect('/itinerarylist')
    return render(request, 'edititinerary.html', {'post': post})

# ======================= new itinerary Tool =================================


@staff_member_required
def stateItinerary(request):
    form = StateItineraryDataForm()
    states = States.objects.all()
    print(states)
    if request.method == 'POST':
        form = StateItineraryDataForm(request.POST or None)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, 'Added !')
        return redirect('/state-itinerary-form/')

    context = {
        'form': form,
        'states': states
    }
    return render(request, 'state-itinerary-form.html', context)


@staff_member_required
def StateItineraryList(request):
    stateItineraryDatas = StateItineraryData.objects.all()
    states = States.objects.all()
    trip_data = []
    activity = []
    day_schedule = []
    transport = []
    for i in stateItineraryDatas:
        if i.trip_name is not None:
            trip_data.append(i)
        elif i.day_schedule_heading is not None:
            day_schedule.append(i)
        elif i.activity_name is not None:
            activity.append(i)
        elif i.other_transport_name is not None:
            transport.append(i)

    context = {
        'trip_data': trip_data,
        'activity': activity,
        'day_schedule': day_schedule,
        'transport': transport,
        'states': states,
    }
    return render(request, 'state-itinerary-list.html', context)


@staff_member_required
def GetStateItineraryData(request):
    state = request.GET.get('state')
    stateItineraryDatas = StateItineraryData.objects.filter(state=state)
    trip_data = []
    activity = []
    day_schedule = []
    transport = []
    for i in stateItineraryDatas:
        if i.trip_name is not None:
            trip_data.append(i)
        elif i.day_schedule_heading is not None:
            day_schedule.append(i)
        elif i.activity_name is not None:
            activity.append(i)
        elif i.other_transport_name is not None:
            transport.append(i)

    context = {
        'trip_data': trip_data,
        'activity': activity,
        'day_schedule': day_schedule,
        'transport': transport,
        'state': state,
    }

    data = render_to_string('state-itinerary-data.html', context)

    return JsonResponse({'data': data})


@staff_member_required
def cityHotel(request):
    form = CityHotelDataForm()
    states = States.objects.all()
    cities = Cities.objects.all()
    if request.method == 'POST':
        form = CityHotelDataForm(request.POST or None, request.FILES or None)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, 'added !')
        return redirect('/city-hotel-form/')

    context = {
        'form': form,
        'states': states,
        'cities': cities
    }
    return render(request, 'city-hotel-form.html', context)


@staff_member_required
def CityHotelList(request):
    cityHotels = CityHotelData.objects.all()
    states = States.objects.all()
    context = {
        'cityHotels': cityHotels,
        'states': states
    }
    return render(request, 'city-hotel-list.html', context)


@staff_member_required
def GetCityHotelData(request):
    state = request.GET.get('state')
    context = {}
    if state:
        city_hotel = CityHotelData.objects.filter(state=state)
        data = render_to_string('city-hotel-data.html',
                                {'cityHotels': city_hotel})
        context['data'] = data
    else:
        hotel_id = request.GET.get('id')
        print(hotel_id)
        city_hotel = CityHotelData.objects.get(id=hotel_id)
        data = render_to_string('city-hotel-image.html',
                                {'city_hotel': city_hotel})

        context['data'] = data

    return JsonResponse(context)


@staff_member_required
def AddItineraryData(request):
    form = ItineraryDataForm()
    states = States.objects.all()
    if request.method == 'POST':
        form = ItineraryDataForm(request.POST or None)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, 'added !')
        return redirect('/add-itinerary-form/')

    context = {
        'form': form,
        'states': states,
    }

    return render(request, 'itinerary-data-form.html', context)


@staff_member_required
def getItineraryData(request):
    arr_1 = []
    arr_2 = []
    hotel_cities = []
    state = request.GET.get('state')
    state_itineraries = StateItineraryData.objects.filter(state=state).values()
    city_hotels = CityHotelData.objects.filter(state=state).values()

    for i in state_itineraries:
        arr_1.append(i)
    for j in city_hotels:
        arr_2.append(j)
        hotel_cities.append(j['city'])

    hotel_cities = list(dict.fromkeys(hotel_cities))

    return JsonResponse({'state_itineraries': arr_1, 'city_hotels': arr_2, 'hotel_cities': hotel_cities})


def itineraryData(request, slug):
    hotel1 = ''
    hotel2 = ''
    hotel3 = ''
    hotel4 = ''
    hotel5 = ''
    itinerary = ItineraryData.objects.get(slug=slug)
    if itinerary.hotel_stay_name_1:
        hotel1 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_1, stay_name=itinerary.hotel_stay_name_1)
    if itinerary.hotel_stay_name_2:
        hotel2 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_2, stay_name=itinerary.hotel_stay_name_2)
    if itinerary.hotel_stay_name_3:
        hotel3 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_3, stay_name=itinerary.hotel_stay_name_3)
    if itinerary.hotel_stay_name_4:
        hotel4 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_4, stay_name=itinerary.hotel_stay_name_4)
    if itinerary.hotel_stay_name_5:
        hotel5 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_5, stay_name=itinerary.hotel_stay_name_5)

    context = {
        'itinerary': itinerary,
        'hotel1': hotel1,
        'hotel2': hotel2,
        'hotel3': hotel3,
        'hotel4': hotel4,
        'hotel5': hotel5,
    }
    return render(request, 'itinerary-data.html', context)


@staff_member_required
def ItineraryDataList(request):
    itineraryDatas = ItineraryData.objects.all()
    states = States.objects.all()
    context = {
        'itineraryDatas': itineraryDatas,
        'states': states,
    }
    return render(request, 'itinerary-data-list.html', context)


@staff_member_required
def GetItineraryListData(request):
    state = request.GET.get('state')

    itinerary_datas = ItineraryData.objects.filter(state=state)

    data = render_to_string('itinerary-list-data.html',
                            {'itineraryDatas': itinerary_datas})

    return JsonResponse({'data': data})


@staff_member_required
def ItineraryDataEdit(request, pk):
    states = States.objects.all()
    itinerary = get_object_or_404(ItineraryData, id=pk)
    hotel1 = ''
    hotel2 = ''
    hotel3 = ''
    hotel4 = ''
    hotel5 = ''
    if itinerary.hotel_stay_name_1:
        hotel1 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_1, stay_name=itinerary.hotel_stay_name_1)
    if itinerary.hotel_stay_name_2:
        hotel2 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_2, stay_name=itinerary.hotel_stay_name_2)
    if itinerary.hotel_stay_name_3:
        hotel3 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_3, stay_name=itinerary.hotel_stay_name_3)
    if itinerary.hotel_stay_name_4:
        hotel4 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_4, stay_name=itinerary.hotel_stay_name_4)
    if itinerary.hotel_stay_name_5:
        hotel5 = CityHotelData.objects.get(state=itinerary.state,
                                           city=itinerary.hotel_city_name_5, stay_name=itinerary.hotel_stay_name_5)

    inclusion = itinerary.additional_inclusion.split('</div>')
    print(itinerary)

    # form = ItineraryDataForm()

    if request.method == 'POST':
        form = ItineraryDataForm(request.POST or None, instance=itinerary)
        print(form.errors)
        form.save()
        messages.success(request, 'updated Successfully !')
        return redirect('/itinerary-data-list/')

    context = {
        'states': states,
        'itinerary': itinerary,
        'inclusion': inclusion,
        'hotel1': hotel1,
        'hotel2': hotel2,
        'hotel3': hotel3,
        'hotel4': hotel4,
        'hotel5': hotel5,
    }
    return render(request, 'itinerary-data-edit.html', context)


@staff_member_required
def EditErp(request, slug):
    post = get_object_or_404(Erp, booking_id=slug)
    if request.method == 'POST':
        form = UpdateErpForm(request.POST or None, instance=post)
        print(form.errors)
        form.save()
        messages.success(request, "Changed!")
        return redirect('/erplist')
    return render(request, 'editerp.html', {'post': post})


def profile(request):
    context = {
        'purchase': Purchase.objects.all(),
        'amount': wallet.objects.filter(user=request.user)
    }

    return render(request, 'profile.html', context)


@csrf_exempt
def SendErpMail(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        booking_id = request.POST.get('booking_id')
        booking_date = request.POST.get('booking_date')
        tour_name = request.POST.get('tour_name')
        tour_date = request.POST.get('tour_date')
        total_package_cost = request.POST.get('total_package_cost')
        payment = request.POST.get('payment1')
        payment_no = request.POST.get('payment_no')
        payment_date = request.POST.get('payment_date')
        payment_mod = request.POST.get('payment_mod')
        due_payment_amount = request.POST.get('due_payment_amount')

        if str(payment) == 'None':
            return JsonResponse({'data': 'payment not done At.', 'status': 'info'})
        else:
            message = render_to_string('mail.html', {
                'name': name,
                'email': email,
                'phone_no': phone_no,
                'booking_id': booking_id,
                'booking_date': booking_date,
                'tour_name': tour_name,
                'tour_date': tour_date,
                'total_package_cost': total_package_cost,
                'payment': payment,
                'payment_no': payment_no,
                'payment_date': payment_date,
                'payment_mod': payment_mod,
                'due_payment_amount': due_payment_amount

            })
            mail = EmailMessage(
                subject='Payment Recept',
                body=message,
                from_email='adiblog2021@gmail.com',
                # from_email='bookings@universaladventures.in',
                to=['aditya2462001@gmail.com', ]
            )
            mail.content_subtype = "html"
            mail.send()

            return JsonResponse({'data': 'mail sended to client successfully', 'status': 'success'})


def affiliate(request):
    total = 0
    m = []
    if request.user.is_authenticated:
        catprods = Affiliate.objects.filter(
            email=request.user.email).values("margin_earned", "coupon_uid")
        catprod2 = promo.objects.filter(email=request.user.email)
        if len(catprod2) > 0:
            print(catprod2)
            for item in catprods:
                if len(Purchase.objects.filter(coupon_uid=item["coupon_uid"])) > 0:
                    if get_object_or_404(Purchase, coupon_uid=item["coupon_uid"]).status == "SUCCESS":
                        m.append(item["coupon_uid"])
            for item in Affiliate.objects.filter(email=request.user.email, coupon_uid__in=m).values("margin_earned", "coupon_uid"):
                total = total+int(item["margin_earned"])
            if len(phone.objects.filter(user=request.user)) > 0:
                phon = get_object_or_404(phone, user=request.user).phone
            else:
                phon = 'Phone Not Registered'
            try:
                all_active = 0
                promos = promo.objects.filter(email=request.user.email)
                total_coupons = len(promos)
                for i in promos:
                    if i.status == 'active':
                        all_active += 1

            except:
                pass
            context = {
                'affiliate': Affiliate.objects.filter(email=request.user.email, coupon_uid__in=m),
                'coupons': promo.objects.filter(email=request.user.email),
                'phone': phon,
                'total': total,
                'length': 1,
                'all_active': all_active,
                'used_coupons': len(Affiliate.objects.filter(email=request.user.email, coupon_uid__in=m)),
                'total_coupons': total_coupons + len(Affiliate.objects.filter(email=request.user.email, coupon_uid__in=m))
            }
            return render(request, 'affiliate.html', context)
        else:
            if len(phone.objects.filter(user=request.user)) > 0:
                phon = get_object_or_404(phone, user=request.user).phone
            else:
                phon = 'Phone Not Registered'
            context = {
                'length': 0,
                'phone': phon,
            }
            return render(request, 'affiliate.html', context)
    else:
        return render(request, 'affiliate.html')


# ================================== affiliate ==================================================

def affiliateUser(request):
    print(request.affiliate_id)
    form = AffiliateUserForm()
    context = {
        'form': form
    }
    if request.user.is_active:
        if AffiliateUser.objects.filter(email=request.user.email).exists():
            messages.success(
                request, 'Email id is already exits please try again')
            return redirect('/affiliate-dashboard')

    if request.method == 'POST':
        form = AffiliateUserForm(request.POST or None, request.FILES or None)
        print(form.errors)
        if AffiliateUser.objects.filter(email=form['email']).exists():
            messages.success(
                request, 'Email id is already exits please try again')
            return render(request, 'affiliate_form.html', context)
        if form.is_valid():
            affiliate_user = form.save(commit=False)
            affiliate_user.save()
            form.save_m2m()
            affiliate_earning = AffiliateEarning(aid=affiliate_user)
            affiliate_earning.save()
        else:
            messages.success(
                request, 'Something wents wrong please try again!')
            return redirect('/affiliate-add')

        messages.success(request, 'Your account is created wait for approval')
        return redirect('/affiliate-dashboard')
    context = {
        'form': form
    }

    return render(request, 'affiliate_form.html', context)


@staff_member_required
def affiliateList(request):
    return render(request, 'affiliate_list.html')


@staff_member_required
def affiliateListData(request):
    status = request.GET.get('status')
    print(status)
    data = ''
    affiliateUsers = AffiliateUser.objects.filter(status=status)
    data = render_to_string('affiliate_list_data.html', {
                            'affiliateusers': affiliateUsers, 'status': status})

    return JsonResponse({'data': data})


@staff_member_required
def AffiliateUserStatus(request, status, slug):
    if status == 'active':
        affiliate_user = AffiliateUser.objects.get(aid=slug)
        affiliate_user.status = 'active'
        affiliate_user.save()

    elif status == 'inactive':
        affiliate_user = AffiliateUser.objects.get(aid=slug)
        affiliate_user.status = 'inactive'
        affiliate_user.save()

    messages.info(request, 'Account is activated !!')
    return redirect('/affiliate-list')


def AffiliateDashbord(request):
    print(request.affiliate_id)
    print(request.GET.get('aid'))
    affiliate_user = None
    affiliate_links = None
    affiliate_purchases = None
    affiliate_earining = None
    affiliate_withdraw = None
    total_withdraw_amount = 0
    link_count = 0
    total_hits = 0
    remain_price = 0
    total_success_booking = 0
    conversion_rate = 0
    links = []
    if request.user.is_active:
        try:
            affiliate_user = AffiliateUser.objects.get(
                email=request.user.email)
            affiliate_earining = AffiliateEarning.objects.get(
                aid=affiliate_user)
            affiliate_purchases = Purchase.objects.filter(
                aid=affiliate_user.aid)
            affiliate_earining = AffiliateEarning.objects.get(
                aid=affiliate_user)
            affiliate_links = AffiliateLink.objects.filter(aid=affiliate_user)
            affiliate_link_hits = LinkHits.objects.filter(
                aid=affiliate_user.aid)
            affiliate_withdraw = AffiliateWithdraw.objects.filter(
                aid=affiliate_user)
            for i in affiliate_links:
                link_hits = LinkHits.objects.filter(
                    aid=affiliate_user.aid, product_link=i.product_link)
                links.append({'link': i, 'hits': len(link_hits)})
            for i in affiliate_withdraw:
                total_withdraw_amount += int(i.amount)
            for i in affiliate_purchases:
                if i.status == 'SUCCESS':
                    total_success_booking += 1

            conversion_rate = (int(len(affiliate_purchases))
                               * 100) / len(affiliate_link_hits)

            print(conversion_rate)

            link_count = len(affiliate_links)
            total_hits = len(affiliate_link_hits)
            remain_price = affiliate_earining.remain_price

        except Exception as e:
            pass
    context = {
        'affiliateUser': affiliate_user,
        'affiliateLinks': links,
        'affiliate_purchases': affiliate_purchases,
        'affiliate_earn': affiliate_earining,
        'affiliate_withdraw': affiliate_withdraw,
        'link_count': link_count,
        'total_hits': total_hits,
        'total_withdraw_amount': total_withdraw_amount,
        'remain_price': remain_price,
        'total_success_booking': total_success_booking,
        'conversion_rate': conversion_rate
    }
    return render(request, 'affiliate-dashboard.html', context)


@csrf_exempt
def affiliateLink(request):
    if request.user.is_active:
        affiliate_user = AffiliateUser.objects.get(email=request.user.email)
        product_name = None
        product_link = None
        if request.method == 'POST':
            link = request.POST.get('link')
            split_link = link.split('/')

            if len(split_link) >= 4:
                if Product.objects.filter(manual_slug=split_link[4]):
                    product = Product.objects.get(manual_slug=split_link[4])
                    product_name = product.name
                    product_link = f'/products/{product.manual_slug}/?aid={affiliate_user.aid}'

            if link[len(link) - 1] == '/':
                created_link = link + f'?aid={affiliate_user.aid}'
            else:
                created_link = link + f'/?aid={affiliate_user.aid}'

            print(created_link)

            if AffiliateLink.objects.filter(link=created_link).exists():
                return JsonResponse({'data': ''})

            affiliate_link = AffiliateLink(aid=affiliate_user,
                                           link=created_link,
                                           product_name=product_name,
                                           product_link=product_link)
            affiliate_link.save()
            if LinkHits.objects.filter(aid=affiliate_user.aid, product_link=product_link).exists:
                created_link_hit = len(LinkHits.objects.filter(
                    aid=affiliate_user.aid, product_link=product_link))

    return JsonResponse({'data': created_link, 'date': affiliate_link.date, 'link': created_link, 'product_name': product_name,
                         'product_link': product_link, 'affiliate_link_hit': created_link_hit})


def affiliateWithdraw(request):
    if request.method == 'POST':
        aid = request.POST.get('aid')
        amount = request.POST.get('withdraw-amount')
        ip = request.META.get('REMOTE_ADDR')

        if AffiliateUser.objects.filter(aid=aid).exists():
            affiliate_user = AffiliateUser.objects.get(aid=aid)
            affiliate_earn = AffiliateEarning.objects.get(aid=affiliate_user)
            if int(affiliate_earn.withdrawlable_amount) == 0 or int(affiliate_earn.withdrawlable_amount) < int(amount):
                messages.info(
                    request, 'in your account not have sufficient balance')
                return redirect('/affiliate-dashboard')

            affiliate_earn.withdrawlable_amount = int(
                affiliate_earn.withdrawlable_amount) - int(amount)
            affiliate_earn.save()

            affiliate_withdraw = AffiliateWithdraw(aid=affiliate_user, ip=ip, account_number=affiliate_user.account_number,
                                                   name=affiliate_user.name, ifsc_code=affiliate_user.ifsc_code, bank_name=affiliate_user.bank_name, amount=amount)
            affiliate_withdraw.save()

            messages.success(
                request, 'Your Withdraw request is recored please wait until accepeted')

    return redirect('/affiliate-dashboard')


@staff_member_required
def affiliate_withdraw_list(request):
    withdraw_requests = AffiliateWithdraw.objects.all()

    context = {
        'affiliate_requests': withdraw_requests
    }
    return render(request, 'affiliate-withdraw-list.html', context)


@staff_member_required
def AffiliatePayment(request):
    aid = request.GET.get('aid')
    withdraw_id = request.GET.get('withdraw_id')
    payment_status = request.GET.get('payment_status')
    if AffiliateUser.objects.filter(aid=aid).exists():
        affiliate_user = AffiliateUser.objects.get(aid=aid)
        affiliate_earning = AffiliateEarning.objects.get(aid=affiliate_user)
        affiliate_withdraw = AffiliateWithdraw.objects.get(id=withdraw_id)
        if payment_status == 'processed':
            affiliate_withdraw.payemt_status = 'processed'
            affiliate_withdraw.save()
            affiliate_earning.remain_price = affiliate_earning.remain_price - \
                int(affiliate_withdraw.amount)
            affiliate_earning.save()
        elif payment_status == 'declined':
            affiliate_withdraw.payemt_status = 'declined'
            affiliate_withdraw.save()
            affiliate_earning.withdrawlable_amount = affiliate_earning.withdrawlable_amount + \
                int(affiliate_withdraw.amount)
            affiliate_earning.save()

        messages.success(request, 'Payment status updated')

        return redirect('/affiliate-withdraw-list/')

    return redirect('/affiliate-add')


# ======================== agent dashboard ===================================
# def Agent_dashborad(request):
#     return render(request, 'agent-dashboard.html', {})


def product(request, slug):
    testimonial = Testimonials.objects.filter(
        display_page_url="127.0.0.1:8000"+request.path)
    print(request.path)
    if request.GET.get('aid'):
        if AffiliateUser.objects.filter(aid=request.GET.get('aid')).exists():
            affiliate_user = AffiliateUser.objects.get(
                aid=request.GET.get('aid'))
            product_link = request.path + "?aid=" + str(affiliate_user.aid)
            ip = request.META.get('REMOTE_ADDR')
            if not LinkHits.objects.filter(product_link=product_link, ip_address=ip):
                link_hit = LinkHits(aid=affiliate_user.aid,
                                    ip_address=ip, product_link=product_link)
                link_hit.save()

    product = get_object_or_404(Product, manual_slug=slug)
    city = product.city
    recommended = Product.objects.filter(city=city)
    form = Addphone()
    catprods = Product.objects.filter(city=city).values("adventuretype", "id")
    cats = {item["adventuretype"] for item in catprods}
    cat2 = []

    for i in cats:
        if i:
            j = re.sub("\s+", "-", i.strip())
            cat2.append(j)
    if request.method == 'POST':
        current_user = request.user
        phones = phone(user=current_user, phone=request.POST.get('phone'))
        phones.save()
        messages.success(request, "Added")
        return redirect('index')

    context = {
        'product': product,
        'form': form,
        'recommended': recommended,
        'tel': phone.objects.filter(name='aditya'),
        'cats': cat2,
        'testimonial': testimonial
    }

    return render(request, 'product.html', context)


@csrf_exempt
def destination(request):
    paginator = Paginator(Product.objects.all(), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'states': states.objects.all(),
        'products': page_obj,

    }

    return render(request, 'destination.html')


@csrf_exempt
def Adventure(request, slug):
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')
    if slug == 'all':
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', city=city), 15)

        elif len(state) > 0:
            print(slug)
            paginator = Paginator(Product.objects.filter(
                category='Adventure', state=state), 15)
        else:
            paginator = Paginator(
                Product.objects.filter(category='Adventure'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name=slug),
            'slug': slug,
        }
    elif slug == 'High-Fly':
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='High Fly', city=city), 15)

        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='High Fly', state=state), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='High Fly'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name='High Fly'),
            'slug': slug,
        }
    elif slug == 'High-Thrills':
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='High Thrills', city=city), 15)

        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='High Thrills', state=state), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='High Thrills'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name='High Thrills'),
            'slug': slug,
        }
    elif slug == 'Land-Adventure':
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='Land Adventure', city=city), 15)

        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='Land Adventure', state=state), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='Land Adventure'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name='Land Adventure'),
            'slug': slug,
        }
    elif slug == 'Aqua-Experiences':
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='Aqua Experiences', city=city), 15)

        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='Aqua Experiences', state=state), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', tag_category='Aqua Experiences'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name='Aqua Experiences'),
            'slug': slug,
        }

    else:
        a = slug.split('-')
        if len(a) > 1:
            slug = a[0]+' '+a[1]
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', city=city, adventuretype=slug), 15)
        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', state=state, adventuretype=slug), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', adventuretype=slug), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name=slug),
            'slug': slug,
        }

    return render(request, 'adventure.html', context)


@csrf_exempt
def City(request, slug):
    context = {
        'city': slug,
        'destination': Destination.objects.filter(type='city', name=slug),
        'adventure': Product.objects.filter(category='Adventure', city=slug),
        'tour': Product.objects.filter(category='Tour', city=slug),
        'popular': Product.objects.filter(city=slug, order=1),
        'len': len(Product.objects.filter(city=slug))

    }

    return render(request, 'city.html', context)


@csrf_exempt
def State(request, slug):
    destination = Destination.objects.get(type='state', name=slug)
    if TravelGuide.objects.filter(name=slug, tag='Top places to visit').exists():
        top_places_to_visit = TravelGuide.objects.get(
            name=slug, tag='Top places to visit')
    else:
        top_places_to_visit = ''

    if TravelGuide.objects.filter(name=slug, tag='Things to Do').exists():

        things_to_do = TravelGuide.objects.get(name=slug, tag='Things to Do')
    else:
        things_to_do = ''

    if destination.location:
        locations = destination.location.split(',')
    else:
        locations = []
    print(TravelGuide.objects.filter(name=slug, tag='General Travel Guide'))
    context = {
        'city': slug,
        'destination': Destination.objects.filter(type='state', name=slug),
        'destination_loc': locations,
        'adventure': Product.objects.filter(category='Adventure', state=slug),
        'tour': Product.objects.filter(category='Tour', state=slug),
        'popular': Product.objects.filter(state=slug, order=1),
        'populartags': Populartags.objects.filter(tag=slug),
        'travelguide': TravelGuide.objects.filter(name=slug, tag='General Travel Guide'),
        'top_places_to_visit': top_places_to_visit,
        'things_to_do': things_to_do,
        'len': len(Product.objects.filter(state=slug))

    }

    return render(request, 'state.html', context)


@csrf_exempt
def Tour(request, slug):
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')

    if slug == 'all':
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Tour', city=city), 15)
            place = city
        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Tour', state=state), 15)

        else:
            paginator = Paginator(Product.objects.filter(category='Tour'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'slug': slug,
            'len': len(page_obj),
        }
    else:
        a = slug.split('-')
        if len(a) > 1:
            slug = a[0]+' '+a[1]
        if len(a) > 2:
            slug = a[0]+' '+a[1]+' '+a[2]
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Tour', city=city, tag_category=slug), 15)
        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Tour', state=state, tag_category=slug), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Tour', tag_category=slug), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'len': len(page_obj),
            'slug': slug,
            'len': len(page_obj),
            'adven': AdventureTourTypes.objects.filter(name=slug)
        }

    return render(request, 'tour.html', context)


@csrf_exempt
def FilterData(request):
    slug = request.POST.get('slug')
    adventure = request.POST.getlist('level[]')
    duration = request.POST.getlist('duration[]')
    typee = request.POST.getlist('type[]')
    citye = request.POST.getlist('citye[]')
    category = request.POST.get('category')
    max_price = int(request.POST.get('maximum_price'))
    min_price = int(request.POST.get('minimum_price'))
    search = request.POST.get('search')
    loc = request.POST.getlist('loc[]')

    print(citye)

    a = slug.split('-')

    allproducts = Product.objects.filter(category='Adventure', adventuretype__in=a,
                                         sale__gte=min_price, sale__lte=max_price).distinct()

    slug1 = ''

    if len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype__in=slug1).distinct()

    if len(typee) > 0:
        allproducts = Product.objects.filter(
            category='Adventure',  adventuretype__in=typee, sale__gte=min_price, sale__lte=max_price).distinct()

    if len(citye) > 0 and len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug1,  city__in=citye, sale__gte=min_price, sale__lte=max_price).distinct()
    elif len(citye) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  city__in=citye, sale__gte=min_price, sale__lte=max_price).distinct()

    if len(adventure) > 0 and len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug1, city__in=citye,  adventurelevel__in=adventure, sale__gte=min_price, sale__lte=max_price).distinct()
    elif len(adventure) > 0:
        print(adventure)
        allproducts = Product.objects.filter(category='Adventure', city__in=citye, adventuretype__in=a, adventurelevel__in=adventure,
                                             sale__gte=min_price, sale__lte=max_price).distinct()
        print(allproducts)
    if len(duration) > 0 and len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug1,  duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
    elif len(duration) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(loc) > 0 and len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug1,  adventureloc__in=loc, sale__gte=min_price, sale__lte=max_price).distinct()
    elif len(loc) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  adventureloc__in=loc, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(search) > 0 and len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug1,  name__icontains=search, sale__gte=min_price, sale__lte=max_price).distinct()
    elif len(search) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug, name__icontains=search,).distinct()

    if (min_price > 1000 or max_price < 100000) and len(a) >= 2:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(Q(city__in=citye),
                                             category='Adventure', tag_category=slug1, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()
    elif min_price > 1000 or max_price < 100000:
        allproducts = Product.objects.filter(Q(city__in=citye),
                                             category='Adventure', adventuretype__in=a, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()
        print(allproducts)

    if category == 'Tour':
        allproducts = Product.objects.filter(
            category=category, tag_category=slug)
        if len(typee) > 0:
            allproducts = Product.objects.filter(
                category=category,  adventuretype__in=typee, sale__gte=min_price, sale__lte=max_price).distinct()
        if len(citye) > 0:
            allproducts = Product.objects.filter(category=category, tag_category=slug,
                                                 city__in=citye, sale__gte=min_price, sale__lte=max_price)
        if len(duration) > 0:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug, duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
        if len(duration) > 0 and len(a) > 1:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug,  duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
        if len(search) > 0:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug,  name__icontains=search,).distinct()
        if len(search) > 0 and len(a) > 1:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug,  name__icontains=search, sale__gte=min_price, sale__lte=max_price).distinct()
        if min_price > 1000 or max_price < 100000:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()
        if min_price > 1000 or max_price < 100000 and len(a) > 1:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()

    t = render_to_string('prodlist.html', {'products': allproducts})

    return JsonResponse({'data': t, 'len': len(t), 'product_len': len(allproducts)})


def Privacy(request):
    return render(request, 'privacy.html')


def Partial(request):
    return render(request, 'partial-payment.html')


def Refund(request):
    return render(request, 'refundpolicy.html')


def Contact(request):
    return render(request, 'contact.html')


def About(request):
    return render(request, 'about.html')


@staff_member_required
def Response_Itinerary(request, slug):
    post = Itinerary.objects.filter(phone=slug)[0]
    hello = {'post': post
             }
    return render(request, 'itinerary_response.html', hello)


def blog(request):
    mypost = Blogpost.objects.all()
    params = {"mypost": mypost}
    return render(request, 'blog.html', params)


def blogpost(request, slug):
    Products = Product.objects.filter(state='Goa')
    post = Blogpost.objects.filter(slug=slug)[0]
    dic = {'post': post,
           'products': Products
           }

    return render(request, 'blogpos.html', dic)


def UserItierary(request, slug):
    print(slug)
    post = Itinerary.objects.filter(slug=slug)[0]
    dic = {'post': post}
    return render(request, 'useritinerary.html', dic)


@staff_member_required
def ItineraryList(request):
    context = {
        'post': Itinerary.objects.all()[::-1]
    }
    return render(request, 'itinerarylist.html', context)


@staff_member_required
def ErpList(request):
    context = {
        'post': Erp.objects.all()[::-1]
    }
    return render(request, 'erplist.html', context)


def booking(request):
    if request.method == "POST":
        postData = {
            "customerName": request.POST.get('name'),
            "customerEmail": request.POST.get('email'),
            "adultPrice": request.POST.get('adult_price'),
            "product": request.POST.get('product'),
            "childPrice": request.POST.get('child_price'),
            "adultPrice2": request.POST.get('adult_price2'),
            "childPrice2": request.POST.get('child_price2'),
            "date": request.POST.get('date'),
            "number": request.POST.get('number1'),
            "number2": request.POST.get('number2'),
            "id": request.POST.get('orderid'),
            "amount": request.POST.get('amount'),
            "slug": request.POST.get('slug'),
            "max_discount": request.POST.get('max_discount'),
            "discount": (int(request.POST.get('adult_price'))*int(request.POST.get('number1')) + (int(request.POST.get('child_price'))*int(request.POST.get('number2')))) - (int(request.POST.get('adult_price2'))*int(request.POST.get('number1'))+(int(request.POST.get('child_price2'))*int(request.POST.get('number2'))))
        }
        return render(request, 'bookingform.html', {'postData': postData})


def walletpromo(request):
    if request.method == "POST":
        promo = request.POST.get('wallet_promo', '')
        adult = request.POST.get('adult_promo', '')
        child = request.POST.get('child_promo', '')
        promo_total = (int(adult)+int(child)) * int(promo)
        try:
            amount = wallet.objects.filter(
                user=request.user).values('amount')[0]['amount']
            idlite = wallet.objects.filter(
                user=request.user).values('id')[0]['id']
            wall = wallet.objects.get(id=idlite)
            if amount > 0:
                if amount >= promo_total:
                    left_amount = int(amount) - int(promo_total)
                    wall.amount = left_amount
                    wall.save()
                    response = json.dumps(
                        {"status": "success", "used_amount": promo_total}, default=str)
                    return HttpResponse(response)
                else:
                    response = json.dumps(
                        {"status": "lesswalletamount", "used_amount": amount}, default=str)
                    return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse(f'{e}')


def promocode(request):
    if request.method == "POST":
        amount = int(request.POST.get('amount', ''))
        product = request.POST.get('product')
        get_product = Product.objects.get(name=product)

        try:
            coupon = get_object_or_404(
                promo, coupon=request.POST.get('promo_code', ''))
            print(coupon.coupon)
            if (coupon.coupon[0] == "A" and coupon.coupon[1] == "U") or (coupon.coupon == get_product.promo_code):
                if coupon.status == 'active':
                    if coupon.type == 'price':
                        price = coupon.price
                        final_amount = amount-price
                        margin_earned = (int(request.POST.get(
                            'amount', ''))*coupon.margin)//100
                        coupon_id = uuid.uuid4()
                        purchase = Affiliate(coupon=coupon.coupon, email=coupon.email, product=request.POST.get('product', ''), date=datetime.date.today(
                        ).strftime('%d/%m/%Y'), total_price=request.POST.get('amount', ''), margin_earned=margin_earned, coupon_uid=coupon_id)
                        purchase.save()
                        response = json.dumps({"status": "success", "used_amount": price,
                                               "final_amount": final_amount, "coupon_id": coupon_id}, default=str)
                        return HttpResponse(response)
                    if coupon.type == 'percentage':
                        price = (coupon.price*amount)//100
                        final_amount = amount-price
                        margin_earned = (int(request.POST.get(
                            'amount', ''))*coupon.margin)//100
                        coupon_id = uuid.uuid4()
                        purchase = Affiliate(coupon=coupon.coupon, email=coupon.email, product=request.POST.get('product', ''), date=datetime.date.today(
                        ).strftime('%d/%m/%Y'), total_price=request.POST.get('amount', ''), margin_earned=margin_earned, coupon_uid=coupon_id)
                        purchase.save()
                        response = json.dumps({"status": "success", "used_amount": price,
                                               "final_amount": final_amount, "coupon_id": coupon_id}, default=str)
                        return HttpResponse(response)
                else:
                    response = json.dumps({"status": "Expired"}, default=str)
                    return HttpResponse(response)

        except Exception as e:
            response = json.dumps({"status": f"{e}"}, default=str)
            return HttpResponse(response)


def checkout(request):
    if request.method == "POST":
        prod = get_object_or_404(Product, id=request.POST.get('orderid'))
        # 3116246b3ec6d019344fd492a26113
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderId": uuid.uuid4().hex[:6].upper(),
            "orderAmount": request.POST.get('amount'),
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": request.POST.get('name'),
            "customerPhone": request.POST.get('phone'),
            "customerEmail": request.POST.get('email'),
            "returnUrl": 'http://127.0.0.1:8000/handlerequest/',
            "notifyUrl": 'http://127.0.0.1:8000/'
        }
        dates = datetime.datetime.strptime(
            request.POST.get('date'), "%Y-%m-%d").strftime("%Y-%m-%d")
        affiliateId = ''
        affiliate_user = None

        if request.affiliate_id:
            if AffiliateUser.objects.filter(aid=request.affiliate_id).exists():
                affiliate_user = AffiliateUser.objects.get(
                    aid=request.affiliate_id)
                if affiliate_user.status == 'active':
                    affiliateId = request.affiliate_id

        purchase = Purchase(user=request.user, product=prod, date=dates, days=request.POST.get(
            'number'), orderId=postData["orderId"], orderAmount=request.POST.get('amountTotal'), paidAmount=request.POST.get('amount'), booking_date=datetime.date.today(),
            coupon_uid=request.POST.get('coupon_id'), aid=affiliateId, margin=prod.margin, phone=request.POST.get('phone'), number_of_adults=request.POST.get('number'), number_of_child=request.POST.get('number2'))
        purchase.save()

        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+postData[key]

        message = signatureData.encode('utf-8')
        # get secret key from your config
        secretkey = "b8caf62ce5e932034897da856129873bf0dace3e"
        # secretkey = "96d9e9a3801fc8914dde8e92a19ad866302335f5"
        secret = secretkey.encode('utf-8')
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        postData["signature"] = signature
        return render(request, 'checkoutform.html', {'postData': postData})


def checkout2(request):
    if request.method == "POST":
        orderId = uuid.uuid4().hex[:6].upper()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        package_type = request.POST.get('package-type')
        package_name = request.POST.get('package-name')
        service_date = request.POST.get('service_date')
        package_cost = request.POST.get('package-cost')
        paid_amount = request.POST.get('paid_amount')
        partialPayment = PartialPayment(orderId=orderId, name=name, email=email, phone=phone, package_type=package_type,
                                        package_name=package_name, service_date=service_date, booking_date=datetime.date.today(), package_cost=package_cost, paid_amount=paid_amount)
        partialPayment.save()
        purchase = Purchase(partial_pay=partialPayment, date=service_date,
                            orderId=orderId, orderAmount=package_cost, paidAmount=paid_amount, phone=phone, package_type=package_type, booking_date=datetime.date.today())
        purchase.save()
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderId": orderId,
            "orderAmount": paid_amount,
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": request.POST.get('name'),
            "customerPhone": request.POST.get('phone'),
            "customerEmail": request.POST.get('email'),
            "returnUrl": 'http://127.0.0.1:8000/handlerequestpartial/',
            "notifyUrl": 'http://127.0.0.1:8000/'
        }
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+str(postData[key])

        message = signatureData.encode('utf-8')
        # get secret key from your config
        secretkey = "b8caf62ce5e932034897da856129873bf0dace3e"
        # secretkey = "96d9e9a3801fc8914dde8e92a19ad866302335f5"
        secret = secretkey.encode('utf-8')
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        postData["signature"] = signature
        return render(request, 'checkoutform.html', {'postData': postData})


def checkout3(request):
    if request.method == "POST":
        print(request.POST.get('name'))
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderId": uuid.uuid4().hex[:6].upper(),
            "orderAmount": request.POST.get('amount'),
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": request.POST.get('name'),
            "customerPhone": request.POST.get('phone'),
            "customerEmail": request.POST.get('email'),
            "paymentType": request.POST.get('payment_type'),
            "returnUrl": 'http://127.0.0.1:8000/handlerequestpartial/',
            "notifyUrl": 'http://127.0.0.1:8000/'
        }
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+postData[key]

        message = signatureData.encode('utf-8')
        # get secret key from your config
        secretkey = "b8caf62ce5e932034897da856129873bf0dace3e"
        secret = secretkey.encode('utf-8')
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        postData["signature"] = signature
        return render(request, 'checkoutform.html', {'postData': postData})


@csrf_exempt
def cashpartial(request):
    if request.method == "POST":
        postData = {
            "orderId":  request.POST.get('orderId'),
            "orderAmount":  request.POST.get('orderAmount'),
            "referenceId":  request.POST.get('referenceId'),
            "txStatus":  request.POST.get('txStatus'),
            "paymentMode":  request.POST.get('paymentMode'),
            "txMsg": request.POST.get('txMsg'),
            "signature":  request.POST.get('signature'),
            "txTime":  request.POST.get('txTime')
        }
        partialPayment = get_object_or_404(
            PartialPayment, orderId=request.POST.get('orderId'))
        partialPayment.status = request.POST.get('txStatus')
        partialPayment.save()
        purchase = get_object_or_404(
            Purchase, orderId=request.POST.get('orderId'))
        purchase.status = request.POST.get('txStatus')
        purchase.save()
        return render(request, 'partial.html', postData)


@csrf_exempt
def cash(request):
    if request.method == "POST":
        postData = {
            "orderId":  request.POST.get('orderId'),
            "orderAmount":  request.POST.get('orderAmount'),
            "referenceId":  request.POST.get('referenceId'),
            "txStatus":  request.POST.get('txStatus'),
            "paymentMode":  request.POST.get('paymentMode'),
            "txMsg": request.POST.get('txMsg'),
            "signature":  request.POST.get('signature'),
            "txTime":  request.POST.get('txTime')
        }
        purc = get_object_or_404(Purchase, orderId=request.POST.get('orderId'))
        purc.status = request.POST.get('txStatus')
        purc.referenceId = request.POST.get('referenceId')
        purc.save()

        if len(purc.aid) != 0:
            if AffiliateUser.objects.filter(aid=purc.aid).exists():
                affiliate_user = AffiliateUser.objects.get(aid=purc.aid)
                affiliate_ern = AffiliateEarning.objects.get(
                    aid=affiliate_user)
                margin_earned = (int(request.POST.get('amount'))
                                 * int(purc.margin))//100
                affiliate_ern.total_price = int(
                    affiliate_ern.total_price) + margin_earned
                affiliate_ern.remain_price = int(
                    affiliate_ern.remain_price) + margin_earned
                if request.POST.get('txStatus') == 'SUCCESS':
                    affiliate_ern.withdrawlable_amount = int(
                        affiliate_ern.withdrawlable_amount) + margin_earned

                affiliate_ern.save()

        signatureData = ""
        signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + \
            postData['txStatus'] + postData['paymentMode'] + \
            postData['txMsg'] + postData['txTime']
        message = signatureData.encode('utf-8')

        secretkey = "96d9e9a3801fc8914dde8e92a19ad866302335f5"

        secret = secretkey.encode('utf-8')
        computedsignature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
        context = {
            'postData': postData,
            'computedsignature': computedsignature,
            'purchase': purc
        }

        return render(request, 'pdf.html', context)


@staff_member_required
def adminr(request):
    context = {
        'purchases': Purchase.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'admins.html', context)


@staff_member_required
def ProductCreate(request):
    ImageFormSet = modelformset_factory(Images,
                                        fields=('image',), extra=5)
    DescriptionFormSet = modelformset_factory(
        des, fields=('description',), extra=3)
    form = ProductForm()
    states = States.objects.all()
    cities = Cities.objects.all()
    locality = Localities.objects.all()
    print(states, cities, locality)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        print(form.errors)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        formset2 = DescriptionFormSet(request.POST or None)
        if formset.is_valid() and formset2.is_valid():
            prod = form.save(commit=False)
            prod.save()
            form.save_m2m()
            for f in formset:
                try:
                    photo = Images(product=prod, image=f.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    break

            for f in formset2:
                try:
                    desc = des(
                        product=prod, description=f.cleaned_data['description'])
                    desc.save()
                except Exception as e:
                    break

            messages.success(request,
                             "Posted!")
            return redirect('index')

        else:

            messages.success(request,
                             "error")

    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=Images.objects.none())
        formset2 = DescriptionFormSet(queryset=des.objects.none())

    context = {
        'form': form,
        'formset': formset,
        'formset2': formset2,
        'states': states,
        'cities': cities,
        'locality': locality

    }
    return render(request, 'form.html', context)


@staff_member_required
def BlogCreate(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, "Posted!")
        return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'addblog.html', context)


@staff_member_required
def AddItinerary(request):
    form = ItineraryForm()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        form = ItineraryForm(request.POST)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, "Posted!")
        return redirect('/itinerary_response/'+phone)
    context = {
        'form': form,
    }
    return render(request, 'itinerary.html', context)


@staff_member_required
def AddPopularTag(request):
    form = PopularTagForm()
    if request.method == 'POST':
        form = PopularTagForm(request.POST)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, "Posted!")
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'addpopulartag.html', context)


@csrf_exempt
def Locality(request, slug):

    context = {
        'city': slug,
        'destination': Destination.objects.filter(type='locality', name=slug),
        'adventure': Product.objects.filter(category='Adventure', locality=slug),
        'tour': Product.objects.filter(category='Tour', locality=slug),
        'popular': Product.objects.filter(locality=slug, order=1),
        'len': len(Product.objects.filter(locality=slug))

    }

    return render(request, 'locality.html', context)


@csrf_exempt
def travelGuide(request, slug, slug1):
    if slug1 == "Top-places-to-visit" or slug1 == "Things-to-do":
        slug1 = slug1.split('-')
        slug2 = ''
        for i in range(len(slug1)):
            if i+1 >= len(slug1):
                slug2 += slug1[i]
            else:
                slug2 += slug1[i] + " "
        bestplace = TravelGuide.objects.get(name=slug, tag=slug2)
    else:
        bestplace = TravelGuide.objects.get(name=slug, manual_slug=slug1)

    trandings = TravelGuide.objects.filter(
        name=slug, tag='General travel guide')[:10]
    context = {
        'city': slug,
        'bestplace': bestplace,
        'trandings': trandings,
    }

    return render(request, 'travelguide.html', context)


@staff_member_required
def travelGuideEntryForm(request):
    form = TravelGuideEntryForm()
    if request.method == 'POST':
        form = TravelGuideEntryForm(
            request.POST or None, request.FILES or None)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, "Posted!")
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'travelguideentryform.html', context)


@staff_member_required
def travelGuideList(request):
    states = States.objects.all()
    cities = Cities.objects.all()
    localities = Localities.objects.all()

    context = {
        'states': states,
        'cities': cities,
        'localities': localities,
    }
    return render(request, 'travel-guide-list.html', context)


@staff_member_required
def travelGuideData(request):
    state = request.GET.get('state')
    travel_guide = TravelGuide.objects.filter(name=state)

    print(travel_guide)
    data = render_to_string('travel-guide-data.html',
                            {'travel_guide': travel_guide})

    return JsonResponse({'data': data})


@staff_member_required
def travelGuideEdit(request, slug):
    travel_guide = TravelGuide.objects.get(manual_slug=slug)
    if request.method == 'POST':
        form = TravelGuideEntryForm(
            request.POST or None, request.FILES or None, instance=travel_guide)
        print(form.errors)
        form.save()
        messages.success(request, 'updated Successfully !')
        return redirect('/travel-guide-list/')

    return render(request, 'travel-guide-edit.html', {'travel_guide': travel_guide})


@staff_member_required
def ProductsList(request):
    context = {
        'products': Product.objects.all()[::-1]
    }
    return render(request, 'productslist.html', context)


def Deleteproduct(request, pk):
    cat = get_object_or_404(Product, id=pk)

    if request.method == 'POST':         # If method is POST,
        cat.delete()
        return redirect('/productslist')

    return render(request, 'productslist.html', {'post': cat})


@staff_member_required
def AddErp(request):
    form = ErpForm()
    if request.method == 'POST':
        form = ErpForm(request.POST)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, "Posted!")
        return redirect('/erplist')
    context = {
        'form': form,
    }
    return render(request, 'erp.html', context)


def download(request, slug):

    detail = get_object_or_404(Purchase, orderId=slug)
    return render(request, 'download.html', {'purchase': detail})


@staff_member_required
def ProductUpdate(request, slug):
    form = UpdateForm()
    states = States.objects.all()
    cities = Cities.objects.all()
    locality = Localities.objects.all()
    ImageFormSet = modelformset_factory(Images,
                                        fields=('image',), extra=5)
    DescriptionFormSet = modelformset_factory(
        des, fields=('description',), extra=3)

    product = get_object_or_404(Product, slug=slug)
    description = product.description
    # itenary=product.itenary

    if request.method == 'POST':
        # =================== deleting ing ======================== #
        img = request.POST.get('delete')
        del__img = img.split('-')

        for m1 in del__img:
            if len(m1) != 0:
                each_img = Images.objects.get(product=product, id=m1)
                each_img.delete()

        form = UpdateForm(request.POST or None, instance=product)

        # if form.data['a_inclusion']:
        #     print("we gate the a_inclusion Data : ",form.data['a_inclusion'])
        # else:
        #     print("is not empty========================\n\n\n\n")

        form.save()
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        formset2 = DescriptionFormSet(request.POST or None)
        if request.POST.get('description') == "":
            product.description = description

        # if request.POST.get('itenary') == "":
        #     # product.itenary= itenary

        product.save()
        if formset.is_valid() and formset2.is_valid():
            for f in formset:
                try:
                    photo = Images(product=product,
                                   image=f.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    break

            for f in formset2:
                try:
                    desc = des(product=product,
                               description=f.cleaned_data['description'])
                    desc.save()
                except Exception as e:
                    break

            return redirect('/productslist')
    else:
        form = UpdateForm()
        formset = ImageFormSet(queryset=Images.objects.none())
        formset2 = DescriptionFormSet(queryset=des.objects.none())

    if product.inclusion:
        inclusion = product.inclusion.split('</div>')
    else:
        inclusion = []

    context = {
        'product': product,
        'inclusions': inclusion,
        'form': form,
        'formset': formset,
        'formset2': formset2,
        'states': states,
        'cities': cities,
        'locality': locality
    }

    return render(request, 'editproduct.html', context)


@staff_member_required
def DeleteImg(request, slug):
    image = Images.objects.get(id=slug)
    image.delete()

    return redirect('index')


# =========================== top picks ====================================== #

@staff_member_required
def topPicksEntryForm(request):
    form = Top_picks_entryForm()
    if request.method == 'POST':
        form = Top_picks_entryForm(request.POST, request.FILES)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, 'Added !')
        return redirect('/')
    context = {
        'form': form,
    }

    return render(request, 'top-picks-entry-form.html', context)


def topPicks(request, slug):
    form = BestPackageForm()
    all_products = []
    if TopPicksEntryForm.objects.filter(manual_slug=slug).exists():
        top_picks = TopPicksEntryForm.objects.get(manual_slug=slug)

        if top_picks.slug_1:
            product = Product.objects.get(manual_slug=top_picks.slug_1)
            all_products.append(product)
        if top_picks.slug_2:
            product = Product.objects.get(manual_slug=top_picks.slug_2)
            all_products.append(product)
        if top_picks.slug_3:
            product = Product.objects.get(manual_slug=top_picks.slug_3)
            all_products.append(product)
        if top_picks.slug_4:
            product = Product.objects.get(manual_slug=top_picks.slug_4)
            all_products.append(product)
        if top_picks.slug_5:
            product = Product.objects.get(manual_slug=top_picks.slug_5)
            all_products.append(product)
        if top_picks.slug_6:
            product = Product.objects.get(manual_slug=top_picks.slug_6)
            all_products.append(product)
        if top_picks.slug_7:
            product = Product.objects.get(manual_slug=top_picks.slug_7)
            all_products.append(product)
        if top_picks.slug_8:
            product = Product.objects.get(manual_slug=top_picks.slug_8)
            all_products.append(product)
        if top_picks.slug_9:
            product = Product.objects.get(manual_slug=top_picks.slug_9)
            all_products.append(product)
        if top_picks.slug_10:
            product = Product.objects.get(manual_slug=top_picks.slug_10)
            all_products.append(product)
        if top_picks.slug_11:
            product = Product.objects.get(manual_slug=top_picks.slug_11)
            all_products.append(product)
        if top_picks.slug_12:
            product = Product.objects.get(manual_slug=top_picks.slug_12)
            all_products.append(product)
        if top_picks.slug_13:
            product = Product.objects.get(manual_slug=top_picks.slug_13)
            all_products.append(product)
        if top_picks.slug_14:
            product = Product.objects.get(manual_slug=top_picks.slug_14)
            all_products.append(product)
        if top_picks.slug_15:
            product = Product.objects.get(manual_slug=top_picks.slug_15)
            all_products.append(product)
        if top_picks.slug_16:
            product = Product.objects.get(manual_slug=top_picks.slug_16)
            all_products.append(product)
        if top_picks.slug_17:
            product = Product.objects.get(manual_slug=top_picks.slug_17)
            all_products.append(product)
        if top_picks.slug_18:
            product = Product.objects.get(manual_slug=top_picks.slug_18)
            all_products.append(product)
        if top_picks.slug_19:
            product = Product.objects.get(manual_slug=top_picks.slug_19)
            all_products.append(product)
        if top_picks.slug_20:
            product = Product.objects.get(manual_slug=top_picks.slug_20)
            all_products.append(product)
    else:
        top_picks = ''

    if request.method == "POST":
        form = BestPackageForm(request.POST)
        if form.data['top_picks']:
            manual_slug = form.data['top_picks']
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, 'Added !')
        return redirect('/toppicks/' + str(manual_slug))

    context = {
        'top_picks': top_picks,
        'all_products': all_products,
        'form': form,
    }

    return render(request, 'top-picks.html', context)


@csrf_exempt
def productEnqueryForm(request):
    product_slug = request.POST.get('product_slug')
    name = request.POST.get('name')
    number = request.POST.get('number')
    email = request.POST.get('email')
    date_of_travel = request.POST.get('date_of_travel')
    number_of_people = request.POST.get('number_of_people')
    message = request.POST.get('message')

    product_enquiry = ProductEnquiry(product_slug=product_slug,
                                     name=name, number=number, email=email, date_of_travel=date_of_travel,
                                     number_of_people=number_of_people, message=message)

    product_enquiry.save()

    return JsonResponse({'data': name + " your Enquiry successfully added in enquiry Box !"})

    #  ======================================== cource Entry form =====================================


@staff_member_required
def courseEntryForm(request):
    form = CourseEntryForm()
    if request.method == 'POST':
        form = CourseEntryForm(request.POST, request.FILES)
        print(form.errors)
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        messages.success(request, 'Added !')
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'courseentryform.html', context)


def course(request):
    return render(request, 'course.html')


# ================================ state-city ============================

def StateCity(request):
    return render(request, 'state-city.html')


# ===================================== rentals =========================================
# rentals-submit
@ staff_member_required
def rentalsForm(request):
    states = States.objects.all()
    cities = Cities.objects.all()
    context = {'states': states, 'cities': cities}
    return render(request, 'rentals-form.html', context)


def rentalsSubmit(request):
    if request.method == "POST":
        state = request.POST['state']
        city = request.POST['city']
        rentals_type = request.POST['rentals_type']
        vehicle_gear_type = request.POST['vehicle_gear_type']
        category = request.POST['category']
        brand_name = request.POST['brand_name']
        product_name = request.POST['product_name']
        # if len(request.FILES) != 0:
        #     product_image = request.FILES['product_image']
        product_image = request.FILES['product_image']
        product_image_2 = request.FILES['product_image_2']
        specification_1 = request.POST['specification_1']
        specification_2 = request.POST['specification_2']
        specification_3 = request.POST['specification_3']
        popularity_score = request.POST['popularity_score']
        delivery_option = request.POST['delivery_option']
        terms_and_conditions = request.POST['terms_and_conditions']
        price_1_3 = request.POST['price_1_3']
        price_4_7 = request.POST['price_4_7']
        price_8_15 = request.POST['price_8_15']
        price_16_30 = request.POST['price_16_30']
        rental = Rentals(state=state, city=city, rentals_type=rentals_type, product_image=product_image, product_image_2=product_image_2,
                         vehicle_gear_type=vehicle_gear_type, category=category, brand_name=brand_name, product_name=product_name,
                         specification_1=specification_1,
                         specification_2=specification_2, specification_3=specification_3, popularity_score=popularity_score,
                         delivery_option=delivery_option, terms_and_conditions=terms_and_conditions, price_1_3=price_1_3, price_4_7=price_4_7,
                         price_8_15=price_8_15, price_16_30=price_16_30)
        rental.save()
        messages.success(request, "Submitted Successfully")
        return redirect('/rentals-form')

    return redirect('rentals-form')


@ csrf_exempt
def rentals(request, slug):
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')

    if slug == 'all':
        if len(city) > 0:
            paginator = Paginator(Rentals.objects.filter(city=city), 15)
        elif len(state) > 0:
            paginator = Paginator(Rentals.objects.filter(state=state), 15)
        else:
            paginator = Paginator(
                Rentals.objects.all(), 15)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name=slug),
            'slug': slug,
        }
    elif slug == 'Self-Driving-Vehicle':

        if len(city) > 0:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Self Driving Vehicle', city=city), 15)

        elif len(state) > 0:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Self Driving Vehicle', state=state), 15)

        else:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Self Driving Vehicle'), 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        brands = []
        for p in page_obj:
            brands.append(p.brand_name)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            # 'adven': AdventureTourTypes.objects.filter(name='High Fly'),
            'field': 'Self Driving Vehicle',
            'slug': slug,
            'brands': brands,
        }
    elif slug == 'Trekking-Gears':
        if len(city) > 0:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Trekking Gear', city=city), 15)
        elif len(state) > 0:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Trekking Gear', state=state), 15)
        else:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Trekking Gear'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        brands = []
        for p in page_obj:
            brands.append(p.brand_name)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            # 'adven': AdventureTourTypes.objects.filter(name='High Thrills'),
            'slug': slug,
            'brands': brands,
            'field': 'Trekking Gear'
        }
    elif slug == 'Sleeping-Bag-Tents':
        if len(city) > 0:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Sleeping Bag & Tent', city=city), 15)
        elif len(state) > 0:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Sleeping Bag & Tent', state=state), 15)
        else:
            paginator = Paginator(Rentals.objects.filter(
                rentals_type='Sleeping Bag & Tent'), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            # 'adven': AdventureTourTypes.objects.filter(name='Land Adventure'),
            'slug': slug,
            'field': 'Sleeping Bag & Tent'
        }
    else:
        a = slug.split('-')
        if len(a) > 1:
            slug = a[0]+' '+a[1]
        if len(city) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', city=city, adventuretype=slug), 15)
        elif len(state) > 0:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', state=state, adventuretype=slug), 15)
        else:
            paginator = Paginator(Product.objects.filter(
                category='Adventure', adventuretype=slug), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'city': city,
            'state': state,
            'adven': AdventureTourTypes.objects.filter(name=slug),
            'slug': slug,
        }

    return render(request, 'rentals.html', context)


@ csrf_exempt
def FilterRentals(request):
    category = request.POST.getlist('category[]')
    rentals_type = request.POST.get('rentals_type')
    search = request.POST.get('search')
    a = request.POST.get('a')

    if rentals_type == 'Self Driving Vehicle':
        allproducts = Rentals.objects.filter(
            rentals_type='Self Driving Vehicle')
    elif rentals_type == 'Sleeping Bag & Tent':
        allproducts = Rentals.objects.filter(
            rentals_type='Sleeping Bag & Tent')
    elif rentals_type == 'Trekking Gear':
        allproducts = Rentals.objects.filter(
            rentals_type='Trekking Gear')
    filters = []

    if a == '0':
        allproducts = Rentals.objects.filter(
            rentals_type='Self Driving Vehicle', city__icontains=search)

        for p in allproducts:
            filters.append(p.brand_name)
        context = {'products': allproducts}
        t = render_to_string('rental_card.html', context)
        print(filters)

        return JsonResponse({'data': t, 'len': len(t), 'product_len': len(allproducts), 'filters': filters})
    elif a == '1':
        if len(category) > 0:
            allproducts = Rentals.objects.filter(
                rentals_type=rentals_type, category__in=category).distinct()
            for p in allproducts:
                filters.append(p.brand_name)

        context = {'products': allproducts}
        t = render_to_string('rental_card.html', context)
        print(filters)

        return JsonResponse({'data': t, 'len': len(t), 'product_len': len(allproducts), 'filters': filters})


@ csrf_exempt
def FilterRentalsBrand(request):
    category = request.POST.getlist('category[]')
    brands = request.POST.getlist('brand[]')
    gear = request.POST.getlist('gear[]')
    rentals_type = request.POST.get('rentals_type')

    # if rentals_type == 'Self Driving Vehicle':
    #     allproducts = Rentals.objects.filter(
    #         rentals_type='Self Driving Vehicle')
    # elif rentals_type == 'Sleeping Bag & Tent':
    #     allproducts = Rentals.objects.filter(
    #         rentals_type='Sleeping Bag & Tent')
    # elif rentals_type == 'Trekking Gear':
    #     allproducts = Rentals.objects.filter(
    #         rentals_type='Trekking Gear')

    if len(category) > 0:
        allproducts = Rentals.objects.filter(
            rentals_type=rentals_type, category__in=category).distinct()
        if len(brands) > 0:
            allproducts = Rentals.objects.filter(
                rentals_type=rentals_type, category__in=category, brand_name__in=brands).distinct()
            if len(gear) > 0:
                if gear[0] != "Both":
                    allproducts = Rentals.objects.filter(
                        rentals_type=rentals_type, category__in=category, brand_name__in=brands, vehicle_gear_type__in=gear).distinct()
        elif len(gear) > 0:
            if gear[0] != "Both":
                allproducts = Rentals.objects.filter(
                    rentals_type=rentals_type, category__in=category, vehicle_gear_type__in=gear).distinct()
    context = {'products': allproducts}
    t = render_to_string('rental_card.html', context)
    return JsonResponse({'data': t, 'len': len(t), 'product_len': len(allproducts)})


@ csrf_exempt
def rentalsBooking(request):
    if request.method == "POST":
        postData = {
            "product": request.POST.get('productName'),
            "date": request.POST.get('date'),
            "amount": request.POST.get('totalPrice'),
        }
        return render(request, 'bookingform.html', {'postData': postData})
    return render(request, 'course.html')

# Agents


def agentRegistration(request):
    return render(request, 'agent-registration-form.html')


@ csrf_exempt
def agentSubmit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        aadhar = request.POST.get('aadhar')
        address = request.POST.get('address')
        gstin = request.POST.get('gstin')
        pan = request.POST.get('pan')
        photo_id = request.FILES['photo-id']
        alternate_name = request.POST.get('alternate-name')
        alternate_phone = request.POST.get('alternate-phone')
        bank_name = request.POST.get('bank-name')
        account_number = request.POST.get('account-number')
        ifsc_code = request.POST.get('ifsc-code')
        upi_id = request.POST.get('upi-id')

        agent = Agent(name=name, email=email, phone=phone, aadhar=aadhar, address=address,
                      gstin=gstin, pan=pan, photo_id=photo_id, alternate_name=alternate_name, alternate_phone=alternate_phone,
                      bank_name=bank_name,
                      account_number=account_number, ifsc_code=ifsc_code, upi_id=upi_id)
        agent.save()
        messages.success(request, "Submitted Successfully")
        return redirect('/agent-dashboard')
        # otp = random.randint(0, 9999)
        # mail = EmailMessage(
        #     subject='Payment Recept',
        #     body='Hello ' + name + "!. Here, is your OTP: " + otp,
        #     from_email='bookings@universaladventures.in',
        #     to=[email, ]
        # )
        # mail.content_subtype = "html"
        # mail.send()
        return render(request, 'rentals-form')


def agentList(request):
    agents = Agent.objects.all()
    context = {'agents': agents}
    return render(request, "agent-list.html", context)


def FilterAgents(request):
    if request.method == "GET":
        status = request.GET.get('status')
        agents = Agent.objects.filter(status=status).distinct()
        data = render_to_string('agent-list-data.html', {
            'agents': agents, 'status': status})
    return JsonResponse({'data': data})


@staff_member_required
def AgentStatus(request, status, slug):
    if status == 'active':
        agent = Agent.objects.get(agent_id=slug)
        agent.status = 'active'
        agent.save()

    elif status == 'inactive':
        agent = Agent.objects.get(agent_id=slug)
        agent.status = 'inactive'
        agent.save()

    messages.info(request, 'Account is activated !!')
    return redirect('/agent-list')


def agentDashboard(request):
    if request.user.is_active:
        agent = get_object_or_404(Agent, email=request.user.email)
        states = States.objects.all()
        paginator = Paginator(Product.objects.filter(
            available_for_agent=True), 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        bookings = AgentProductBooking.objects.filter(agent=agent)
        withdraws = AgentWithdrawHistory.objects.filter(agent=agent)
        context = {
            'products': page_obj,
            'len': len(page_obj),
            'bookings': bookings,
            'lenBookings': len(bookings),
            'agent': agent,
            'withdraws': withdraws,
            'states': states
        }
        return render(request, 'agent-dashboard.html', context)
    print('user')
    return render(request, 'agent-dashboard.html')


@csrf_exempt
def filterAgentProducts(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        bookings = AgentProductBooking.objects.filter(
            guest_name__icontains=search)
        t = render_to_string('agent-booking-list.html', {'bookings': bookings})
        return JsonResponse({'data': t})

    if request.method == 'POST':
        adventuretype = request.POST.getlist('filters[]')
        state = request.POST.get('state')
        allproducts = Product.objects.filter(available_for_agent=True)
        search = request.POST.get('search')
        if len(adventuretype) > 0:
            allproducts = Product.objects.filter(available_for_agent=True,
                                                 adventuretype__in=adventuretype).distinct()
        if len(state) > 0:
            allproducts = allproducts.filter(state=state)
        if len(search) > 0:
            allproducts = allproducts.filter(name__icontains=search)
        t = render_to_string('prodlist.html', {'products': allproducts})
        return JsonResponse({'data': t})


def agentProduct(request, slug):
    product = get_object_or_404(Product, manual_slug=slug)
    context = {
        'product': product
    }
    return render(request, 'agent-product.html', context)


@staff_member_required
def agentBooking(request, slug):
    agent = get_object_or_404(Agent, email=request.user.email)
    product = get_object_or_404(Product, manual_slug=slug)
    context = {
        'product': product,
        'agent': agent
    }
    return render(request, 'agent-product-booking.html', context)


def agentProductBooking(request):
    if request.method == 'POST':
        orderId = random.randint(100000, 999999)
        agent = get_object_or_404(Agent, agent_id=request.POST.get('agent_id'))
        product = get_object_or_404(Product, id=request.POST.get('product_id'))
        guest_name = request.POST.get('guest_name')
        guest_phone = request.POST.get('guest_phone')
        guest_other_phone = request.POST.get('guest_other_phone')
        guest_email = request.POST.get('guest_email')
        number_of_guests = request.POST.get('number_of_guests')
        service_date = request.POST.get('service_date')
        product_price = request.POST.get('price-per-product')
        total_price = request.POST.get('total-price')
        # calcluate agent margin x% of total payment
        margin_earned = (int(total_price) * int(product.margin_agent))/100
        receipt_send_type = request.POST.get('receipt_send_type')
        terms_and_conditions = request.POST.get('terms_and_conditions')
        booking = AgentProductBooking(
            agent=agent, product=product, guest_name=guest_name, guest_phone=guest_phone, guest_other_phone=guest_other_phone, guest_email=guest_email, number_of_guests=number_of_guests, service_date=service_date, product_price=product_price, total_price=total_price, margin_earned=margin_earned, receipt_send_type=receipt_send_type, terms_and_conditions=terms_and_conditions, orderId=orderId)
        booking.save()
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderAmount": total_price,
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": agent.name,
            "customerPhone": agent.phone,
            "customerEmail": agent.email,
            "returnUrl": 'http://127.0.0.1:8000/handlerequestagent/',
            "notifyUrl": 'https://universaladventures.in/',
            "orderId": orderId,
            "margin_earned": margin_earned
        }

        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+str(postData[key])

        message = signatureData.encode('utf-8')
        # get secret key from your config
        secretkey = "b8caf62ce5e932034897da856129873bf0dace3e"
        secret = secretkey.encode('utf-8')
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        postData["signature"] = signature
        return render(request, 'agent-checkout-form.html', {'postData': postData})


@csrf_exempt
def cash_agent(request):
    if request.method == "POST":
        postData = {
            "orderId":  request.POST.get('orderId'),
            "orderAmount":  request.POST.get('orderAmount'),
            # "referenceId":  request.POST.get('referenceId'),
            "txStatus":  request.POST.get('txStatus'),
            "paymentMode":  request.POST.get('paymentMode'),
            "txMsg": request.POST.get('txMsg'),
            "signature":  request.POST.get('signature'),
            "txTime":  request.POST.get('txTime')
        }
        booking = get_object_or_404(
            AgentProductBooking, orderId=request.POST.get('orderId'))
        booking.status = request.POST.get('txStatus')
        booking.save()
        agent = booking.agent
        if str(request.POST.get('txStatus')) == 'SUCCESS':
            agent = get_object_or_404(
                Agent, agent_id=str(request.POST.get('agent_id')))
            agent.total_earned = int(
                agent.total_earned) + int(request.POST.get('margin_earned'))
            agent.available_balance = int(
                agent.available_balance) + int(request.POST.get('margin_earned'))
            agent.save()
        signatureData = ""
        signatureData = postData['orderId'] + postData['orderAmount'] +  \
            postData['txStatus'] + postData['paymentMode'] + \
            postData['txMsg'] + postData['txTime']
        message = signatureData.encode('utf-8')

        secretkey = "96d9e9a3801fc8914dde8e92a19ad866302335f5"

        secret = secretkey.encode('utf-8')
        computedsignature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
        if booking.receipt_send_type == "Download receipt and share with guest manually":
            context = {
                'postData': postData,
                'computedsignature': computedsignature,
                'booking': booking
            }
            return render(request, 'agent-pdf.html', context)
        else:
            mail = EmailMessage(
                subject='Payment Recept',
                body=('Hello!,Here are your booking detailsOrder ID: ' +
                      postData['orderId'] + 'Order Amount: ' +
                      postData['orderAmount']),
                from_email='kaushiky655@gmail.com',
                # from_email='bookings@universaladventures.in',
                to=['aditya2462001@gmail.com', ]
            )
            mail.content_subtype = "html"
            mail.send()
            return redirect('/agent-dashboard')


@csrf_exempt
def agentWithdraw(request):
    if request.method == "POST":
        amt = request.POST.get('withdraw-amount')
        agent = get_object_or_404(Agent, agent_id=request.POST.get('agent_id'))
        ip = request.META.get('REMOTE_ADDR')
        agent.withdrawn_till_date = int(agent.withdrawn_till_date) + int(amt)
        agent.available_balance = int(agent.available_balance) - int(amt)
        declaration = request.POST.get('declaration')
        agent.save()
        if declaration == 'on':
            declaration = True
        else:
            declaration = False
        withdraw = AgentWithdrawHistory(
            agent=agent, amount=amt, status="PENDING", ip=ip, declaration=declaration)
        withdraw.save()
        return redirect('/agent-dashboard')


def testimonialsForm(request):
    return render(request, "testimonials-form.html")


def testimonialsSubmit(request):
    if request.method == "POST":
        display_page_url = request.POST.get('display_page_url')
        product_page_url = request.POST.get('product_page_url')
        full_name = request.POST.get('full_name')
        rating = request.POST.get('rating')
        profile_photo = request.FILES['profile_photo']
        tags = request.POST.get('tags')
        testimonials = request.POST.get('testimonials')
        photo_1 = request.FILES['photo1'] if 'photo1' in request.FILES else None
        photo_2 = request.FILES['photo2'] if 'photo2' in request.FILES else None
        photo_3 = request.FILES['photo3'] if 'photo3' in request.FILES else None
        photo_4 = request.FILES['photo4'] if 'photo4' in request.FILES else None
        photo_5 = request.FILES['photo5'] if 'photo5' in request.FILES else None
        photo_6 = request.FILES['photo6'] if 'photo6' in request.FILES else None
        photo_7 = request.FILES['photo7'] if 'photo7' in request.FILES else None
        photo_8 = request.FILES['photo8'] if 'photo8' in request.FILES else None
        testimonial = Testimonials(display_page_url=display_page_url, product_page_url=product_page_url, full_name=full_name, rating=rating, profile_photo=profile_photo, tags=tags,
                                   testimonials=testimonials, photo_1=photo_1, photo_2=photo_2, photo_3=photo_3, photo_4=photo_4, photo_5=photo_5, photo_6=photo_6, photo_7=photo_7, photo_8=photo_8)
        testimonial.save()
        messages.success(request, "Submitted Successfully")
        return redirect('/testimonials-form')

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
from .models import Affiliate, CityHotelData, Erp,Populartags, Product, Destination, Images, StateItineraryData, TopPicksEntryForm, duration, phone, Purchase, states, des, promo, AdventureTourTypes, TravelGuide,BestPackage,ProductEnquiry
from .models import Blogpost, wallet
from .models import Itinerary,ItineraryData
from .forms import CityHotelDataForm, ItineraryDataForm, ItineraryForm, ProductEnquiryForm, ProductForm, Addphone, StateItineraryDataForm, purchaseform, UpdateForm, BlogForm, UpdateItineraryForm, ErpForm, UpdateErpForm, TravelGuideEntryForm, PopularTagForm,Top_picks_entryForm,BestPackageForm,CourseEntryForm
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
from django.db.models import Q
from functools import reduce


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def index(request):
    allprods = []
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
    post = get_object_or_404(Itinerary, id=slug)
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

@staff_member_required
def stateItinerary(request):
    form = StateItineraryDataForm()
    if request.method == 'POST':
        form = StateItineraryDataForm(request.POST or None)
        print(form.errors)
        prod = form.save(commit = False)
        prod.save()
        form.save_m2m()
        messages.success(request,'Added !')
        return redirect('/')

    context = {
        'form':form,
    }
    return render(request,'state-itinerary-form.html',context)


@staff_member_required
def cityHotel(request):
    form = CityHotelDataForm()
    if request.method == 'POST':
        form = CityHotelDataForm(request.POST or None,request.FILES or None)
        print(form.errors)
        prod = form.save(commit = False)
        prod.save()
        form.save_m2m()
        messages.success(request,'added !')
        return redirect('/')
    return render(request,'city-hotel-form.html',{'form':form})




@staff_member_required
def AddItineraryData(request):
    form = ItineraryDataForm()
    if request.method == 'POST':
        form = ItineraryDataForm(request.POST or None)
        print(form.errors)
        prod = form.save(commit = False)
        prod.save()
        form.save_m2m()
        messages.success(request,'added !')
        return redirect('/')
    
    context = {
        'form':form,
    }

    return render(request,'itinerary-data-form.html',context)

@staff_member_required
def getItineraryData(request):
    arr_1 = []
    arr_2 = []
    state = request.GET.get('state')
    state_itineraries = StateItineraryData.objects.filter(state = state).values()
    city_hotels = CityHotelData.objects.filter(state = state).values()

    for i in state_itineraries:
        arr_1.append(i)
    for j in city_hotels:
        arr_2.append(j)
    
    return JsonResponse({'state_itineraries':arr_1,'city_hotels':arr_2})


def itineraryData(request,slug):
    hotel1 = ''
    hotel2 = ''
    hotel3 = ''
    hotel4 = ''
    hotel5 = ''
    itinerary = ItineraryData.objects.get(slug = slug)
    if itinerary.hotel_stay_name_1 :
        hotel1 = CityHotelData.objects.get(state = itinerary.state , city = itinerary.hotel_city_name_1 , stay_name = itinerary.hotel_stay_name_1)
    if itinerary.hotel_stay_name_2 :
        hotel2 = CityHotelData.objects.get(state = itinerary.state , city = itinerary.hotel_city_name_2 , stay_name = itinerary.hotel_stay_name_2)
    if itinerary.hotel_stay_name_3 :
        hotel3 = CityHotelData.objects.get(state = itinerary.state , city = itinerary.hotel_city_name_3 , stay_name = itinerary.hotel_stay_name_3)
    if itinerary.hotel_stay_name_4 :
        hotel4 = CityHotelData.objects.get(state = itinerary.state , city = itinerary.hotel_city_name_4 , stay_name = itinerary.hotel_stay_name_4)
    if itinerary.hotel_stay_name_5 :
        hotel5 = CityHotelData.objects.get(state = itinerary.state , city = itinerary.hotel_city_name_5 , stay_name = itinerary.hotel_stay_name_5)

    context = {
        'itinerary':itinerary,
        'hotel1':hotel1,
        'hotel2':hotel2,
        'hotel3':hotel3,
        'hotel4':hotel4,
        'hotel5':hotel5,
    }
    return render(request,'itinerary-data.html',context)




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
            context = {
                'affiliate': Affiliate.objects.filter(email=request.user.email, coupon_uid__in=m),
                'coupons': promo.objects.filter(email=request.user.email),
                'phone': phon,
                'total': total,
                'length': 1,
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


def product(request, slug):
    print(slug)
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
        'cats': cat2
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
        top_places_to_visit = TravelGuide.objects.get(name=slug, tag='Top places to visit')
    else:
        top_places_to_visit = ''
    
    if TravelGuide.objects.filter(name=slug, tag='Things to do').exists():
        things_to_do = TravelGuide.objects.get(name=slug, tag='Things to do')
    else:
        things_to_do = ''


    if destination.location:
        locations = destination.location.split(',')
    else:
        locations = []
    context = {
        'city': slug,
        'destination': Destination.objects.filter(type='state', name=slug),
        'destination_loc':locations,
        'adventure': Product.objects.filter(category='Adventure', state=slug),
        'tour': Product.objects.filter(category='Tour', state=slug),
        'popular': Product.objects.filter(state=slug, order=1),
        'populartags': Populartags.objects.filter(tag=slug),
        'travelguide': TravelGuide.objects.filter(name=slug, tag='General travel guide'),
        'top_places_to_visit':top_places_to_visit,
        'things_to_do':things_to_do,
        'len': len(Product.objects.filter(state=slug))

    }

    return render(request,'state.html', context)




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
            'slug':slug,
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
            'slug':slug,
            'len': len(page_obj),
            'adven': AdventureTourTypes.objects.filter(name=slug)
        }

    return render(request,'tour.html', context)


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

    a = slug.split('-')
    allproducts = Product.objects.filter(
        category='Adventure', adventuretype=slug)
    if len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1).distinct()
    if len(typee) > 0:
        allproducts = Product.objects.filter(
            category='Adventure',  adventuretype__in=typee, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(citye) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  city__in=citye, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(citye) > 0 and len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1,  city__in=citye, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(adventure) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  adventurelevel__in=adventure, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(adventure) > 0 and len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1,  adventurelevel__in=adventure, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(duration) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(duration) > 0 and len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1,  duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(loc) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug,  adventureloc__in=loc, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(loc) > 0 and len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1,  adventureloc__in=loc, sale__gte=min_price, sale__lte=max_price).distinct()
    if len(search) > 0:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug, name__icontains=search,).distinct()
    if len(search) > 0 and len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1,  name__icontains=search, sale__gte=min_price, sale__lte=max_price).distinct()
    if min_price > 1000 or max_price < 100000:
        allproducts = Product.objects.filter(
            category='Adventure', adventuretype=slug, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()
    if min_price > 1000 or max_price < 100000 and len(a) > 1:
        slug1 = a[0]+' '+a[1]
        allproducts = Product.objects.filter(
            category='Adventure', tag_category=slug1, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()


    if category == 'Tour':
        allproducts = Product.objects.filter(category = category , tag_category=slug)
        if len(typee) > 0:
            allproducts = Product.objects.filter(
            category=category,  adventuretype__in=typee, sale__gte=min_price, sale__lte=max_price).distinct()
        if len(citye) > 0:
            allproducts = Product.objects.filter(category = category ,tag_category=slug, 
            city__in= citye,sale__gte=min_price, sale__lte=max_price)
        if len(duration) > 0:
            allproducts = Product.objects.filter(
                category=category,tag_category=slug, duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
        if len(duration) > 0 and len(a) > 1:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug,  duration__in=duration, sale__gte=min_price, sale__lte=max_price).distinct()
        if len(search) > 0:
            allproducts = Product.objects.filter(
                category=category,tag_category=slug,  name__icontains=search,).distinct()
        if len(search) > 0 and len(a) > 1:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug,  name__icontains=search, sale__gte=min_price, sale__lte=max_price).distinct()
        if min_price > 1000 or max_price < 100000:
            allproducts = Product.objects.filter(
                category=category,tag_category=slug, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()
        if min_price > 1000 or max_price < 100000 and len(a) > 1:
            allproducts = Product.objects.filter(
                category=category, tag_category=slug, sale__gte=min_price, sale__lte=max_price).order_by('sale').distinct()

    t = render_to_string('prodlist.html', {'products': allproducts})

    return JsonResponse({'data': t, 'len': len(t),'product_len':len(allproducts)})


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
        get_product = Product.objects.get(name = product)

        try:
            coupon = get_object_or_404(
                promo, coupon=request.POST.get('promo_code', ''))
            print(coupon.coupon)
            if (coupon.coupon[0] == "A" and coupon.coupon[1] == "U" ) or (coupon.coupon == get_product.promo_code):
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
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderId": uuid.uuid4().hex[:6].upper(),
            "orderAmount": request.POST.get('amount'),
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": request.POST.get('name'),
            "customerPhone": request.POST.get('phone'),
            "customerEmail": request.POST.get('email'),
            "returnUrl": 'https://universaladventures.in/handlerequest/',
            "notifyUrl": 'https://universaladventures.in/'
        }
        dates = datetime.datetime.strptime(
            request.POST.get('date'), "%Y-%m-%d").strftime("%Y-%m-%d")
        purchase = Purchase(user=request.user, product=prod, date=dates, days=request.POST.get(
            'number'), orderId=postData["orderId"], orderAmount=request.POST.get('amount'), coupon_uid=request.POST.get('coupon_id'))
        purchase.save()
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


def checkout2(request):
    if request.method == "POST":
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderId": uuid.uuid4().hex[:6].upper(),
            "orderAmount": request.POST.get('amount'),
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": request.POST.get('name'),
            "customerPhone": request.POST.get('phone'),
            "customerEmail": request.POST.get('email'),
            "returnUrl": 'https://universaladventures.in/handlerequestpartial/',
            "notifyUrl": 'https://universaladventures.in/'
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


def checkout3(request):
    if request.method == "POST":
        postData = {
            "appId": '3116246b3ec6d019344fd492a26113',
            "orderId": uuid.uuid4().hex[:6].upper(),
            "orderAmount": request.POST.get('amount'),
            "orderCurrency": 'INR',
            "orderNote": "g",
            "customerName": request.POST.get('name'),
            "customerPhone": request.POST.get('phone'),
            "customerEmail": request.POST.get('email'),
            "returnUrl": 'https://universaladventures.in/handlerequestpartial/',
            "notifyUrl": 'https://universaladventures.in/'
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
def travelGuide(request,slug,slug1):
    if slug1 == "Top-places-to-visit" or slug1 == "Things-to-do":
        slug1 = slug1.split('-')
        slug2 = ''
        for i in range(len(slug1)):
            if i+1 >= len(slug1):
                slug2 += slug1[i] 
            else:
                slug2 += slug1[i] + " "
        bestplace = TravelGuide.objects.get(name = slug, tag=slug2)
    else:
        bestplace = TravelGuide.objects.get(name = slug,manual_slug = slug1)

    trandings = TravelGuide.objects.filter(name = slug, tag='General travel guide')
    context = {
        'city': slug,
        'bestplace': bestplace,
        'trandings':trandings,
    }

    return render(request, 'travelguide.html', context)


@staff_member_required
def travelGuideEntryForm(request):
    form = TravelGuideEntryForm()
    if request.method == 'POST':
        form = TravelGuideEntryForm(request.POST or None , request.FILES or None)
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
    ImageFormSet = modelformset_factory(Images,
                                        fields=('image',), extra=5)
    DescriptionFormSet = modelformset_factory(
        des, fields=('description',), extra=3)

    product = get_object_or_404(Product, slug=slug)
    description = product.description
    # itenary=product.itenary

    if request.method == 'POST':
        # =================== deleting ing ======================== #
        img= request.POST.get('delete')
        del__img = img.split('-')

        for m1 in del__img:
            if len(m1) != 0:
                each_img = Images.objects.get(product = product ,id = m1)
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

            return redirect('index')
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
        'inclusions':inclusion,
        'form': form,
        'formset': formset,
        'formset2': formset2,
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
        form = Top_picks_entryForm(request.POST,request.FILES)
        print(form.errors)
        prod = form.save(commit = False)
        prod.save()
        form.save_m2m()
        messages.success(request,'Added !')
        return redirect('/')
    context = {
        'form':form,
    }

    return render(request,'top-picks-entry-form.html',context)

def topPicks(request,slug):
    form  = BestPackageForm()
    all_products = []
    if TopPicksEntryForm.objects.filter(manual_slug = slug).exists():
        top_picks = TopPicksEntryForm.objects.get(manual_slug = slug)

        if top_picks.slug_1:
            product = Product.objects.get(manual_slug = top_picks.slug_1)
            all_products.append(product)
        if top_picks.slug_2:
            product = Product.objects.get(manual_slug = top_picks.slug_2)
            all_products.append(product)
        if top_picks.slug_3:
            product = Product.objects.get(manual_slug = top_picks.slug_3)
            all_products.append(product)
        if top_picks.slug_4:
            product = Product.objects.get(manual_slug = top_picks.slug_4)
            all_products.append(product)
        if top_picks.slug_5:
            product = Product.objects.get(manual_slug = top_picks.slug_5)
            all_products.append(product)
        if top_picks.slug_6:
            product = Product.objects.get(manual_slug = top_picks.slug_6)
            all_products.append(product)
        if top_picks.slug_7:
            product = Product.objects.get(manual_slug = top_picks.slug_7)
            all_products.append(product)
        if top_picks.slug_8:
            product = Product.objects.get(manual_slug = top_picks.slug_8)
            all_products.append(product)
        if top_picks.slug_9:
            product = Product.objects.get(manual_slug = top_picks.slug_9)
            all_products.append(product)
        if  top_picks.slug_10:
            product = Product.objects.get(manual_slug = top_picks.slug_10)
            all_products.append(product)
        if  top_picks.slug_11:
            product = Product.objects.get(manual_slug = top_picks.slug_11)
            all_products.append(product)
        if  top_picks.slug_12:
            product = Product.objects.get(manual_slug = top_picks.slug_12)
            all_products.append(product)
        if top_picks.slug_13:
            product = Product.objects.get(manual_slug = top_picks.slug_13)
            all_products.append(product)
        if top_picks.slug_14:
            product = Product.objects.get(manual_slug = top_picks.slug_14)
            all_products.append(product)
        if top_picks.slug_15:
            product = Product.objects.get(manual_slug = top_picks.slug_15)
            all_products.append(product)
        if top_picks.slug_16:
            product = Product.objects.get(manual_slug = top_picks.slug_16)
            all_products.append(product)
        if top_picks.slug_17:
            product = Product.objects.get(manual_slug = top_picks.slug_17)
            all_products.append(product)
        if top_picks.slug_18:
            product = Product.objects.get(manual_slug = top_picks.slug_18)
            all_products.append(product)
        if top_picks.slug_19:
            product = Product.objects.get(manual_slug = top_picks.slug_19)
            all_products.append(product)
        if top_picks.slug_20:
            product = Product.objects.get(manual_slug = top_picks.slug_20)
            all_products.append(product)
    else:
        top_picks = ''

    if request.method == "POST":
        form = BestPackageForm(request.POST)
        if form.data['top_picks']:
             manual_slug = form.data['top_picks']
        print(form.errors)
        prod = form.save(commit = False)
        prod.save()
        form.save_m2m()
        messages.success(request,'Added !')
        return redirect('/toppicks/'+ str(manual_slug))

    

    context = {
        'top_picks':top_picks,
        'all_products':all_products,
        'form':form,
    }

    return render(request,'top-picks.html',context)


@csrf_exempt
def productEnqueryForm(request):
    product_slug = request.POST.get('product_slug')
    name = request.POST.get('name')
    number = request.POST.get('number')
    email = request.POST.get('email')
    date_of_travel = request.POST.get('date_of_travel')
    number_of_people = request.POST.get('number_of_people')
    message = request.POST.get('message')


    product_enquiry = ProductEnquiry(product_slug = product_slug,
    name = name,number = number , email = email , date_of_travel = date_of_travel,
    number_of_people = number_of_people,message = message)

    product_enquiry.save()

    return JsonResponse({'data': name + " your Enquiry successfully added in enquiry Box !"})




    #  ======================================== cource Entry form =====================================
@staff_member_required
def courseEntryForm(request):
    form = CourseEntryForm()
    if request.method == 'POST':
        form = CourseEntryForm(request.POST,request.FILES)
        print(form.errors)
        prod = form.save(commit = False)
        prod.save()
        form.save_m2m()
        messages.success(request,'Added !')
        return redirect('/')

    context = {
        'form':form,
    }
    return render(request,'courseentryform.html',context)


def course(request):
    return render(request,'course.html')

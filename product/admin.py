from django.contrib import admin
from .models import CityHotelData, ItineraryData, Product, Countries, StateItineraryData, states, Destination, Images, phone, Purchase, duration, Blogpost, wallet, Itinerary, Erp, Citie, promo, Affiliate, AdventureTourTypes, TravelGuide, Populartags,TopPicksEntryForm,BestPackage,ProductEnquiry,Course

admin.site.register(Product)
admin.site.register(Destination)
admin.site.register(Images)
admin.site.register(states)
admin.site.register(phone)
admin.site.register(Purchase)
admin.site.register(duration)
admin.site.register(Blogpost)
admin.site.register(wallet)
admin.site.register(Itinerary)
admin.site.register(Erp)
admin.site.register(Citie)
admin.site.register(promo)
admin.site.register(Affiliate)
admin.site.register(AdventureTourTypes)
admin.site.register(TravelGuide)
admin.site.register(Populartags)
admin.site.register(TopPicksEntryForm)
admin.site.register(BestPackage)
admin.site.register(ProductEnquiry)
admin.site.register(Course)
admin.site.register(StateItineraryData)
admin.site.register(CityHotelData)
admin.site.register(ItineraryData)
# Register your models here.

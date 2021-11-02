from django.contrib import admin
from .models import Cities, CityHotelData, ItineraryData, AffiliateWithdraw, LinkHits, PartialPayment, Product, Countries, State, StateItineraryData, states, Destination, Images, phone, Purchase, duration, Blogpost, wallet, Itinerary, Erp, Citie, promo, Affiliate, AdventureTourTypes, TravelGuide, Populartags, TopPicksEntryForm, BestPackage, ProductEnquiry, Course, Locality, Rentals, AffiliateUser, AffiliateEarning, AffiliateLink, Agent, AgentProductBooking, AgentWithdrawHistory, Testimonials, PartialPayment

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
admin.site.register(State)
admin.site.register(Cities)
admin.site.register(Locality)
admin.site.register(Rentals)
admin.site.register(Agent)
admin.site.register(AgentProductBooking)
admin.site.register(AgentWithdrawHistory)
admin.site.register(Testimonials)
admin.site.register(AffiliateUser)
admin.site.register(AffiliateEarning)
admin.site.register(AffiliateLink)
admin.site.register(LinkHits)
admin.site.register(AffiliateWithdraw)
admin.site.register(PartialPayment)
# Register your models here.


admin.site.site_header = "Universal Adventure Administration"
admin.site.site_title = "Universal Adventure admin site"
admin.site.index_title = "Universal Adventure Admin"

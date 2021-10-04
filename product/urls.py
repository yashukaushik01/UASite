from os import name
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<slug:slug>/', views.product, name='product'),
    path('destination/', views.destination, name='destination'),
    path('filter-data/', views.FilterData, name='filter-data'),
    path('handlerequest/', views.cash, name='cash'),
    path('handlerequestpartial/', views.cashpartial, name='cashpartial'),
    path('booking/', views.booking, name='booking'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout2/', views.checkout2, name='checkout2'),
    path('checkout3/', views.checkout3, name='checkout3'),
    path('add/', views.ProductCreate, name='productcreate'),
    path('itinerary/', views.AddItinerary, name='Itinerary'),
    path('travel-guide-form/', views.travelGuideEntryForm, name='AddPlaceToVisit'),
    path('add-popular-tag/', views.AddPopularTag, name='Addpopulartag'),
    path('productslist/', views.ProductsList, name='productslist'),
    path('erp/', views.AddErp, name='Erp'),
    path('erplist/', views.ErpList, name='erplist'),
    path('itinerarylist/', views.ItineraryList, name='itinerarylist'),

    path('state-itinerary-form/',views.stateItinerary , name="stateItineraryForm"),
    path('state-itinerary-list/',views.StateItineraryList,name="StateItineraryList"),
    path('get-state-itinerary/',views.GetStateItineraryData,name="GetStateItineraryData"),
    path('city-hotel-form/',views.cityHotel , name="cityHotel"),
    path('city-hotel-list/',views.CityHotelList , name="cityHotelList"),
    path('get-city-hotel/',views.GetCityHotelData , name="GetCityHotelData"),
    path('add-itinerary-form/',views.AddItineraryData , name="addItineraryForm"),
    path('getItineraryData/',views.getItineraryData , name="getItineraryData"),
    path('itinerary-data-edit/<slug:pk>',views.ItineraryDataEdit,name="ItineraryDataEdit"),
    path('itinerary-data/<slug:slug>',views.itineraryData,name="itinerary-data"),
    path('itinerary-data-list/',views.ItineraryDataList , name="ItineraryDataList"),
    path('get-itinerary-list-data/',views.GetItineraryListData , name="GetItineraryListData"),

    path('addblog/', views.BlogCreate, name='blogcreate'),
    path('profile/', views.profile, name='profile'),
    path('download/<slug:slug>/', views.download, name='download'),
    path('product/all/', views.more, name='more'),
    path('ajax_calls/search/', views.autocompleteModel, name='autocompleteModel'),
    path('search/', views.search, name='search'),
    path('autosuggest/', views.autosuggest, name='autosuggest'),
    path('admin_route/', views.adminr, name='admins'),
    path('tag/<slug:tag_slug>', views.Tagged, name='tagged_product'),
    path('update/<slug:slug>/', views.ProductUpdate, name='up'),
    path('delete/<slug:slug>/', views.DeleteImg, name='del'),
    path('privacy-policy/', views.Privacy, name='privacy'),
    path('adventure/<slug:slug>/', views.Adventure, name='adventure'),
    path('tour/<slug:slug>/', views.Tour, name='tour'),
    path('city/<slug:slug>/', views.City, name='city'),
    path('state/<slug:slug>/', views.State, name='state'),
    path('locality/<slug:slug>/', views.Locality, name='locality'),

    path('travel-guide/<slug:slug>/<slug:slug1>', views.travelGuide, name='travelguide'),
    path('travel-guide-list/', views.travelGuideList, name='travelGuideList'),
    path('travel-guide-data/', views.travelGuideData, name='travelGuideData'),
    path('travel-guide-edit/<slug:slug>/', views.travelGuideEdit, name='travelGuideEdit'),

    path('partial-payment/', views.Partial, name='partial-payment'),
    path('tour-payment/<slug:slug>', views.TourPayment, name='tourpayment'),
    path('refund-policy/', views.Refund, name='refund-policy'),
    path('blog/', views.blog, name="BlogHome"),
    path('walletpromo/', views.walletpromo, name="WalletPromo"),
    path('promocode/', views.promocode, name="Promocode"),

    path('affiliate/', views.affiliate, name="affiliate"),
    path('affiliate-add/', views.affiliateUser, name="affiliate-add"),
    path('affiliate-dashboard/', views.AffiliateDashbord, name="affiliate-dashboard"),
    path('affiliate-list/', views.affiliateList, name="affiliate-list"),
    path('affiliate-list-data/', views.affiliateListData, name="affiliate-list-data"),
    path('affiliate-user-status/<status>/<slug>', views.AffiliateUserStatus, name="affiliate-user-status"),

    path('about/', views.About, name="about"),
    path('contact/', views.Contact, name="contact"),
    path('blogpos/<slug:slug>', views.blogpost, name="BlogPost"),
    path('useritinerary/<slug:slug>', views.UserItierary, name="UserItierary"),
    url(r'^deleteproduct/(?P<pk>[0-9]+)/$',
        views.Deleteproduct, name='delete_view3'),
    url(r'^delete2/(?P<pk>[0-9]+)/$', views.Delete, name='delete_view'),
    url(r'^delete3/(?P<pk>[0-9]+)/$', views.Delete2, name='delete_view2'),
    path('edititinerary/<slug:slug>', views.EditItinerary, name='edit_itinerary'),
    path('editerp/<slug:slug>', views.EditErp, name='edit_erp'),
    path('itinerary_response/<slug:slug>',
         views.Response_Itinerary, name='Itinerary_response'),

    path('send-erp-mail/',views.SendErpMail,name='SendErpMail'),
    
    path('top-picks-entry-form/',views.topPicksEntryForm,name="toppicksentryform"),
    path('top-picks/<slug:slug>',views.topPicks,name="toppicks"),
    path('productEnquiry/',views.productEnqueryForm,name="product_enquiry"),
    # course 
    path('course-entry-form/',views.courseEntryForm,name="courceEntryForm"),
    path('course/',views.course,name="course"),
    path('state-city',views.StateCity,name="state-city"),


     # rentals-form
    path('rentals-form/', views.rentalsForm, name='rentals-form'),
    path('rentals-submit/', views.rentalsSubmit, name='rentals-submit'),
    path('rentals/<slug:slug>/', views.rentals, name='rentals'),
    path('filter-rentals/', views.FilterRentals, name='filter-rentals'),
    path('filter-rentals-brand/', views.FilterRentalsBrand,
         name='filter-rentals-brand'),
    path('rentals-booking', views.rentalsBooking, name='rentals-booking'),
]

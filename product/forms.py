from django import forms
from django.db.models import fields
from .models import Product, phone, Purchase, Blogpost, Itinerary, Erp, TravelGuide, Populartags,TopPicksEntryForm,BestPackage,ProductEnquiry,Course


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'manual_slug', 'tag_category', 'description', 'duration', 'sale_child', 'start_loc', 'map', 'highlights', 'city', 'adventurelevel', 'adventureloc', 'reviews', 'inclusion', 'order', 'child', 'cashback', 'ques1', 'ques2', 'ques3', 'ques4',
                  'ques5', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'additional_info', 'a_inclusion', 'overview', 'rating', 'regular', 'sale', 'category', 'days', 'location', 'state', 'country', 'duration_type', 'loca_city', 'adventuretype', 'discount',)


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'manual_slug', 'tag_category', 'description', 'duration', 'sale_child', 'start_loc', 'map', 'highlights', 'city', 'adventurelevel', 'adventureloc', 'reviews', 'inclusion', 'order', 'child', 'cashback', 'ques1', 'ques2', 'ques3', 'ques4',
                  'ques5', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'additional_info', 'a_inclusion', 'overview', 'rating', 'regular', 'sale', 'category', 'days', 'location', 'state', 'country', 'duration_type', 'loca_city', 'adventuretype', 'discount',)


class PopularTagForm(forms.ModelForm):
    class Meta:
        model = Populartags
        fields = ('name', 'link', 'tag')


class ErpForm(forms.ModelForm):
    class Meta:
        model = Erp
        fields = ('phone', 'name', 'email', 'package', 'start_date',
                  'total_cost', 'agent', 'agent_phone', 'reminder_date', 'booking_id',)


class UpdateErpForm(forms.ModelForm):
    class Meta:
        model = Erp
        fields = ('net', 'due', 'phone', 'name', 'email', 'package', 'start_date', 'total_cost', 'agent', 'agent_phone', 'reminder_date', 'booking_id', 'payment_client1', 'payment_date1', 'mop1', 'comment1',
                  'payment_client2', 'payment_date2', 'mop2', 'comment2', 'payment_client3', 'payment_date3', 'mop3', 'comment3', 'payment_client4', 'payment_date4', 'mop4', 'comment4',
                  'hotel_name1', 'hotel_contact1', 'hotel_phone1', 'hotel_cost1', 'hotel_comment1', 'hotel_name2', 'hotel_contact2', 'hotel_phone2', 'hotel_cost2', 'hotel_comment2',
                  'hotel_name3', 'hotel_contact3', 'hotel_phone3', 'hotel_cost3', 'hotel_comment3', 'payment1_hotel1', 'paymet1_date_hotel1', 'mop1_hotel1', 'comment1_hotel1', 'payment2_hotel1', 'paymet2_date_hotel1', 'mop2_hotel1', 'comment2_hotel1',
                  'payment3_hotel1', 'paymet3_date_hotel1', 'mop3_hotel1', 'comment3_hotel1', 'payment4_hotel1', 'paymet4_date_hotel1', 'mop4_hotel1', 'comment4_hotel1', 'dueh1', 'payment1_hotel2', 'paymet1_date_hotel2', 'mop1_hotel2', 'comment1_hotel2', 'payment2_hotel2', 'paymet2_date_hotel2', 'mop2_hotel2', 'comment2_hotel2',
                  'payment3_hotel2', 'paymet3_date_hotel2', 'mop3_hotel2', 'comment3_hotel2', 'payment4_hotel2', 'paymet4_date_hotel2', 'mop4_hotel2', 'comment4_hotel2', 'dueh2', 'payment1_hotel3', 'paymet1_date_hotel3', 'mop1_hotel3', 'comment1_hotel3', 'payment2_hotel3', 'paymet2_date_hotel3', 'mop2_hotel3', 'comment2_hotel3',
                  'payment3_hotel3', 'paymet3_date_hotel3', 'mop3_hotel3', 'comment3_hotel3', 'payment4_hotel3', 'paymet4_date_hotel3', 'mop4_hotel3', 'comment4_hotel3', 'dueh3',
                  'transport_name1', 'transport_contact1', 'transport_phone1', 'transport_cost1', 'transport_comment1', 'transport_name2', 'transport_contact2', 'transport_phone2', 'transport_cost2', 'transport_comment2',
                  'transport_name3', 'transport_contact3', 'transport_phone3', 'transport_cost3', 'transport_comment3', 'payment1_transport1', 'paymet1_date_transport1', 'mop1_transport1', 'comment1_transport1', 'payment2_transport1', 'paymet2_date_transport1', 'mop2_transport1', 'comment2_transport1',
                  'payment3_transport1', 'paymet3_date_transport1', 'mop3_transport1', 'comment3_transport1', 'payment4_transport1', 'paymet4_date_transport1', 'mop4_transport1', 'comment4_transport1', 'duet1', 'payment1_transport2', 'paymet1_date_transport2', 'mop1_transport2', 'comment1_transport2', 'payment2_transport2', 'paymet2_date_transport2', 'mop2_transport2', 'comment2_transport2',
                  'payment3_transport2', 'paymet3_date_transport2', 'mop3_transport2', 'comment3_transport2', 'payment4_transport2', 'paymet4_date_transport2', 'mop4_transport2', 'comment4_transport2', 'duet2', 'payment1_transport3', 'paymet1_date_transport3', 'mop1_transport3', 'comment1_transport3', 'payment2_transport3', 'paymet2_date_transport3', 'mop2_transport3', 'comment2_transport3',
                  'payment3_transport3', 'paymet3_date_transport3', 'mop3_transport3', 'comment3_transport3', 'payment4_transport3', 'paymet4_date_transport3', 'mop4_transport3', 'comment4_transport3', 'duet3',)


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ('phone', 'name', 'location', 'days', 'person', 'category', 'hotel_type', 'meal_type', 'vehicle', 'other_inclusion', 'start_loc', 'end_loc', 'days1', 'days2', 'days3', 'days4', 'days5', 'days6', 'days7', 'days8', 'days9', 'days10', 'days11', 'days12', 'textdays1', 'textdays2', 'textdays3', 'textdays4', 'textdays5', 'textdays6', 'textdays7', 'textdays8', 'textdays9', 'textdays10', 'textdays11', 'textdays12', 'hotel_location1',
                  'hotel_location2', 'hotel_location3', 'hotel_location4', 'hotel_nights1', 'hotel_nights2', 'hotel_nights3', 'hotel_nights4', 'hotel_rooms1',
                  'hotel_rooms2', 'hotel_rooms3', 'hotel_rooms4', 'meal_type1', 'meal_type2', 'meal_type3', 'meal_type4', 'hotel_name1', 'hotel_name2',
                  'hotel_name3', 'hotel_name4', 'payment', 'payment_type', 'payment2', 'agent', 'agent_phone',)


class TravelGuideEntryForm(forms.ModelForm):
    class Meta:
        model = TravelGuide
        fields = ('name', 'type', 'manual_slug', 'tag', 'heading','timestamp', 'summary', 'image', 'blog1', 'blog2', 'blog3', 'blog4', 'blog5', 'blog6', 'blog7', 'blog8', 'blog9',
                  'blog10', 'blog11', 'blog12', 'blog13', 'blog14', 'blog15')


class UpdateItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ('days', 'person', 'category', 'hotel_type', 'meal_type', 'vehicle', 'other_inclusion', 'start_loc', 'end_loc', 'days1', 'days2', 'days3', 'days4', 'days5', 'days6', 'days7', 'days8', 'days9', 'days10', 'days11', 'days12', 'textdays1', 'textdays2', 'textdays3', 'textdays4', 'textdays5', 'textdays6', 'textdays7', 'textdays8', 'textdays9', 'textdays10', 'textdays11', 'textdays12', 'hotel_location1',
                  'hotel_location2', 'hotel_location3', 'hotel_location4', 'hotel_nights1', 'hotel_nights2', 'hotel_nights3', 'hotel_nights4', 'hotel_rooms1',
                  'hotel_rooms2', 'hotel_rooms3', 'hotel_rooms4', 'meal_type1', 'meal_type2', 'meal_type3', 'meal_type4', 'hotel_name1', 'hotel_name2',
                  'hotel_name3', 'hotel_name4', 'payment', 'payment_type', 'payment2', 'agent', 'agent_phone',)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ('title', 'head0', 'chead0', 'head1', 'chead1',
                  'head2', 'chead2', 'pub_date', 'thumbnail',)


class Addphone(forms.ModelForm):
    class Meta:
        model = phone
        fields = ('phone',)


class purchaseform(forms.ModelForm):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Purchase
        fields = ('date',)

class Top_picks_entryForm(forms.ModelForm):
    class Meta:
        model =  TopPicksEntryForm
        fields = ('heading','cover_img','manual_slug','box1_text','box1_background','box1_url','box2_text','box2_background','box2_url','box3_text','box3_background','box3_url',
        'text5','text5_image','text_1','slug_1','text_2','slug_2','text_3','slug_3','text_4','slug_4','text_5','slug_5','text_6','slug_6','text_7','slug_7','text_8','slug_8',
        'text_9','slug_9','text_10','slug_10','text_11','slug_11','text_12','slug_12','text_13','slug_13','text_14','slug_14','text_15','slug_15','text_16','slug_16','text_7','slug_7',
        'text_18','slug_18','text_19','slug_19','text_20','slug_20',)

class BestPackageForm(forms.ModelForm):
    class Meta:
        model = BestPackage
        fields = ('top_picks','name','number','email','date_of_travel','number_of_people','message')


class ProductEnquiryForm(forms.ModelForm):
    class Meta:
        model = ProductEnquiry
        fields = ('product_slug','name','number','email','date_of_travel','number_of_people','message')


class CourseEntryForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('state','city','locality','course_name','course_category','course_duration','course_dur_type','course_level','popularity',
        'course_display_name','certification','trainer_detail','manual_slug','summary','achivement','course_details','inclusion',
        'after_course_next_step','regular_price','sale_price','cover_image','image2','image3','image4')



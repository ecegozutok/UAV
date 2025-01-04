from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-page/', views.create_page, name='create_page'),
    path('create_tail/', views.create_tail, name='create_tail'),
    path('create_wing/', views.create_wing, name='create_wing'),
    path('create_fuselage/', views.create_fuselage, name='create_fuselage'),
    path('create_avionics/', views.create_avionics, name='create_avionics'),
    path('create_aircraft/', views.create_aircraft, name='create_aircraft'),
    path('api/wing_counts/', views.wing_counts, name='wing_counts'),
    path('api/fuselage_counts/', views.fuselage_counts, name='fuselage_counts'),
    path('api/tail_counts/', views.tail_counts, name='tail_counts'),
    path('api/avionics_counts/', views.avionics_counts, name='avionics_counts'),
    path('api/wing_availability/', views.wing_availability, name='wing_availability'),
    path('api/wing_availability/<str:type_code>/', views.wing_availability,
         name='wing_availability_filtered'),
    path('api/fuselage_availability/', views.fuselage_availability, name='fuselage_availability'),
    path('api/fuselage_availability/<str:type_code>/', views.fuselage_availability,
         name='fuselage_availability_filtered'),

    path('api/tail_availability/', views.tail_availability, name='tail_availability'),
    path('api/tail_availability/<str:type_code>/', views.tail_availability, name='tail_availability_filtered'),

    path('api/avionics_availability/', views.avionics_availability, name='avionics_availability'),
    path('api/avionics_availability/<str:type_code>/', views.avionics_availability,
         name='avionics_availability_filtered'),

]
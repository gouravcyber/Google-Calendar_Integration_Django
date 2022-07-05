from . import views as core_views
from django.urls import path 

urlpatterns = [
    path('init/',core_views.GoogleCalendarInitView,name ='Auth Initialisation'),
    path('redirect/',core_views.GoogleCalendarRedirectView,name ="EventList"),
]
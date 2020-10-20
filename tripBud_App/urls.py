from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  #Displays Log-in/Registration
    path('reg', views.register),
    path('login', views.signIn),
    path('logout', views.signOut),
    path('travels', views.home),    #Displays homepage
    path('cancel/<tripId>', views.cancelPlans),
    path('delete/<tripId>', views.deletePlans),
    path('join/<tripId>', views.addOn),
    path('addtrip', views.create),
    path('creation', views.tripAdd),    #Displays Job addition
    path('view/<int:tripId>', views.showInfo)    #Shows Trip Info
]

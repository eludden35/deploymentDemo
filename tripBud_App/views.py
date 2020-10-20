from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# **************************************************************

# Displays welcome page for registration and login


def index(request):
    if 'loggedInUser' in request.session:
        return redirect('/travels')             # If user is logged in this -  
                                                # method will redirect to home page


    return render(request, 'index.html')

# ************************************************************

# This method processes registration form and logs user in

def register(request):

    isValid = User.objects.regiValidator(request.POST)
    print(isValid)
    if len(isValid) > 0:
        for key, value in isValid.items():
            messages.error(request, value)
        return redirect('/')
    
    
    newUser = User.objects.create(name= request.POST['name'], username= request.POST['uName'], password= request.POST['pwd'],)

    request.session['loggedInUser'] = newUser.id
    
    return redirect('/travels')

# ************************************************************

# This method logs user in and redirects to homepage

def signIn(request):
    
    isValid = User.objects.logInValid(request.POST)

    if len(isValid) > 0:
        for key, value in isValid.items():
            messages.error(request, value)
        return redirect('/')

    userMatch = User.objects.filter(username = request.POST['uName'])

    request.session['loggedInUser'] = userMatch[0].id

    return redirect('/travels')

# ************************************************************

# This method logs the user out and redirects to login/registration

def signOut(request):
			request.session.clear()
			return redirect("/")

# ************************************************************

# This method displays homepage with tables

def home(request):
    if 'loggedInUser' not in request.session:
        return redirect('/')


    loggedInUser = User.objects.get(id = request.session['loggedInUser'])
    usersPlans = Trip.objects.filter(join = loggedInUser)
    usersNotplanned = Trip.objects.exclude(join = loggedInUser)
    print(usersPlans)
    context = {
        'loggedIn': loggedInUser,
        'plans': usersPlans,
        'notPlans': usersNotplanned,
        # 'allWish': Wish.objects.all()
        
    }

    return render(request, 'homepage.html', context)

# ************************************************************

# This method adds travel plan to database with assigned one to many user connection

def addOn(request, tripId):


    joinTrip = Trip.objects.get(id= tripId).join.add(User.objects.get(id= request.session['loggedInUser']))
    
    # print(User.objects.get(id=loggedInUser))
    return redirect('/travels')

# ************************************************************

# This method adds travel plan to database with assigned one to many user connection

def create(request):


    return render(request, 'addTrip.html')

# ************************************************************

# This method processes form info from "Add a Trip" page; redirects to homepage

def tripAdd(request):

    isValid = Trip.objects.tripValidator(request.POST)

    if len(isValid) > 0:
        for key, value in isValid.items():
            messages.error(request, value)
        return redirect('/addtrip')
    
    loggedInUser = User.objects.get(id = request.session['loggedInUser'])

    newTrip = Trip.objects.create(dest= request.POST['dest'], desc= request.POST['desc'], travStart= request.POST['dtStart'], travEnd= request.POST['dtEnd'], plan= loggedInUser )
    newTripMany = Trip.objects.get(id=newTrip.id).join.add(User.objects.get(id= request.session['loggedInUser']))
    print(newTrip.id)
    return redirect('/travels')

# ************************************************************

# This method shows travel info and users that have joined trip

def showInfo(request, tripId):
    print('****************************************************************')
    print(Trip.objects.get(id = tripId).join.all())
    print('****************************************************************')
    context = {
        'tripJoin': Trip.objects.get(id = tripId).join.all(),
        'tripInfo': Trip.objects.get(id = tripId),
        'trip': Trip.objects.all()
    }

    return render(request, 'showTrip.html', context)

# ***************************************************************************************

# This method cancel's plan's

def cancelPlans(request, tripId):

    loggedInUser = User.objects.get(id = request.session['loggedInUser'])

    removeTrip = Trip.objects.get(id=tripId).join.remove(User.objects.get(id= request.session['loggedInUser']))

    return redirect('/')

# ***************************************************************************************

# This method deletes plans

def deletePlans(request, tripId):

    c=Trip.objects.get(id= tripId)
    c.delete()

    return redirect('/')
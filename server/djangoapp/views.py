from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_state_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request,'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request,'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/4f3dab5f-e011-4b95-b1dd-09ba787c1077/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealership_list = get_dealers_from_cf(url)
        context = dict()
        context["dealership_list"] = dealership_list
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealership):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/4f3dab5f-e011-4b95-b1dd-09ba787c1077/dealership-package/get-review.json"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealership)
        context = dict()
        context["reviews"] = reviews
        context["id"] = dealership
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.name for dealer in reviews])
        # Return a list of dealer short name
        # dealer_sentiments = ' '.join([dealer.sentiment for dealer in reviews])
        # dealer_reviews = ' '.join([dealer.review for dealer in reviews])
        # final_list = [*dealer_names, *dealer_sentiments, *dealer_reviews]
        # dealer_names += ' '.join([dealer.review for dealer in reviews])
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
# def add_review(request, dealer_id):
#     if(User.is_authenticated):
#         if request.method == "GET":
#             url = "https://au-syd.functions.appdomain.cloud/api/v1/web/4f3dab5f-e011-4b95-b1dd-09ba787c1077/dealership-package/get-review.json"
#         # Get reviews from the URL
#             reviews = get_dealer_reviews_from_cf(url, dealership)
#             context = dict()
#             context["reviews"] = reviews
#         # { "review": { "id": 1114, "name": "Upkar Lidder", 
#         # "dealership": 15, "review": "Great service!", "purchase": false, 
#         # "another": "field", 
#         # "purchase_date": "02/16/2021", 
#         # "car_make": "Audi", "car_model": "Car", 
#         # "car_year": 2021 } }
#         review = dict()
#         review["time"] = datetime.utcnow().isoformat()
#         review["dealership"] = dealer_id
#         review["review"] = "This is a great car dealer"
#         review["name"] = "Surin"
#         review["id"] = 115
#         json_payload = dict()
#         json_payload["review"] = review
#         url = "https://au-syd.functions.appdomain.cloud/api/v1/web/4f3dab5f-e011-4b95-b1dd-09ba787c1077/dealership-package/post-review"
#         result = post_request(url, json_payload, dealerId=dealer_id)

#         return render(request, 'djangoapp/add_review.html', context)
def add_review(request, id):
    context = {}
    dealer_url = "https://au-syd.functions.appdomain.cloud/api/v1/web/4f3dab5f-e011-4b95-b1dd-09ba787c1077/dealership-package/get-dealership.json"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    print(dealer)
    context["id"] = id
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            cars = request.POST["car"]
            print(cars)
            car = CarModel.objects.get(id=cars)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.carmake.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://au-syd.functions.appdomain.cloud/api/v1/web/4f3dab5f-e011-4b95-b1dd-09ba787c1077/dealership-package/post-review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", dealership=id)
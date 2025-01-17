from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

# from .models import related models
from .models import CarMake, CarModel
from .restapis import (
    get_dealers_from_cf,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    post_request,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, "djangoapp/contact.html")


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST["username"]
        password = request.POST["password"]
        # Try to check if provide credential can be authenticated
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect("djangoapp:index")
        else:
            # If not, return to login page again
            return render(request, "djangoapp/login.html", context)
    else:
        return render(request, "djangoapp/login.html", context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            pass
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)


def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/adcdf2ed-53dd-4e00-af0e-683561df3afe/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = dict()
        context["dealership_list"] = dealerships
        return render(request, "djangoapp/index.html", context)


def get_dealerships_(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id=None):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/adcdf2ed-53dd-4e00-af0e-683561df3afe/dealership-package/revew-get.json"
        # Get review from the URL
        reviews_response = get_dealer_reviews_from_cf(url, dealer_id)

        context = dict()
        context["reviews_response"] = reviews_response
        context["dealer_id"] = dealer_id
        return render(request, "djangoapp/dealer_details.html", context)


# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealer_id=None):
    context = dict()
    if request.method == "POST":
        review = dict()
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.user.username
        review["dealership"] = dealer_id
        review["review"] = review_data
        review["purchase"] = bool(purchase_data)

        car_id = request.POST.get("car")

        json_payload = dict()
        json_payload["review"] = {
            "review": request.POST.get("content"),
            "purchase": bool(request.POST.get("purchasecheck")),
        }

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/adcdf2ed-53dd-4e00-af0e-683561df3afe/dealership-package/add_review"

        add_review = post_request(url, json_payload)

        return render(request, "djangoapp/add_review.html", context)

    context["cars"] = CarModel.objects.all()
    context["dealer_id"] = dealer_id
    return render(request, "djangoapp/add_review.html", context)

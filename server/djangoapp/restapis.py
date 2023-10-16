import requests
import json

from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get("api_key")
    params = {key: value for key, value in kwargs.items() if key != "apikey"}
    try:
        if api_key:
            # Call get method of requests library with URL and parameters
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                params=params,
                auth=HTTPBasicAuth("apikey", api_key),
            )
        else:
            response = requests.get(
                url, headers={"Content-Type": "application/json"}, params=params
            )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"],
            )
            # dealer_obj = {}  # Borrar cuando se cree CarDealer
            results.append(dealer_obj)

    return results


def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip=dealer["zip"],
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId=None):
    results = []
    # Call get_request with a URL parameter
    if dealerId:
        json_result = get_request(url, dealerId=dealerId)
    else:
        json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["rows"]
        # For each dealer object
        for review in reviews:
            review = review["doc"]
            print(review)
            # Create a CarDealer object with values
            review_obj = DealerReview(
                dealership=review.get("dealership"),
                name=review.get("name"),
                purchase=review.get("purchase"),
                review=review.get("review"),
                purchase_date=review.get("purchase_date"),
                car_make=review.get("car_make"),
                car_model=review.get("car_model"),
                car_year=review.get("car_year"),
                sentiment=review.get("sentiment"),
                id=review.get("id"),
            )
            # review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    params = dict()
    api_key = ""
    response = requests.get(
        url,
        params=params,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth("apikey", api_key),
    )

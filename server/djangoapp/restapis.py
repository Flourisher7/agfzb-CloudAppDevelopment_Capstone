import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


# Create a `get_request` to make HTTP GET requests

def get_request(url, **kwargs):
    print(kwargs)
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # Call get method of requests library with URL and parameters
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
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
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    for key in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result[key]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealer_id):
    results = []

    json_result = get_request(url, id=dealer_id)
    for key in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result[key]
        # For each dealer object
        # for dealer in dealers:
        for i in range(len(dealers)):
            # Get its content in `doc` object
            dealer_doc = dealers[i]
            if dealer_doc["id"] == dealer_id:
                dealer_name = dealer_doc["short_name"]
                # Create a CarDealer object with values in `doc` object

                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                       full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], zip=dealer_doc["zip"])
                print("***************************************************************")

                print(dealer_obj)
                return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_reviews_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    
    for key in json_result:
        # Get the row list in JSON as dealers
        reviews = json_result[key]
        # For each dealer object
        
        # for dealer in dealers:
        for i in range(len(reviews)):
            # Get its content in `doc` object
            dealer_review = reviews[i]
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(dealer_review["doc"])
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

            if dealer_review["doc"]["dealership"] == id:
                sentiment = analyze_review_sentiments(dealer_review["doc"]["review"])
                review_obj = DealerReview(dealership=dealer_review["doc"]["dealership"],
                                          name=dealer_review["doc"]["name"],
                                          purchase=dealer_review["doc"]["purchase"],
                                          review=dealer_review["doc"]["review"], purchase_date=dealer_review["doc"]["purchase_date"],
                                          car_make=dealer_review["doc"]["car_make"], car_model=dealer_review["doc"]["car_model"],
                                          car_year=dealer_review["doc"]["car_year"], 
                                          sentiment=sentiment, id=dealer_review["doc"]["id"])
                
                print(sentiment)
                results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/239e90eb-c172-4166-b142-8731703dc31c"
    api_key = "Lz3vQ4-V54MHZui-C0hKEsTJoq36-pvUGVUko-1XlhiF"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)

# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


def get_cars(request):
    count = CarMake.objects.count()
    if (count == 0):
        init_car_models()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarMake": car_model.car_make.name,
            "CarModel": car_model.name
        })
    return JsonResponse({"CarModels": cars})


def init_car_models():
    # Seed some data if empty
    toyota = CarMake.objects.create(
        name="Toyota", description="Toyota makes great cars"
    )
    honda = CarMake.objects.create(
        name="Honda", description="Honda makes great cars"
    )
    CarModel.objects.create(
        name="Camry", car_make=toyota, type="Sedan", year=2023
    )
    CarModel.objects.create(
        name="Corolla", car_make=toyota, type="Sedan", year=2023
    )
    CarModel.objects.create(
        name="Civic", car_make=honda, type="Sedan", year=2023
    )
    CarModel.objects.create(
        name="CR-V", car_make=honda, type="SUV", year=2023
    )


@csrf_exempt
# NOTE: @csrf_exempt is used here because this is a JSON API consumed by the
# React SPA.  To properly protect this endpoint in production, configure the
# frontend to send the Django CSRF token in the X-CSRFToken request header and
# remove this decorator.
def login_user(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    username = data.get('userName', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)


def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
# NOTE: @csrf_exempt is used here because this is a JSON API consumed by the
# React SPA.  To properly protect this endpoint in production, configure the
# frontend to send the Django CSRF token in the X-CSRFToken request header and
# remove this decorator.
def registration(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    username = data.get('userName', '').strip()
    password = data.get('password', '')
    first_name = data.get('firstName', '').strip()
    last_name = data.get('lastName', '').strip()
    email = data.get('email', '').strip()
    if not username or not password or not email:
        return JsonResponse(
            {"error": "Username, password, and email are required"}, status=400
        )
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def get_dealerships(request, state="All"):
    if (state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if (dealer_id):
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        if reviews is not None:
            for review_detail in reviews:
                try:
                    response = analyze_review_sentiments(
                        review_detail['review']
                    )
                    if response and 'sentiment' in response:
                        review_detail['sentiment'] = response['sentiment']
                    else:
                        review_detail['sentiment'] = "neutral"
                except Exception:
                    review_detail['sentiment'] = "neutral"
        else:
            reviews = []
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if (dealer_id):
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
# NOTE: @csrf_exempt is used here because this is a JSON API consumed by the
# React SPA.  Authentication is enforced below. To fully protect this endpoint
# in production, configure the frontend to send the Django CSRF token in the
# X-CSRFToken request header and remove this decorator.
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"status": 400, "message": "Invalid JSON"})
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception:
        return JsonResponse({
            "status": 500,
            "message": "Error in posting review"
        })

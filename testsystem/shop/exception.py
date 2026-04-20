from functools import wraps
import stripe
from .models import Item
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


def exception_stripe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except stripe.error.CardError as e:
        # A declined card error
            print('Status: %s' % e.http_status)
            print('Code: %s' % e.code)
            if e.param:
                print('Param: %s' % e.param)
            print('Message: %s' % e.user_message)
            print('Request ID: %s' % e.request_id)
            raise
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            print('Request ID: %s' % e.request_id)
            raise

        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            print('Message: %s' % e.user_message)
            if e.param:
                print('Param: %s' % e.param)
                print('Request ID: %s' % e.request_id)
            raise

        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
            print('Request ID: %s' % e.request_id)
            raise

        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            print('Request ID: %s' % e.request_id)
            raise

        except stripe.error.StripeError as e:
        # All other Stripe errors
            print('Status: %s' % e.http_status)
            print('Code: %s' % e.code)
            print('Message: %s' % e.user_message)
            print('Request ID: %s' % e.request_id)
            raise

        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            pass
            raise

    return wrapper
    
def not_found_item(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Item.DoesNotExist:
            return HttpResponseNotFound("Продукт не найден")
    return wrapper
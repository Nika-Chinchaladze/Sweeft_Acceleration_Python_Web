from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Sum
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from datetime import date
from uuid import uuid4

from .models import Client, Link
from .my_date import date_difference

# Create your views here.

MAIN_DOMAIN = "http://127.0.0.1:8000/"

# ======================================= REQUESTS SECTION ======================================= #


@api_view(["GET"])
def index(request):
    """returns welcome message with some extra necessary information."""
    if request.method == "GET":
        return JsonResponse({
            "How To Use": {
                "Data Restrictions": {
                    "is_premium": "True or False"
                },
                "What Data must be provided - JSON Format": {
                    "client_name": "Tommy Shelby",
                    "is_premium": "True",
                    "original_link": "https://www.youtube.com/watch?v=4NF_27ZRWCk"
                },
                "What Result should expect": {
                    "Client_name": "Tommy Shelby",
                    "is_premium_client": "True",
                    "Original_link": "https://www.youtube.com/watch?v=4NF_27ZRWCk",
                    "Shortened_link": "http://127.0.0.1:5000/Tommy-Shelby"
                }

            }
        })


@api_view(["POST"])
def add_link(request):
    """
        1. Adds new link into database and returns shortened link.
        2. Type of shortened link is determined by Client Type: is or not premium client.
        3. Executes different type of Validations.
    """
    if request.method == "POST":
        json_data = JSONParser().parse(request)

        user_name = json_data["client_name"].rstrip()
        formatted_user_name = user_name.replace(" ", "-")
        provided_data = {
            "client_name": formatted_user_name,
            "is_premium": json_data["is_premium"].rstrip(),
            "original_link": json_data["original_link"].rstrip()
        }

        # check if provided link is valid
        if provided_data["original_link"][:4] != "http":
            return JsonResponse({
                "error": {
                    "Message": "Please Provide Only Valid Urls!",
                    "Good-Example": "https://www.youtube.com/",
                    "Bad-Example": "www.youtube.com"
                }
            })

        # check if length of the provided link is acceptable
        if len(provided_data["original_link"]) > 250:
            return JsonResponse({
                "error": {
                    "Message": "Length of Provided Link must contain less than - 250 characters!"
                }
            })

        # check is_premium data is valid:
        if provided_data["is_premium"].capitalize() not in ["True", "False"]:
            return JsonResponse({
                "error": {
                    "Message": "Please Provide Correct Values For - is_premium field: True or False Only!"
                }
            })

        current_client = Client.objects.filter(
            client_name=provided_data["client_name"]).first()

        # when client with provided name exists
        if current_client is not None:
            current_client_data = Link.objects.filter(
                client=current_client).all()
            links_list = [item.original_link for item in current_client_data]

            # when client already has provided link in his personal data list
            if provided_data["original_link"] in links_list:
                desired_link = Link.objects.filter(
                    client=current_client,
                    original_link=provided_data["original_link"]
                ).first()
                return JsonResponse({
                    "Data": {
                        "Client_name": current_client.client_name,
                        "is_premium_client": current_client.is_premium_client,
                        "Original_link": desired_link.original_link,
                        "Shortened_link": desired_link.shortened_link
                    }
                })

            # when client does not have provided link - so it must be added
            else:
                # when existing client is premium user:
                if current_client.is_premium_client:
                    defined_shorten_link = f"{MAIN_DOMAIN}{str(uuid4())[:5]}-{current_client.client_name}"
                    new_link = Link(
                        original_link=provided_data["original_link"],
                        shortened_link=defined_shorten_link,
                        creation_date=date.today(),
                        access_counter=0,
                        client_id=current_client.id
                    )
                # when existing client is common user:
                else:
                    defined_shorten_link = f"{MAIN_DOMAIN}{str(uuid4())[:10]}"
                    new_link = Link(
                        original_link=provided_data["original_link"],
                        shortened_link=defined_shorten_link,
                        creation_date=date.today(),
                        access_counter=0,
                        client_id=current_client.id
                    )
                new_link.save()

                desired_link = Link.objects.filter(
                    shortened_link=defined_shorten_link).first()
                return JsonResponse({
                    "Data": {
                        "Client_name": current_client.client_name,
                        "is_premium_client": current_client.is_premium_client,
                        "Original_link": desired_link.original_link,
                        "Shortened_link": desired_link.shortened_link
                    }
                })

        # when client with provided name does not exist
        else:
            client_type = provided_data["is_premium"].capitalize()
            if client_type == "True":
                final_type = True
            else:
                final_type = False

            new_client = Client(
                client_name=provided_data["client_name"],
                is_premium_client=final_type
            )
            new_client.save()

            my_client = Client.objects.filter(
                client_name=provided_data["client_name"]).first()

            # when registered client is premium user:
            if my_client.is_premium_client:
                new_link = Link(
                    original_link=provided_data["original_link"],
                    shortened_link=f"{MAIN_DOMAIN}{my_client.client_name}",
                    creation_date=date.today(),
                    access_counter=0,
                    client_id=my_client.id
                )
            # when registered client is common user:
            else:
                new_link = Link(
                    original_link=provided_data["original_link"],
                    shortened_link=f"{MAIN_DOMAIN}{str(uuid4())[:10]}",
                    creation_date=date.today(),
                    access_counter=0,
                    client_id=my_client.id
                )
            new_link.save()

            my_link = Link.objects.filter(client=my_client).first()

            return JsonResponse({
                "success": {
                    "Data": {
                        "Client_name": my_client.client_name,
                        "is_premium_client": my_client.is_premium_client,
                        "Original_link": my_link.original_link,
                        "Shortened_link": my_link.shortened_link
                    }
                }
            })


@api_view(["GET"])
def redirect_website(request, new_link):
    """
        1. Based on unique shortened link - query will return original link and redirects to it.
        2. During every execution - special query will check for old links and delete them from database.
    """
    chosen_link = Link.objects.filter(
        shortened_link=f"{MAIN_DOMAIN}{new_link}").first()
    if chosen_link is not None:
        chosen_link.access_counter += 1
        redirect_url = chosen_link.original_link
        chosen_link.save()

        # deletion of urls older than 30 days
        all_links = Link.objects.all()
        current_date = f"{date.today()}"
        for item in all_links:
            difference = date_difference(current_date, item.creation_date)
            if difference > 30:
                item.delete()
            else:
                pass

        return redirect(redirect_url)

    else:
        return JsonResponse({
            "error": {
                "Message": "URL was not found"
            }
        })


# ======== Extra Feature => Return Grouped Data -> Accessed Quantity: in General and through each Client =========== #
@api_view(["GET"])
def grouped_data_in_general(request):
    """returns list of original links with accessed quantity"""
    my_data = Link.objects.all().values("original_link").annotate(
        total=Sum("access_counter")).order_by("total")
    my_dictionary = {item["original_link"]: item["total"] for item in my_data}

    return JsonResponse({
        "URL Access Quantity in General": my_dictionary
    })


@api_view(["GET"])
def grouped_data_each_client(request):
    """returns original link along with provider - client name and accessed quantity"""
    my_data = Link.objects.all()
    my_dictionary = {}
    i = 1
    for item in my_data:
        my_dictionary[i] = {
            "client_name": item.client.client_name,
            "original_link": item.original_link,
            "access_counter": item.access_counter
        }
        i += 1

    return JsonResponse({
        "success": my_dictionary
    })


# django super-user username: chincho
# password: Contact12@

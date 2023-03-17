from fastapi import FastAPI, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from uuid import uuid4

from .base import NewLink
from .models import Client, LinkModel, Base
from .database import SessionLocal, engine
from .my_date import date_difference

Base.metadata.create_all(bind=engine)
MAIN_DOMAIN = "http://127.0.0.1:8000/"

app = FastAPI()


# ==================================== DEPENDENCY ======================================= #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================================== REQUESTS SECTION =================================== #
@app.get("/")
def index():
    """returns welcome message with some extra necessary information."""
    return {
        "Message": {
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
        }
    }


@app.post("/link", status_code=status.HTTP_201_CREATED)
def add_link(tool: NewLink, db: Session = Depends(get_db)):
    """
        1. Adds new link into database and returns shortened link.
        2. Type of shortened link is determined by Client Type: is or not premium client.
        3. Executes different type of Validations.
    """
    user_name = tool.client_name.rstrip()
    formatted_user_name = user_name.replace(" ", "-")
    provided_data = {
        "client_name": formatted_user_name,
        "is_premium": tool.is_premium.rstrip(),
        "original_link": tool.original_link.rstrip()
    }

    # check if provided link is valid
    if provided_data["original_link"][:4] != "http":
        return {
            "error": {
                "Message": "Please Provide Only Valid Urls!",
                "Good-Example": "https://www.youtube.com/",
                "Bad-Example": "www.youtube.com"
            }
        }
    
    # check if length of the provided link is acceptable
    if len(provided_data["original_link"]) > 250:
        return {
            "error": {
                "Message": "Length of Provided Link must contain less than - 250 characters!"
            }
        }

    # check is_premium data is valid:
    if provided_data["is_premium"].capitalize() not in ["True", "False"]:
        return {
            "error": {
                "Message": "Please Provide Correct Values For - is_premium field: True or False Only!"
            }
        }

    current_client = db.query(Client).filter_by(client_name=provided_data["client_name"]).first()

    # when client with provided name exists
    if current_client is not None:
        current_client_data = db.query(LinkModel).filter_by(client_id=current_client.id).all()
        links_list = [item.original_link for item in current_client_data]

        # when client already has provided link in his personal data list
        if provided_data["original_link"] in links_list:
            desired_link = db.query(LinkModel).filter(
                (LinkModel.client_id == current_client.id) &
                (LinkModel.original_link == provided_data["original_link"])
            ).first()
            return {
                "success": {
                    "Data": {
                        "Client_name": current_client.client_name,
                        "is_premium_client": current_client.is_premium_client,
                        "Original_link": desired_link.original_link,
                        "Shortened_link": desired_link.shortened_link
                    }
                }
            }
        
        # when client does not have provided link - so it must be added
        else:
            # when existing client is premium user:
            if current_client.is_premium_client:
                defined_shorten_link = f"{MAIN_DOMAIN}{str(uuid4())[:5]}-{current_client.client_name}"
                new_link = LinkModel(
                    original_link=provided_data["original_link"],
                    shortened_link=defined_shorten_link,
                    creation_date=date.today(),
                    access_counter=0,
                    client_id=current_client.id
                )
            # when existing client is common user:
            else:
                defined_shorten_link = f"{MAIN_DOMAIN}{str(uuid4())[:10]}"
                new_link = LinkModel(
                    original_link=provided_data["original_link"],
                    shortened_link=defined_shorten_link,
                    creation_date=date.today(),
                    access_counter=0,
                    client_id=current_client.id
                )
                
            db.add(new_link)
            db.commit()

            desired_link = db.query(LinkModel).filter_by(shortened_link=defined_shorten_link).first()
            return {
                "success": {
                    "Data": {
                        "Client_name": current_client.client_name,
                        "is_premium_client": current_client.is_premium_client,
                        "Original_link": desired_link.original_link,
                        "Shortened_link": desired_link.shortened_link
                    }
                }
            }
    
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
        db.add(new_client)
        db.commit()

        my_client = db.query(Client).filter_by(client_name=provided_data["client_name"]).first()

        # when registered client is premium user:
        if my_client.is_premium_client:
            new_link = LinkModel(
                original_link=provided_data["original_link"],
                shortened_link=f"{MAIN_DOMAIN}{my_client.client_name}",
                creation_date=date.today(),
                access_counter=0,
                client_id=my_client.id
            )
        # when registered client is common user:
        else:
            new_link = LinkModel(
                original_link=provided_data["original_link"],
                shortened_link=f"{MAIN_DOMAIN}{str(uuid4())[:10]}",
                creation_date=date.today(),
                access_counter=0,
                client_id=my_client.id
            )
        db.add(new_link)
        db.commit()

        my_link = db.query(LinkModel).filter_by(client_id=my_client.id).first()

        return {
            "success": {
                "Data": {
                    "Client_name": my_client.client_name,
                    "is_premium_client": my_client.is_premium_client,
                    "Original_link": my_link.original_link,
                    "Shortened_link": my_link.shortened_link
                }
            }
        }


@app.get("/{new_link}")
def redirect_website(new_link: str, db: Session = Depends(get_db)):
    """
        1. Based on unique shortened link - query will return original link and redirects to it.
        2. During every execution - special query will check for old links and delete them from database.
    """
    chosen_link = db.query(LinkModel).filter_by(shortened_link=f"{MAIN_DOMAIN}{new_link}").first()
    if chosen_link is not None:
        chosen_link.access_counter += 1
        redirect_url = str(chosen_link.original_link)
        db.commit()

        # deletion of urls older than 30 days
        all_links = db.query(LinkModel).all()
        current_date = f"{date.today()}"
        for item in all_links:
            difference = date_difference(current_date, item.creation_date)
            if difference > 30:
                db.delete(item)
                db.commit()
            else:
                pass
        return RedirectResponse(redirect_url)
    
    else:
        return {
            "error": {
                "Message": "URL was not found"
            }
        }

 
# ======== Extra Feature => Return Grouped Data -> Accessed Quantity: in General and through each Client =========== #
@app.get("/grouped-data/in-general")
def grouped_data_in_general(db: Session = Depends(get_db)):
    """returns list of original links with accessed quantity"""
    my_data = db.query(LinkModel.original_link, func.sum(LinkModel.access_counter)).group_by(LinkModel.original_link).all()
    my_dictionary = {i: j for i, j in my_data}
    return {
        "URL Access Quantity in General": my_dictionary
    }


@app.get("/grouped-data/each-client")
def grouped_data_each_client(db: Session = Depends(get_db)):
    """returns original link along with provider - client name and accessed quantity"""
    my_data = db.query(Client, LinkModel).filter(Client.id == LinkModel.client_id).all()
    my_dictionary = {}
    i = 1
    for user, info in my_data:
        my_dictionary[i] = {
            "client_name": user.client_name,
            "original_link": info.original_link,
            "access_counter": info.access_counter
        }
        i += 1

    return {
        "success": my_dictionary
    }

from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import date
from my_date import date_difference
from sqlalchemy import func

MAIN_DOMAIN = "http://127.0.0.1:5000/"

app = Flask(__name__)

# ============================= PREPARE SQL DATABASE ============================= #
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shorten.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(100), unique=True, nullable=False)
    is_premium_client = db.Column(db.Boolean)
    links = db.relationship("Link", backref="client", lazy=True)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_link = db.Column(db.String(250), nullable=False)
    shortened_link = db.Column(db.String(100), unique=True, nullable=False)
    creation_date = db.Column(db.String(100), nullable=False)
    access_counter = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id", ondelete="CASCADE"), nullable=False)


# ================================ REQUESTS SECTION =============================== #
@app.route("/")
def index():
    """returns welcome message with some extra necessary information."""
    return jsonify(
        URL_SHORTENER_REST_API={
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
    )


@app.route("/link", methods=["POST"])
def add_link():
    """
        1. Adds new link into database and returns shortened link.
        2. Type of shortened link is determined by Client Type: is or not premium client.
        3. Executes different type of Validations.
    """
    user_name = request.json["client_name"].rstrip()
    formatted_user_name = user_name.replace(" ", "-")
    provided_data = {
        "client_name": formatted_user_name,
        "is_premium": request.json["is_premium"].rstrip(),
        "original_link": request.json["original_link"].rstrip()
    }

    # check if provided link is valid
    if provided_data["original_link"][:4] != "http":
        return jsonify(
            error={
                "Message": "Please Provide Only Valid Urls!",
                "Good-Example": "https://www.youtube.com/",
                "Bad-Example": "www.youtube.com"
            }
        )

    # check if length of the provided link is acceptable
    if len(provided_data["original_link"]) > 250:
        return jsonify(
            error={
                "Message": "Length of Provided Link must contain less than - 250 characters!"
            }
        )

    # check is_premium data is valid:
    if provided_data["is_premium"].capitalize() not in ["True", "False"]:
        return jsonify(
            error={
                "Message": "Please Provide Correct Values For - is_premium field: True or False Only!"
            }
        )

    current_client = db.session.query(Client).filter_by(client_name=provided_data["client_name"]).first()

    # when client with provided name exists
    if current_client is not None:
        current_client_data = db.session.query(Link).filter_by(client_id=current_client.id).all()
        links_list = [item.original_link for item in current_client_data]

        # when client already has provided link in his personal data list - DONE
        if provided_data["original_link"] in links_list:
            desired_link = db.session.query(Link).filter(
                (Link.client_id == current_client.id) &
                (Link.original_link == provided_data["original_link"])
            ).first()
            return jsonify(
                success={
                    "Data": {
                        "Client_name": current_client.client_name,
                        "is_premium_client": current_client.is_premium_client,
                        "Original_link": desired_link.original_link,
                        "Shortened_link": desired_link.shortened_link
                    }
                }
            )

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
            db.session.add(new_link)
            db.session.commit()

            desired_link = db.session.query(Link).filter_by(shortened_link=defined_shorten_link).first()
            return jsonify(
                success={
                    "Data": {
                        "Client_name": current_client.client_name,
                        "is_premium_client": current_client.is_premium_client,
                        "Original_link": desired_link.original_link,
                        "Shortened_link": desired_link.shortened_link
                    }
                }
            )

    # when client with provided name does not exist - DONE
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
        db.session.add(new_client)
        db.session.commit()

        my_client = db.session.query(Client).filter_by(client_name=provided_data["client_name"]).first()

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
        db.session.add(new_link)
        db.session.commit()

        my_link = db.session.query(Link).filter_by(client_id=my_client.id).first()

        return jsonify(
            success={
                "Data": {
                    "Client_name": my_client.client_name,
                    "is_premium_client": my_client.is_premium_client,
                    "Original_link": my_link.original_link,
                    "Shortened_link": my_link.shortened_link
                }
            }
        )


@app.route("/<string:new_link>", methods=["GET"])
def redirect_website(new_link):
    """
        1. Based on unique shortened link - query will return original link and redirects to it.
        2. During every execution - special query will check for old links and delete them from database.
    """
    chosen_link = db.session.query(Link).filter_by(shortened_link=f"{MAIN_DOMAIN}{new_link}").first()
    if chosen_link is not None:
        chosen_link.access_counter += 1
        redirect_url = str(chosen_link.original_link)
        db.session.commit()

        # deletion of urls older than 30 days
        all_links = db.session.query(Link).all()
        current_date = f"{date.today()}"
        for item in all_links:
            difference = date_difference(current_date, item.creation_date)
            if difference > 30:
                db.session.delete(item)
                db.session.commit()
            else:
                pass
        return redirect(redirect_url)

    else:
        return jsonify(
            error={
                "Message": "URL was not found"
            }
        )


# ======== Extra Feature => Return Grouped Data -> Accessed Quantity: in General and through each Client =========== #
@app.route("/grouped-data/in-general", methods=["GET"])
def grouped_data_in_general():
    """returns list of original links with accessed quantity"""
    my_data = db.session.query(Link.original_link, func.sum(Link.access_counter)).group_by(Link.original_link).all()
    my_dictionary = {i: j for i, j in my_data}
    return {
        "URL Access Quantity in General": my_dictionary
    }


@app.route("/grouped-data/each-client", methods=["GET"])
def grouped_data_each_client():
    """returns original link along with provider - client name and accessed quantity"""
    my_data = db.session.query(Client, Link).filter(Client.id == Link.client_id).all()
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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

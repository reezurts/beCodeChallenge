from flask import Flask, request
import random
import requests
import json
import pyrebase
import base64
#import firebase_admin

from PIL import Image
from io import BytesIO


app = Flask(__name__)

config = {
    "apiKey": "AIzaSyDMD-wjaa4Ea-fH8Q5Z_9tQkUW1O2lx1ec",
    "authDomain": "disco-sky-153015.firebaseapp.com",
    "databaseURL": "https://disco-sky-153015.firebaseio.com",
    "projectId": "disco-sky-153015",
    "storageBucket": "disco-sky-153015.appspot.com",
    "messagingSenderId": "181295702557",
    "appId": "1:181295702557:web:0fea4b55edebb16b581cf4",
    "measurementId": "G-RW8ZQFSGJ7",
}


@app.route("/")
def home():
    return "Hello World"


@app.route("/user/<firstname>/<lastname>")
def user(firstname, lastname):
    return f"Hello {firstname} {lastname}!"


@app.route("/status/")
def status():
    return f"Alive!"


@app.route(
    "/predict/<seller_avaible>/<month>/<customer_visiting_website>", methods=["GET"]
)
def predict(seller_avaible, month, customer_visiting_website):
    """
    DOCSTRING Predict
    """
    return f"""<h1>seller_avaible {seller_avaible}
                  month {month}
                  customer_visiting_website {customer_visiting_website}
                  Random prediction {random.randint(2000,5000)}
            </h1>"""


@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    DOCSTRING Login
    """
    if (
        request.method == "POST"
    ):  # this block is only entered when the form is submitted
        user = request.form.get("user")
        password = request.form["password"]
        length_pwd = str(len(password))

        try:
            response = auth_fb.sign_in_with_email_and_password(user, password)
            print(response)
            print("signed in")

        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)["error"]["message"]
            print(error)
            if error == "EMAIL_NOT_FOUND":
                auth_fb.create_user_with_email_and_password(user, password)
                return """user created"""
            elif error == "INVALID_PASSWORD":
                auth_fb.send_password_reset_email(user)
                return """sending verification mail"""

        return """user signed in"""

    return """<form method="POST">
                    User: <input type="text" name="user"><br>
                    Password: <input type="text" name="password"><br>
                    <input type="submit" value="Submit"><br>
                </form>"""


@app.route("/delete/", methods=["GET", "POST"])
def delete():
    """
    DOCSTRING Delete NOT WORKING :(:(:(
    """
    if (
        request.method == "POST"
    ):  # this block is only entered when the form is submitted
        user = request.form.get("user")
        password = request.form["password"]
        length_pwd = str(len(password))

        try:
            response = auth_fb.sign_in_with_email_and_password(user, password)
            print(response)
            print("signed in")
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)["error"]["message"]
            print(error)
            if error == "EMAIL_NOT_FOUND":
                auth_fb.create_user_with_email_and_password(user, password)
                return """user created"""
            elif error == "INVALID_PASSWORD":
                auth_fb.send_password_reset_email(user)
                return """sending verification mail"""
        else:
            response_delete = requests.post('https://firebase.googleapis.com/identitytoolkit/v0/b/disco-sky-153015.firebaseapp.com/deleteAccount', json={'localId': '7iAIY7bDRbNZJfEO5BPn01idiwk2'})

            print("Status code: ", response_delete.status_code)
            print("Printing Entire Post Request")
            print(response_delete.json())

            return """user deleted"""

    return """<form method="POST">
                    User: <input type="text" name="user"><br>
                    Password: <input type="text" name="password"><br>
                    <input type="submit" value="Delete"><br>
                </form>"""

@app.route("/saveimage/", methods=["GET", "POST"])
def saveimage():
    """
    DOCSTRING Login
    """
    if (
        request.method == "POST"
            ):

        url_img = request.form.get("url_img")
        name_img = request.form.get("name_img")
        response = requests.get(url_img)
        img = Image.open(BytesIO(response.content))
        img_base64 = base64.b64encode(img.tobytes())
        print(img_base64)

        child_token = storage.child(name_img).put(response)#, user['idToken'])
        print(child_token)
        store_url = storage.child(name_img).get_url('')

        return f"""image saved in {store_url}"""

    return """<form method="POST">
                    Image URL: <input type="text" name="url_img"><br>
                    Image Name: <input type="text" name="name_img"><br>
                    <input type="submit" value="Submit"><br>
                </form>"""

if __name__ == "__main__":
    firebase = pyrebase.initialize_app(config)
    auth_fb = firebase.auth()
    db = firebase.database()
    storage = firebase.storage()
    #app.run()
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, host='0.0.0.0', port=8123)

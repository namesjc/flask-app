import os
from datetime import datetime
from app import app
from flask import render_template, request, redirect, jsonify, make_response, session, url_for, flash
from werkzeug.utils import secure_filename


users = {
    "julian": {
        "username": "julian",
        "email": "julian@gmail.com",
        "password": "example",
        "bio": "Some guy from the internet"
    },
    "clarissa": {
        "username": "clarissa",
        "email": "clarissa@icloud.com",
        "password": "sweetpotato22",
        "bio": "Sweet potato is life"
    }
}


app.config["IMAGE_UPLOADS"] = "/mnt/c/Users/cje5szh/Documents/project/flask-app/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"


def allowed_image(filename):

    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/about')
def about():
    return 'About Page'


@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")

        if username not in users:
            print("Username not found")
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user["password"]:
            print("Incorrect password")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            print("session username set")
            return redirect(url_for("profile"))

    return render_template("public/sign_in.html")


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        if not len(password) >= 10:
            flash("Password length must be at least 10 characters", "warning")
            return redirect(request.url)
        flash("Account created!", "success")
        return redirect(request.url)
    return render_template("public/sign_up.html")


@app.route("/sign-out")
def sign_out():

    session.pop("USERNAME", None)

    return redirect(url_for("sign_in"))


@app.route("/profile")
def profile():

    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/profile.html", user=user)
    else:
        print("No username found in session")
        return redirect(url_for("sign_in"))


@app.route('/json', methods=["POST"])
def json_example():
    if request.is_json:
        req = request.get_json()
        print(req)
        response_body = {
            'message': 'JSON reveived!',
            'sender': req.get('name')
        }
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({'message': 'Request body must be JSON'}), 400)


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res

# http://127.0.0.1:5000/query?foo=foo&bar=bar&baz=baz&title=query+strings+with+flask


@app.route("/query")
def query():
    if request.args:

        # We have our query string nicely serialized as a Python dictionary
        args = request.args

        # We'll create a string to display the parameters & values
        serialized = ", ".join(f"{k}: {v}" for k, v in request.args.items())

        # Display the query string to the client in a different format
        return f"(Query) {serialized}", 200

    else:

        return "No query string received", 200


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                    print("Image saved")

                    return redirect(request.url)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    return render_template("public/upload_image.html")


@app.route("/cookies")
def cookies():

    resp = make_response("Cookies")

    resp.set_cookie(
        "flavor",
        value="chocolate chip",
        max_age=10,
        path=request.path
    )

    return resp


@app.route('/the/request/object')
def public_index():
    headers = request.headers
    print(headers)
    return render_template('public/index.html')


@app.route('/jinja')
def jinja():
    # Strings
    my_name = "Julian"

    # Integers
    my_age = 30

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>This is some HTML</h1>"

    suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date=date, my_html=my_html,
        suspicious=suspicious
    )

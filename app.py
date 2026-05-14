# import os module for handling file paths
import os
# import Flask and render_template for rendering HTML templates, request for handling form data
# session for managing user sessions, redirect and url_for for handling redirects after form submissions
from flask import Flask, render_template, request, session, redirect, url_for
# import secure_filename for handling file uploads.
from werkzeug.utils import secure_filename
# import SQLite3 to set up a database connection and execute SQL commands
import sqlite3

# create a Flask app instance
app = Flask(__name__)
app.secret_key = "temporary_secret_key"  # set a secret key for session management. Will need to be updated for production use.
# set up the upload folder and allowed file extensions for image uploads
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# configure the Flask app to use the upload folder and set a maximum content length for uploads (1.2 MB)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = int(1.2 * 1024 * 1024)

# helper function to get a database connection, connects to the SQLite database and sets the row factory to sqlite3.
# Row for easier access to query results
def get_db_connection():
    print(os.getcwd())
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
# Create a user table if one does not already exist. It will store user registration information
#  user_id is the primary key
def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

#  route for the home page, renders the home.html template
@app.route("/")
def home():
    return render_template("home.html")
    
    
# route for the login page, verifies the username and password against the users table in the database and
#  displays a success or error message.. Renders the login.html with the message to display success or error.
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        # search for user with matching username and password in the users table. 
        # fetchone return the first result found or returns None if no match is found.
        user = conn.execute("""
            SELECT * FROM users
            WHERE username = ? AND password = ?
        """, (username, password)).fetchone()

        conn.close()
        # if a mathcing user is create a session and redirect to the view posts page. 
        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            return redirect(url_for("viewPosts"))
        else:
            message = "Invalid username or password."

    return render_template("login.html", message=message)
# ============================ route for the logout page, clears the user session and redirects to the home page=========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# =================route for the register page, renders the register.html template=========================

@app.route("/register", methods=["GET", "POST"])

def register():
    message = ""
    # Check if the method is POST meaning form has been submitted.
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
    # Try to insert new user into users table.
        try:
            # call helper function to create a database connection and execute an SQL command to insert the new user data into the users table.
            conn = get_db_connection()
            # execute the SQL command. Parameterized query is used to prevent SQL injection attacks. 
            conn.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, password))
        # commit the changes to the database and close the connection
            conn.commit()
            conn.close()
    # display success message
            message = "User registered successfully."
    # If the username already exists, an IntegrityError will be raised due 
    # to the UNIQUE on the username column. 
        except sqlite3.IntegrityError:
            message = "That username already exists. Please choose another."
            #  finally clause is used to ensure that the database connection is closed even if an error occurs.
            #  help prevent database being locked due to open connections.
        finally:
            if conn:
                conn.close()

    return render_template("register.html", message=message)

# ===================route for the new post page, renders the newPost.html template===========================

# helper function to check if the uploaded file has an allowed extension stired in the ALLOWED_EXTENSIONS 
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/new_post", methods=["GET", "POST"])
def newPost():
    message = "" # create message with empty string to prevent error if routre is accessed with GET method.
    # Check if the method is POST meaning form has been submitted.
    if request.method == "POST":
        username = request.form.get("username")
        location = request.form.get("location")
        observation_date = request.form.get("observation_date")
        observation_time = request.form.get("observation_time")
        bird_species = request.form.get("bird_species")
        activity = request.form.get("activity")
        duration = request.form.get("duration")
        comments = request.form.get("comments")
    # print the form data to show handling of posted data
        print("Username:", username)
        print("Location:", location)
        print("Date:", observation_date)
        print("Time:", observation_time)
        print("Bird:", bird_species)
        print("Activity:", activity)
        print("Duration:", duration)
        print("Comments:", comments)
        # handle the image upload, get the image file from the form data
        image = request.files.get("image")
        # check if an image was uploaded and if the filename is not empty
        if image and image.filename != "":
            # check if the uploaded file has an allowed extension using the allowed_file helper function
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(save_path)
                print("Image saved:", filename)
                # set a success message to be displayed in the template
                message = "Post and image uploaded successfully."
            else:
                message = "Invalid image type. Please upload a JPG or PNG file."
        else:
            message = "Post submitted without an image."

    return render_template("newPost.html", message=message)


#================== route for the view posts page, renders the viewPosts.html template=================
@app.route("/view_posts")
def viewPosts():
    return render_template("viewPosts.html")

create_tables() # call the create_tables function to make sure the database and user table are set uo when the app starts

if __name__ == "__main__":
    app.run(debug=True)
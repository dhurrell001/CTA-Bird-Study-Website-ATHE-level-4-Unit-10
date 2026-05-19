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
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# configure the Flask app to use the upload folder and set a maximum content length for uploads (1.2 MB)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = int(1.2 * 1024 * 1024)

# helper function to get a database connection, connects to the SQLite database and sets the row factory to sqlite3.
# Row for easier access to query results
def get_db_connection():
    
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
    # Creta a table to store user posts. Uses a foreign key to link each post to a user in the users table.
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        location TEXT NOT NULL,
        observation_date TEXT NOT NULL,
        observation_time TEXT NOT NULL,
        bird_species TEXT NOT NULL,
        activity TEXT NOT NULL,
        duration INTEGER NOT NULL,
        comments TEXT,
        image_filename TEXT,

        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    conn.commit()
    conn.close()

#  =====================route for the home page, renders the home.html template===========

@app.route("/")
def home():
    return render_template("home.html")

#=========================== Login route ===============================    
    
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
    message = ""
    #  check if user is logged in by seeing if user_id is in the session. If the user is not logged redirect
    #  to the login page. only logged in users can post.
    if "user_id" not in session:
        return redirect(url_for("login"))
    #  if method is POST gather data from the form.
    if request.method == "POST":
        user_id = session["user_id"]

        location = request.form["location"]
        observation_date = request.form["observation_date"]
        observation_time = request.form["observation_time"]
        bird_species = request.form["bird_species"]
        activity = request.form["activity"]
        duration = request.form["duration"]
        comments = request.form["comments"]

        image = request.files.get("image")
        image_filename = ""
        # check if an image was uploaded and if the filename is not empty. If an image was uploaded, 
        # check if the file type is allowed using the allowed_file helper function.
        if image and image.filename != "":
            if allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
            else:
                message = "Invalid image type. Please upload a JPG or PNG file."
                return render_template("newPost.html", message=message)

        conn = get_db_connection()
        # execute an SQL command to insert the new post data into the posts table. 
        # The user_id is included to link the post to the user who created it.
        conn.execute("""
            INSERT INTO posts (
                user_id, location, observation_date, observation_time,
                bird_species, activity, duration, comments, image_filename
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, location, observation_date, observation_time,
            bird_species, activity, duration, comments, image_filename
        ))

        conn.commit()
        conn.close()

        message = "Post saved successfully."

    return render_template("newPost.html", message=message)


#================== route for the view posts page, renders the viewPosts.html template=================

@app.route("/view_posts")
def viewPosts():
    conn = get_db_connection()
    # execute an SQL to retrieve all posts from the posts table with the username of the user who created the post.
    # send result ast posts to the viewPost template.
    posts = conn.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.user_id
        ORDER BY posts.post_id DESC
    """).fetchall()

    conn.close()

    return render_template("viewPosts.html", posts=posts)

# ========================== Delete posts =================================================

# PostID is passed as a parameter in the URL and used to identify which post to delete. 
# Only the user who created the post can delete it.
@app.route("/deletePost/<int:post_id>", methods=["POST"])
def deletePost(post_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    # use post_id and user_id to find the post in database.
    post = conn.execute("""
        SELECT * FROM posts
        WHERE post_id = ? AND user_id = ?
    """, (post_id, session["user_id"])).fetchone()
    # if post is found, execute an SQL command to delete the post.
    if post:
        conn.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
        conn.commit()

    conn.close()

    return redirect(url_for("viewPosts"))

#========================== Edit posts =================================================

# PostID is passed as a parameter in URL and used to identify which post to edit.
@app.route("/editPost/<int:post_id>", methods=["GET", "POST"])
def editPost(post_id):

    # check user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    # get the post that belongs to logged in user
    post = conn.execute("""
        SELECT * FROM posts
        WHERE post_id = ? AND user_id = ?
    """, (post_id, session["user_id"])).fetchone()

    # close connection if post not found or user does not own post
    if not post:
        conn.close()
        return "Post not found"

    # submit the form to update the post. Form is pre-filled with the posts data to be edited by user.
    if request.method == "POST":

        location = request.form["location"]
        observation_date = request.form["observation_date"]
        observation_time = request.form["observation_time"]
        bird_species = request.form["bird_species"]
        activity = request.form["activity"]
        duration = request.form["duration"]
        comments = request.form["comments"]

        # update existing database record with new data from form. 
        # post_id is used to identify which record to update.
        conn.execute("""
            UPDATE posts
            SET
                location = ?,
                observation_date = ?,
                observation_time = ?,
                bird_species = ?,
                activity = ?,
                duration = ?,
                comments = ?
            WHERE post_id = ?
        """, (
            location,
            observation_date,
            observation_time,
            bird_species,
            activity,
            duration,
            comments,
            post_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("viewPosts"))

    conn.close()

    # show form pre-filled with current post data
    return render_template("newPost.html", post=post, username=session["username"])

#======================= Create tables and run the app =========================

create_tables() # call the create_tables function to make sure the database and user table are set uo when the app starts

if __name__ == "__main__":
    app.run(debug=True)
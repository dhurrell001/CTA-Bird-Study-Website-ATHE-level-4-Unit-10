# import os module for handling file paths
import os
# import Flask and render_template for rendering HTML templates, request for handling form data
from flask import Flask, render_template, request
# import secure_filename for handling file uploads.
from werkzeug.utils import secure_filename

# create a Flask app instance
app = Flask(__name__)

# set up the upload folder and allowed file extensions for image uploads
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# configure the Flask app to use the upload folder and set a maximum content length for uploads (1.2 MB)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = int(1.2 * 1024 * 1024)

#  route for the home page, renders the home.html template
@app.route("/")
def home():
    return render_template("home.html")
    
    
# route for the login page, renders the login.html template 
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

# =================route for the register page, renders the register.html template=========================
@app.route("/register", methods=["GET", "POST"])
#  Print register form data to console for testing purposes, to show handling of posted data

def register():
    # Check if the request method is POST meaning form has been submitted
    message = "" # create message with empty string to prevent error if routre is accessed with GET method.
    if request.method == "POST":
        # get the form data
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # print the form data to the console
        print("Username:", username)
        print("Email:", email)
        print("Password:", password)

        # Send message back to the htnl template to display, to show that form was sucessfully posted.
        message = "Registration form submitted successfully."

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

if __name__ == "__main__":
    app.run(debug=True)
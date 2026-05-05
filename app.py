from flask import Flask, render_template

app = Flask(__name__)
#  route for the home page, renders the home.html template
@app.route("/")
def home():
    return render_template("home.html")
    
    
# route for the login page, renders the login.html template 
@app.route("/login")
def login():
    return render_template("login.html")

# route for the register page, renders the register.html template
@app.route("/register")
def register():
    return render_template("register.html")
# route for the new post page, renders the newPost.html template
@app.route("/newPost")
def newPost():
    return render_template("newPost.html")
# route for the view posts page, renders the viewPosts.html template
@app.route("/viewPosts")
def viewPosts():
    return render_template("viewPosts.html")

if __name__ == "__main__":
    app.run(debug=True)
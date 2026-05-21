CTA Bird Study Website

Overview

This project was created as part of the ATHE Level 4 Extended Diploma in Computing – Unit 10 Web Design and Programming.

The website was developed for the Centrala Trust for Ornithology (CTO) and the Centrala Environmental Agency (CEA). The aim of the site is to allow residents of Centrala to record bird sightings and upload information about observations.

Users can create accounts, submit sightings, upload images, edit posts, delete posts, and search existing sightings.

The website uses client-side technologies for structure, styling, and interaction, combined with server-side processing and a database for storing information.

------------------------------------------------------------

 Technologies Used

Client-side

- HTML
- CSS
- JavaScript

 Server-side

- Python
- Flask
- SQLite

------------------------------------------------------------

 Features

Current functionality includes:

- User registration
- User login/logout
- Session handling
- Create new bird sighting posts
- Upload images
- View all posts
- Search posts by keyword
- Edit existing posts
- Delete posts
- Client-side form validation
- Server-side form processing
- CRUD database operations

------------------------------------------------------------

 Database Structure

The project currently uses SQLite with two main tables.

 Users Table

Stores:

- User ID
- Username
- Email
- Password

Posts Table

Stores:

- Post ID
- User ID
- Location
- Observation date
- Observation time
- Bird species
- Activity
- Duration
- Comments
- Image filename

------------------------------------------------------------
```
Project Structure

CTA Bird Study Website
│
├── app.py
├── database.db
├── uploads
│
├── templates
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── newPost.html
│   └── viewPosts.html
│
├── static
│   ├── css
│   │   └── style.css
│   │
│   ├── js
│   │   ├── script.js
│   │   └── script.min.js
│   │
│   └── images
```
------------------------------------------------------------

Installation

1. Clone the repository:

git clone https://github.com/dhurrell001/CTA-Bird-Study-Website-ATHE-level-4-Unit-10

2. Open the project folder:

cd CTA-Bird-Study-Website

3. Install requirements:

pip install -r requirements.txt

4. Run the application:

python app.py

5. Open a browser and go to:

http://127.0.0.1:5000

------------------------------------------------------------

Notes

This project was developed for educational purposes and is not intended for production use.

Passwords are currently stored in plaintext for demonstration purposes only.

Some security considerations that would need improving before a production deployment include:

- Password hashing
- Stronger server-side validation
- Protection against malicious file uploads
- Additional security around sessions and authentication

------------------------------------------------------------

 Author

David Hurrell

ATHE Level 4 Extended Diploma in Computing
Unit 10 Web Design and Programming

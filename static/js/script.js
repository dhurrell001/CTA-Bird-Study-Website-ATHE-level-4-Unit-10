

// ================ Js for validating registration form before submission =======================================
// this contain only basic validation as a proof of concept.

// Get the registration form element by its ID
const registerForm = document.getElementById("register-form");
// Check if the form exists before adding event listener, this prevents errors on pages that don't have the form
if (registerForm) {
    // add event listener to registration form submit event
    registerForm.addEventListener("submit", function(event) {
    // get form values by their IDs
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        // stop form submitting if validation fails
        if (username === "") {
            alert("Username is required");
            // prevent defaultform submission behavior
            event.preventDefault();
            return;
        }
        // basic email format validation
        if (!email.includes("@")) {
            alert("Please enter a valid email address");
            event.preventDefault();
            return;
        }
        // password length validation
        if (password.length < 6) {
            alert("Password must be at least 6 characters");
            event.preventDefault();
            return;
        }
        // password confirmation validation
        if (password !== confirmPassword) {
            alert("Passwords do not match");
            event.preventDefault();
            return;
        }

    });

}
// ================ Js for validating login form before submission =======================================

// Get the login form element by its ID
const loginForm = document.getElementById("login-form");
// Check if the form exists before adding event listener, this prevents errors if form is not on the page
if (loginForm) {
    // add event listener to login form submit event    
    loginForm.addEventListener("submit", function(event) {
        // get form values by their IDs
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        // stop form submitting if validation fails
        if (username === "") {
            alert("Username is required");
            // prevent defaultform submission behavior
            event.preventDefault();
            return;
        }
        if (password === "") {
            alert("Password is required");
            event.preventDefault();
            return;
        }
    })};

    // ================ Js for validating new post form before submission =======================================

// Get the new post form element by its ID
const newPostForm = document.getElementById("new-post-form");
// Check if the form exists before adding event listener.
if (newPostForm) {  
    // add event listener to new post form submit event  
    newPostForm.addEventListener("submit", function(event) {
        // get form values by their IDs
        const username = document.getElementById("username").value;
        const location = document.getElementById("location").value;
        const date = document.getElementById("observation-date").value;
        const time = document.getElementById("observation-time").value;
        const birdSpecies = document.getElementById("bird-species").value;
        const activity = document.getElementById("activity").value;
        const duration = document.getElementById("duration").value;
        const image = document.getElementById("image").value;
        // stop form submitting if validation fails
        if (username === "") {
            alert("Username is required");
            // prevent defaultform submission behavior
            event.preventDefault();
            return;
        }
        if (birdSpecies === "") {
            alert("Bird species is required");
            event.preventDefault();
            return;
        }
        if (location === "") {
            alert("Location is required");
            event.preventDefault();
            return;
        }
        if (date === "") {
            alert("Date is required");
            event.preventDefault();
            return;
        }
        if (activity === "") {
            alert("Activity is required");
            event.preventDefault();
            return;
        }

        // check duration in a number format and greater than 0 using OR operator 
      
        if (isNaN(duration) || duration <= 0) {
          alert("Duration must be a number greater than 0");
            event.preventDefault();
            return;
        }
        // Use regular expression to validate image file extension if an image is uploaded
        if (image) {
            const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
            if (!allowedExtensions.test(image)) {
                alert("Invalid image format. Please upload a JPG, JPEG, PNG, or GIF file.");
                event.preventDefault();
                return;
            }
        }

    })};

    // ================= Js for validating search form before submission =======================================

// Get the search form element by its ID
const searchForm = document.getElementById("search-form");
// Check if the form exists before adding event listener.
if (searchForm) {   
    // add event listener to search form submit event
    searchForm.addEventListener("submit", function(event) {
        // get form values by their IDs
        const searchQuery = document.getElementById("search-query").value;
        // stop form submitting if validation fails
        if (searchQuery === "") {
            alert("Please enter a search query");
            // prevent defaultform submission behavior
            event.preventDefault();
            return;
        }
    })};
    // ================ delete post confirmation =======================================
    // Get delete post button by its ID
    const deletePostButton = document.getElementById("delete-post");
    // Check if the button exists before adding event listener.
    if (deletePostButton) {
        // add event listener to delete post button click event
        deletePostButton.addEventListener("click", function(event) {
            // show confirmation dialog box and prevent deleting post if user clicks cancel
            if (!confirm("Are you sure you want to delete this post?")) {
                event.preventDefault();
            }
        });
    }

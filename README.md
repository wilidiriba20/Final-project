# Food Recipes
#### Video Demo: <https://youtu.be/-sMiwuvzIXU?si=bmz_UYssVS8dc74y>
#### Description:

This project is a web application built using Flask, designed to help users find and save recipes tailored to their dietary preferences and food intolerances. By leveraging an external API for recipe data, users can search for recipes based on specific ingredients, save their favorites, and manage their account details including their passwords and dietary restrictions.

The application includes user registration and login functionalities, customizable dietary preferences, and a simple interface for searching and saving recipes. The primary goal is to provide a user-friendly experience while ensuring secure handling of user data.

#File Structure
###1. app.py
This is the main application file where the Flask app is configured. It handles all routing for user actions including registration, login, and searching for recipes. Key functionalities include:

User Registration (/register): This route allows new users to create an account. The app checks for existing usernames, confirms password matches, and collects dietary preferences and food intolerances.

User Login (/login): Users can log in using their credentials. The app verifies the username and password against stored records and maintains session data.

Recipe Search (/): Authenticated users can search for recipes. This route interacts with the external recipe API based on the user's dietary preferences and query inputs.

Save Favorite Recipes (/save): Users can save their favorite recipes for future access. This includes displaying saved recipes and deleting them as desired.

Password Management (/password): Users can update their password securely once logged in.

###2. helpers.py

This utility file contains helper functions that are used throughout the application. The primary function in this file (image) interacts with an external recipe API to fetch recipe data based on the user's dietary restrictions and search queries. The function formats API requests and handles responses by compiling a list of recipe cards.

###3. templates/ (HTML files)
The templates directory contains the following HTML files that form the front end of the application:

register.html: Contains the registration form where users can sign up by providing their desired username, password, and dietary preferences .

login.html: Provides a simple login form for returning users to authenticate themselves.

search.html: Displays search results as well as options for saving recipes. It processes the user’s query and shows the returned recipe images.
save.html: Lists all saved recipes for the logged-in user, enabling them to view and delete saved items.

password.html: Allows users to change their passwords with verification checks.

###4. static/
contain images


###Conclusion
This Flask-based web application serves as a comprehensive tool for users looking to manage their dietary preferences and discover new recipes. Through secure handling of user data, an intuitive interface, and the power of an external API, it provides a valuable resource for anyone interested in cooking while adhering to specific dietary restrictions. As this project evolves, new features like user reviews of recipes, advanced search filters, and enhanced aesthetic designs could further improve engagement and usability.

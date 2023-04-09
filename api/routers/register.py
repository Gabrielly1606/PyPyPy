from flask import Blueprint, render_template, request, redirect, url_for


user_registration_bp = Blueprint('user_registration', __name__)

@user_registration_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle user registration form submission
        # create a new user object and save it to the database
        # redirect to a success page or display an error message
        pass
    else:
        # display the user registration form
        return "hi"
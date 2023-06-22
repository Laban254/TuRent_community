from flask import render_template, request, redirect, session, flash, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,  LoginManager, current_user, login_user, logout_user
from app import app
from .models import Base, PlotInformation, HouseInformation, TenantInformation, Reviews, LoginDetails, TenantLoginDetails


# Set a secret key for session management
app.secret_key = 'your_secret_key'


# Flask-Login initialization
login_manager = LoginManager()
login_manager.init_app(app)


# Configuration for  the login view
login_manager.login_view = 'login'

# Create SQLite database engine and bind it to the session using a connection pool
engine = create_engine('sqlite:///turent_commun1.db')
Session = scoped_session(sessionmaker(bind=engine))
db_session = Session
# Create the tables
Base.metadata.create_all(engine)


# user loader function
@login_manager.user_loader
def load_user(user_id):
    # Load the user object from the database based on the user ID
    return db_session.query(PlotInformation).get(user_id)


@app.route("/")
@app.route("/home")
def turent_home():
    """
    Render the home page template.

    Returns:
        The rendered home page template.
    """
    return render_template("Home.html")


@app.route('/register_plot', methods=['GET', 'POST'])
def register_plot():
    """
    Register a new plot based on the form data.

    If the request method is POST, the function retrieves the plot information from the form,
    checks if a plot with the given plot_number already exists, creates a new PlotInformation object,
    adds it to the session, and commits the changes. Then it flashes a success message and redirects
    the user to the login page.

    If the request method is GET, the function renders the plot registration template.

    Returns:
        If the request method is POST and the plot is successfully registered, it redirects the user
        to the login page.
        If the request method is GET or the plot registration fails, it renders the plot registration template.
    """
    if request.method == 'POST':
        # Get plot information from the form
        plot_number = request.form['plot_number']
        phone_number = request.form['phone_number']
        total_houses = request.form['total_houses']
        email = request.form['email']
        location = request.form['location']
        password1 = request.form['password1']
        hashed_password = generate_password_hash(password1)

        # Check if a plot with the given plot_number already exists
        existing_plot = db_session.query(PlotInformation).filter_by(plot_number=plot_number).first()
        if existing_plot:
            flash('Plot already exists!')
            return redirect('/register_plot')

        # Create a new PlotInformation object
        plot = PlotInformation(plot_number=plot_number, phone_number=phone_number,
                               total_houses=total_houses, email=email, location=location, password1=hashed_password)

        # Add the plot to the session and commit the changes
        db_session.add(plot)
        db_session.commit()

        flash('Plot added successfully!')
        return redirect('/login')

    return render_template('plot_registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # Get login information from the form
        email = request.form['email']
        password = request.form['password']
        session["email"] = email

        # Check if the login credentials belong to a landlord
        landlord = db_session.query(PlotInformation).filter_by(email=email).first()
        if landlord and check_password_hash(landlord.password1, password):
            session['plot_id'] = landlord.id
            session['plot_number'] = landlord.plot_number  # Store the plot number in the session

            flash('Login successful as landlord!')
            login_user(landlord)  # Log in the landlord user
            return redirect(url_for('landlord_page'))

        # Check if the login credentials belong to a tenant
        tenant_login = db_session.query(TenantLoginDetails).filter_by(username=email).first()
        if tenant_login and check_password_hash(tenant_login.password, password):
            session['tenant_id'] = tenant_login.tenant_id
            flash('Login successful as tenant!')
            login_user(tenant_login)  # Log in the tenant user
            return redirect(url_for('home'))  # Redirect to the home page

        flash('Invalid email or password!')
        return redirect('/login')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    Returns:
        The user is logged out and redirected to the home page.
    """
    logout_user()
    return redirect(url_for('turent_home'))


@app.route('/landlord_landing_page', methods=['GET', 'POST'])
@login_required
def landlord_page():
    # Retrieve the plot information from the database
    plot = db_session.query(PlotInformation).filter_by(email=session.get('email')).first()

    if plot:
        return render_template("landlord_landing_page.html", plot=plot)
    else:
        return render_template("landlord_landing_page.html")
    
@app.route("/update_landlord_info", methods=["POST"])
def update_landlord_info():
    plot = db_session.query(PlotInformation).filter_by(email=session.get('email')).first()
    if request.method == 'POST':
        # Update the plot information
        plot.plot_number = request.form.get('plot_number')
        plot.phone_number = request.form.get('phone_number')
        plot.email = request.form.get('email')
        plot.total_houses = request.form.get('number_of_houses')

        session["plot"] = plot

        # Commit the changes to the database
        db_session.commit()

        return render_template("landlord_landing_page.html", plot=plot)
    
@app.route("/forgot_password", methods=['POST', 'GET'])
def forgot_password():
    user_email = session.get("email")
    if request.method == 'POST':
        landlord = db_session.query(PlotInformation).filter_by(email=user_email).first()
        if landlord is not None and user_email == landlord.email:
            landlord.password1 = request.form['password']
            confirm_password = request.form['confirm_password']
            
            if landlord.password1 == confirm_password:
                landlord.password1= generate_password_hash(landlord.password1)
                db_session.commit()
                return redirect(url_for("login_page"))
    return render_template("forgot_password.html", email=user_email)


#landlord rating page route
@app.route("/rate_landlord")
def rate_landlord():
    return render_template("rate_landlord.html")

#tenant landing page route
@app.route("/tenant_landing_page")
def tenant_landing_page():
    return render_template("tenant_landing_page.html")

#tenant screening page route
@app.route("/tenant_screening_page")
def tenant_screening_page():
    return render_template("tenant_screening.html")

#Tenant registration page route
@app.route("/new_tenant", methods=["POST", "GET"])
def tenant_registration():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        name = first_name + " " + last_name
        email = request.form.get("email")
        phone_number = request.form.get("phone_Number")
        #house id to be changed
        house_id = 140
        house_info = db_session.query(TenantInformation).filter_by(house_id = house_id).first()
        if house_info:
            with app.test_request_context():
                session.pop('_flashes', None)
            flash("You already have a tenant in that house")
            return redirect(url_for("tenant_registration"))
        else:
            new_tenant = TenantInformation(name = name, email = email, phone_number = phone_number, house_id = house_id )
            db_session.add(new_tenant)
            db_session.commit()
            
            plot = session.get("plot")
            return render_template("landlord_landing_page.html", plot=plot)
    else:
        return render_template("new_tenant_info.html")


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/house_information")
def house_information():
    return render_template("house_information_view.html")




@app.route("/house_registration")
def house_registration():
    return render_template("house_info.html")

@app.route("/edit_tenant_info")
def edit_tenant_info():
    return render_template("tenants.html")

@app.route("/landlord_screening")
def landlord_screening():
    return render_template("landlord_screening.html")

@app.route('/view_database')
def view_database():
    plots = db_session.query(PlotInformation).all()
    houses = db_session.query(HouseInformation).all()
    tenants = db_session.query(TenantInformation).all()
    reviews = db_session.query(Reviews).all()
    logins = db_session.query(LoginDetails).all()
    tenant_logins = db_session.query(TenantLoginDetails).all()

    return render_template('view_database.html', plots=plots, houses=houses, tenants=tenants,
                           reviews=reviews, logins=logins, tenant_logins=tenant_logins)


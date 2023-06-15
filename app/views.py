from app import app
from flask import render_template, request, redirect, session, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Base, PlotInformation, HouseInformation, TenantInformation, Reviews, LoginDetails, TenantLoginDetails
from flask_login import login_required,  LoginManager, current_user, login_user
# Set a secret key for session management
app.secret_key = 'your_secret_key'


# Flask-Login initialization
login_manager = LoginManager()
login_manager.init_app(app)


# Configuration for  the login view
login_manager.login_view = 'login'

# Create SQLite database engine and bind it to the session using a connection pool
engine = create_engine('sqlite:///turent.db')
Session = scoped_session(sessionmaker(bind=engine))
db_session = Session


# user loader function
@login_manager.user_loader
def load_user(user_id):
    # Load the user object from the database based on the user ID
    return db_session.query(PlotInformation).get(user_id)


@app.route("/")
@app.route("/home")
def turent_home():
    return render_template("Home.html")

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

#login page route
@app.route("/login")
def login_page():
    return render_template("login.html")

#Tenant registration page route
@app.route("/new_tenant")
def tenant_registration():
    return render_template("new_tenant_info.html")

#Plot registration page route
@app.route("/plot_registration")
def plot_registration():
    return render_template("plot_registration.html")
    
"""
@app.route("/log_in")
@login_required
def home():
    print("Current user:", current_user)  # Print the current user for debugging purposes
    
    if 'plot_id' in session and 'plot_number' in session:
        plot_id = session['plot_id']
        plot_number = session['plot_number']
        print("Logged in as landlord. Plot ID:", plot_id)
        print("Plot Number:", plot_number)

        plot = db_session.query(PlotInformation).filter_by(plot_number=plot_number).first()
        return render_template('landlord_home.html', plot=plot)  # Pass the 'plot' variable to the template context

    
    elif 'tenant_id' in session:
        tenant_id = session['tenant_id']
        print("Logged in as tenant. Tenant ID:", tenant_id)
        return render_template('plot_info.html', user_type='tenant')
    
    else:
        print("User is not properly authenticated. Redirecting to the login page.")
        return redirect('/login')


    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get login information from the form
        email = request.form['email']
        password = request.form['password']

        # Check if the login credentials belong to a landlord
        landlord = db_session.query(PlotInformation).filter_by(email=email).first()
        if landlord and check_password_hash(landlord.password1, password):
            session['plot_id'] = landlord.id
            session['plot_number'] = landlord.plot_number  # Store the plot number in the session

            flash('Login successful as landlord!')
            login_user(landlord)  # Log in the landlord user
            return redirect(url_for('home'))

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


#registering the plot
@app.route('/register_plot', methods=['GET', 'POST'])
def register_plot():
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

        return 'Plot registered successfully!'

    return render_template('register_plot.html')


from flask import flash

@app.route('/edit_plot', methods=['POST'])
@login_required
def edit_plot():
    if 'plot_number' not in session:
        return 'User is not a landlord. Access denied!'

    plot_number = session['plot_number']
    plot = db_session.query(PlotInformation).filter_by(plot_number=plot_number).first()
    if plot:
        # Get updated plot information from the AJAX request
        updated_phone_number = request.form['phone_number']
        updated_total_houses = request.form['total_houses']
        updated_email = request.form['email']
        updated_location = request.form['location']
        updated_password = request.form['password1']

        # Check if any field has been updated
        if (
            plot.phone_number != updated_phone_number or
            plot.total_houses != updated_total_houses or
            plot.email != updated_email or
            plot.location != updated_location or
            plot.password1 != updated_password
        ):
            # Update plot information in the database
            plot.phone_number = updated_phone_number
            plot.total_houses = updated_total_houses
            plot.email = updated_email
            plot.location = updated_location
            plot.password1 = updated_password
            db_session.commit()

            flash('Plot information updated successfully!', 'success')  # Flash success message
            return 'success'  # Return success response
        else:
            flash('No changes were made to the plot information.', 'info')  # Flash info message
            return 'no_update'  # Return no update response

    return 'Plot not found!'





@app.route('/plot_info/<int:plot_id>')
def plot_info(plot_id):
    # Retrieve plot information from the database based on the plot_id
    plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
    if plot:
        houses = db_session.query(HouseInformation).filter_by(plot_id=plot_id).all()
        return render_template('plot_info.html', plot=plot, houses=houses)
    else:
        return 'Plot not found!'
    
# delete plot
@app.route('/delete_plot/<int:plot_id>', methods=['GET', 'POST'])
def delete_plot(plot_id):
    plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
    if plot:
        db_session.delete(plot)
        db_session.commit()
        return 'Plot deleted successfully!'
    else:
        return 'Plot not found!'

    
from flask import redirect, url_for, flash

@app.route('/add_tenant', methods=['GET', 'POST'])
@login_required
def add_tenant():
    if 'plot_number' not in session:
        return 'User is not a landlord. Access denied!'

    plot_number = session['plot_number']
    plot = db_session.query(PlotInformation).filter_by(plot_number=plot_number).first()
    if plot:
        if request.method == 'POST':
            # Get tenant information from the form
            name = request.form['name']
            phone_number = request.form['phone_number']
            house_id = request.form['house_id']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)

            # Create a new TenantInformation object
            tenant = TenantInformation(name=name, phone_number=phone_number, house_id=house_id, email=email)
            db_session.add(tenant)
            db_session.commit()

            # Create a new TenantLoginDetails object
            tenant_login = TenantLoginDetails(tenant_id=tenant.id, username=username, password=hashed_password)
            db_session.add(tenant_login)
            db_session.commit()

            flash('Tenant added successfully!', 'success')
            return redirect(url_for('home'))

        houses = db_session.query(HouseInformation).filter_by(plot_id=plot.id).all()
        return render_template('add_tenant.html', houses=houses)

    return 'Plot not found!'


@app.route('/edit_tenant', methods=['GET', 'POST'])
def edit_tenant():
    tenant_id = session.get('tenant_id')
    
    if not tenant_id:
        return 'Tenant ID not found in session!'

    tenant = db_session.query(TenantInformation).filter_by(id=tenant_id).first()

    if not tenant:
        return 'Tenant not found!'

    if request.method == 'POST':
        # Get updated tenant information from the form
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        house_id = request.form['house_id']

        # Check if the house exists
        house = db_session.query(HouseInformation).filter_by(id=house_id).first()

        if not house:
            return 'House not found!'

        # Update the tenant information
        tenant.name = name
        tenant.phone_number = phone_number
        tenant.email = email
        tenant.house_id = house_id
        db_session.commit()

        return 'Tenant information updated successfully!'
    
    houses = db_session.query(HouseInformation).filter_by(plot_id=tenant.house_id).all()
    return render_template('edit_tenant.html', tenant=tenant, houses=houses)


@app.route('/delete_tenant/<int:tenant_id>', methods=['GET', 'POST'])
def delete_tenant(tenant_id):
    tenant = db_session.query(TenantInformation).filter_by(id=tenant_id).first()
    if tenant:
        # Delete the tenant's login details
        tenant_login = db_session.query(TenantLoginDetails).filter_by(tenant_id=tenant_id).first()
        if tenant_login:
            db_session.delete(tenant_login)

        # Delete the tenant
        db_session.delete(tenant)
        db_session.commit()
        
        return 'Tenant and login details deleted successfully!'
    else:
        return 'Tenant not found!'


from flask import session

@app.route('/plot')
def plot_details():
    # Get the plot number from the session or request arguments
    plot_number = session.get('plot_number') or request.args.get('plot_number')

    # Retrieve the plot based on the plot number
    plot = db_session.query(PlotInformation).filter_by(plot_number=plot_number).first()

    if plot:
        # Get the houses associated with the plot
        houses = db_session.query(HouseInformation).filter_by(plot_id=plot.id).all()

        # Get the tenants associated with the houses
        tenants = db_session.query(TenantInformation).join(HouseInformation).filter(HouseInformation.plot_id == plot.id).all()

        # Render the template with the plot, houses, and tenants
        return render_template('tenant_list.html', plot=plot, houses=houses, tenants=tenants)
    else:
        # Render the template with the plot not found message
        return render_template('tenant_list.html', plot=None)

@app.route('/add_house_info', methods=['GET', 'POST'])
@login_required
def add_house_info():
    if request.method == 'POST':
        plot_id = session.get('plot_id')
        if not plot_id:
            flash('Plot ID not found in session!')
            return redirect('/')

        plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
        if not plot:
            flash('Plot does not exist!')
            return redirect('/')

        # Get house information from the form
        phone_number = request.form['phone_number']
        house_number = request.form['house_number']
        rental_price = float(request.form['rental_price'])
        rooms_available = int(request.form['rooms_available'])
        images_location = request.form['images_location']
        description = request.form['description']

        # Create a new HouseInformation object
        house = HouseInformation(plot_id=plot_id, phone_number=phone_number,
                                 house_number=house_number, rental_price=rental_price,
                                 rooms_available=rooms_available, images_location=images_location,
                                 description=description)

        db_session.add(house)
        db_session.commit()

        flash('House added successfully!')
        return redirect(url_for('home'))

    return render_template('add_house_info.html')






@app.route('/edit_house/<int:house_id>', methods=['GET', 'POST'])
def edit_house(house_id):
    house = db_session.query(HouseInformation).filter_by(id=house_id).first()
    if house:
        if request.method == 'POST':
            # Update the attributes of the house object with form data
            house.phone_number = request.form['phone_number']
            house.house_number = request.form['house_number']
            house.rental_price = float(request.form['rental_price'])
            house.rooms_available = int(request.form['rooms_available'])
            house.images_location = request.form['images_location']
            house.description = request.form['description']

            db_session.commit()  # Persist the changes in the database

            return 'House information updated successfully!'
        else:
            return render_template('edit_house.html', house=house)
    else:
        return 'House not found!'



@app.route('/delete_house/<int:house_id>', methods=['POST'])
def delete_house(house_id):
    house = db_session.query(HouseInformation).filter_by(id=house_id).first()
    if house:
        # Delete the house
        db_session.delete(house)
        db_session.commit()
        flash('House deleted successfully!')
    else:
        flash('House not found!')
    
    return redirect(url_for('plot_info', plot_id=house.plot_id))




# Add a route for the landlord to review the tenant
@app.route('/landlord_review/<int:tenant_id>', methods=['GET', 'POST'])
def landlord_review(tenant_id):
    if request.method == 'POST':
        # Get review information from the form
        user_id = session.get('landlord_id')  # Assuming you have a logged-in landlord
        star_ratings = int(request.form['star_ratings'])
        comments = request.form['comments']

        # Create a new Reviews object
        review = Reviews(user_id=user_id, tenant_id=tenant_id, star_ratings=star_ratings, comments=comments)

        # Add the review to the session and commit the changes
        db_session.add(review)
        db_session.commit()

        return 'Landlord review submitted successfully!'

    return render_template('landlord_review.html', tenant_id=tenant_id)


# Add a route for the tenant to review the landlord
@app.route('/tenant_review/<int:plot_id>', methods=['GET', 'POST'])
def tenant_review(plot_id):
    if request.method == 'POST':
        # Get review information from the form
        user_id = session.get('tenant_id')  # Assuming you have a logged-in tenant
        star_ratings = int(request.form['star_ratings'])
        comments = request.form['comments']

        # Create a new Reviews object
        review = Reviews(user_id=user_id, plot_id=plot_id, star_ratings=star_ratings, comments=comments)

        # Add the review to the session and commit the changes
        db_session.add(review)
        db_session.commit()

        return 'Tenant review submitted successfully!'

    return render_template('tenant_review.html', plot_id=plot_id)

# to be commented on production
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
"""
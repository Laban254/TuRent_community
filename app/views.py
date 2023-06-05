from app import app
from flask import render_template, request, redirect, session, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Base, PlotInformation, HouseInformation, TenantInformation, Reviews, LoginDetails, TenantLoginDetails

# Set a secret key for session management
app.secret_key = 'your_secret_key'

# Create SQLite database engine and bind it to the session using a connection pool
engine = create_engine('sqlite:///turent.db')
Session = scoped_session(sessionmaker(bind=engine))
db_session = Session

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


@app.route('/edit_plot/<int:plot_id>', methods=['GET', 'POST'])
def edit_plot(plot_id):
    plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
    if plot:
        if request.method == 'POST':
            # Get updated plot information from the form
            plot.plot_number = request.form['plot_number']
            plot.phone_number = request.form['phone_number']
            plot.total_houses = request.form['total_houses']
            plot.email = request.form['email']
            plot.location = request.form['location']
            plot.password1 = request.form['password1']
            db_session.commit()
            return 'Plot updated successfully!'
        else:
            return render_template('edit_plot.html', plot=plot)
    else:
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

    
@app.route('/add_tenant/<int:plot_id>', methods=['GET', 'POST'])
def add_tenant(plot_id):
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
        tenant = TenantInformation(name=name, phone_number=phone_number,  house_id=house_id, email=email)
        db_session.add(tenant)
        db_session.commit()

        # Create a new TenantLoginDetails object
        tenant_login = TenantLoginDetails(tenant_id=tenant.id,  username=username, password=hashed_password)
        db_session.add(tenant_login)
        db_session.commit()

        return 'Tenant added successfully!'

    houses = db_session.query(HouseInformation).filter_by(plot_id=plot_id).all()
    return render_template('add_tenant.html', houses=houses)



@app.route('/edit_tenant/<int:tenant_id>', methods=['GET', 'POST'])
def edit_tenant(tenant_id):
    tenant = db_session.query(TenantInformation).filter_by(id=tenant_id).first()
    if tenant:
        if request.method == 'POST':
            # Get updated tenant information from the form
            name = request.form['name']
            phone_number = request.form['phone_number']
            email = request.form['email']
            house_id = request.form['house_id']

            # Check if the house exists
            house = db_session.query(HouseInformation).filter_by(id=house_id).first()
            if house:
                # Update the tenant information
                tenant.name = name
                tenant.phone_number = phone_number
                tenant.email = email
                tenant.house_id = house_id
                db_session.commit()
                return 'Tenant information updated successfully!'
            else:
                return 'House not found!'
        else:
            houses = db_session.query(HouseInformation).filter_by(plot_id=tenant.house_id).all()
            return render_template('edit_tenant.html', tenant=tenant, houses=houses)
    else:
        return 'Tenant not found!'
    

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




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password1 = request.form['password']

        plot = db_session.query(PlotInformation).filter_by(email=email).first()
        if plot and plot.password1 == password1:
            session['plot_id'] = plot.id
            return 'Login successful!'
        else:
            return 'Invalid email or password!'
    
    return render_template('login.html')



@app.route('/plot_info/<int:plot_id>', methods=['GET', 'POST'])
def plot_details(plot_id):
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        house_number = request.form['house_number']
        rental_price = float(request.form['rental_price'])
        rooms_available = int(request.form['rooms_available'])
        images_location = request.form['images_location']
        description = request.form['description']
        
        house = HouseInformation(plot_id=plot_id, phone_number=phone_number,
                                 house_number=house_number, rental_price=rental_price,
                                 rooms_available=rooms_available, images_location=images_location,
                                 description=description)
        
        db_session.add(house)
        db_session.commit()
        
        return redirect(f'/plot_info/{plot_id}')
    
    plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
    houses = db_session.query(HouseInformation).filter_by(plot_id=plot_id).all()
    
    return render_template('plot_info.html', plot=plot, houses=houses)


@app.route('/delete_plot/<int:plot_id>', methods=['POST'])
def delete_plot(plot_id):
    plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
    if plot:
        db_session.delete(plot)
        db_session.commit()
        return 'Plot deleted successfully!'
    else:
        return 'Plot not found!'
    # reirect to be added return remder_template(delete_plot.html)




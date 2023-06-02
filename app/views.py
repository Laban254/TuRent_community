from app import app
from flask import Flask, render_template, request, redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from models import Base, PlotInformation, HouseInformation, TenantInformation, Reviews, LoginDetails, TenantLoginDetails

app.secret_key = 'your_secret_key'  # Set a secret key for session management
engine = create_engine('sqlite:///turent.db')  # SQLite database file
Base.metadata.create_all(engine)  # Create the tables based on the models
Session = sessionmaker(bind=engine)
db_session = Session()

#registering the plot
@app.route('/register_plot', methods=['GET', 'POST'])
def register_plot():
    if request.method == 'POST':
        plot_number = request.form['plot_number']
        phone_number = request.form['phone_number']
        total_houses = request.form['total_houses']
        email = request.form['email']
        location = request.form['location']
        password1 = request.form['password1']
        
        plot = PlotInformation(plot_number=plot_number, phone_number=phone_number,
                               total_houses=total_houses, email=email, location=location, password1=password1)
        
        db_session.add(plot)
        db_session.commit()
        
        return 'Plot registered successfully!'
    
    return render_template('register_plot.html')

@app.route('/plot_info/<int:plot_id>')
def plot_info(plot_id):
    plot = db_session.query(PlotInformation).filter_by(id=plot_id).first()
    if plot:
        houses = db_session.query(HouseInformation).filter_by(plot_id=plot_id).all()
        return render_template('plot_info.html', plot=plot, houses=houses)
    else:
        return 'Plot not found!'
    
@app.route('/add_tenant/<int:plot_id>', methods=['GET', 'POST'])
def add_tenant(plot_id):
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        house_id = request.form['house_id']
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        tenant = TenantInformation(name=name, phone_number=phone_number, email=email, house_id=house_id)
        db_session.add(tenant)
        db_session.commit()

        tenant_login = TenantLoginDetails(tenant_id=tenant.id, username=username, password=hashed_password)
        db_session.add(tenant_login)
        db_session.commit()

        return 'Tenant added successfully!'
    
    houses = db_session.query(HouseInformation).filter_by(plot_id=plot_id).all()
    return render_template('add_tenant.html', houses=houses)
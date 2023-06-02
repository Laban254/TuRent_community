# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PlotInformation(Base):
    __tablename__ = 'plot_information'
    id = Column(Integer, primary_key=True)
    plot_number = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    total_houses = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    password1 = Column(String(100), nullable=False)

class HouseInformation(Base):
    __tablename__ = 'house_information'
    id = Column(Integer, primary_key=True)
    plot_id = Column(Integer, ForeignKey('plot_information.id'), nullable=False)
    phone_number = Column(String(50), nullable=False)
    house_number = Column(String(50), nullable=False)
    rental_price = Column(Float, nullable=False)
    rooms_available = Column(Integer, nullable=False)
    images_location = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)

class TenantInformation(Base):
    __tablename__ = 'tenant_information'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    house_id = Column(Integer, ForeignKey('house_information.id'), nullable=False)
    login_details = relationship("TenantLoginDetails", uselist=False)


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plot_number = Column(Integer, ForeignKey('plot_information.id'), nullable=False)
    house_number = Column(Integer, ForeignKey('house_information.id'), nullable=False)
    star_ratings = Column(Float, nullable=False)
    comments = Column(String(200), nullable=False)

class LoginDetails(Base):
    __tablename__ = 'login_details'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password1 = Column(String(50), nullable=False)

class TenantLoginDetails(Base):
    __tablename__ = 'tenant_login_details'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenant_information.id'), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)

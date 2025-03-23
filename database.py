from datetime import date
from sqlalchemy import create_engine, inspect, text, Column, Integer, String, Float, Text, LargeBinary, ForeignKey, DateTime, Date
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import LONGBLOB

# Database Configuration
username = "root"
password = ""
host = "localhost"
port = "3306"
database = "TripMaster"
db_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# ----------------------------------------------------------------------------------------------------------------------------

class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

class TravelPackages(Base):
    __tablename__ = 'travel_packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in days
    type = Column(String(100), nullable=False)  # Relaxation, Adventure, etc.
    image = Column(LONGBLOB, nullable=False)  # Storing image as binary data

class CustomPackages(Base):
    __tablename__ = 'custom_packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    destination = Column(Text, nullable=False)
    budget = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in days
    activity = Column(Text, nullable=False)  # Relaxation, Adventure, etc.
    status = Column(String(100), default="Pending", nullable=False)
    
class Buses(Base):
    __tablename__ = 'buses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String(100), nullable=False)
    driver = Column(String(100), nullable=False)

class Routes(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    destination = Column(String(100), nullable=False)
    departure = Column(String(100), nullable=False)
    ass_buses = Column(String(100), nullable=False)

class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    number = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    status = Column(String(100), default="Pending", nullable=False)

# ----------------------------------------------------------------------------------------------------------------------------

def create_database():
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}")
    with engine.connect() as connection:
        try:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
            print(f"Database '{database}' created or already exists.")    
        except ProgrammingError as e:
            print(f"Error creating database: {e}")

def create_tables():
    try:
        # inspector = inspect(engine)
        # existing_tables = inspector.get_table_names()
        # if existing_tables:
        #     Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Tables created.")
    except Exception as e:
        print(f"Error while creating tables: {e}")

# ----------------------------------------------------------------------------------------------------------------------------

def insert_admin(username, password):
    session = Session()
    try:
        new_admin = Admins(username=username, password=password)
        session.add(new_admin)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def authenticate_admin(username, password):
    session = Session()
    try:
        admin = session.query(Admins).filter_by(username=username, password=password).first()
        return bool(admin)
    finally:
        session.close()

def insert_user(name, email, password):
    session = Session()
    try:
        new_user = Users(username=name, email=email, password=password)
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def find_user(name, password):
    session = Session()
    try:
        user = session.query(Users).filter_by(username=name, password=password).first()
        return user.username if user else False
    finally:
        session.close()


#--------------------------------------------------------------------------------------------------------------------------------------#

def insert_package(name, description, price, duration, package_type, image):
    session = Session()
    try:
        # Open the image and convert it to binary
        # Create a new package record
        new_package = TravelPackages(
            name=name,
            description=description,
            price=price,
            duration=duration,
            type=package_type,
            image=image  # Save image as binary data
        )
        
        # Add and commit the new package to the database
        session.add(new_package)
        session.commit()

    except Exception as e:
        print("Error inserting package:", str(e))
        session.rollback()  # Rollback in case of error

    finally:
        session.close()  # Always close the session


def insert_custom_package(name, destination, duration, budget, activity):
    session = Session()
    try:

        # Create a new package record
        new_custom_package = CustomPackages(
            name = name,
            destination = destination,
            duration=duration,
            budget = budget,
            activity = activity
        )
        
        # Add and commit the new package to the database
        session.add(new_custom_package)
        session.commit()

    except Exception as e:
        print("Error inserting package:", str(e))
        session.rollback()  # Rollback in case of error

    finally:
        session.close()  # Always close the session


def select_package():
    session = Session()
    try:
        packages = session.query(TravelPackages).all()
        return packages
    finally:
        session.close()

def get_packages():
    session = Session()
    try:
        package_list = []
        packages = session.query(TravelPackages).all()
        session.close()
        for package in packages:
            package_list.append(
                {
                    "id": package.id,
                    "name": package.name,
                    "description": package.description,
                    "price": package.price,
                    "duration": package.duration,
                    "type": package.type,
                    # "image": package.image  # Adjust path if storing images in a folder
                }
                
            )
        print(package_list)
        return package_list

    except Exception as e:
        print("Error:", str(e))
        return False
    finally:
        session.close()


def insert_bus(reg_number, driver_name):
    session = Session()
    try:
        new_bus = Buses(reg_number=reg_number, driver=driver_name)
        session.add(new_bus)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting category: {e}")
        return False
    finally:
        session.close()


def get_buses():
    session = Session()
    try:
        buses_list = []
        buses = session.query(Buses).all()
        for bus in buses:
            buses_list.append({
                "id": bus.id,
                "reg_number": bus.reg_number,
                "driver": bus.driver,
            })
        return buses_list
    finally:
        session.close()

def insert_route(departure, destination, ass_busses):
    session = Session()
    try:
        new_route = Routes(departure=departure, destination=destination, ass_buses=ass_busses)
        session.add(new_route)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting category: {e}")
        return False
    finally:
        session.close()

def get_route():
    session = Session()
    try:
        return session.query(Routes).all()
    finally:
        session.close()


def get_custome_route():
    session = Session()
    try:
        return session.query(CustomPackages).all()
    finally:
        session.close()

def insert_booking(package_name, name, email, number, start_date, end_date, number_of_people):
    session = Session()
    try:
        new_booking = Booking(
            package_name= package_name,
            name= name,
            email= email,
            number= number,
            start_date= start_date,
            end_date= end_date,
            number_of_people= number_of_people,
        )
        session.add(new_booking)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()

def get_booking():
    session = Session()
    try:
        return session.query(Booking).all()
    finally:
        session.close()


def update_booking_status(id):
    session = Session()
    try:
        session.query(Booking).filter(Booking.id==id).update(
            {Booking.status: "Confirm"}
        )
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()
        return True

def get_all_packages():
    session = Session()
    try:
        all_packages = []
        traval = session.query(TravelPackages).all()
        for info in traval:
            all_packages.append({
                "tid": info.id,
                "name": info.name,
            })
        cusomte = session.query(CustomPackages).all()
        for info in cusomte:
            all_packages.append({
                "cid": info.id,
                "destination": info.destination
            })
        print(all_packages)
        return all_packages
    finally:
        session.close()

def acccept_custom(id=id):
    session = Session()
    try:
        session.query(CustomPackages).filter(CustomPackages.id == id).update({
            CustomPackages.status: "Accept"
        })
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

def count_admin():
    session = Session()
    
    package_count = 0
    buses_count = 0
    routes_count = 0
    booking_count = 0
    custome_count = 0
    try:
        package_count =  len(session.query(TravelPackages).all())
        buses_count =  len(session.query(Buses).all())
        routes_count =  len(session.query(Routes).all())
        booking_count = len(session.query(Booking).all())
        custome_count = len(session.query(CustomPackages).all())
        return package_count, buses_count, routes_count, booking_count, custome_count
    finally:
        session.close()
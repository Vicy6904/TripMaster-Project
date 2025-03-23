import datetime
from io import BytesIO
import json
import secrets
import os
from flask import Flask, render_template, request, redirect, send_file, url_for, session, jsonify
import mysql
from database import *

app = Flask(__name__)
app.secret_key = "lodu"

# Set the upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.before_request
def create_session_on_first_visit():
    if 'user_id' not in session:
        session['user_id'] = f"user_{datetime.datetime.now().timestamp()}"
        session['user'] = str(secrets.token_urlsafe(10))
        session['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"New session created: {session['user_id']} at {session['created_at']}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def booking():
    packages = get_all_packages()
    bookings = get_booking()
    print(packages)
    return render_template('booking.html', packages=packages, bookings=bookings)



@app.route('/Packages')
def packages():
    packages = get_packages()
    return render_template('packages.html', packages=packages)

@app.route('/login-signup', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if authenticate_admin(username, password):
            session["admin"] = True
            print("Admin session set:", session["admin"])  # Debug print
            return redirect(url_for("admin"))
        
        if find_user(username, password):
            session['user'] = find_user(username, password)
            return redirect(url_for('home'))

        return render_template("login-signup.html", error="Invalid credentials")
    
    return render_template("login-signup.html")

@app.route("/add/user", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password == confirm_password:
        insert_user(username, email, password)
    else:
        return redirect(url_for('login'))
    
    return redirect(url_for('login'))

@app.route('/Admin')
def admin():
    package_count, buses_count, routes_count, booking_count, custome_count = count_admin()
    print("Session admin status:", session.get("admin"))  # Debug print
    if "admin" not in session:
        return redirect(url_for("login"))
    packages = get_packages()
    buses = get_buses()
    routes = get_route()
    customes = get_custome_route()
    bookings = get_booking()
    return render_template('admin.html', packages=packages, buses=buses ,routes=routes, customes=customes, bookings=bookings, package_count=package_count, buses_count=buses_count, routes_count=routes_count, booking_count=booking_count, custome_count=custome_count)

from flask import jsonify  # Import jsonify to return JSON responses

@app.route("/add_package", methods=["GET","POST"])
def add_package():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]
        package_type = request.form["type"]
        uploaded_image = None
        if "image" in request.files and request.files["image"].filename != "":
            uploaded_image = request.files["image"].read()

        insert_package(name, description, price, duration, package_type, uploaded_image)

        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route("/add_custom_package", methods=["GET", "POST"])
def add_custom_package():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        destination = request.form["destination"]
        duration = request.form["duration"]
        budget = request.form["budget"]
        activity = request.form.get("activity")
        # Insert the data into the database
        insert_custom_package(name,destination, duration, budget, activity)

        # Send success response
        return redirect(url_for('packages'))
    return redirect(url_for('packages'))

def authenticate_admin(username, password):
    # Load the admins' data from the JSON file
    with open('admins.json', 'r') as file:
        data = json.load(file)
    
    # Loop through the admins and check the username and password
    for admin in data['admins']:
        if admin['username'] == username and admin['password'] == password:
            return True
    return False



@app.route('/delete_package/<id>')
def delete_package(id):
    # Logic to delete the package from the database
    session = Session()
    try:
        session.delete(session.query(TravelPackages).filter(TravelPackages.id == id).first())
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('admin'))

@app.route("/package_image/<int:package_id>")
def get_package_image(package_id):
    """
    This function return jpg iamge
    that fatch form the database and
    convert perfact formate
    """
    session = Session()
    package_info = session.query(TravelPackages).filter_by(id=package_id).first()
    if package_info and package_info.image:
        return send_file(
            BytesIO(package_info.image),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name=f"{package_info.name}_image.jpg",
        )
    else:
        return "Image not found", 404

@app.route("/add-bus", methods=['GET', 'POST'])
def add_bus():
    if request.method == "POST":
        reg_number = request.form['reg_number']
        driver_name = request.form["driver_name"]
        insert_bus(reg_number=reg_number, driver_name=driver_name)
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route("/add-route", methods=['GET', 'POST'])
def add_route():
    if request.method == "POST":
        departure = request.form['departure']
        destination = request.form['destination']
        ass_buses = request.form['ass_buses']
        insert_route(departure=departure, destination=destination, ass_busses=ass_buses )
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route("/add-booking", methods=["GET", "POST"])
def submit_booking():
    if request.method == "POST":
        session = Session()
        try:
            package_id = request.form['package_id']
            type_id = package_id.split("-")
            print(type_id)
            if type_id[0] == "T":
                package = session.query(TravelPackages).filter_by(id=type_id[1]).first()
            else:
                package = session.query(CustomPackages).filter_by(id=type_id[1]).first()
            name = request.form['name']
            email = request.form['email']
            number = request.form['phone']
            start_date = request.form['start_date']
            date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = date_obj + datetime.timedelta(days=package.duration)
            number_of_people = request.form['number_of_people']
            insert_booking(package_name=package.name, name=name, email=email, number=number, start_date=start_date, end_date=end_date, number_of_people=number_of_people) 
        finally:
            session.close()
        return redirect(url_for('home'))
    return redirect(url_for('booking'))


@app.route("/confirm_booking/<int:id>", methods=["GET", "POST"])
def confirm_booking(id):
    if request.method == "POST":
        update_booking_status(id)
        return redirect(url_for('admin'))
    return redirect(url_for("admin"))

@app.route("/acccept_custom_package", methods=["GET", "POST"])
def acccept_custom_package():
    if request.method == "POST":
        id = request.form["custom_id"]
        acccept_custom(id=id)
        print(id)
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route("/delete-bus/<int:id>")
def delete_bus(id):
    session = Session()
    try:
        session.delete(session.query(Buses).filter(Buses.id == id).first())
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('admin'))


@app.route("/delete-routes/<int:id>")
def delete_routes(id):
    session = Session()
    try:
        session.delete(session.query(Routes).filter(Routes.id == id).first())
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    create_database()
    create_tables()
    app.run(debug=True)

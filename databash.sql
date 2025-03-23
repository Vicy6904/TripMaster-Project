CREATE DATABASE trip_master;

USE trip_master;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
);

CREATE TABLE TravelPackages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    duration INTEGER NOT NULL,  -- duration in days
    type TEXT NOT NULL,  -- Relaxation, Adventure, etc.
    image_path TEXT NOT NULL
);

CREATE TABLE Bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(package_id) REFERENCES TravelPackages(id)
);

CREATE TABLE TravelCompanies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    buses INTEGER NOT NULL,
    staff_count INTEGER NOT NULL,
    contact_info TEXT
);

CREATE TABLE Routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_location TEXT NOT NULL,
    end_location TEXT NOT NULL,
    distance REAL NOT NULL,  -- distance between start and end locations in kilometers
    travel_time INTEGER NOT NULL  -- estimated travel time in minutes
);

CREATE TABLE Buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    bus_number TEXT NOT NULL UNIQUE,
    capacity INTEGER NOT NULL,
    route_id INTEGER NOT NULL,
    driver_name TEXT NOT NULL,
    contact_info TEXT,
    FOREIGN KEY(company_id) REFERENCES TravelCompanies(id),
    FOREIGN KEY(route_id) REFERENCES Routes(id)
);

CREATE TABLE Testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    testimonial TEXT NOT NULL,
    rating INTEGER NOT NULL,  -- Rating from 1 to 5
    FOREIGN KEY(user_id) REFERENCES Users(id)
);

CREATE TABLE NewsletterSubscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE
);

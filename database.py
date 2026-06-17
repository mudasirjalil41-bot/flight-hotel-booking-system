import sqlite3

def get_db():
    conn =  sqlite3.connect("booking.db")
    conn.row_factory = sqlite3.Row
    return conn

def int_db():
    db = get_db()
    c = db.cursor()

    #____Users_____
    c.execute(""" CREATE TABLE IF USER NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    password text
    )
    """)

    #_____Hotels_____
    c.execute(""" CREATE TABLE IF USER NOT EXISTS hotels(
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    room INTEGER,
    price REAL
    )
    """)

    #_____Flights_____
    c.execute(""" CREATE TABLE IF USER NOT EXISTS flights(
    id INTEGER PRIMARY KEY,
    origin TEXT,
    destination TEXT,
    seats INTEGER,
    price REAL
    )
    """)

    #_____Booking_____
    c.execute(""" CREATE TABLE IF USER NOT EXISTS booking(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    type TEXT,
    ref_id INTEGER,
    paid INTEGER DEFAULT 0
    )
    """)

    db.commit()
    db.close()




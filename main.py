from database import get_db
from models import (User,Hotels,Flights,Booking)
from utils import hash_password,verify_password
from validators import safe_int,safe_str,safe_gmail
from datetime import datetime


def setup_db():
    db = get_db()
    cur = db.cursor()
    #____Users Table____
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT ,
                password TEXT,
                email TEXT UNIQUE
                )
                """)

    # ____Hotels Table____
    cur.execute("""CREATE TABLE IF NOT EXISTS hotels(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT ,
    city TEXT ,
    rooms INTEGER ,
    price FLOAT ,
    booking_date TEXT,  ___new colum
    )
    """)

    # ____Flights Table____
    cur.execute("""CREATE TABLE IF NOT EXISTS flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT,
    destination TEXT,
    seats INTEGER,
    price FLOAT,
    booking_date TEXT,  ___new colum

    )
    """)
    # ____Hotel_Booking Table____
    cur.execute("""CREATE TABLE IF NOT EXISTS hotels_bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    hotel_id INTEGER,
    paid FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id)
    )
    """)
    # ____flight_Booking Table____
    cur.execute("""CREATE TABLE IF NOT EXISTS flights_bookings(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id INTEGER NOT NULL,
     flight_id INTEGER,
     paid FLOAT,
     FOREIGN KEY (user_id) REFERENCES users(id),
     FOREIGN KEY (flight_id) REFERENCES flights(id)
     )
     """)
    db.commit()
    db.close()

def add_booking_data_colm():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("ALTER TABLE hotels_bookings ADD COLUMN booking_date TEXT")

    except Exception:
        pass


    try:
        cur.execute("ALTER TABLE flights_bookings ADD COLUMN booking_date TEXT")

    except Exception:
        pass
    db.commit()
    db.close()

# ----- Seed initial hotels and flights -----
def seed_data():
    db = get_db()
    cur = db.cursor()

    # Hotels
    hotels = [
            ("Grand Hotel", "New York", 50, 200.0),
            ("City Inn", "New York", 20, 120.0),
            ("Sea View Resort", "Miami", 30, 250.0),
        ]
    for name, city, rooms, price in hotels:
            cur.execute("INSERT INTO hotels (name, city, rooms, price) VALUES (?, ?, ?, ?)",
                        (name, city, rooms, price))

    # Flights
    flights = [
            ("New York", "Los Angeles", 100, 300.0),
            ("Miami", "Chicago", 80, 200.0),
            ("Los Angeles", "Miami", 120, 350.0),
        ]
    for origin, destination, seats, price in flights:
            cur.execute("INSERT INTO flights (origin, destination, seats, price) VALUES (?, ?, ?, ?)",
                        (origin, destination, seats, price))

    db.commit()
    db.close()

#______user functions______
def register_user():
    print("\n Registering new user")
    name = safe_str("name: ")
    email = safe_gmail("email: ")
    password = safe_str("password: ")


    # check email already exists
    if User.find_by_email(email):
        print("Email already registered!")
        return None
    # hash password before saving
    hashed_password = hash_password(password)
    #create user object and save db
    user = User(name = name,password = hashed_password,email = email)
    user.save()
    print(f"User registered! {user.name}")
    return user

def login():

    print("\n___login___")
    email = safe_str("email: ")
    password = safe_str("password: ")

    #find user by email
    user =  User.find_by_email(email)
    if not user:
        print("User does not exist!")
        return None

    # verify hash password
    if not verify_password(password, user.password):
        print("Wrong password!")
        return None

    print(f"Login successful! {user.name}")
    return user

# ____hotels functions____
def list_hotels():
    city = safe_str("city: ")
    hotels = Hotels.get_by_city(city)
    if not hotels:
        print("No hotels found!")
        return
    print(f"\nHotels: {hotels}")
    for h in hotels:
        print(f" {h.id}:  {h.name} |rooms: {h.rooms} | price: {h.price} ")

def list_flights():
    origin = safe_str("origin: ")
    destination = safe_str("destination: ")
    flights = Flights.get_by_route(origin, destination)
    if not flights:
        print("No flights found!")
        return
    print(f"\nFlights: {flights}")
    for f in flights:
        print(f" {f.id}: {f.origin} -> {f.destination} |seats: {f.seats} | price: {f.price}")

def booking(user):
    b_type = safe_str("Booking type (hotels/flights): ").strip().lower()
    if b_type == 'hotels':
        list_hotels()
        ref_id = safe_str("Select hotel ID: ")
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM hotels WHERE id = ?",(ref_id,))
        row = cur.fetchone()
        db.close()
        if not row:
            print("invalid hotel ID!")
            return
        price = row["price"]

    elif b_type == "flights":
        list_flights()
        ref_id = safe_str("Select flight ID: ")
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM flights WHERE id = ?",(ref_id,))
        row = cur.fetchone()
        db.close()
        if not row:
            print("invalid flight ID!")
            return
        price = row["price"]
    else:
        print("invalid type.")
        return

    date_time = safe_str("Enter booking date(YYYY MM DD HH MM)").strip()
    if date_time:
        try:
            booking_date = datetime.strptime(date_time,"%Y %m %d %H %M")
        except ValueError:
            print("invalid date format.")
            booking_date = datetime.now()

    else:
        booking_date = datetime.now()

    booking_obj = Booking(
        user_id=user.id,
        type=b_type,
        ref_id=ref_id,
        paid=price,
        scheduled_time = booking_date   # pass the date/time to your model
    )
    booking_obj.save()
    print(f"Booking successful! booking_id: {booking_obj.id}, paid: {booking_obj.paid}, scheduled: {booking_date}")




def cancel_booking():
    booking_id = safe_str("booking_id: ")
    Booking.cancel(booking_id)
    print(f"Cancel booking id: {booking_id}")


#_____main_____
def main():
    print("MAIN FUNCTION CALLED")

    setup_db()
    add_booking_data_colm()
    seed_data()

    current_user = None

    while True:
        if not current_user:
          print("1. Register\n2. Login\n0. Exit")
          choice = safe_int("choice: ")
          if choice == 1:
              current_user = register_user()

          elif choice == 2:
             current_user =  login()

          elif choice == 0:
              break

          else:
              print("invalid choice.")

        else:
            print("1. list hotels\n2. list flights\n3. booking\n4. cancel booking\n5. Logout")
            choice = safe_int("choice: ")
            if choice == 1:
                list_hotels()

            elif choice == 2:
               list_flights()

            elif choice == 3:
                booking(current_user)

            elif choice == 4:
                cancel_booking()

            elif choice == 5:
                current_user = None
                print("logout success full.")

            else:
                print("invalid choice.")

if __name__ == '__main__':
    main()






























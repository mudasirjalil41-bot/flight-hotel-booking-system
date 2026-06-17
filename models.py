import datetime
from database import get_db
class User:
    def __init__(self ,id = None, name = None,email = None, password = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        """Inset user into database"""
        db = get_db()
        cur = db.cursor()
        if self.id:
            cur.execute(
                """UPDATE users SET name = ?,email = ?,password = ?) WHERE id = ?""",
                        (self.name, self.email, self.password,self.id)
                        )

        else:
           cur.execute(
               """INSERT INTO users(name,email,password) VALUES(?,?,?)""",
                    (self.name,self.email,self.password)
                    )
           self.id = cur.lastrowid

        db.commit()
        db.close()




    @staticmethod
    def find_by_email(email):

        """Fid a user by email"""

        db = get_db()
        cur = db.cursor()
        cur.execute(
           "SELECT *FROM users WHERE lOWER(email) =LOWER(?)", (email,))
        row = cur.fetchone()
        db.close()
        if row:
            # Use tuple indices: id=0, name=1, password=2, email=3

            return User(id = row['id'],name = row['name'],email = row['email'],password = row["password"])
        return None






class Hotels:
    def __init__(self,id = None, name = None, city = None, rooms = None, price = None):
        self.id = id
        self.name = name
        self.city = city
        self.rooms = rooms
        self.price = price

    def save(self):
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO hotels(name,city,rooms,price)VALUES(?,?,?,?)",
                    (self.name,self.city,self.rooms,self.price))
        self.id = cur.lastrowid
        db.commit()
        db.close()





    @staticmethod
    def get_by_city(city):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM hotels WHERE LOWER(city) = LOWER(?)",(city.lower(),))
        rows = cur.fetchall()
        db.close()
        return [Hotels(id = r["id"],name = r["name"],city =r["city"],rooms = r["rooms"],price = r["price"]) for r in rows]


class Flights:
    def __init__(self,id = None,origin = None,destination = None,seats = None, price = None):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.price = price

    def save(self):
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO flights(origin,destination,seats,price)VALUES(?,?,?,?)",
                    (self.origin,self.destination,self.seats,self.price))
        self.id = cur.lastrowid
        db.commit()
        db.close()



    @staticmethod
    def get_by_route(origin,destination):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM flights WHERE LOWER(origin) = LOWER(?) AND LOWER(destination) =LOWER(?)",(origin.lower(),destination.lower()))
        rows = cur.fetchall()
        db.close()
        return [Flights(id = r["id"],origin = r["origin"],destination =r["destination"],seats = r["seats"],price = r["price"])for r in rows]



class Booking:
    def __init__(self,id = None,user_id = None,type = None,ref_id =None,paid = 0 ,scheduled_time = None):
        self.id = id
        self.user_id = user_id
        self.type = type.strip().lower()
        self.ref_id = ref_id
        self.paid = paid
        self.scheduled_time = scheduled_time or datetime.now

    def save(self):
        print("DEBUG TYPE:", repr(self.type))
        db = get_db()
        cur = db.cursor()

        if self.type == "hotels":
            table = "hotels_bookings"
            colum = "hotel_id"

        elif  self.type =="flights":
            table = "flights_bookings"
            colum = "flight_id"

        else:
            raise ValueError (f"invalid booking type {self.type}.")

        cur.execute(f"INSERT INTO {table} (user_id, {colum},paid,booking_date)VALUES(?,?,?,?)",
                    (self.user_id,self.ref_id,self.paid,self.scheduled_time.strftime("%Y-%m-%d,%H:%M")))
        self.id = cur.lastrowid
        db.commit()
        db.close()


    @staticmethod
    def cancel(booking_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM hotels_bookings WHERE id = ?",
                    (booking_id,))
        cur.execute("DELETE FROM flights_bookings WHERE id = ?",
                    (booking_id,))

        db.commit()
        db.close()







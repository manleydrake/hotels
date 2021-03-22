import database
import os.path
from random import randint
from datetime import date


def create_customer_profile(conn, conf_num, phone):
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    payment = input("Enter payment type: ")
    email = input("Enter email address: ")

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customer (confirmation_num, first_name, last_name, payment_type, email, phone_num) VALUES (?, ?, ?, ?, ?, ?)",
            (conf_num, first, last, payment, email, phone),
        )
        conn.commit()
    cur.close()


def display_available_rooms(conn):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT room_num, room_type FROM rooms WHERE status = 'Available';")
        avail_rooms = cur.fetchall()
        print(avail_rooms)
    cur.close()


def display_arrivals(conn):
    if conn is not None:
        cur = conn.cursor()
        today = date.today()
        sql = """SELECT * FROM reservation WHERE check_in_date = '%s'""" % today
        cur.execute(sql)
        arrivals = cur.fetchall()
        print(arrivals)
    cur.close()
    conn.close()


def display_departures(conn):
    if conn is not None:
        cur = conn.cursor()
        today = date.today()
        sql = """SELECT * FROM reservation WHERE check_out_date = '%s'""" % today
        cur.execute(sql)
        arrivals = cur.fetchall()
        print(arrivals)
    cur.close()
    conn.close()


def create_reservation(conn):
    conf_num = randint(1, 10000) * 1.2
    check_in = input("Enter desired check in date (YYYY-MM-DD): ")
    check_out = input("Enter desired check out date (YYYY-MM-DD): ")
    num_nights = int(input("Enter the number of nights: "))
    phone = int(input("Enter phone number in form xxxxxxxxxx: "))

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reservation (confirmation_num, num_nights, check_in_date, check_out_date, phone_num) VALUES (?, ?, ?, ?, ?)",
            (conf_num, num_nights, check_in, check_out, phone),
        )
        conn.commit()
    create_customer_profile(conn, conf_num, phone)


def check_in(conn):
    conf_num = int(input("Enter the confirmation number: "))
    room_num = int(input("Please assign a room number: "))

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rooms SET status = 'Occupied' WHERE room_num = ?", (room_num,)
        )
        cur.execute(
            "INSERT INTO booking (room_num, late_check_out) VALUES (?, 'No')",
            (room_num,),
        )
        cur.execute(
            "INSERT INTO booking (confirmation_num, num_nights, check_in_date, check_out_date, phone_num) SELECT * FROM reservation WHERE reservation.confirmation_num = ? AND booking.roon_num = ?",
            (conf_num, room_num),
        )

    conn.commit()


def check_out(conn):
    room_num = int(input("Enter the room you want to check out: "))

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rooms SET status = 'Needs Cleaning' WHERE room_num = ?", (room_num,)
        )
        cur.execute("DELETE FROM booking WHERE room_num = ?", (room_num,))
    conn.commit()


def request_late_check_out(conn):
    room_selected = int(input("Enter a room number: "))
    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE booking SET late_check_out = 'Yes' WHERE room_num = ?",
            (room_selected),
        )
    conn.commit()


def change_room_status(conn):
    room_num = int(input("Enter a room number: "))

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rooms SET status = 'Available' WHERE room_num = ?", (room_num,)
        )
    conn.commit()


def main():
    if not os.path.exists("hotel.db"):
        database.fill_db()
    else:
        print("db already set up")
        db = r"hotel.db"
        conn = database.create_connection(db)

    loop = True
    while loop:
        print("Enter 1 to view available rooms")
        print("Enter 2 to create a reservation")
        print("Enter 3 to check in a guest")
        print("Enter 4 to check out a guest")
        print("Enter 5 to mark a room as clean")
        print("Enter 6 to quit")
        choice = int(input("Enter option: "))

        if choice == 1:
            display_available_rooms(conn)
        elif choice == 2:
            create_reservation(conn)
        elif choice == 3:
            check_in(conn)
        elif choice == 4:
            check_out(conn)
        elif choice == 5:
            change_room_status(conn)
        else:
            loop = False
    conn.close()


main()

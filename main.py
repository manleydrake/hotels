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


def update_customer_profile(conn):
    confirmation_num = input("Enter confirmation number: ")
    fName = input("Enter the first name: ")
    lName = input("Enter the last name: ")
    payment = input("Enter payment method: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE customer SET  first_name = ?, last_name = ?, payment_type = ?, email = ?, phone_num = ? WHERE confirmation_num = ?",
            (fName, lName, payment, email, phone, confirmation_num),
        )
        conn.commit()


def display_available_rooms(conn):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM rooms WHERE status = 'Available';")
        avail_rooms = cur.fetchall()
        for i in range(len(avail_rooms)):
            for j in range(7):
                print(avail_rooms[i][j], end=" ")
            print()
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


def display_departures(conn):
    if conn is not None:
        cur = conn.cursor()
        today = date.today()
        sql = """SELECT * FROM reservation WHERE check_out_date = '%s'""" % today
        cur.execute(sql)
        arrivals = cur.fetchall()
        print(arrivals)
    cur.close()


def create_reservation(conn):
    conf_num = randint(1, 10000)
    check_in = input("Enter desired check in date (YYYY-MM-DD): ")
    check_out = input("Enter desired check out date (YYYY-MM-DD): ")
    num_nights = int(input("Enter the number of nights: "))
    phone = int(input("Enter phone number in form xxxxxxxxxx: "))
    res_status = "Reserved"

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reservation (confirmation_num, num_nights, check_in_date, check_out_date, phone_num, res_status) VALUES (?, ?, ?, ?, ?, ?)",
            (conf_num, num_nights, check_in, check_out, phone, res_status),
        )
        conn.commit()
    create_customer_profile(conn, conf_num, phone)
    print("Your confirmation number is: ", conf_num)


def check_in(conn):
    conf_num = input("Enter the confirmation number: ")
    room_num = int(input("Please assign a room number: "))

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rooms SET status = 'Occupied' WHERE room_num = ?", (room_num,)
        )

        cur.execute(
            "UPDATE reservation SET res_status = 'Checked_In' WHERE confirmation_num = ?",
            (conf_num,),
        )

        cur.execute(
            "SELECT num_nights from reservation WHERE confirmation_num = ?",
            (conf_num,),
        )
        num_nights = cur.fetchall()
        num_nights = num_nights[0][0]

        cur.execute(
            "SELECT check_in_date from reservation WHERE confirmation_num = ?",
            (conf_num,),
        )
        check_in_date = cur.fetchall()
        check_in_date = check_in_date[0][0]

        cur.execute(
            "SELECT check_out_date from reservation WHERE confirmation_num = ?",
            (conf_num,),
        )
        check_out_date = cur.fetchall()
        check_out_date = check_out_date[0][0]

        cur.execute(
            "SELECT phone_num from reservation WHERE confirmation_num = ?",
            (conf_num,),
        )
        phone_number = cur.fetchall()
        phone_number = phone_number[0][0]

        late = "No"

        print(
            room_num, conf_num, num_nights, check_in_date, check_out_date, phone_number
        )
        cur.execute(
            "INSERT INTO booking (room_num, confirmation_num, num_nights, check_in_date, check_out_date, phone_num, late_check_out) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                room_num,
                conf_num,
                num_nights,
                check_in_date,
                check_out_date,
                phone_number,
                late,
            ),
        )

    conn.commit()


def check_out(conn):
    room_num = int(input("Enter the room you want to check out: "))
    conf_num = input("Enter the confirmation number: ")

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rooms SET status = 'Needs Cleaning' WHERE room_num = ?", (room_num,)
        )
        cur.execute("DELETE FROM booking WHERE room_num = ?", (room_num,))
        cur.execute(
            "UPDATE reservation SET res_status = 'Checked Out' WHERE confirmation_num = ?",
            (conf_num,),
        )
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


def filter_rooms(conn):
    filter_room = int(input("How many people will be staying? "))
    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "SELECT room_num, max_capacity FROM rooms WHERE status = 'Available' and max_capacity >= ?",
            (filter_room,),
        )
        conn.commit()
        avail_rooms = cur.fetchall()
        for i in range(len(avail_rooms)):
            for j in range(2):
                print(avail_rooms[i][j], end=" ")
            print()


def mark_no_show(conn):
    conf_num = input("Enter the confirmation number: ")
    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE reservation SET res_status = 'No Show' WHERE confirmation_num = ?",
            (conf_num,),
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
        print("Enter 2 to sort rooms by max capacity")
        print("Enter 3 to create a reservation")
        print("Enter 4 to check in a guest")
        print("Enter 5 to check out a guest")
        print("Enter 6 to mark a room as clean")
        print("Enter 7 to update customer profile")
        print("Enter 8 to quit")
        choice = int(input("Enter option: "))

        if choice == 1:
            display_available_rooms(conn)
        elif choice == 2:
            filter_rooms(conn)
        elif choice == 3:
            create_reservation(conn)
        elif choice == 4:
            check_in(conn)
        elif choice == 5:
            check_out(conn)
        elif choice == 6:
            change_room_status(conn)
        elif choice == 7:
            update_customer_profile(conn)
        else:
            loop = False
    conn.close()


main()

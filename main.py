import database
import os.path
from random import randint
from datetime import date
from easygui import *


def create_customer_profile(conn, conf_num, phone):
    msg = "Enter Customer Information"
    title = "Customer Information"
    fieldNames = ["First Name", "Last Name", "Payment Type", "Email Address"]
    fieldValues = multenterbox(msg, title, fieldNames)
    first = fieldValues[0].strip()
    last = fieldValues[1].strip()
    payment = fieldValues[2].strip()
    email = fieldValues[3].strip()

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
        rooms = "Room #, Floor, Type, Pull Out, Max Cap, Price, Status \n"
        for i in range(len(avail_rooms)):
            for j in range(7):
                rooms += str(avail_rooms[i][j])
                rooms += " "
            rooms += "\n"
        msgbox(msg=rooms, title="Available Rooms")
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
    msg = "Enter Reservation Information"
    title = "Create Reservation"
    fieldNames = ["Check in Date (YYYY-MM-DD)", "Check out Date (YYYY-MM-DD)", "Number of Nights", "Phone Number"]
    fieldValues = multenterbox(msg, title, fieldNames)
    check_in = fieldValues[0].strip()
    check_out = fieldValues[1].strip()
    num_nights = fieldValues[2].strip()
    phone = fieldValues[3].strip()
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
    conf_num = enterbox(msg="Enter the confirmation number: ", title="Check In")

    if conn is not None:
        cur = conn.cursor()

        msg = "Select a Room Number"
        title = "Check In"
        cur.execute("SELECT room_num FROM rooms WHERE status = 'Available'")
        avail_rooms = [int(record[0]) for record in cur.fetchall()]
        choices = avail_rooms
        room_num = choicebox(msg, title, choices)

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
        msgbox(msg="Reservation checked in successfully.")
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
    room_num = enterbox(msg="Enter the room you want to check out: ", title="Check Out")
    conf_num = enterbox(msg="Enter the confirmation number: ", title="Check Out")

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
    msgbox(msg="Reservation has been checked out.")
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


def display_in_house_reservations(conn):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM booking")
        in_house = cur.fetchall()
        in_house_res = (
            "Room#, Conf#, #Nights, C/I Date,    C/O Date,    Phone#,   Late C/O \n"
        )
        for j in range(len(in_house)):
            for k in range(7):
                in_house_res += str(in_house[j][k])
                in_house_res += "    "
            in_house_res += "\n"
        msgbox(msg=in_house_res, title="In House")


def change_room_status(conn):
    room_num = enterbox(msg="Enter a room number: ", title="Update Room Status")

    if conn is not None:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rooms SET status = 'Available' WHERE room_num = ?", (room_num,)
        )
    msgbox(msg="Room status has been updated successfully.")
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
    conf_num = enterbox(
        msg="Enter the confirmation number: ", title="Mark Reservation as No Show"
    )
    if conf_num is None:
        msgbox(msg="Invalid confimation number entered.")
    else:
        if conn is not None:
            cur = conn.cursor()
            cur.execute(
                "UPDATE reservation SET res_status = 'No Show' WHERE confirmation_num = ?",
                (conf_num,),
            )
            msgbox(msg="Reservation status changed to No Show.")
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
        msg = "What Would You Like to Do?"
        title = "Options"
        choices = [
            "View Available Rooms",
            "View Reservations In House",
            "Sort Rooms by Max Capacity",
            "Create a New Reservation",
            "Check In",
            "Check Out",
            "Mark a Room as Clean",
            "Mark a Reservation as a No Show",
        ]
        choice = choicebox(msg, title, choices)

        if choice == "View Available Rooms":
            display_available_rooms(conn)
        elif choice == "View Reservations In House":
            display_in_house_reservations(conn)
        elif choice == "Sort Rooms by Max Capacity":
            filter_rooms(conn)
        elif choice == "Create a New Reservation":
            create_reservation(conn)
        elif choice == "Check In":
            check_in(conn)
        elif choice == "Check Out":
            check_out(conn)
        elif choice == "Mark a Room as Clean":
            change_room_status(conn)
        elif choice == "Mark a Reservation as a No Show":
            mark_no_show(conn)
        else:
            loop = False
    conn.close()


main()

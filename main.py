import database
import os.path
from random import randint
from datetime import date
from easygui import *
import pdb


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


def display_available_rooms(conn, display):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM rooms WHERE status = 'Available';")
        avail_rooms = cur.fetchall()
        if display:
            rooms = "Room #, Floor, Type, Pull Out, Max Cap, Price, Status \n"
            for i in range(len(avail_rooms)):
                for j in range(7):
                    rooms += str(avail_rooms[i][j])
                    rooms += " "
                rooms += "\n"
            msgbox(msg=rooms, title="Available Rooms")
        return avail_rooms
    cur.close()


def display_arrivals(conn):
    if conn is not None:
        cur = conn.cursor()
        today = date.today()
        sql = """SELECT * FROM reservation WHERE check_in_date = '%s'""" % today
        cur.execute(sql)
        arrivals = cur.fetchall()
        msg = "What Would You Like to Do?"
        title = "Options"
        choices = ["Conf Num/Num Nights/Check In/Check Out/Phone/Status"]
        for i in range(len(arrivals)):
            arr = ""
            for j in range(6):
                arr += str(arrivals[i][j])
                arr += " "
            choices.append(arr)
        choice = choicebox(msg, title, choices)
        conf_num = choice.split(" ")
        conf_num = conf_num[0]
        check_in(conn, conf_num)

    cur.close()


def display_departures(conn):
    if conn is not None:
        cur = conn.cursor()
        today = date.today()
        sql = """SELECT * FROM reservation WHERE check_out_date = '%s'""" % today
        cur.execute(sql)
        departures = cur.fetchall()
        msg = "What Would You Like to Do?"
        title = "Options"
        choices = ["Conf Num/Num Nights/Check In/Check Out/Phone/Status"]
        for i in range(len(departures)):
            arr = ""
            for j in range(6):
                arr += str(departures[i][j])
                arr += " "
            choices.append(arr)
        choice = choicebox(msg, title, choices)
        conf_num = choice.split(" ")
        conf_num = conf_num[0]
        check_out(conn, conf_num)
    cur.close()


def create_reservation(conn):
    conf_num = randint(1, 10000)
    msg = "Enter Reservation Information"
    title = "Create Reservation"
    fieldNames = [
        "Check in Date (YYYY-MM-DD)",
        "Check out Date (YYYY-MM-DD)",
        "Number of Nights",
        "Phone Number",
    ]
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


def check_in(conn, conf_num):
    avail_rooms = display_available_rooms(conn, False)
    msg = "Click on an available room to check in to"
    title = "Options"
    choices = ["Room #/Floor/Type/Pull Out/Max Cap/Price/Status"]
    for i in range(len(avail_rooms)):
        arr = ""
        for j in range(7):
            arr += str(avail_rooms[i][j])
            arr += " "
        choices.append(arr)
    choice = choicebox(msg, title, choices)
    room_num = choice.split(" ", 1)
    room_num = int(choice[0])
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


def check_out(conn, conf_num):
    room_num = enterbox("Enter the room number to be checked out", "Check Out", "")

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
    room_num = enterbox("Enter the room number to change", "Change Room Status", "")

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
        msg = "What Would You Like to Do?"
        title = "Options"
        choices = [
            "View Available Rooms",
            "Sort Rooms by Max Capacity",
            "Create a New Reservation",
            "Check In",
            "Check Out",
            "Mark a Room as Clean",
            "View Arrivals Today",
            "View Departures Today",
            "Change Room Status"
        ]
        choice = choicebox(msg, title, choices)

        if choice == "View Available Rooms":
            display_available_rooms(conn, True)
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
        elif choice == "View Arrivals Today":
            display_arrivals(conn)
        elif choice == "View Departures Today":
            display_departures(conn)
        elif choice == "Change Room Status":
            change_room_status(conn)
        else:
            loop = False
    conn.close()


main()

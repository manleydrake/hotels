import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def fill_db():
    database = r"hotel.db"

    create_rooms_table = """ CREATE TABLE IF NOT EXISTS rooms (
                                        room_num integer PRIMARY KEY,
                                        floor integer NOT NULL,
                                        room_type text NOT NULL,
                                        sofa_bed text NOT NULL,
                                        max_capacity integer NOT NULL,
                                        price integer NOT NULL,
                                        status text NOT NULL
                                    ); """

    create_booking_table = """CREATE TABLE IF NOT EXISTS booking (
                                        room_num integer PRIMARY KEY,
                                        confirmation_num text NOT NULL,
                                        num_nights integer NOT NULL,
                                        check_in_date text NOT NULL,
                                        check_out_date text NOT NULL,
                                        phone_num text NOT NULL,
                                        late_check_out text NULL,
                                        FOREIGN KEY (confirmation_num) REFERENCES rooms (room_num)
                                    );"""

    create_customer_table = """CREATE TABLE IF NOT EXISTS customer (
                                    confirmation_num integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    payment_type text NOT NULL,
                                    email text NOT NULL,
                                    phone_num integer NOT NULL
                                );"""

    create_reservation_table = """CREATE TABLE IF NOT EXISTS reservation (
                                            confirmation_num text PRIMARY KEY,
                                            num_nights integer NOT NULL,
                                            check_in_date text NOT NULL,
                                            check_out_date text NOT NULL,
                                            phone_num text NOT NULL
                                        );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create rooms table
        create_table(conn, create_rooms_table)

        # create booking table
        create_table(conn, create_booking_table)

        # create customer table
        create_table(conn, create_customer_table)

        # create reservation table
        create_table(conn, create_reservation_table)
    else:
        print("Error! cannot create the database connection.")

    # fill rooms table
    if conn is not None:
        insert = """ INSERT INTO rooms (room_num, floor, room_type, sofa_bed, max_capacity, price, status)
                        VALUES (100, 1, "King", "No", 2, 120, "Available"), 
                        (101, 1, "King", "No", 2, 120, "Available"),
                        (102, 1, "2Queen", "Yes", 6, 140, "Available"),
                        (103, 1, "KingSuite", "Yes", 4, 130, "Available"),
                        (200, 2, "King", "No", 2, 120, "Available"),
                        (201, 2, "KingSuite", "Yes", 4, 130, "Available"),
                        (202, 2, "2Queen", "Yes", 6, 140, "Available"),
                        (203, 2, "King", "No", 2, 120, "Available"),
                        (204, 2, "2Queen", "Yes", 6, 140, "Available"),
                        (205, 2, "King", "No", 2, 120, "Available"),
                        (206, 2, "KingSuite", "Yes", 4, 130, "Available"),
                        (207, 2, "King", "No", 2, 120, "Available"),
                        (208, 2, "KingSuite", "Yes", 4, 130, "Available"),
                        (300, 3, "KingSuite", "Yes", 4, 130, "Available"),
                        (301, 3, "King", "No", 2, 120, "Available"),
                        (302, 3, "2Queen", "Yes", 6, 140, "Available"),
                        (303, 3, "2Queen", "Yes", 6, 140, "Available"),
                        (304, 3, "KingSuite", "Yes", 4, 130, "Available"),
                        (305, 3, "King", "No", 2, 120, "Available"),
                        (306, 3, "King", "No", 2, 120, "Available"),
                        (307, 3, "KingSuite", "Yes", 4, 130, "Available"),
                        (308, 3, "2Queen", "Yes", 6, 140, "Available"); """
        cur = conn.cursor()
        cur.execute(insert)
        conn.commit()

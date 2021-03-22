def filter_rooms(conn): 
	filter_room = int(input("How many people will be staying? "))

	if conn is not None: 
		cur = conn.cursor()
		cur.execute("SELECT room_num, capacity FROM rooms WHERE status = 'Available' and capacity >= ?, (filter_room);")
		conn.commit()

def update_status(conn):
	if conn is not None: 
		cur = conn.cursor()
		cur.execute("UPDATE rooms JOIN reservation ON rooms.room_num = reservation.room_num SET rooms.status="Available" WHERE reservation.room_num = ?, (room_num)";



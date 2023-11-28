from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_connection():
    return sqlite3.connect('hotel.db')

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_beds INTEGER,
            num_rooms INTEGER,
            num_sofas INTEGER,
            price INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(num_beds, num_rooms, num_sofas, price):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rooms (num_beds, num_rooms, num_sofas, price) VALUES (?, ?, ?, ?)',
                   (num_beds, num_rooms, num_sofas, price))
    conn.commit()
    conn.close()

def update_data(room_id, num_beds, num_rooms, num_sofas, price):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE rooms SET num_beds=?, num_rooms=?, num_sofas=?, price=? WHERE id=?',
                   (num_beds, num_rooms, num_sofas, price, room_id))
    conn.commit()
    conn.close()

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        num_beds = request.form['num_beds']
        num_rooms = request.form['num_rooms']
        num_sofas = request.form['num_sofas']
        price = request.form['price']
        insert_data(num_beds, num_rooms, num_sofas, price)
        return redirect('/')
    return render_template('add_edit_room.html', action='Add', room=None)

@app.route('/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms WHERE id=?', (room_id,))
    room = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        num_beds = request.form['num_beds']
        num_rooms = request.form['num_rooms']
        num_sofas = request.form['num_sofas']
        price = request.form['price']
        update_data(room_id, num_beds, num_rooms, num_sofas, price)
        return redirect('/')
    
    return render_template('add_edit_room.html', action='Edit', room=room)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize the database and create the table
def init_db():
    conn = sqlite3.connect("vehicle.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,  -- ID column as primary key
            name TEXT NOT NULL,      -- Name column
            brand TEXT NOT NULL,     -- Brand column
            fuel_type TEXT NOT NULL   -- Fuel Type column
        );
    ''')
    conn.commit()
    conn.close()

# Call the database initialization
init_db()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    # Fetch data from the submitted form
    vehicle_id = request.form.get('id')  # Fetching the ID
    name = request.form.get('name')
    brand = request.form.get('brand')
    fuel_type = request.form.get('fuel-type')

    # Print data to the console (optional)
    print(f"ID: {vehicle_id}, Name: {name}, Brand: {brand}, Fuel Type: {fuel_type}")

    # Insert data into the database
    try:
        conn = sqlite3.connect("vehicle.db")
        cursor = conn.cursor()
        
        # Insert the data, including the ID
        cursor.execute('''
            INSERT INTO vehicles (id, name, brand, fuel_type) VALUES (?, ?, ?, ?)
        ''', (vehicle_id, name, brand, fuel_type))
        
        # Commit the transaction
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Error: Vehicle with ID {vehicle_id} already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    # Redirect to the home page or any other page after submission
    return redirect(url_for('home'))


@app.route('/vehicles')
def display_vehicles():
    # Connect to the SQLite database
    conn = sqlite3.connect("vehicle.db")
    cursor = conn.cursor()

    # Fetch all vehicle data
    cursor.execute('SELECT * FROM vehicles')
    vehicles = cursor.fetchall()

    # Close the connection
    conn.close()

    # Pass the data to the 'result.html' template for rendering
    return render_template('result.html', vehicles=vehicles)


if __name__ == '__main__':
    app.run(debug=True)

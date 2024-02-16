import sqlite3
from datetime import datetime, timedelta
from datetime import *
import streamlit as st

def calculate_time_intervals(start_time, end_time, interval_length):

    if not isinstance(start_time, time):
        raise TypeError("start_time must be a datetime.time object.")
    if not isinstance(end_time, time):
        raise TypeError("end_time must be a datetime.time object.")
    if not isinstance(interval_length, timedelta):
        raise TypeError("interval_length must be a datetime.timedelta object.")

    # Ensure start_time is earlier than end_time for correct processing
    if start_time > end_time:
        end_time += datetime.timedelta(days=1)  # Wrap to the next day if necessary

    start_datetime = datetime.combine(date.today(), start_time)
    end_datetime = datetime.combine(date.today(), end_time)

    # Create an iterator of timedelta objects representing consecutive intervals
    time_intervals = iter(lambda: interval_length, None)
    # Generate intervals within the workday timeframe
    intervals = []
    current_datetime = start_datetime
    while current_datetime < end_datetime:
        next_interval = next(time_intervals)
        next_datetime = current_datetime + next_interval
        if next_datetime <= end_datetime:
            intervals.append(current_datetime.time())
        current_datetime = next_datetime

    return intervals

def get_user_id_by_username(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT person_id FROM personal_info WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            print(f"User with username {username} not found.")
            return None
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        return None

def add_info_doc(conn,username,specialty):
    try:
        user_id = get_user_id_by_username(conn, username)

        if user_id is not None:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id_doctor FROM info_doctor WHERE id_doctor = ?
            ''', (user_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                pass
            else:
                cursor.execute('''
                    INSERT INTO info_doctor (id_doctor, id_specialty)
                    VALUES (?, ?)
                ''', (user_id, specialty))

            conn.commit()
        else:
            print(f"User profile not saved. User with username {username} not found.")
    except sqlite3.Error as e:
        print(f"Error 138")
def save_doc_sched(conn, username, day, start_time, end_time):
    try:
        doc_id = get_user_id_by_username(conn, username)
        cursor = conn.cursor()
        interval_length = timedelta(minutes=20)
        cursor.execute('''SELECT * FROM schedule WHERE id_doctor = ? AND date = ?''', (doc_id, day))
        existing = cursor.fetchone()
        if start_time != None and end_time != None:
            time_intervals = calculate_time_intervals(start_time, end_time, interval_length)

            if existing:
                for interval in time_intervals:
                    hr = interval.strftime('%H:%M:%S')
                    cursor.execute('UPDATE schedule SET hour=? WHERE id_doctor=? AND date=? AND hour=?', (hr, doc_id, day, hr))
            else:
                for interval in time_intervals:
                    hr = interval.strftime('%H:%M:%S')
                    cursor.execute('INSERT INTO schedule (id_doctor, date, hour) VALUES (?, ?, ?)', (doc_id, day, hr))


        conn.commit()
    except sqlite3.Error as e:
        print("Error saving doctor schedule:", e)


def get_doctor_schedule(conn, username):
    cursor = conn.cursor()
    doc_id = get_user_id_by_username(conn, username)
    
    cursor.execute('''
        SELECT date, hour
        FROM schedule
        WHERE id_doctor = ?
        ORDER BY date
    ''', (doc_id,))

    schedule = cursor.fetchall()

    # Create a dictionary to store the first and last hour for each date
    schedule_dict = {}

    for date, hour in schedule:
        # Check if the date is already in the dictionary
        if date in schedule_dict:
            # Update the maximum and minimum hours for the existing date
            schedule_dict[date] = (min(schedule_dict[date][0], hour), max(schedule_dict[date][1], hour))
        else:
            # Add the date to the dictionary with the initial hour
            schedule_dict[date] = (hour, hour)

    return schedule_dict





def modify_schedule_for_doctor(conn, doctor_id):
    try:
        # Disable foreign key checks
        conn.execute("PRAGMA foreign_keys = OFF;")

        # Delete rows from 'schedule' where id_doctor = doctor_id
        conn.execute("DELETE FROM schedule WHERE id_doctor = ?;", (doctor_id,))

        # Enable foreign key checks
        conn.execute("PRAGMA foreign_keys = ON;")

        # Commit the changes
        conn.commit()

        print("Schedule modified successfully.")
    except Exception as e:
        # Handle any exceptions
        print(f"Error modifying schedule: {e}")

def modify_week_for_doctor(conn, doctor_id):
    try:
        # Disable foreign key checks
        conn.execute("PRAGMA foreign_keys = OFF;")

        # Delete rows from 'schedule' where id_doctor = doctor_id
        conn.execute("DELETE FROM week_hours WHERE id_doctor = ?;", (doctor_id,))

        # Enable foreign key checks
        conn.execute("PRAGMA foreign_keys = ON;")

        # Commit the changes
        conn.commit()

        print("Schedule modified successfully.")
    except Exception as e:
        # Handle any exceptions
        print(f"Error modifying schedule: {e}")

def check_if_exists(conn,username):
    doc_id = get_user_id_by_username(conn,username)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM week_hours WHERE id_doctor = ?',(doc_id,))
    exist = cursor.fetchone()

    if exist:
        return True
    else:
        return False
    
def week_hours(conn,username,day,start_time,end_time):
    cursor = conn.cursor()
    
    doc_id = get_user_id_by_username(conn,username)

    start_time_str = start_time.strftime('%H:%M:%S')
    end_time_str = end_time.strftime('%H:%M:%S')
    cursor.execute('SELECT * FROM week_hours WHERE id_doctor = ? AND day = ?', (doc_id, day))
    existing = cursor.fetchone()

    if existing:
        existing_day = existing[3]  # Replace 'day' with the actual column name
        cursor.execute('UPDATE week_hours SET start = ?, end = ? WHERE id_doctor = ? AND day = ?', (start_time_str, end_time_str, doc_id, existing_day))
    else:
        cursor.execute('INSERT INTO week_hours (id_doctor, day, start, end) VALUES (?, ?, ?, ?)', (doc_id, day, start_time_str, end_time_str))

    conn.commit()

def get_doctors_by_city_and_specialty(conn, city, specialty):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT personal_info.first_name, personal_info.last_name
        FROM personal_info
        JOIN city ON personal_info.id_city = city.id
        JOIN info_doctor ON personal_info.person_id = info_doctor.id_doctor
        JOIN specialties ON info_doctor.id_specialty = specialties.id
        WHERE city.city = ? AND specialties.specialty = ?
    ''', (city, specialty))

    doctors =  cursor.fetchall()
    return doctors

def get_available_hours(conn, doctor_name, selected_date):
    cursor = conn.cursor()

    # Extract the first name and last name of the doctor from the doctor_name string
    first_name, last_name = doctor_name.split(' ')[1], doctor_name.split(' ')[2]

    # Query to fetch available hours for the selected doctor on the selected date
    cursor.execute('''
        SELECT s.hour
        FROM schedule s
        LEFT JOIN appointments a ON s.date = a.date AND s.hour = a.hour
        JOIN personal_info p ON s.id_doctor = p.person_id
        WHERE p.first_name = ? AND p.last_name = ?
        AND s.date = ?
        AND a.date IS NULL
    ''', (first_name, last_name, selected_date))

    available_hours = [row[0] for row in cursor.fetchall()]

    return available_hours

def save_appointment(conn, doctor_name, username, selected_date, selected_hour):
    cursor = conn.cursor()

    patient_id = get_user_id_by_username(conn, username)
    # Extract the first name and last name of the doctor from the doctor_name string
    first_name, last_name = doctor_name.split(' ')[1], doctor_name.split(' ')[2]

    # Get the doctor's ID from the personal_info table
    cursor.execute('''
        SELECT person_id
        FROM personal_info
        WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    doctor_id = cursor.fetchone()[0]

    # Insert the appointment into the appointments table
    cursor.execute('''
        INSERT INTO appointments (doctor_id, patient_id, date, hour)
        VALUES (?, ?, ?, ?)
    ''', (doctor_id, patient_id, selected_date, selected_hour))

    # Commit the transaction
    conn.commit()

def get_doctor_names(conn,username):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT first_name, last_name, phone FROM personal_info WHERE person_id = ?',(username,))
        details = cursor.fetchone()

        if details:
            first_name, last_name, phone_number = details
            return first_name, last_name, phone_number
        else:
            return None, None, None
    except sqlite3.Error as e:
        print("Error getting doctor names:", e)
        return None, None
    
def is_schedule_exist_for_day(conn, id_doctor, current_date):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM schedule WHERE id_doctor=? AND date=?"
        cursor.execute(query, (id_doctor, current_date))
        result = cursor.fetchone()
        
        if result:
            return True  # Schedule exists
        else:
            return False  # Schedule does not exist
    except Exception as e:
        print(f"Error checking schedule existence: {e}")
        return False
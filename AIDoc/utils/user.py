import sqlite3

def save_user_info(conn, first_name, last_name, email, phone, username, id_role, id_city):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT * FROM personal_info WHERE username = ?
                       ''', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute('''
                           UPDATE personal_info
                           SET first_name = ?, last_name = ?, phone = ?
                           WHERE username=?
                           ''', (first_name,last_name,phone, username))
        else:
            cursor.execute('''
                            INSERT INTO personal_info (first_name, last_name,email, phone, username, id_role, id_city)
                            VALUES(?, ?, ?, ?, ?, ?, ?)
                           ''',(first_name,last_name,email,phone,username,id_role,id_city))
        
        conn.commit()
        subprocess.run(["git", "add", "AIDoc/aidoc.db"])
        subprocess.run(["git", "commit", "-m", "Update SQLite database with new data"])
        subprocess.run(["git", "push", "origin", "main"])
    except sqlite3.Error as e:
        print(f"error 46 {e}")

def get_tel_num(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT phone
                       FROM personal_info
                       WHERE username = ?
                       ''',(username,))
        telephone = cursor.fetchone()
        return (telephone[0]) if telephone else None
    except sqlite3.Error as e:
        print(f"Error 73")
        return None
    
def get_first_name(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT first_name
                       FROM personal_info
                       WHERE username = ?
                       ''', (username,))
        first_name = cursor.fetchone()
        return (first_name[0]) if first_name else None
    except sqlite3.Error as e:
        print("Error 87")
        return None
    
def get_firsty_name(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT first_name
                       FROM personal_info
                       WHERE person_id = ?
                       ''', (username,))
        first_name = cursor.fetchone()
        return (first_name[0]) if first_name else None
    except sqlite3.Error as e:
        print("Error 87")
        return None
    
def get_last_name(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT last_name
                       FROM personal_info
                       WHERE username = ?
                       ''', (username,))
        last_name = cursor.fetchone()
        return (last_name[0]) if last_name else None
    except sqlite3.Error as e:
        print("Error 101")
        return None
    
def get_lasty_name(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT last_name
                       FROM personal_info
                       WHERE person_id = ?
                       ''', (username,))
        last_name = cursor.fetchone()
        return (last_name[0]) if last_name else None
    except sqlite3.Error as e:
        print("Error 101")
        return None
    
def get_tel_number(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT phone
                       FROM personal_info
                       WHERE person_id = ?
                       ''', (username,))
        first_name = cursor.fetchone()
        return (first_name[0]) if first_name else None
    except sqlite3.Error as e:
        print("Error 87")
        return None
    
def change_user_role(conn, username, new_role):
    try:
        save_user_role(conn, username, new_role)
    except sqlite3.Error as e:
        print("Error 115")


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

def save_user_profile(conn, username, age, sex, pregnancies, height, weight):
    try:
        user_id = get_user_id_by_username(conn, username)

        if user_id is not None:
            cursor = conn.cursor()

            # Check if user profile already exists
            cursor.execute('''
                SELECT id_patient FROM info_patient WHERE id_patient = ?
            ''', (user_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute('''
                    UPDATE info_patient
                    SET age=?, sex=?, pregnancies=?, height=?, weight=?
                    WHERE id_patient=?
                ''', (age, sex, pregnancies, height, weight, user_id))
            else:
                cursor.execute('''
                    INSERT INTO info_patient (id_patient, age, sex, pregnancies, height, weight)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, age, sex, pregnancies, height, weight))

            conn.commit()
            subprocess.run(["git", "add", "AIDoc/aidoc.db"])
            subprocess.run(["git", "commit", "-m", "Update SQLite database with new data"])
            subprocess.run(["git", "push", "origin", "main"])
        else:
            print(f"User profile not saved. User with username {username} not found.")
    except sqlite3.Error as e:
        print(f"Error 138")

def save_user_role(conn, username, role):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE personal_info
                       SET id_role = ?
                       WHERE username = ?
                       ''', (role,username))
        conn.commit()
        subprocess.run(["git", "add", "AIDoc/aidoc.db"])
        subprocess.run(["git", "commit", "-m", "Update SQLite database with new data"])
        subprocess.run(["git", "push", "origin", "main"])
    except sqlite3.Error as e:
        print("Error 172")

def get_user_profile(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personal_info WHERE username = ?', (username,))
    return cursor.fetchone()
def get_age_of_user(conn, username):
    cursor = conn.cursor()
    user_id = get_user_id_by_username(conn,username)
    cursor.execute('''
                SELECT id_patient FROM info_patient WHERE id_patient = ?
            ''', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('SELECT age FROM info_patient WHERE id_patient = ?', (user_id,))
    age = cursor.fetchone()
    return age[0] if age else None
def get_height_of_user(conn, username):
    cursor = conn.cursor()
    user_id = get_user_id_by_username(conn,username)
    cursor.execute('''
                SELECT id_patient FROM info_patient WHERE id_patient = ?
            ''', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('SELECT height FROM info_patient WHERE id_patient = ?', (user_id,))
    height = cursor.fetchone()
    return height[0] if height else None
def get_sex_of_user(conn, username):
    cursor = conn.cursor()
    user_id = get_user_id_by_username(conn,username)
    cursor.execute('''
                SELECT id_patient FROM info_patient WHERE id_patient = ?
            ''', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('SELECT sex FROM info_patient WHERE id_patient = ?', (user_id,))
    sex = cursor.fetchone()
    return sex[0] if sex else None
def get_kilo_of_user(conn, username):
    cursor = conn.cursor()
    user_id = get_user_id_by_username(conn,username)
    cursor.execute('''
                SELECT id_patient FROM info_patient WHERE id_patient = ?
            ''', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('SELECT weight FROM info_patient WHERE id_patient = ?', (user_id,))
    weight = cursor.fetchone()
    return weight[0] if weight else None
def get_pregnancies_of_user(conn, username):
    cursor = conn.cursor()
    user_id = get_user_id_by_username(conn,username)
    cursor.execute('''
                SELECT id_patient FROM info_patient WHERE id_patient = ?
            ''', (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('SELECT pregnancies FROM info_patient WHERE id_patient = ?', (user_id,))
    pregnancies = cursor.fetchone()
    return pregnancies[0] if pregnancies else None
def get_user_role(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT id_role FROM personal_info WHERE username = ?',(username,))
    role = cursor.fetchone()
    return role[0] if role else None

def get_user_appointments(conn,username):
    cursor = conn.cursor()
    pt_id = get_user_id_by_username(conn,username)
    cursor.execute('''
                   SELECT doctor_id, date, hour
                   FROM appointments
                   WHERE patient_id = ?
                   ''',(pt_id,))
    appointments = cursor.fetchall()

    return appointments

def get_doctor_appointments(conn,username):
    doc_id = get_user_id_by_username(conn,username)
    try:
        cursor = conn.cursor()
        cursor.execute('''
                        SELECT patient_id, date, hour
                        FROM appointments
                        WHERE doctor_id = ?
                        ''',(doc_id,))
        doc_app = cursor.fetchall()

        return doc_app
    except sqlite3.Error as e:
        print("Error fetching doctor appointments:", e)
        return []

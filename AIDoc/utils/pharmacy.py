def select_pharmacies_by_medication(cursor, medication_name):
    cursor.execute('''
        SELECT pharmacies.name, pharmacies.latitude, pharmacies.longitude
        FROM pharmacies
        JOIN stock ON pharmacies.id = stock.id_pharmacy
        JOIN medication ON stock.id_medication = medication.id
        WHERE medication.name = ?
    ''', (medication_name,))

    pharmacies = cursor.fetchall()
    return pharmacies

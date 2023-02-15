kurssit = db.execute("SELECT K.nimi, COUNT(Ko.opettaja_id) FROM Kurssit K LEFT JOIN Kurssinopettajat Ko ON Ko.kurssi_id = K.id GROUP BY K.id ORDER BY K.nimi").fetchall()
    return kurssit
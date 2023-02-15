def random():
    ryhmat = db.execute("SELECT R.nimi, SUM(K.op) FROM Ryhmat R LEFT JOIN Ryhmanjasenet Rj ON Rj.ryhma_id=R.id LEFT JOIN Opiskelijat O ON Rj.opiskelija_id = O.id LEFT JOIN Kurssisuoritukset Ks ON Ks.opiskelija_id = O.id LEFT JOIN Kurssit K ON Ks.kurssi_id = K.id GROUP BY R.nimi").fetchall()
    return ryhmat
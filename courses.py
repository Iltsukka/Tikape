import os
import sqlite3

# poistaa tietokannan alussa (kätevä moduulin testailussa)
os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

# luo tietokantaan tarvittavat taulut
def create_tables():
    db.execute("CREATE TABLE Opettajat (id INTEGER PRIMARY KEY, nimi TEXT)")
    db.execute("CREATE TABLE Kurssit (id INTEGER PRIMARY KEY, nimi TEXT, op INTEGER)")
    db.execute("CREATE TABLE Kurssinopettajat (kurssi_id INTEGER REFERENCES Kurssit, opettaja_id INTEGER REFERENCES Opettajat)")
    db.execute("CREATE TABLE Opiskelijat (id INTEGER PRIMARY KEY, nimi TEXT)")
    db.execute("CREATE TABLE Kurssisuoritukset (id INTEGER PRIMARY KEY, opiskelija_id INTEGER REFERENCES Opiskelijat, kurssi_id INTEGER REFERENCES Kurssit, date TEXT, grade INTEGER)")
    db.execute("CREATE TABLE Ryhmat (id INTEGER PRIMARY KEY, nimi TEXT)")
    db.execute("CREATE TABLE Ryhmanjasenet (id INTEGER PRIMARY KEY, ryhma_id INTEGER REFERENCES Ryhmat, opettaja_id INTEGER REFERENCES Opettajat, opiskelija_id INTEGER REFERENCES Opiskelijat)")

# lisää opettajan tietokantaan
def create_teacher(name):
    opettaja = db.execute("INSERT INTO Opettajat (nimi) VALUES (?)", [name])
    return opettaja.lastrowid

# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
    kurssi = db.execute("INSERT INTO Kurssit (nimi, op) VALUES (?,?)", [name, credits])
    l = kurssi.lastrowid
    k = 0
    while k < len(teacher_ids):
        db.execute("INSERT INTO Kurssinopettajat (kurssi_id, opettaja_id) VALUES (?,?)", [l,teacher_ids[k]])
        k += 1
    return l
# lisää opiskelijan tietokantaan
def create_student(name):
    opiskelija = db.execute("INSERT INTO Opiskelijat (nimi) VALUES (?)", [name])
    return opiskelija.lastrowid

# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
    suoritus = db.execute("INSERT INTO Kurssisuoritukset (opiskelija_id, kurssi_id, date, grade) VALUES (?,?,?,?)", [student_id, course_id, date, grade])
    return suoritus.lastrowid

# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):
    ryhma = db.execute("INSERT INTO Ryhmat (nimi) VALUES (?)", [name])
    v = ryhma.lastrowid
    for i in range(len(teacher_ids)):
        for k in range(len(student_ids)):
            db.execute("INSERT INTO Ryhmanjasenet (ryhma_id, opettaja_id, opiskelija_id) VALUES (?,?,?)", [v, teacher_ids[i], student_ids[k]])
    
    return v
    

# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    kurssit = db.execute("SELECT K.nimi FROM Kurssit K, Opettajat O, Kurssinopettajat T WHERE T.kurssi_id = K.id AND T.opettaja_id = O.id AND O.nimi =? ORDER BY O.nimi", [teacher_name]).fetchall()
    return [x[0] for x in kurssit]

# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    opintopisteet = db.execute("SELECT (K.op * COUNT(Ks.kurssi_id)) FROM Opettajat O, Kurssit K, Kurssisuoritukset Ks, Kurssinopettajat Ko WHERE Ks.kurssi_id = K.id AND Ko.kurssi_id = K.id AND Ko.opettaja_id = O.id AND O.nimi=?", [teacher_name]).fetchone()
    return opintopisteet[0] 
# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    kurssit = db.execute("SELECT K.nimi, Ks.grade FROM Kurssit K, Opiskelijat O, Kurssisuoritukset Ks WHERE Ks.opiskelija_id = O.id AND Ks.kurssi_id = K.id AND O.nimi=? ORDER BY K.nimi", [student_name]).fetchall()
    return kurssit
# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    pass

# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
    arvosanat = db.execute("SELECT Ks.grade FROM Kurssisuoritukset Ks, Kurssit K WHERE Ks.kurssi_id = K.id AND K.nimi=?", [course_name]).fetchall()
    arvosanat = [x[0] for x in arvosanat]
    sanakirja = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for luku in arvosanat:
        sanakirja[luku] += 1
    return sanakirja

# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    kurssit = db.execute("SELECT K.nimi, COUNT(DISTINCT Ko.opettaja_id), COUNT(DISTINCT Ks.opiskelija_id) FROM Kurssit K LEFT JOIN Kurssinopettajat Ko ON Ko.kurssi_id = K.id LEFT JOIN Kurssisuoritukset Ks ON Ks.kurssi_id = K.id GROUP BY K.id ORDER BY K.nimi").fetchall()
    return kurssit
# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
    pass

# hakee ryhmässä olevat henkilöt (aakkosjärjestyksessä)
def group_people(group_name):
    pass

# hakee ryhmissä saatujen opintopisteiden määrät (aakkosjärjestyksessä)
def credits_in_groups():
    pass

# hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
def common_groups(teacher_name, student_name):
    pass
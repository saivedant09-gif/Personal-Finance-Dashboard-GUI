import sqlite3

def create_database():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

def save_transaction(typ,cat,amt,dat):
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    INSERT INTO transactions(type,category,amount,date) VALUES(?,?,?,?)
    """,
    (typ,cat,amt,dat)
    )
    connection.commit()
    connection.close()

def display():
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    SELECT * FROM transactions
    """)
    rows=cursor.fetchall()
    connection.close()
    return rows

def Display_Report():
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    SELECT SUM(amount) FROM transactions WHERE type='Income'
    """)
    inc=cursor.fetchone()[0]
    cursor.execute("""
    SELECT SUM(amount) FROM transactions WHERE type='Expense'
    """)
    exp=cursor.fetchone()[0]
    if inc==None:
        inc=0
    if exp==None:
        exp=0
    a={
    "income": inc,
    "expense": exp,
    "savings": inc - exp
    }
    connection.close()
    return a

def Delete(id1):
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    SELECT * FROM transactions WHERE id=?
    """,(id1,))
    rows=cursor.fetchone()
    cursor.execute("""
    DELETE FROM transactions WHERE id=?
    """,(id1,))
    connection.commit()
    connection.close()
    return rows

def Analytics():
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    SELECT category,SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category
    """)
    rows=cursor.fetchall()
    connection.close()
    return rows

def Update(id2,typ,cat,amt,date):
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    UPDATE transactions SET type=?,category=?,amount=?,date=? WHERE id=?
    """,(typ,cat,amt,date,id2))
    connection.commit()
    connection.close()

def search(cat):
    connection=sqlite3.connect("finance.db")
    cursor=connection.cursor()
    cursor.execute("""
    SELECT * FROM transactions WHERE Category LIKE ?
    """,("%" + cat + "%",))
    rows=cursor.fetchall()
    return rows
    connection.close()

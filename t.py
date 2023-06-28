from datetime import datetime
import sqlite3

def save_record_to_database():
    now = datetime.now()
    # Connect to the database (create a new one if it doesn't exist)
    conn = sqlite3.connect('database.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table if it doesn't exist


    # Insert the record into the table
    cursor.execute("""INSERT INTO users (
        time_created,
        username,
        pwd_login,
        pwd_money,
        url_web,
        bank_account,
        bank_branch,
        name,
        phone
        ) VALUES (?,?,?,?,?,?,?,?,?)""", (now,
                                        'pheoct354',
                                        'OtMEBTkY@aA0',
                                        35466002,
                                        'https://www.69vn1.com/',
                                        9704229201311223344,
                                        'Chi Nhánh Điện Biên Phủ TP Hà Nội',
                                        'TRAN CHI PHEO',
                                        925081234))

    # Commit the changes
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
save_record_to_database()
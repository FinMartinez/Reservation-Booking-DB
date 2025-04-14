"""
CS3810: Principles of Database Systems
Instructor: Thyago Mota
Student(s): Fin Martinez
Description: A room reservation system
"""

import psycopg2
from psycopg2 import extensions, errors
import configparser as cp
from datetime import datetime

def menu(): 
    print('1. List')
    print('2. Reserve')
    print('3. Delete')
    print('4. Quit')

def db_connect():
    config = cp.RawConfigParser()
    config.read('ConfigFile.properties')
    params = dict(config.items('db'))
    conn = psycopg2.connect(**params)
    conn.autocommit = False 
    conn.isolation_level = extensions.ISOLATION_LEVEL_SERIALIZABLE
    with conn.cursor() as cur: 
        cur.execute('''
            PREPARE QueryReservationExists AS 
                SELECT * FROM Reservations 
                WHERE abbr = $1 AND room = $2 AND date = $3 AND period = $4;
        ''')
        cur.execute('''
            PREPARE QueryReservationExistsByCode AS 
                SELECT * FROM Reservations 
                WHERE code = $1;
        ''')
        cur.execute('''
            PREPARE NewReservation AS 
                INSERT INTO Reservations (abbr, room, date, period) VALUES
                ($1, $2, $3, $4);
        ''')
        #cur.execute('''
        #    PREPARE UpdateReservationUser AS 
        #        UPDATE Reservations SET "user" = $1
        #        WHERE abbr = $2 AND room = $3 AND date = $4 AND period = $5; 
        #''')
        #cur.execute('''
        #    PREPARE DeleteReservation AS 
        #        DELETE FROM Reservations WHERE code = $1;
        #''')
    return conn

# TODO: display all reservations in the system using the information from ReservationsView
def list_op(conn):
    if conn:
        print('Retrieving Reservations...') 
        cursor = conn.cursor()

        sql = '''SELECT code, TO_CHAR(date, 'YYYY-MM-dd'), period, TO_CHAR(start, 'HH:MI:SS'),
                 TO_CHAR("end", 'HH:MI:SS'), room, name FROM ReservationsView;'''

        cursor.execute(sql)
        
        results = cursor.fetchall()
        print("code " + "date      " + " period  " + "start    " + "   end      " + "building-room " + "user")
        for row in results:
            print('    '.join(str(x) for x in row))
        print("Returning to main menu \n")
        conn.commit()


# TODO: reserve a room on a specific date and period, also saving the user who's the reservation is for
def reserve_op(conn): 
    if conn:
        print('Please provide desired reservation date (YYYY-MM-dd).')
        reservation_date = input('Check in: ')
        print('Please select a period of the time (A-H). ')
        period = input('Period: ')
        print('Please provide the building abbreviation and room number.')
        bldg = input('Building: ')
        room = int(input('Room: '))

        print('Searching...\n')

        with conn.cursor() as cur:

            res_query = '''
                            SELECT abbr, room, date, period FROM Reservations
                            WHERE abbr = %s AND room = %s AND date = %s AND period = %s;
                        '''
            cur.execute(res_query, (bldg, room, reservation_date, period))
            if cur.fetchone() is not None:
                print('Reservation not secured.\n')
                conn.rollback()
            else:
                print('Room available! Reservation booked.')
                reservation = '''
                                INSERT INTO Reservations(abbr, room, date, period) VALUES
                                (%s, %s, %s, %s);'''
                cur.execute(reservation, (bldg, room, reservation_date, period))
                print('Please provide your name.')
                name = input('Name: ')
                set_user = '''
                            PREPARE setUSer AS
                            INSERT INTO Users(name)
                            VALUES($1);'''
                cur.execute(set_user)
                cur.execute("execute setUser (%s)", (name,))
                get_id = '''
                            PREPARE getID AS 
                            SELECT "user" FROM Users
                            WHERE name = $1;
                            '''
                cur.execute(get_id)
                cur.execute("execute getId (%s)", (name,))
                id = cur.fetchone()

                update = '''
                            PREPARE UpdateReservationUser AS
                            UPDATE Reservations SET "user" = $1
                            WHERE abbr = $2 AND room = $3 AND date = $4 AND period = $5; 
                            '''  
                cur.execute(update)
                cur.execute("execute UpdateReservationUser (%s, %s, %s, %s, %s)", 
                            (id, bldg, room, reservation_date, period))
                conn.commit()
                print('Reservation sucessfully updated!')

# TODO: delete a reservation given its code
def delete_op(conn):
    if conn:
        with conn.cursor() as cur:
            print('Please provide provide the name on the reservation.')
            name = input('Name: ')
            print('Searching...')

            get_code = '''
                        PREPARE getCode AS
                        SELECT "user" FROM Users
                        WHERE name = $1;
                        '''
            cur.execute(get_code)
            cur.execute("execute getCode(%s)", (name,))
            code = cur.fetchone()

            if code is not None:
                delete = '''
                            PREPARE DeleteReservation AS 
                            DELETE FROM Reservations WHERE "user" = $1;
                        '''
                cur.execute(delete)
                cur.execute("execute DeleteReservation(%s)", (code,))
                print('Reservation Deleted.')
            else:
                print('Reservation not found.')
                conn.rollback()


if __name__ == "__main__":
    with db_connect() as conn: 
        op = 0
        while op != 4: 
            menu()
            op = int(input('? '))
            if op == 1: 
                list_op(conn)
            elif op == 2:
                reserve_op(conn)
            elif op == 3:
                delete_op(conn)
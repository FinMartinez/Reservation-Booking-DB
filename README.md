# Instructions 

This application is the implementation of a simple room reservation system. The program creates the database named **booking** and is specified in **booking.sql**. All tables are created and populated, and a view named **ReservationsView** is created for further functionality. 

## Features
- DB CRUD operations to List, Reserve, and Delete reservations
- Normalized DB Schema for security and optimization
- SQL view to retrieve all reservation information in chronological order

## Stack
- Python
- PostgreSQL (psycopg)

## Depedencies
This application functions inside a virtual environment and, after its activation, you will need to install the **configparser** and **psycopg** modules. 

- [ConfigParser Documentation](https://docs.python.org/3/library/configparser.html)
- [Psycopg Documentation](https://www.psycopg.org/docs/) 

## Operation
The script **booking.py** is the driver for this database and is present in the virtual environment folder (src). The booking application implements the following menu of options: 

```
1. List
2. Reserve
3. Delete
4. Quit
```

Each of the options are explained in the sections below. 

### List Reservations 

This option aims to display all of the reservations using the **ReservationsView**. The output will be similar to the following: 

```
code,date,period,start,end,building-room,user
4,2023-06-23,F,16:00,18:00,JSS-230,James Brandy
3,2023-06-23,E,14:00,16:00,AES-220,Morbid Mojito
2,2023-06-12,D,12:00,14:00,AES-210,Sam Mai Tai
1,2023-05-15,C,10:00,12:00,AES-210,Sam Mai Tai
```

### Make a New Reservation 

To make a new reservation, you will need to has to first gather all parameters needed for a reservation, which includes: 

* the date, 
* the period of the day (A-H), 
* the building abbreviation, and 
* the room number.

### Delete a Reservation

To delete an existing reservation, the program requests a reservation code from the user. Then transaction begins by checking if there is a reservation with that code. If yes, the reservation is deleted and the transaction is committed. If there is an exception while trying to delete the reservation, or if there is no reservation with the given code, a rollback for the transaction is executed and the procedure is terminated.

### Prepared Statements 

The following prepared statements can be used to assist with operation: 

* QueryReservationExists: tries to retrieve a reservation with parameters (building, room, date, and period)
* QueryReservationExistsByCode: tries to retrieve a reservation with a given code 
* NewReservation: creates a new reservation with parameters (building, room, date, and period)
* UpdateReservationUser: updates the user of a reservation with parameters (user, building, room, date, and period)
* DeleteReservation: deletes a reservation with a given code

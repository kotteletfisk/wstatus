# wstatus

## A script made for scraping washing machine status at my dorm, written in Python 3.

Shows whether they are free, reserved or in use, and displays the time until finished.

Usage:

wstatus [-f] [num]

8 Machines can be checked. it is possible to check an individual machine by passing an integer,
corresponding to the machine number.

if "-f" is passed while a machine is in use, it will keep the script running and check the status of the machine every 60 seconds.
When the machine info returns "Fri", it will print the status, ring the terminal bell and quit the script.

tested on linux and android termux, both running bash.
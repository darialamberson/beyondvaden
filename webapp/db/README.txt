STEPS TO IMPORT DATA FROM SQLITE TO POSTGRES
=============================================

1. Install postgres
Using homebrew, for example

2. Start postgres server
postgres -D /usr/local/var/postgres

3. In a separate terminal window, create "therapists" postgres database
createdb therapists

4. Log into postgres
psql therapists

5. In a separate terminal window, migrate SQL data into postgres
psql -d therapists -U `whoami` -W < <path_to_beyondvaden>/beyondvaden/webapp/db/sqlite_dump.txt

6. In postgres, run SQL commands
therapists=# SELECT * FROM th_specialties; 

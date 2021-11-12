## PostgreSQL Microservice
- PostgreSQL sticks closer to ACID standards and throws lesser surprises, hence the choice.

- Importing seed data is implemented with "COPY" feature of postgres like this ;
```
copy titanic(survived,"passengerClass",name,sex,age,"siblingsOrSpousesAboard","parentsOrChildrenAboard",fare) from '/docker-entrypoint-initdb.d/titanic.csv' DELIMITER ',' CSV HEADER;         
```                                                                                                                                                                                           
- The official postgres image on hub.docker.com, is designed for seeding. So init contianer is not needed.
-  We put the seeding scripts, as .sql statements that we need to run, at the location shown & described, on the official postgres hub.docker.com 
 page, as recommended by the official postgres image.

- For example, a table is automatically created by the instantiation of this docker image, using this sql, which has been inserted into the container ;
```                          
CREATE TABLE titanic(uuid UUID DEFAULT uuid_generate_v4 () PRIMARY KEY, survived BOOL,"passengerClass" INT,Name VARCHAR(150),sex VARCHAR(6),age FLOAT,"siblingsOrSpousesAboard" INT,"parentsOrChildrenAboard" INT,fare FLOAT);
```
- The UUID data-type is a postgres inbuilt data-type. This data-type column, also provides for auto-generation of UUID values.
- The python psycopg2 "cursor_factory.RealDictCursor" function, extracts & returns the column-names (along with values) for the sql queries, so that was an advantage in this use case because no schema is needed in the code.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE titanic(uuid UUID DEFAULT uuid_generate_v4 () PRIMARY KEY, survived BOOL,"passengerClass" INT,Name VARCHAR(150),sex VARCHAR(6),age FLOAT,"siblingsOrSpousesAboard" INT,"parentsOrChildrenAboard" INT,fare FLOAT);
copy titanic(survived,"passengerClass",name,sex,age,"siblingsOrSpousesAboard","parentsOrChildrenAboard",fare) from '/docker-entrypoint-initdb.d/titanic.csv' DELIMITER ',' CSV HEADER;

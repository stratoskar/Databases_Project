import psycopg2
from psycopg2 import Error

try:

    username = input("Please insert the username of server. Leave blank for default value (postgres):\n")
    passcode = input("Please insert the password of postgreSQL server:\n")
    hostname = input("Please insert the host ip address. Leave blank for default value (127.0.0.1):\n")
    port_number = input("Please insert the port number. Leave blank for default value (5432):\n")
    db_name = input("Please insert the name of the database that you would like to connect to:\n")

    if (hostname == ""):
        hostname = "127.0.0.1"

    if (username == ""):
        username = "postgres"

    if (port_number == ""):
        port_number = "5432"

    # Connect to an existing database
    connection = psycopg2.connect(user=username,
                                  password=passcode,
                                  host=hostname,
                                  port=port_number,
                                  database=db_name)

    # if the connection was successfull, then show a messsage to user
    if (connection):
        print("PostgreSQL successfully connected with python API!\n")

    # open a cursor
    cur = connection.cursor()

    print("2a:")

    # excecute query 2a using cursor
    cur.execute('''-- Ερώτημα 2a
                    --Βρες όλους τους οδηγούς που σχετίζονται με συμβόλαια
                    --τα οποία υπεγράφησαν τον τελευταίο μήνα
                    (
                        SELECT first_name,last_name,contract_code,'Driver' AS Category
                        FROM contracts NATURAL JOIN drivers NATURAL JOIN drivers_info
                        WHERE contract_code IN
				              -- Νέα συμβόλαια
                              (
                                SELECT contract_code
                                FROM contracts
                                WHERE EXTRACT (YEAR FROM start_date)=(SELECT date_part('year',CURRENT_DATE)) AND EXTRACT (MONTH FROM start_date)=(SELECT date_part('month',CURRENT_DATE))
                              )
                    )
                    UNION
                    --Βρες όλους τους πελάτες που σχετίζονται με συμβόλαια
                    -- τα οποία υπεγράφησαν τον τελευταίο μήνα
                    (
                        SELECT first_name,last_name,contract_code,'Client' AS Category
                        FROM contracts NATURAL JOIN clients NATURAL JOIN clients_info
                        WHERE contract_code IN
				             -- Νέα συμβόλαια
                             (
                                SELECT contract_code
                                FROM contracts
                                WHERE EXTRACT (YEAR FROM start_date)=(SELECT date_part('year',CURRENT_DATE)) AND EXTRACT (MONTH FROM start_date)=(SELECT date_part('month',CURRENT_DATE))
                            )
                    )
                    ORDER BY contract_code''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("first_name =",row[0], ", last_name =",row[1], ", contract_code =",row[2], ", category =",row[3])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2b:")

    # excecute query 2b using cursor
    cur.execute('''-- Ερώτημα 2b
                    -- Παραδοχή: Θεωρούμε ότι η τρέχουσα ημερομηνία είναι Ιούνιος του 2021 (06/2021)
                    SELECT contract_code,phone_number1,phone_number2
                    FROM contracts natural join clients natural join clients_info
                    WHERE contract_code IN
                        (
                            SELECT contract_code
                            FROM contracts
                            WHERE EXTRACT (YEAR FROM end_date)=2021 AND EXTRACT (MONTH FROM end_date)=7
                        )''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("contract_code =",row[0], ", phone_number1 =",row[1], ", phone_number2 =",row[2])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2c:")

    # excecute query 2c using cursor
    cur.execute('''-- Ερώτημα 2c
                    SELECT COUNT(DISTINCT contract_code) AS number_of_contracts, insurance_category, EXTRACT (YEAR FROM start_date) AS contract_year
                    FROM contracts
                    WHERE EXTRACT (YEAR FROM start_date)>=2016 AND EXTRACT (YEAR FROM start_date)<=2020
                    GROUP BY insurance_category,EXTRACT (YEAR FROM start_date)''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("number_of_contracts =",row[0], ", insurance_category =",row[1], ", contract_year =",row[2])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2c-variation:")

    # excecute query 2c-variation using cursor
    cur.execute('''-- Eρώτημα 2c (Παραλλαγή)
                        SELECT COUNT(DISTINCT contract_code) AS number_of_contracts, insurance_category, EXTRACT (YEAR FROM end_date) AS expired_year
                        FROM contracts
                        WHERE (EXTRACT (YEAR FROM end_date)>=2016 AND EXTRACT (YEAR FROM end_date)<=2020) AND (EXTRACT (YEAR FROM start_date)<2016 OR EXTRACT (YEAR FROM start_date)>2020)
                        GROUP BY insurance_category,EXTRACT (YEAR FROM end_date)''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("number_of_contracts =",row[0], ", insurance_category =",row[1], ", expired_year =",row[2])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2d-first variation:")

    # excecute query 2d (first variation) using cursor
    cur.execute('''-- Ερώτημα 2d (Πρώτη παραλλαγή - σε απόλυτους αριθμούς)
                    WITH sum_per_category (insurance_category,sum_cost) AS
                    (
                        SELECT insurance_category,SUM(contract_cost) AS sum_cost
                        FROM contracts
                        GROUP BY insurance_category
                    )
                    SELECT insurance_category,sum_cost
                    FROM sum_per_category
                    WHERE sum_cost IN
                    (
                        SELECT MAX(sum_cost)
                        FROM sum_per_category
                    )''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("insurance_category =",row[0], ", sum_cost =",row[1])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2d-second variation:")

    # execute query 2d - second variation using cursor
    cur.execute('''-- Ερώτημα 2d (Δεύτερη παραλλαγή - με αναγωγή βάσει πλήθους συμβολαίων)
                    WITH count_per_category (insurance_category,count_contracts) AS
                    (
                        SELECT insurance_category,COUNT(DISTINCT contract_code) AS count_contracts
                        FROM contracts
                        GROUP BY insurance_category
                    )
                    SELECT insurance_category,count_contracts
                    FROM count_per_category
                    WHERE count_contracts IN
                    (
                        SELECT MAX(count_contracts)
                        FROM count_per_category
                    )''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("insurance_category =",row[0], ", count_contracts =",row[1])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2e:")

    # execute query 2e using cursor
    cur.execute('''-- Ερώτημα 2e
                    -- 1η παραδοχή: Θεωρούμε ότι δεν υπάρχουν αυτοκίνητα που κυκλοφόρησαν πρώτη φορά πριν τον 1980
                    -- 2η παραδοχή: Όσα οχήματα υπάρχουν, τόσα είναι και τα διαφορετικά συμβόλαια
                    WITH contracts_0_4 (first_year,count_contracts) AS
                    (
                        SELECT first_year, COUNT(DISTINCT plate_number) AS count_contracts
                        FROM vehicles
                        WHERE (SELECT date_part('year',CURRENT_DATE))-first_year <= 4
                        GROUP BY first_year
                    )
                    ,
                    contracts_5_9 (first_year,count_contracts) AS
                    (
                        SELECT first_year, COUNT(DISTINCT plate_number) AS count_contracts
                        FROM vehicles
                        WHERE (SELECT date_part('year',CURRENT_DATE))-first_year <= 9 AND (SELECT date_part('year',CURRENT_DATE))-first_year >= 5
                        GROUP BY first_year
                    )
                    ,
                    contracts_10_19 (first_year,count_contracts) AS
                    (
                        SELECT first_year, COUNT(DISTINCT plate_number) AS count_contracts
                        FROM vehicles
                        WHERE (SELECT date_part('year',CURRENT_DATE))-first_year <= 19 AND (SELECT date_part('year',CURRENT_DATE))-first_year >= 10
                        GROUP BY first_year
                    )
                    ,
                    contracts_20plus (first_year,count_contracts) AS
                    (
                        SELECT first_year, COUNT(DISTINCT plate_number) AS count_contracts
                        FROM vehicles
                        WHERE (SELECT date_part('year',CURRENT_DATE))-first_year >=20
                        GROUP BY first_year
                    )

                    (SELECT '0-4' AS group,CAST(SUM(count_contracts)/5 AS DECIMAL(10,2)) AS average_contracts
                    FROM contracts_0_4)
                    UNION
                    (SELECT '5-9' AS group,CAST(SUM(count_contracts)/5 AS DECIMAL(10,2)) AS average_contracts
                    FROM contracts_5_9)
                    UNION
                    (SELECT '10-19' AS group,CAST(SUM(count_contracts)/10 AS DECIMAL(10,2)) AS average_contracts
                    FROM contracts_10_19)
                    UNION
                    (SELECT '20+' AS group,CAST(SUM(count_contracts)/((SELECT date_part('year',CURRENT_DATE))-1999) AS DECIMAL(10,2)) AS average_contracts
                    FROM contracts_20plus)''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("group =",row[0], ", average_contracts =",row[1])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

    print("2f:")

    # execute query 2f - second variation using cursor
    cur.execute('''-- Ερώτημα 2f
                    -- Παραδοχή: Δεν υπάρχει οδηγός που να είναι άνω των 80 ετών

                    WITH infringements_18_24 (birth_date,infringements_number) AS
                    (
                        SELECT EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date) AS age,COUNT(infringement_code) AS infringements_number
                        FROM infringements NATURAL JOIN infringements_drivers NATURAL JOIN drivers_info
                        WHERE (EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)) >= 18 AND (EXTRACT(YEAR FROM infringement_date)-EXTRACT (YEAR FROM birth_date)) <= 24
                        GROUP BY EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)
                    )
                    ,
                    infringements_25_49 (birth_date,infringements_number) AS
                    (
                        SELECT EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date) AS age,COUNT(infringement_code) AS infringements_number
                        FROM infringements NATURAL JOIN infringements_drivers NATURAL JOIN drivers_info
                        WHERE (EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)) >= 25 AND (EXTRACT(YEAR FROM infringement_date)-EXTRACT (YEAR FROM birth_date)) <= 49
                        GROUP BY EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)
                    )
                    ,
                    infringements_50_69 (birth_date,infringements_number) AS
                    (
                        SELECT EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date) AS age,COUNT(infringement_code) AS infringements_number
                        FROM infringements NATURAL JOIN infringements_drivers NATURAL JOIN drivers_info
                        WHERE (EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)) >= 50 AND (EXTRACT(YEAR FROM infringement_date)-EXTRACT (YEAR FROM birth_date)) <= 69
                        GROUP BY EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)
                    )
                    ,
                    infringements_70plus (birth_date,infringements_number) AS
                    (
                        SELECT EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date) AS age,COUNT(infringement_code) AS infringements_number
                        FROM infringements NATURAL JOIN infringements_drivers NATURAL JOIN drivers_info
                        WHERE (EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)) >= 70
                        GROUP BY EXTRACT(YEAR FROM infringement_date)-EXTRACT(YEAR FROM birth_date)
                    )

                    (SELECT '18-24' AS age_group,CAST(SUM(infringements_number)/7 AS DECIMAL(10,2)) AS average_contracts
                    FROM infringements_18_24)
                    UNION
                    (SELECT '25-49' AS age_group,CAST(SUM(infringements_number)/25 AS DECIMAL(10,2)) AS average_contracts
                    FROM infringements_25_49)
                    UNION
                    (SELECT '50-69' AS age_group,CAST(SUM(infringements_number)/20 AS DECIMAL(10,2)) AS average_contracts
                    FROM infringements_50_69)
                    UNION
                    (SELECT '70+' AS age_group,CAST(SUM(infringements_number)/11 AS DECIMAL(10,2)) AS average_contracts
                    FROM infringements_70plus)''')

    # fetch rows
    rows = cur.fetchall()
    for row in rows:
        print ("age_group =",row[0], ", average_contracts =",row[1])

    print("\n")
    print("--------------------------------------------------------------")
    print("\n")

except (Exception, Error) as error: # problem with connection occured

    print("Error while connecting to PostgreSQL", error)

finally:

    try:
        if (connection):
            cur.close()
            connection.close()
            print("PostgreSQL connection is closed")

    finally:
        input("Press ENTER to EXIT")

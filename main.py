import sqlite3
from prettytable import PrettyTable

class DBOperations:
    sql_create_table_firsttime = "CREATE TABLE IF NOT EXISTS EmployeeUoB" \
                                 "(employee_id INTEGER PRIMARY KEY, " \
                       "title VARCHAR(3), " \
                       "forename VARCHAR(20), " \
                       "surname VARCHAR(20), " \
                       "emailAddress VARCHAR(30), " \
                       "salary SMALLINT UNSIGNED);"
    sql_create_table = "CREATE TABLE EmployeeUoB " \
                       "(employee_id INTEGER PRIMARY KEY, " \
                       "title VARCHAR(3), " \
                       "forename VARCHAR(20), " \
                       "surname VARCHAR(20), " \
                       "emailAddress VARCHAR(30), " \
                       "salary SMALLINT UNSIGNED)"
    sql_insert = "INSERT INTO EmployeeUoB " \
                 "(employee_id, title, forename, surname, emailAddress, salary) " \
                 "VALUES (?, ?, ?, ?, ?, ?)"
    sql_select_all = "SELECT * from EmployeeUoB"
    sql_search = "SELECT * FROM EmployeeUoB WHERE employee_id = ?"
    sql_update_title = "UPDATE EmployeeUoB SET title = ? WHERE employee_id = ?"
    sql_update_forename = "UPDATE EmployeeUoB SET forename = ? WHERE employee_id = ?"
    sql_update_surname = "UPDATE EmployeeUoB SET surname = ? WHERE employee_id = ?"
    sql_update_emailAddress = "UPDATE EmployeeUoB SET emailAddress = ? WHERE employee_id = ?"
    sql_update_salary = "UPDATE EmployeeUoB SET salary = ? WHERE employee_id = ?"
    sql_delete_data = "DELETE FROM EmployeeUoB WHERE employee_id = ?"
    sql_drop_table = "DROP TABLE IF EXISTS EmployeeUoB"

    def __init__(self):
        try:
            self.conn = sqlite3.connect("UoBath.db")
            self.cur = self.conn.cursor()
            self.cur.execute(self.sql_create_table_firsttime)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #connects to database 
    def get_connection(self):
        self.conn = sqlite3.connect("UoBath.db")
        self.cur = self.conn.cursor()

    #creates table if it doesnt already exist 
    def create_table(self):
        try:
            self.get_connection()
            if self.cur.execute(self.sql_select_all).rowcount != 0:
                print("This table already exists.")
            else:
                self.cur.execute(self.sql_create_table)
                self.conn.commit()
                print("Table has been created successfully.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #allows data to be added to table 
    def insert_data(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)
            results = self.cur.fetchall()
            emp = Employee()

            #if first entry 
            if len(results) == 0:
                emp.set_employee_title(input("Enter title: "))
                emp.set_forename(input("Enter forename: "))
                emp.set_surname(input("Enter surname: "))
                emp.set_email(input("Enter email: "))
                emp.set_salary(int(input("Enter salary: ")))

              #for other entries 
            else:
                last_entry=results[-1]
                highest_id = last_entry[0]
                emp.set_employee_id(highest_id+1)
                emp.set_employee_title(input("Enter title: "))
                emp.set_forename(input("Enter forename: "))
                emp.set_surname(input("Enter surname: "))
                emp.set_email(input("Enter email: "))
                emp.set_salary(int(input("Enter salary: ")))

            self.cur.execute(self.sql_insert, tuple(str(emp).split("\n")))
            self.conn.commit()
            print("data inserted successfully.")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #selects all the data from the table 
    def select_all(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)
            results = self.cur.fetchall()

            #creates table for user to see 
            table = PrettyTable([
              "Employee ID", "Title", "Forename", "Surname", "Email Address", "Salary (£)"
            ])

            for item in results:
              table.add_row(item)

            print(table)

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #search for employee record 
    def search_data(self):
        try:
            self.get_connection()
            employee_id = int(input("Enter Employee ID: "))
            self.cur.execute(self.sql_search, tuple(str(employee_id)))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                for index, detail in enumerate(result):
                    if index == 0:
                        print("Employee ID: " + str(detail))
                    elif index == 1:
                        print("Employee Title: " + detail)
                    elif index == 2:
                        print("Employee Name: " + detail)
                    elif index == 3:
                        print("Employee Surname: " + detail)
                    elif index == 4:
                        print("Employee Email: " + detail)
                    else:
                        print("Salary: " + str(detail))
            else:
                print("Record not found.")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #update data in record
    def update_data(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)
            results = self.cur.fetchall()
            table = PrettyTable([
              "Employee ID", "Title", "Forename", "Surname", "Email Address", "Salary (£)"
            ])


            for item in results:
              table.add_row(item)

            #update queries 
            employee_id = input("Enter employee ID: ")
 
            column = input("Enter column to update: ")
            newValue = input("Enter value to update: ")
            update = (newValue, employee_id)

            if column == "Title":
                self.cur.execute(self.sql_update_title, update)
            elif column == "Forename":
                self.cur.execute(self.sql_update_forename, update)
            elif column == "Surname":
                self.cur.execute(self.sql_update_surname, update)
            elif column == "Email Address":
                self.cur.execute(self.sql_update_emailAddress, update)
            elif column == "Salary":
                self.cur.execute(self.sql_update_salary, update)
            else:
                print("Please retry.")
            self.conn.commit()
            affected = self.conn.total_changes
            if affected != 0:
                print(affected, " row(s) affected.")
            else:
                print("No record.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #delete employee record
    def delete_data(self):
        try:
            self.get_connection()

            employee_id = input("Enter employee ID: ")
            self.cur.execute(self.sql_delete_data, tuple(str(employee_id)))

            self.conn.commit()
            self.cur.execute(self.sql_select_all)

            results = self.cur.fetchall()

            #creates table after record deletion
            table = PrettyTable([
              "Employee ID", "Title", "Forename", "Surname", "Email Address", "Salary (£)"
            ])

            
            for item in results:
              table.add_row(item)
               
            affected = self.conn.total_changes
            if affected != 0:
                print(affected, " row(s) affected.")
            else:
                print("No record.")
            print(table)

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

#employee class 
class Employee:
    def __init__(self):
        self.employee_id = 0
        self.empTitle = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def set_employee_title(self, empTitle):
        self.empTitle = empTitle

    def set_forename(self, forename):
        self.forename = forename

    def set_surname(self, surname):
        self.surname = surname

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary


    def get_employee_id(self):
        return self.employee_id

    def get_employee_title(self):
        return self.empTitle

    def get_forename(self):
        return self.forename

    def get_surname(self):
        return self.surname

    def get_email(self):
        return self.email

    def get_salary(self):
        return self.salary

    def __str__(self):
        return str(
            self.employee_id) + "\n" + self.empTitle + "\n" + self.forename + "\n" + self.surname + \
               "\n" + self.email + "\n" + str(self.salary)

#user menu 
while True:
    print("\n Menu:")
    print("**********")
    print(" 1. Create table EmployeeUoB")
    print(" 2. Insert data into EmployeeUoB")
    print(" 3. Select all data in EmployeeUoB")
    print(" 4. Search an employee")
    print(" 5. Update data (to update a record)")
    print(" 6. Delete data (to delete a record)")
    print(" 7. Exit programme\n")
    try:
        __choose_menu = int(input("Enter your choice: "))
        db_ops = DBOperations()
        if __choose_menu == 1:
            db_ops.create_table()
        elif __choose_menu == 2:
            db_ops.insert_data()
        elif __choose_menu == 3:
            db_ops.select_all()
        elif __choose_menu == 4:
            db_ops.search_data()
        elif __choose_menu == 5:
            db_ops.update_data()
        elif __choose_menu == 6:
            db_ops.delete_data()
        elif __choose_menu == 7:
            print("Exiting programme.")
            exit(0)
        else:
            print("Choice is not valid.")
    except Exception as e:
        print("Enter number between 1 and 7.")
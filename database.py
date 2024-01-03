from sqlite3 import connect

class Database:
    db=None
    cursor=None
    @staticmethod
    def connect():
       Database.db = connect("optodatabase.db")
       Database.cursor = Database.db.cursor()
       Database.cursor.execute(
                            """
                            CREATE TABLE IF NOT EXISTS USERS
                            (
                                EMAIL TEXT PRIMARY KEY,
                                PASSWORD TEXT NOT NULL,
                                NAME TEXT NOT NULL
                            )
                            """
                              )
       
       Database.cursor.execute(
                            """
                            CREATE TABLE IF NOT EXISTS ENTRIES
                            (
                                ENTRY_ID INTEGER PRIMARY KEY,
                                EMAIL TEXT NOT NULL,
                                PROBLEM_NAME TEXT NOT NULL
                            )
                            """
                                )
       
       Database.cursor.execute(
                            """
                            CREATE TABLE IF NOT EXISTS DATA_TABLE
                            (
                                ID INTEGER PRIMARY KEY,
                                ENTRY_ID INTEGER NOT NULL,
                                EMAIL TEXT NOT NULL,
                                DISEASE TEXT NOT NULL,
                                PERCENTAGE TEXT NOT NULL
                            )
                            """
                                )
       
       Database.db.commit()

    @staticmethod
    def insert_into_user(email, password, name):
        sql = "INSERT INTO USERS (EMAIL, PASSWORD, NAME) VALUES (?,?,?)"
        val = (email, password, name)
        Database.cursor.execute(sql, val)
        Database.db.commit()
    
    @staticmethod
    def is_valid(email):
        sql=f"SELECT * FROM USERS WHERE EMAIL='{email}'"
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()
        if result:
            return False
        else:
            return True
        
    @staticmethod
    def is_exists(email, password):
        sql=f"SELECT * FROM USERS WHERE EMAIL='{email}' AND PASSWORD='{password}'"
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()
        if result:
            return True
        else:
            return False
        
    @staticmethod
    def truncate_users_table():
        Database.cursor.execute("DELETE FROM USERS")
        Database.db.commit()
    
    @staticmethod
    def get_user_info(email):
        sql=f"SELECT * FROM USERS WHERE EMAIL='{email}'"
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()[0] # Email, Password Name bilgileri dönüyor. [0] ile email bilgisini alıyoruz
        return result
    
    @staticmethod
    def update_user_info(name, email, password):
        sql="UPDATE USERS SET PASSWORD=?, NAME=? WHERE EMAIL=?"
        val = (password, name, email)
        Database.cursor.execute(sql, val)
        Database.db.commit()

    @staticmethod
    def insert_into_entries(email, problem_name):
        sql = "INSERT INTO ENTRIES (EMAIL, PROBLEM_NAME) VALUES (?,?)"
        val = (email, problem_name)
        Database.cursor.execute(sql, val)
        Database.db.commit()

    @staticmethod
    def insert_into_data_table(entry_id, email, disease, percentage):
        sql = "INSERT INTO DATA_TABLE (ENTRY_ID, EMAIL, DISEASE, PERCENTAGE) VALUES (?,?,?,?)"
        val = (entry_id, email, disease, percentage)
        Database.cursor.execute(sql, val)
        Database.db.commit()

    @staticmethod
    def get_last_entry_id(email):
        sql=f"SELECT * FROM ENTRIES WHERE EMAIL='{email}'"
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()[-1]
        return result
    
    @staticmethod
    def get_all_entries(email):
        sql=f"SELECT * FROM ENTRIES WHERE EMAIL='{email}'"
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()
        return result

    @staticmethod
    def get_data(email, entry_id):
        sql=f"SELECT * FROM DATA_TABLE WHERE ENTRY_ID='{entry_id}' AND EMAIL='{email}'"
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()
        return result

    
    

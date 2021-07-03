import mysql.connector
user       = "root"
password   = "123"
host       = "172.17.0.2"
database   = "footwear_db"
class connectdb:
    def __init__(self) -> None:
        pass
 
        
    def executeQuery(sql):
        cnx             = mysql.connector.connect(user=user, password=password ,host=host, database=database)
        cursor          =cnx.cursor(buffered=True)
        cursor.execute(sql)
        myresult        = cursor.fetchall()
        cnx.close()
        return myresult
    def insertData(sql):
        cnx             = mysql.connector.connect(user= user, password= password ,host= host, database= database)
        cursor          = cnx.cursor(buffered=True)
        try:
            cursor.execute(sql)
            cnx.commit()
            cnx.close()
            return {"message": "Đăng ký thành công!"}
        except:
            print(sql)  
            cnx.rollback()
            cnx.close()
            return {"message": "Đăng ký thất bại"}

    def RunQueryData(sql):
        cnx        = mysql.connector.connect(user= user, password= password ,host= host, database= database)
        cursor      = cnx.cursor(buffered=True)
        try:
            cursor.execute(sql)
            cnx.commit()
            cnx.close()
            return {"message": "Successfully"}
        except:
            print(sql)  
            cnx.rollback()
            cnx.close()
            return {"message": "Failure"}

    def RunQueryDataBool(sql):
        cnx             = mysql.connector.connect(user= user, password= password ,host= host, database= database)
        cursor          = cnx.cursor(buffered=True)
        print("RunQueryDataBool: "+str(sql))
        try:
            cursor.execute(sql)
            
            cnx.commit()
            cnx.close()
            return True
        except:
            print(sql)  
            cnx.rollback()
            cnx.close()
            return False
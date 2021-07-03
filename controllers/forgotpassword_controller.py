from configdb.connectdb import connectdb
import datetime
class ForgotPassword:
    def __init__(self) -> None:
        pass
    def checkMailCustommerExit(self,email):
        sql      = "SELECT * FROM `customers`"
        myresult = connectdb.executeQuery(sql)
        for x in myresult:
            if(x[1] == email):
                return x[0]
        return 0
    def checkMailAdminExit(self,email):
        sql         = "SELECT * FROM `admins`"
        myresult    = connectdb.executeQuery(sql)
        for x in myresult:
            if(x[1] == email):
                return x[0]
        return 0
    def checkLimitMailSend(self):
        dt       = datetime.datetime.today()
        sql      = "SELECT count(*) FROM `forgotpassword` WHERE day(`forgotpassword`.`createdAt`) = "+str(dt.day)
        myresult = connectdb.executeQuery(sql)
        for x in myresult:
            if(int(x[0]) <= 30):
                return True
        return False
    def saveCodeCustomer(self, code, id):
        dt  = datetime.datetime.now()
        dt  = dt.strftime("%Y-%m-%d %H:%M:%S")
        exp = datetime.datetime.now() + datetime.timedelta(minutes = 30)
        exp = exp.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO `forgotpassword`(`adminId`, `customerId`, `code`, `createdAt`, `expDay`) VALUES ('0','"+str(id)+"','"+str(code)+"','"+str(dt)+"','"+str(exp)+"')"
        print(sql)
        tmp = connectdb.RunQueryData(sql)
        return True
    def saveCodeAdmin(self, code, id):
        dt  = datetime.datetime.now()
        dt  = dt.strftime("%Y-%m-%d %H:%M:%S")
        exp = datetime.datetime.now() + datetime.timedelta(minutes = 5)
        exp = exp.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO `forgotpassword`(`adminId`, `customerId`, `code`, `createdAt`, `expDay`) VALUES ('"+str(id)+"','0','"+str(code)+"','"+str(dt)+"','"+str(exp)+"')"
        tmp = connectdb.RunQueryData(sql)
        return True
    def checkCode(self,code):
        dt  = datetime.datetime.now()
        dt  = dt.strftime("%Y-%m-%d %H:%M:%S")
        sql = "SELECT * FROM `forgotpassword` WHERE `forgotpassword`.`expDay` >= '"+str(dt) +"' AND code = '"+str(code)+"' AND "+"`forgotpassword`.`createdAt` <= '"+str(dt)+"'"
        print(sql)
        myresult = connectdb.executeQuery(sql)
        for x in myresult:
            return x[2]
        return 0
    def checkCodeA(self,code):
        dt  = datetime.datetime.now()
        dt  = dt.strftime("%Y-%m-%d %H:%M:%S")
        sql = "SELECT * FROM `forgotpassword` WHERE `forgotpassword`.`expDay` >= '"+str(dt) +"' AND code = '"+str(code)+"' AND "+"`forgotpassword`.`createdAt` <= '"+str(dt)+"'"
        print(sql)
        myresult = connectdb.executeQuery(sql)
        for x in myresult:
            return x[1]
        return 0

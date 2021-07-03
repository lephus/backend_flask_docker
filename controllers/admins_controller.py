from models.admins_model import Admin
from configdb.connectdb import connectdb

class AdminController:
    def __init__(self) -> None:
        pass
    @staticmethod
    def get_all_admin():
        sql = "SELECT * FROM `admins` INNER JOIN `cities` ON `cities`.id = `admins`.city INNER JOIN `districts` ON `districts`.id = `admins`.distric INNER JOIN `streets` ON `streets`.id = `admins`.street INNER JOIN `roles` ON `roles`.id = `admins`.roleId"
        myresult = connectdb.executeQuery(sql)
        result = []
        for x in myresult:
            admin = Admin(
                id          = x[0], 
                email       = x[1],
                password    = '',
                image       = x[3],
                gender      = x[4],
                lastName    = x[5],
                firstName   = x[6],
                city        = x[15],
                distric     = x[18],
                street      = x[22],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                roleId      = x[28],
            )
            result.append(admin.serialize())
        return result

    

    def get_admin_byId(self, id):
        sql = 'SELECT * FROM `admins` INNER JOIN `cities` ON `cities`.id = `admins`.city INNER JOIN `districts` ON `districts`.id = `admins`.distric INNER JOIN `streets` ON `streets`.id = `admins`.street INNER JOIN `roles` ON `roles`.id = `admins`.roleId WHERE `admins`.id = '+str(id)
        myresult = connectdb.executeQuery(sql)
        for x in myresult:
            admin = Admin(
                id          = x[0], 
                email       = x[1],
                password    = '',
                image       = x[3],
                gender      = x[4],
                lastName    = x[5],
                firstName   = x[6],
                city        = x[15],
                distric     = x[18],
                street      = x[9],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                roleId      = x[28],
            )
            return (admin.serialize())
        admin = Admin()
        return admin.serialize()

    def delete_admin_byId(self, id):
        sql         = "DELETE FROM `admins` WHERE `admins`.`id` = "+str(id)
        myresult    = connectdb.RunQueryData(sql)
        return myresult

    def update_admin_byId(self,admin: Admin):
        sql         = "UPDATE `admins` SET `email`='"+str(admin.email)+"',`password`='"+str(admin.password)+"',`image`='"+str(admin.image)+"',`gender`='"+str(admin.gender)+"',`lastName`='"+str(admin.lastName)+"',`firstName`='"+str(admin.firstName)+"',`city`='"+str(admin.city)+"',`distric`='"+str(admin.distric)+"',`street`='"+str(admin.street)+"',`address`='"+str(admin.address)+"',`phone`='"+str(admin.phone)+"',`birthDay`='"+str(admin.birthDay)+"',`roleId`='"+str(admin.roleId)+"' WHERE admins.id = "+str(admin.id)+" ;"
        print(sql)
        myresult    = connectdb.RunQueryData(sql)
        return myresult

    def login_admin(self, email, password):
        sql         = "SELECT * FROM `admins` INNER JOIN `cities` ON `cities`.id = `admins`.city INNER JOIN `districts` ON `districts`.id = `admins`.distric INNER JOIN `streets` ON `streets`.id = `admins`.street INNER JOIN `roles` ON `roles`.id = `admins`.roleId WHERE `admins`.email = '"+str(email)+"' AND `admins`.password = '"+str(password)+"'"
        myresult    = connectdb.executeQuery(sql)
        for x in myresult:
            admin   = Admin(
                id          = x[0], 
                email       = x[1],
                password    = '',
                image       = x[3],
                gender      = x[4],
                lastName    = x[5],
                firstName   = x[6],
                city        = x[15],
                distric     = x[18],
                street      = x[22],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                roleId      = x[28],
            )
            return admin, 200
        admin = Admin()
        return admin, 401
    
    def add_admin(self, admin: Admin):
        sql      = "INSERT INTO `admins`(`id`,`email`, `password`, `image`, `gender`, `lastName`, `firstName`, `city`, `distric`, `street`, `address`, `phone`, `birthDay`, `roleId`)VALUES (null,'"+str(admin.email)+"','"+str(admin.password)+"','"+str(admin.image)+"','"+str(admin.gender)+"','"+str(admin.lastName)+"','"+str(admin.firstName)+"','"+str(admin.city)+"','"+str(admin.distric)+"','"+str(admin.street)+"','"+str(admin.address)+"','"+str(admin.phone)+"','"+str(admin.birthDay)+"','"+str(admin.roleId)+"')"
        myresult = connectdb.insertData(sql)
        return myresult
    def get_admin_ID(self, id):
        sql      = 'SELECT * FROM `admins` WHERE `admins`.id = '+str(id)
        myresult = connectdb.executeQuery(sql)
        for x in myresult:
            admin = Admin(
                id          = x[0], 
                email       = x[1],
                password    = x[2],
                image       = x[3],
                gender      = x[4],
                lastName    = x[5],
                firstName   = x[6],
                city        = x[7],
                distric     = x[8],
                street      = x[9],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                roleId      = x[13],
            )
            return admin
        admin = Admin()
        return admin
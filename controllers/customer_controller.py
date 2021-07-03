from models.customers_model import Customer
from configdb.connectdb import connectdb
import base64
class CustomerController:
    def __init__(self) -> None:
        pass
    @staticmethod
    def get_all_customer():
        sql      = "SELECT * FROM `customers` INNER JOIN `cities` ON `cities`.id = `customers`.city INNER JOIN `districts` ON `districts`.id = `customers`.distric INNER JOIN `streets` ON `streets`.id = `customers`.street"
        myresult = connectdb.executeQuery(sql)
        result   = []
        for x in myresult:
            _customer = Customer(
                id          = x[0], 
                email       = x[1],
                password    = x[2],
                image       = x[5],
                gender      = x[6],
                lastName    = x[3],
                firstName   = x[4],
                city        = x[15],
                distric     = x[18],
                street      = x[22],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                acc_point   = x[13],
            )
            result.append(_customer.serialize())
        return result

    

    def get_customer_byId(self, id):
        sql         = 'SELECT * FROM `customers` INNER JOIN `cities` ON `cities`.id = `customers`.city INNER JOIN `districts` ON `districts`.id = `customers`.distric INNER JOIN `streets` ON `streets`.id = `customers`.street WHERE `customers`.id = '+str(id)
        myresult    = connectdb.executeQuery(sql)
        for x in myresult:
            _cus = Customer(
                 id          = x[0], 
                email       = x[1],
                password    = x[2],
                image       = x[5],
                gender      = x[6],
                lastName    = x[3],
                firstName   = x[4],
                city        = x[15],
                distric     = x[18],
                street      = x[22],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                acc_point   = x[13],
            )
            return (_cus.serialize())
        cus = Customer()
        return cus.serialize()

    def delete_customer_byId(self, id):
        sql         = "DELETE FROM `customers` WHERE `customers`.`id` = "+str(id)
        myresult    = connectdb.RunQueryData(sql)
        return myresult

    def update_customer_byId(self,customer: Customer):
        sql         = "UPDATE `customers` SET `email`='"+str(customer.email)+"',`password`='"+str(customer.password)+"',`image`='"+str(customer.image)+"',`gender`='"+str(customer.gender)+"',`lastName`='"+str(customer.lastName)+"',`firstName`='"+str(customer.firstName)+"',`city`='"+str(customer.city)+"',`distric`='"+str(customer.distric)+"',`street`='"+str(customer.street)+"',`address`='"+str(customer.address)+"',`phone`='"+str(customer.phone)+"',`birthDay`='"+str(customer.birthDay)+"',`acc_point`='"+str(customer.acc_point)+"' WHERE id = "+str(customer.id)+" ;"
        myresult    = connectdb.RunQueryData(sql)
        return myresult

    def login_customer(self, email, password):
        sql         = "SELECT * FROM `customers` INNER JOIN `cities` ON `cities`.id = `customers`.city INNER JOIN `districts` ON `districts`.id = `customers`.distric INNER JOIN `streets` ON `streets`.id = `customers`.street WHERE `customers`.email = '"+str(email)+"' AND `customers`.password = '"+str(password)+"'"
        myresult    = connectdb.executeQuery(sql)
        for x in myresult:
            customer = Customer(
                id          = x[0], 
                email       = x[1],
                password    = '',
                image       = x[5],
                gender      = x[6],
                lastName    = x[3],
                firstName   = x[4],
                city        = x[15],
                distric     = x[18],
                street      = x[22],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                acc_point   = x[13],
            )
            return customer, 200
        customer = Customer()
        return customer, 401
    
    def add_customer(self, cus: Customer):
        sql         = "INSERT INTO `customers`(`id`,`email`, `password`, `image`, `gender`, `lastName`, `firstName`, `city`, `distric`, `street`, `address`, `phone`, `birthDay`, `acc_point`)VALUES (null,'"+str(cus.email)+"','"+str(cus.password)+"','"+str(cus.image)+"','"+str(cus.gender)+"','"+str(cus.lastName)+"','"+str(cus.firstName)+"','"+str(cus.city)+"','"+str(cus.distric)+"','"+str(cus.street)+"','"+str(cus.address)+"','"+str(cus.phone)+"','"+str(cus.birthDay)+"','"+str(cus.acc_point)+"')"
        myresult    = connectdb.insertData(sql)
        return myresult

    def customer_ID(self, id):
        sql         = 'SELECT * FROM `customers` WHERE `customers`.id = '+str(id)
        myresult    = connectdb.executeQuery(sql)
        for x in myresult:
            _cus = Customer(
                id          = x[0], 
                email       = x[1],
                password    = x[2],
                image       = x[5],
                gender      = x[6],
                lastName    = x[3],
                firstName   = x[4],
                city        = x[7],
                distric     = x[8],
                street      = x[9],
                address     = x[10],
                phone       = x[11],
                birthDay    = x[12],
                acc_point   = x[13],
            )
            return (_cus)
        cus = Customer()
        return cus
    
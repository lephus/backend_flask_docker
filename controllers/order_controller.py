from models.orders_model import Order
from configdb.connectdb import connectdb
from datetime import date, datetime, timedelta
class orderController:
    def __init__(self) -> None:
        pass
    
    def runOrder(self, id, codeOrder, city, district, street, address, phone, note, shiperId,name, products):
        createdAt       = datetime.now()
        DateOfDeli      = datetime.now() + timedelta(minutes=5000) # 5 ngay sao giao hang
        sql1            = "INSERT INTO `orders` (`codeOrder`, `customerId`, `name`, `city`, `district`, `street`, `address`, `phone`, `note`, `shiperId`, `statusOrderId`, `createdAt`, `DateOfDeli`) VALUES ('"+str(codeOrder)+"', '"+str(id)+"',  '"+str(name)+"', '"+str(city)+"','"+str(district)+"','"+str(street)+"','"+str(address)+"','"+str(phone)+"','"+str(note)+"','"+str(shiperId)+"','1','"+str(createdAt)+"','"+str(DateOfDeli)+"')"
        connectdb.insertData(sql1)
        sqlCount        = "SELECT * FROM `orders` ORDER BY `orders`.`id` DESC"
        myresult2       = connectdb.executeQuery(sqlCount)
        tmp             = myresult2[0]
        id_order        = tmp[0]
        for x in products:
            total = int(x['quantity']) * ( int(x['price']) * ((int(100) - int(x['sale'])) /100) )
            print(total)
            sql3 = "INSERT INTO `orderdetails`(`orderId`, `proId`, `quantity`, `total`, `color`, `zise`) VALUES ('"+str(id_order)+"','"+str(x['id'])+"','"+str(x['quantity'])+"','"+str(total)+"','"+str(x['image'])+"','"+str(x['size'])+"')"
            connectdb.insertData(sql3)
        return ({"messenger" : "Order thành công!"})

    def orderHistory(self, id):
        sql         = "SELECT * FROM `orders` WHERE orders.customerId = "+str(id)
        myresult    = connectdb.executeQuery(sql)
        res         = []
        for x in myresult:
            totallMoneyOrderList = int(50000)
            detail      = []
            sql2        = "SELECT * FROM `orderdetails` INNER JOIN products ON products.id = orderdetails.proId WHERE orderdetails.orderId = "+str(x[0])
            myresult2   = connectdb.executeQuery(sql2)
            for y in myresult2:
                totallMoneyOrderList += int(y[4])
                print(str("y[4]")+str(int(y[4])))
                detail_o = {
                    "proName"   : y[8],
                    "quantity"  : y[3],
                    "color"     : y[5],
                    "size"      : y[6],
                    "total"     : y[4]
                }
                detail.append(detail_o)
            sql3        = "SELECT * FROM `statusorder` WHERE statusorder.id = "+str(x[11])
            myresult3   = connectdb.executeQuery(sql3)
            nameStatus  = ""
            desStatus   = ""
            for z in myresult3:
                nameStatus = z[1]
                desStatus  = z[2]
            print(totallMoneyOrderList)
            order = {
                "id"                    : x[0],
                "codeOrder"             : x[1],
                "name"                  : x[3],
                "city"                  : x[4],
                "district"              : x[5],
                "street"                : x[6],
                "address"               : x[7],
                "phone"                 : x[8],
                "note"                  : x[9],
                "nameStatus"            : nameStatus,
                "desStatus"             : desStatus,
                "createdAt"             : x[12],
                "dateOfDeli"            : x[13],
                "detail"                : detail,
                "totallMoneyOrderList"  : totallMoneyOrderList
            }
            res.append(order)    
        return res
    def getStatusOrder(self, id):
        sql         = "SELECT * FROM `orders` WHERE orders.id = "+str(id)
        myresult    = connectdb.executeQuery(sql)
        for x in myresult:
            sql3        = "SELECT * FROM `statusorder` WHERE statusorder.id = "+str(x[11])
            myresult3   = connectdb.executeQuery(sql3)
            for z in myresult3:
                return z[0]
        return 1

    def updateStatusOrder(self, id, status):
        if(int(status) == 6):
            sql_orderdetails        = "SELECT * FROM `orderdetails` WHERE `orderdetails`.`orderId` = '"+str(id)+"'"
            myresult                = connectdb.executeQuery(sql_orderdetails)
            for z in myresult:
                quanty              = int(z[3])
                print(quanty)
                sql_tmp             = "SELECT * FROM `prosizes` WHERE `prosizes`.proId = '"+str(z[2])+"' AND  `prosizes`.`size` = '"+str(z[6])+"'"
                myresult2           = connectdb.executeQuery(sql_tmp)
                for x in myresult2:
                    number_new      = quanty - int(x[3])
                    print("sososo: "+str(x[3])+" -> "+str(number_new))
                    sql_up          = "UPDATE `prosizes` SET `number`= '"+str(number_new)+"'  WHERE `prosizes`.proId = '"+str(z[2])+"' AND  `prosizes`.`size` = '"+str(z[6])+"'"
                    myresult        = connectdb.RunQueryData(sql_up)


        sql              = "UPDATE `orders` SET `statusOrderId`= '"+str(status)+"' WHERE `orders`.id = '"+str(id)+"' ;"
        myresult         = connectdb.RunQueryData(sql)
        return myresult

    def deleteOrder(self, id):
        sql      = "DELETE FROM `orders` WHERE `orders`.id = '"+str(id)+"' ;"
        myresult = connectdb.RunQueryData(sql)
        return myresult
    @staticmethod
    def orderALL():
        sql = "SELECT * FROM `orders`"
        myresult = connectdb.executeQuery(sql)
        res = []
        
        for x in myresult:
            totallMoneyOrderList = int(50000)
            detail      = []
            sql2        = "SELECT * FROM `orderdetails` INNER JOIN products ON products.id = orderdetails.proId WHERE orderdetails.orderId = "+str(x[0])
            myresult2   = connectdb.executeQuery(sql2)
            for y in myresult2:
                totallMoneyOrderList += int(y[4])
                print(str("y[4]")+str(int(y[4])))
                detail_o = {
                    "proName"   : y[8],
                    "quantity"  : y[3],
                    "color"     : y[5],
                    "size"      : y[6],
                    "total"     : y[4]
                }
                detail.append(detail_o)
            sql3        = "SELECT * FROM `statusorder` WHERE statusorder.id = "+str(x[11])
            myresult3   = connectdb.executeQuery(sql3)
            nameStatus  = ""
            desStatus   = ""
            for z in myresult3:
                nameStatus = z[1]
                desStatus  = z[2]
            print(totallMoneyOrderList)
            order = {
                "id"                    : x[0],
                "codeOrder"             : x[1],
                "name"                  : x[3],
                "city"                  : x[4],
                "district"              : x[5],
                "street"                : x[6],
                "address"               : x[7],
                "phone"                 : x[8],
                "note"                  : x[9],
                "nameStatus"            : nameStatus,
                "desStatus"             : desStatus,
                "createdAt"             : x[12],
                "dateOfDeli"            : x[13],
                "detail"                : detail,
                "totallMoneyOrderList"  : totallMoneyOrderList
            }
            res.append(order)    
        return res
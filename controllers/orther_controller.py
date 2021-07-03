import re
from models.products_model import Product
from configdb.connectdb import connectdb

class OrtherController:
    def __init__(self) -> None:
        pass
    @staticmethod
    def getSupplier():
        sql = "SELECT * FROM `suppliers`"
        result = connectdb.executeQuery(sql)
        res = []
        for x in result:
            tmp  = {
                "id"    : x[0],
                "name"  : x[1],
            }
            res.append(tmp)
        return res
    @staticmethod
    def getCategory():
        sql = "SELECT * FROM `categores`"
        result = connectdb.executeQuery(sql)
        res = []
        for x in result:
            tmp  = {
                "id"    : x[0],
                "name"  : x[1],
            }
            res.append(tmp)
        return res
    @staticmethod
    def getStatusOrder():
        sql = "SELECT * FROM `statusorder`"
        result = connectdb.executeQuery(sql)
        res = []
        for x in result:
            tmp  = {
                "id"    : x[0],
                "name"  : x[1],
                "des"   : x[2]
            }
            res.append(tmp)
        return res

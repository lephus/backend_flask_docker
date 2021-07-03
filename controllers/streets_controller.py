from configdb.connectdb import connectdb

class Streets:
    def __init__(self) -> None:
        pass
    def getStreets(self, id):
        sql         = "SELECT * FROM `streets` WHERE `streets`.district_id = "+str(id)
        myresult1   = connectdb.executeQuery(sql)  
        result      = []
        for x in myresult1:
            dictionary_streets = {
                "id"   : x[0],
                "street" : x[1],
                "type" : x[2] 
            }      
            result.append(dictionary_streets)
        return result
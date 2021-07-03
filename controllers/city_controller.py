from configdb.connectdb import connectdb

class City:
    def __init__(self) -> None:
        pass
    def getAllCity(self):
        sql         = "SELECT * FROM `cities`"
        myresult1   = connectdb.executeQuery(sql)  
        result      = []
        for x in myresult1:
            dictionary_city = {
                "id"   : x[0],
                "district" : x[1],
                "type" : x[2],
            }      
            result.append(dictionary_city)
        return result
from configdb.connectdb import connectdb

class District:
    def __init__(self) -> None:
        pass
    def getDistrict(self, city_id):
        sql         = "SELECT * FROM `districts` WHERE `districts`.city_id = "+str(city_id)
        myresult1   = connectdb.executeQuery(sql)  
        result = []
        for x in myresult1:
            dictionary_districts = {
                "id"   : x[0],
                "district" : x[1],
                "type" : x[2] 
            }      
            result.append(dictionary_districts)
        return result
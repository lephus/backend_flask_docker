from models.products_model import Product
from configdb.connectdb import connectdb

class ProductControler:
    def __init__(self) -> None:
        pass
    @staticmethod
    def get_all_product():
        sql             = "SELECT * FROM `products` INNER JOIN suppliers ON products.supplierId = suppliers.id INNER JOIN categores ON products.categoryId = categores.id"
        myresult1       = connectdb.executeQuery(sql)

        result          = []
        for x in myresult1:
            sql2        = "SELECT * FROM `procolors` WHERE procolors.proId = "+str(x[0])
            myresult2   = connectdb.executeQuery(sql2)
            _colors     = []
            for y in myresult2:
                dictionary_color = {"img": y[2]}
                _colors.append(dictionary_color)
            _product = Product(
                id             =   x[0], 
                proName        =   x[1],  
                content        =   x[2], 
                proPrice       =   x[3], 
                proSale        =   x[4],
                colors         =   _colors,
                supplier       =   x[11],  
                category       =   x[21],   
                proDes         =   'xem ở chi tiết sản phẩm',  
                proSize        =    '',
                createdAt      =   x[8],  
                updateAt       =   x[9], 
            )
            result.append(_product.serializeHome())
        return result

    def get_product_by_suppliers(self, id_suppliers):
        sql         = "SELECT * FROM `products` INNER JOIN suppliers ON products.supplierId = suppliers.id INNER JOIN categores ON products.categoryId = categores.id WHERE suppliers.name like '%"+str(id_suppliers)+"%'"
        myresult1   = connectdb.executeQuery(sql)

        result      = []
        for x in myresult1:
            sql2    = "SELECT * FROM `procolors` WHERE procolors.proId = "+str(x[0])
            myresult2 = connectdb.executeQuery(sql2)
            _colors = []
            for y in myresult2:
                dictionary_color = {"img": y[2]}
                _colors.append(dictionary_color)
            _product = Product(
                id             =   x[0], 
                proName        =   x[1],  
                content        =   x[2], 
                proPrice       =   x[3], 
                proSale        =   x[4],
                colors         =   _colors,
                supplier       =   x[11],  
                category       =   x[21],   
                proDes         =   'xem ở chi tiết sản phẩm',
                proSize        =    '',  
                createdAt      =   x[8],  
                updateAt       =   x[9], 
            )
            result.append(_product.serializeHome())
        return result

    def get_new_hot_product(self):
        sql         = "SELECT * FROM `products` INNER JOIN suppliers ON products.supplierId = suppliers.id INNER JOIN categores ON products.categoryId = categores.id ORDER BY `products`.`createdAt` DESC"
        myresult1   = connectdb.executeQuery(sql)
        result      = []
        for x in myresult1:
            sql2        = "SELECT * FROM `procolors` WHERE procolors.proId = "+str(x[0])
            myresult2   = connectdb.executeQuery(sql2)
            _colors     = []
            for y in myresult2:
                dictionary_color = {"img": y[2]}
                _colors.append(dictionary_color)
            _product = Product(
                id             =   x[0], 
                proName        =   x[1],  
                content        =   x[2], 
                proPrice       =   x[3], 
                proSale        =   x[4],
                colors         =   _colors,
                supplier       =   x[11],  
                category       =   x[21],   
                proDes         =   'xem ở chi tiết sản phẩm',  
                proSize        =    '',
                createdAt      =   x[8],  
                updateAt       =   x[9], 
            )
            result.append(_product.serializeHome())
        return result


    def get_most_sold_product(self):
        sqlOrder    = "SELECT count(proId), proId FROM `orderdetails` GROUP BY proId ORDER BY `count(proId)` DESC"
        myresult    = connectdb.executeQuery(sqlOrder)
        result      = []
        for j in myresult:
            sql = "SELECT * FROM `products` INNER JOIN suppliers ON products.supplierId = suppliers.id INNER JOIN categores ON products.categoryId = categores.id WHERE products.id = "+str(j[1])
            myresult1 = connectdb.executeQuery(sql)
            for x in myresult1:
                sql2        = "SELECT * FROM `procolors` WHERE procolors.proId = "+str(x[0])
                myresult2   = connectdb.executeQuery(sql2)
                _colors     = []
                for y in myresult2:
                    dictionary_color = {"img": y[2]}
                    _colors.append(dictionary_color)
                _product = Product(
                    id             =   x[0], 
                    proName        =   x[1],  
                    content        =   x[2], 
                    proPrice       =   x[3], 
                    proSale        =   x[4],
                    colors         =   _colors,
                    supplier       =   x[11],  
                    category       =   x[21],   
                    proDes         =   'xem ở chi tiết sản phẩm',  
                    proSize        =    '',
                    createdAt      =   x[8],  
                    updateAt       =   x[9], 
                )
                result.append(_product.serializeHome())
            if(len(result) < 8):
                result.extend(self.get_all_product())
        return result
    
    def get_product_by_id(self, id_product):
        sql         = "SELECT * FROM `products` INNER JOIN suppliers ON products.supplierId = suppliers.id INNER JOIN categores ON products.categoryId = categores.id INNER JOIN prosizes ON prosizes.proId = products.id WHERE products.id = "+str(id_product)
        myresult1   = connectdb.executeQuery(sql)
        _size       = []
        for size in myresult1:
            s = {
                "id": size[24],
                "size": size[26],
                "number": size[27]
            }
            _size.append(s)
        for x in myresult1:
            sql2        = "SELECT * FROM `procolors` WHERE `procolors`.proId = "+str(x[0])
            myresult2   = connectdb.executeQuery(sql2)
            _colors     = []
            for y in myresult2:
                sqlListImg          = "SELECT * FROM `listdetailimgcolors` WHERE listdetailimgcolors.idColor = "+str(y[0])
                myList              = connectdb.executeQuery(sqlListImg)
                _list_detail_img    = []
                for z in myList:
                    _list_detail_img.append(z[1])
                dictionary_color = {
                    "id":y[0],
                    "img": y[2],
                    'list_detail_img': _list_detail_img
                }
                _colors.append(dictionary_color)
            _product = Product(
                id             =   x[0], 
                proName        =   x[1],  
                content        =   x[2], 
                proPrice       =   x[3], 
                proSale        =   x[4],
                colors         =   _colors,
                supplier       =   x[11],  
                category       =   x[21],   
                proDes         =   x[7],  
                proSize        =   _size,
                createdAt      =   x[8],  
                updateAt       =   x[9], 
            )
            return (_product.serialize())
        return ('{}')
    def delete_product_by_id(self, id_product):
        sql = "DELETE FROM `products` WHERE `products`.id = "+str(id_product)
        return connectdb.RunQueryData(sql)
    def insert_product(self, proName, content, proPrice, proSale, supplierId, categoryId, proDes, imageColor, listsize):
        sql1  = "INSERT INTO `products` (`proName`, `content`, `proPrice`, `proSale`, `supplierId`, `categoryId`, `proDes`) VALUES ('"+str(proName)+"', '"+str(content)+"', '"+str(proPrice)+"', '"+str(proSale)+"', '"+str(supplierId)+"', '"+str(categoryId)+"', '"+str(proDes)+"');"
        check = connectdb.RunQueryData(sql1)
        if(check['message'] != 'Successfully'):
            return {'message': 'failed'}
        #----------------
        id_sql = "SELECT * FROM products ORDER BY id DESC LIMIT 0, 1"
        res1   = connectdb.executeQuery(id_sql)
        x1     = res1[0]
        id_pro = x1[0]
        #----------------
        for i in  imageColor:
            imgColor    = i['image']
            detail      = i['detail'] #array
            sql2        = "INSERT INTO `procolors` ( `proId`, `image`, `increPrice`) VALUES ('"+str(id_pro)+"', '"+str(imgColor)+"', '0');"
            ok1         = connectdb.RunQueryData(sql2)
            #=======================
            isql2       = "SELECT * FROM procolors ORDER BY id DESC LIMIT 0, 1"
            res2        = connectdb.executeQuery(isql2)
            x2          = res2[0]
            id_color    = x2[0]
            #=======================
            for j in detail:
                img     = j['img']
                sql3    = "INSERT INTO `listdetailimgcolors`(`img`, `idColor`) VALUES ('"+str(img)+"','"+str(id_color)+"')"
                ok2     = connectdb.RunQueryData(sql3)
                print(ok2)
        for z in listsize:
            size        = z['size']
            number      = z['number']
            sql4        = "INSERT INTO `prosizes` (`id`, `proId`, `size`, `number`) VALUES (NULL, '"+str(id_pro)+"', '"+str(size)+"', '"+str(number)+"');"
            tmp4        = connectdb.RunQueryData(sql4)
        return tmp4

    def update_product(self,id, proName, content, proPrice, proSale, supplierId, categoryId, proDes, imageColor, listsize):
        sql1  = "UPDATE `products` SET `proName` = '"+str(proName)+"', `content` = '"+str(content)+"', `proPrice` = '"+str(proPrice)+"', `proSale` = '"+str(proSale)+"', `supplierId` = '"+str(supplierId)+"', `categoryId` = '"+str(categoryId)+"', `proDes` = '"+str(proDes)+"' WHERE `products`.id = '"+str(id)+"' ;"
        check = connectdb.RunQueryData(sql1)
        if(check['message'] != 'Successfully'):
            return {'message': 'failed'}
        #----------------
        delete_sql0 = "DELETE FROM `procolors` WHERE `procolors`.`proId` = '"+str(id)+"' ;"
        delete0     = connectdb.RunQueryData(delete_sql0)
        #----------------
        for i in  imageColor:
            imgColor = i['image']
            detail   = i['detail'] #array
            sql2     = "INSERT INTO `procolors` ( `proId`, `image`, `increPrice`) VALUES ('"+str(id)+"', '"+str(imgColor)+"', '0');"
            ok1      = connectdb.RunQueryData(sql2)
            #=======================
            isql2    = "SELECT * FROM procolors ORDER BY id DESC LIMIT 0, 1"
            res2     = connectdb.executeQuery(isql2)
            x2       = res2[0]
            id_color = x2[0]
            # delete_sql = "DELETE FROM `listdetailimgcolors` WHERE `listdetailimgcolors`.`idColor` = '"+str(id_color)+"' ;"
            # delete2 = connectdb.RunQueryData(delete_sql)
            #=======================
            for j in detail:
                img  = j['img']
                sql3 = "INSERT INTO `listdetailimgcolors`(`img`, `idColor`) VALUES ('"+str(img)+"','"+str(id_color)+"')"
                ok2  = connectdb.RunQueryData(sql3)
                print(ok2)
        delete_sql2  = "DELETE FROM `prosizes` WHERE `prosizes`.`proId` = '"+str(id)+"' ;"
        deleteSize   = connectdb.RunQueryData(delete_sql2)
        for z in listsize:
            size    = z['size']
            number  = z['number']
            sql4    = "INSERT INTO `prosizes` (`id`, `proId`, `size`, `number`) VALUES (NULL, '"+str(id)+"', '"+str(size)+"', '"+str(number)+"');"
            tmp4    = connectdb.RunQueryData(sql4)
        return tmp4

    def get_product_by_name(self, name):
        sql         = "SELECT * FROM `products` INNER JOIN suppliers ON products.supplierId = suppliers.id INNER JOIN categores ON products.categoryId = categores.id INNER JOIN prosizes ON prosizes.proId = products.id WHERE products.proName like '%"+str(name.strip())+"%';"
        print(sql)
        myresult1   = connectdb.executeQuery(sql)
        _size       = []
        for size in myresult1:
            s = {
                "id": size[24],
                "size": size[26],
                "number": size[27]
            }
            _size.append(s)
        for x in myresult1:
            sql2        = "SELECT * FROM `procolors` WHERE `procolors`.proId = "+str(x[0])
            myresult2   = connectdb.executeQuery(sql2)
            _colors     = []
            for y in myresult2:
                sqlListImg          = "SELECT * FROM `listdetailimgcolors` WHERE listdetailimgcolors.idColor = "+str(y[0])
                myList              = connectdb.executeQuery(sqlListImg)
                _list_detail_img    = []
                for z in myList:
                    _list_detail_img.append(z[1])
                dictionary_color = {
                    "id":y[0],
                    "img": y[2],
                    'list_detail_img': _list_detail_img
                }
                _colors.append(dictionary_color)
            _product = Product(
                id             =   x[0], 
                proName        =   x[1],  
                content        =   x[2], 
                proPrice       =   x[3], 
                proSale        =   x[4],
                colors         =   _colors,
                supplier       =   x[11],  
                category       =   x[21],   
                proDes         =   x[7],  
                proSize        =   _size,
                createdAt      =   x[8],  
                updateAt       =   x[9], 
            )
            return (_product.serialize())
        return ('{}')
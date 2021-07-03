from configdb.connectdb import connectdb
import requests
from bs4 import BeautifulSoup
import random
import string
from random import randint
import re

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

response = requests.get("https://giayxshop.vn/danh-muc/giay-thoi-trang")
#print(response)
soup = BeautifulSoup(response.content, "html.parser")
paren = soup.findAll('h3', class_='woocommerce-loop-product__title')

id = 40
idcolor = 69

for i in paren:
    id += 1
    ok1 = i.find('a')
    print(ok1['href'])
    response = requests.get(ok1['href'])
    #print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find('h1', class_='product_title entry-title').text
    content = "Chất liệu cao cấp, bền đẹp theo thời gian. Thiết kế thời trang. Kiểu dáng phong cách. Độ bền cao. Dễ phối đồ.";
    price = soup.findAll('span', class_='woocommerce-Price-amount amount')
    j = 0
    cost = 0
    p1,p2 = 0, 0
    for i in price:
        j+=1
        k = str(i.text)
        t =  int(re.sub(r'\D', "", k))
        if(j==0):
            p1 = t
            cost = p1/2+50000
        if(j==1):
            p2 = p1 - t
        if(j==2):
            break

    colors = soup.findAll('label', class_='wcvaswatchlabel')
    listColor = [] #mau
    for x in colors:
        tmpImg = x["style"].split('(')
        if(len(tmpImg) > 1 ):
            tmp = tmpImg[1].split(')')
            listColor.append(tmp[0])


    listImg = soup.findAll('img')
    srcImg = []
    for x in listImg:
        if ('https' in x['src']):
            srcImg.append(x['src'])
    des = soup.find('div', class_='elementor-section-wrap')
    print(titles)
    supplierId = randint(1, 4)
    categoryId = randint(1, 6)
    batch = randomword(10).upper()

    des = str(des)
    des = des.replace("'", '"')
    huhu = randint(200,1001)
    sql = "INSERT INTO `products`(`id`,`proName`, `proCost`, `proPrice`, `proSale`, `proDes`, `supplierId`, `categoryId`, `batch`,`content` ) VALUES ('"+str(id)+"','"+str(titles)+"','"+str(huhu)+"000','"+str(huhu+randint(200, 600))+"000','"+str(randint(5, 20))+"','"+str(des)+"','"+str(supplierId)+"','"+str(categoryId)+"','"+batch+"','"+str(content)+"')"
    myresult = connectdb.insertData(sql)
    size1 = [36,38,39,42,46,47]
    size2 = [38,39,40,41,42,46,48]
    size3 = [39,40,41,45,46,48]
    size4 = [35,39,40,44,48]
   
    for elementColor in listColor:
        tmp = randint(3, 6)
        idcolor+=1
        sql2 = "INSERT INTO `procolors`(`id`, `proId`, `image`, `increPrice`) VALUES ('"+str(idcolor)+"','"+str(id)+"','"+str(elementColor)+"','"+str(randint(10, 200))+"000')"
        myresult = connectdb.insertData(sql2)
        for j in range(0,randint(3, 6)):
            p = randint(0,len(listColor)-1)
            sql4 = "INSERT INTO `listdetailimgcolors`(`img`, `idColor`) VALUES ('"+str(listColor[p])+"','"+str(idcolor)+"')"
            myresult = connectdb.insertData(sql4)
        check = randint(1, 4)
        if(check == 1):    
            for i in size1:
                sql3 = "INSERT INTO `prosizes`(`proId`, `colorId`, `size`, `number`) VALUES ('"+str(id)+"','"+str(idcolor)+"','"+str(i)+"','"+str(randint(10,200))+"')"
                myresult = connectdb.insertData(sql3)
        if(check == 2):    
            for i in size2:
                sql3 = "INSERT INTO `prosizes`(`proId`, `colorId`, `size`, `number`) VALUES ('"+str(id)+"','"+str(idcolor)+"','"+str(i)+"','"+str(randint(10,200))+"')"
                myresult = connectdb.insertData(sql3)
        if(check == 3):    
            for i in size3:
                sql3 = "INSERT INTO `prosizes`(`proId`, `colorId`, `size`, `number`) VALUES ('"+str(id)+"','"+str(idcolor)+"','"+str(i)+"','"+str(randint(10,200))+"')"
                myresult = connectdb.insertData(sql3)
        if(check == 4):    
            for i in size4:
                sql3 = "INSERT INTO `prosizes`(`proId`, `colorId`, `size`, `number`) VALUES ('"+str(id)+"','"+str(idcolor)+"','"+str(i)+"','"+str(randint(10,200))+"')"
                myresult = connectdb.insertData(sql3)

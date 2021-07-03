from configdb.connectdb import connectdb
import re
from datetime import date, datetime, timedelta
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from flask import send_file
from werkzeug.datastructures import  FileStorage
import string
import random
import os
from flask import Flask, flash, request, redirect, url_for
from flask_jwt_extended import JWTManager
from os import name
from datetime import timedelta
from models.customers_model import Customer
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask_mail import Mail, Message
from controllers.admins_controller import AdminController
from controllers.customer_controller import CustomerController
from controllers.products_controller import ProductControler
from controllers.city_controller import City
from controllers.districts_controller import District
from controllers.streets_controller import Streets
from controllers.order_controller import orderController
from controllers.forgotpassword_controller import ForgotPassword
from controllers.orther_controller import OrtherController
from models.admins_model import Admin
import hashlib
from flask_cors import CORS

PATH                                    = "E:\HOC KY II (2020)\CNWEB\TUHOC_FLASK"
UPLOAD_FOLDER_CUSTOMER                  = PATH+"/images/customer/"
UPLOAD_FOLDER_ADMIN                     = PATH+"/images/admin/"
UPLOAD_FOLDER_PRODUCT                   = PATH+"/images/product/"
ALLOWED_EXTENSIONS                      = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER_CUSTOMER']    = UPLOAD_FOLDER_CUSTOMER
app.config['UPLOAD_FOLDER_ADMIN']       = UPLOAD_FOLDER_ADMIN
app.config['UPLOAD_FOLDER_PRODUCT']     = UPLOAD_FOLDER_PRODUCT
app.config["DEBUG"]                     = True
app.config["TESTING"]                   = False
app.config['MAIL_SERVER']               = 'smtp.gmail.com'
app.config['MAIL_PORT']                 = 587
app.config['MAIL_USE_TLS']              = True
app.config['MAIL_USE_SSL']              = False
#app.config['MAIL_DEBUG']               = True       
app.config['MAIL_USERNAME']             = 'phule002abc@gmail.com'
app.config['MAIL_PASSWORD']             = 'matkhauphule002abc@gmail.com'
app.config['MAIL_DEFAULT_SENDER']       = 'phule002abc@gmail.com'
app.config['MAIL_MAX_EMAILS']           = 2000
app.config['MAIL_ASCII_ATTACHMENTS']    = True
mail = Mail(app)
app.config['JWT_SECRET_KEY']            = "akdncjd938rnfoei039d_team_of_3_idiots"
ACCESS_EXPIRES                          = timedelta(hours=6)
app.config["JWT_ACCESS_TOKEN_EXPIRES"]  = ACCESS_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
CORS(app)

user='root'
password=''
host='127.0.0.1'
database='footwear_db'


# if __name__ == '__main__':
#      app.run(host='0.0.0.0', port='5000', debug=True)

@app.route("/")
def helloWorld():
    return "Hello, cross-origin-world!"

# ------------------------ ADMIN -----------------------------------
@app.route('/admin/upload_image', methods=['POST'])
@jwt_required()
def upload_file_admin():
    curent_user         = get_jwt_identity()
    id                  = curent_user['id']
    admincontroller     = AdminController()
    _ad                 = admincontroller.get_admin_ID(id)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    else:
        file.filename   = str(datetime.now())+".png"
        filename        = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_ADMIN'], filename))
        url             = os.path.join(app.config['UPLOAD_FOLDER_ADMIN'], filename)
    _ad.image           = create_url_image_admin(filename)
    admincontroller.update_admin_byId(_ad)
    return jsonify(_ad.serialize()), 200


@app.route('/admin/getAllAdmin', methods=['GET'])
@jwt_required()
def GetAllAdmin():
    adminControler  = AdminController()
    result          = adminControler.get_all_admin()
    return jsonify(result)
    
@app.route('/admin', methods=['GET', 'PUT','DELETE'])
@jwt_required()
def RequestAdminById():
    curent_user         = get_jwt_identity()
    id                  = curent_user['id']
    
    if (request.method =='GET'):
        adminControler = AdminController()
        result = adminControler.get_admin_byId(id)
        if result['id'] == '':
            return jsonify({"message":"Không tìm thấy thông tin tài khoản này."}), 404
        return jsonify(result)
    if (request.method =='DELETE' and curent_user['roleId'] == 'Admin'):
        adminControler = AdminController()
        result = adminControler.delete_admin_byId(id)
        return jsonify({"message":"Xóa thành công."}), 200
    if (request.method =='DELETE' and curent_user['roleId'] != 'Admin'):
        return jsonify({"message":"Bạn không đủ quyền thực hiện việc này!"}), 403
    if (request.method =='PUT'):
        adminControler = AdminController()
        _admin         = adminControler.get_admin_ID(id)
        body           = request.json
        email          = body.get('email', _admin.email)
        pas            = body.get('confirmPassword', '')
        password       = ""
        if(pas == ''):
            password = _admin.password
        else:
            ConirmNewPas      = body.get('confirmPassword', '')
            Newpas            = body.get('passwordNew', '')
            tmp               =  hashlib.md5(body.get('passwordOld', '').encode())
            pasOld            = tmp.hexdigest()
            if(pasOld !=  _admin.password):
                return jsonify({
                    'message': "Bạn nhập sai mật khẩu cũ !"
                }), 406
            if(Newpas !=  ConirmNewPas):
                return jsonify({
                    'message': "Xác nhận mật khẩu sai !"
                }), 406
            pas = hashlib.md5(Newpas.encode())
            password = pas.hexdigest()
        image      = body.get('image', _admin.image)
        gender     = body.get('gender', _admin.gender)
        lastName   = body.get('lastName', _admin.lastName)
        firstName  = body.get('firstName', _admin.firstName)
        city       = body.get('city', _admin.city)
        distric    = body.get('distric', _admin.distric)
        street     = body.get('street', _admin.street)
        address    = body.get('address', _admin.address)
        phone      = body.get('phone', _admin.phone)
        birthDay   = body.get('birthDay', _admin.birthDay)
        roleId     = body.get('roleId', _admin.roleId)
        admin = Admin(id, email, password, image, gender, lastName, firstName , city, distric, street, address, phone, birthDay, roleId)
        adminControler = AdminController()
        result, status = adminControler.update_admin_byId(admin)
        return jsonify(result), status
    
@app.route('/admin/register', methods=['POST'])
def add_admin():
    body                = request.json
    email               = body.get('email', '')
    image               = 'http://127.0.0.1:5000/image/admin/default.png'
    gender              = body.get('gender', '')
    lastName            = body.get('lastName', '')
    firstName           = body.get('firstName', '')
    city                = body.get('city', '97') 
    distric             = body.get('distric', '974') 
    street              = body.get('street', '32249')
    address             = body.get('address', '')
    phone               = body.get('phone', '')
    birthDay            = body.get('birthDay', '')
    roleId              = body.get('roleId', '2')
    pas                 = hashlib.md5(body.get('password', '').encode())
    password            = pas.hexdigest()
    forgotPassword      = ForgotPassword()
    if body.get('password', '') == '' or len(body.get('password', ''))<6:
        return jsonify({
            'message': "Mật khẩu phải chứa ít nhất 6 ký tự"
        }), 403
    if forgotPassword.checkMailAdminExit(email) == 0 or forgotPassword.checkMailCustommerExit(email) == 0:
        return jsonify({
            'message': "Email đã tồn tại trong hệ thống, hãy dùng email khác."
        }), 403
    admin               = Admin('', email, password, image, gender, lastName, firstName , city, distric, street, address, phone, birthDay, roleId)
    adminControler      = AdminController()
    result              = adminControler.add_admin(admin)
    return jsonify(result)
   

@app.route('/admin/login', methods=['POST'])
def login_admin():
    body                = request.json
    email               = body.get('email', '')
    pas                 = hashlib.md5(body.get('password', '').encode())
    password            = pas.hexdigest()
    adminControler      = AdminController()
    result, status_code = adminControler.login_admin(email, password)
    forgotPassword      = ForgotPassword()
    if forgotPassword.checkMailAdminExit(email) == 0:
        return jsonify({
            'message': "Email đăng nhập sai"
        }), 401
    result, status_code = adminControler.login_admin(email, password)
    if(status_code != 200):
        return jsonify({
            'message': "Mật khẩu đăng nhập sai"
        }), status_code
    # luu thong tin dang nhap vao token
    access_token = create_access_token(identity=result.serialize())
    return jsonify({
        'message': "Đăng nhập thành công",
        'token': access_token,
        'account':result.serialize()
    }), 200

@app.route('/admin/forgotpassword', methods=['POST'])
def AdminforgotPassword():
    body            = request.json
    email           = body.get('email', '')
    # check eamil is exit, check limit 
    forgotPassword  = ForgotPassword()
    id              = forgotPassword.checkMailAdminExit(email)
    if( id != 0 and forgotPassword.checkLimitMailSend()):
        code        = id_generator()
        forgotPassword.saveCodeAdmin(code, id)
        msg         = Message(str(code)+' là mã xác nhận LTP_Xshop của bạn', recipients=[email])
        msg.html    = """<div style="text-align: left;"><h1> """+str(code)+""" là mã xác nhận tài tài khoản của bạn </h1><h1 style="color:rgb(2, 84, 87);">LTP Xshop</h1><p>Chúng tôi đã nhận được yêu cầu đặt lại mật khẩu của bạn.Nhập mã đặt lại mật khẩu sau đây</p><h1 style="color:rgb(255, 0, 0);">Lưu ý:<h2>Mã này có giá trị trong 5 phút, tính từ lúc bạn gửi yêu cầu</h2></h1><i>Tin nhắn này được gửi tới """+str(email)+""" theo yêu cầu của bạn.LTP_Xshop, Inc., Attention: Community Support, 1 LTP xshop Way, Menlo Park, CA 94025</i></div>"""
        mail.send(msg)
        return jsonify({"message":"Vui lòng kiểm tra mail của bạn, để nhận mã xác thực gồm 6 chữ số."}), 200
    if id == 0:
        return jsonify({"message":"Email bạn vừa nhập không có trong hệ thống."}), 406
    return jsonify({"message":"Người dùng hàng ngày đã vượt quá hạn ngạch gửi, thử lại sau 24h."}), 503

#------------------------- MANAGER SHOP ----------------------------

@app.route('/manager/customer/<int:id>', methods=['DELETE'])
@jwt_required()
def managerCustomer(id):
    customerController = CustomerController()
    check = customerController.get_customer_byId(id)
    if check['id'] == '':
        return jsonify({"message":"Xóa thất bại.Không tìm thấy tài khoản này."}), 404
    result = customerController.delete_customer_byId(id)
    return  jsonify({"message":"Xóa thành công."}), 200



#------------------------- ++++++++++++ ----------------------------




# ------------- END ADMIN --------------------
# ------------- CUSTOMER---------------------
@app.route('/customer/upload_image', methods=['POST'])
@jwt_required()
def upload_file_customer():
    curent_user         = get_jwt_identity()
    id                  = curent_user['id']
    customerController  = CustomerController()
    _cus                = customerController.customer_ID(id)
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({
            'message': "No file part"
        })
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return jsonify({
            'message': "No selected file"
        })
    else:
        file.filename   = str(datetime.now())+".png"
        filename        = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_CUSTOMER'], filename))
        url             = os.path.join(app.config['UPLOAD_FOLDER_CUSTOMER'], filename)
    _cus.image          = create_url_image_customer(filename)
    customerController.update_customer_byId(_cus)
    return jsonify(_cus.serialize()), 200

@app.route('/customer/getAllCustomer', methods=['GET'])
@jwt_required()
def GetAllCustomer():
    customerController = CustomerController()
    result = customerController.get_all_customer()
    return jsonify(result)
    
    
@app.route('/customer/login', methods=['POST'])
def login_customer():
    body                = request.json
    email               = body.get('email', '')
    pas                 = hashlib.md5(body.get('password', '').encode())
    password            = pas.hexdigest()
    customerController  = CustomerController()
    forgotPassword      = ForgotPassword()
    if forgotPassword.checkMailCustommerExit(email) == 0 :
        return jsonify({
            'message': "Email đăng nhập sai"
        }), 401
    result, status_code = customerController.login_customer(email, password)
    if(status_code != 200):
        return jsonify({
            'message': "Mật khẩu đăng nhập sai"
        }), status_code
    # luu thong tin dang nhap vao token
    access_token = create_access_token(identity=result.serialize())
    return jsonify({
        'message': "Đăng nhập thành công",
        'token': access_token,
        'account':result.serialize()
    }), 200


@app.route('/customer', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def funtionCustomer():
    customerController  = CustomerController()
    curent_user         = get_jwt_identity()
    id                  = curent_user['id']
    # get profile
    if(request.method == 'GET'):
        result = customerController.get_customer_byId(id)
        if result['id'] == '':
            return jsonify({"message":"Không tìm thấy tài khoản này."}), 404
        return jsonify(result), 200
    #update profile
    if(request.method == 'PUT'):
        body                    = request.json
        _cus                    = customerController.customer_ID(id)
        email                   = body.get('email', _cus.email)
        image                   = _cus.image 
        gender                  = body.get('gender', _cus.gender)
        lastName                = body.get('lastName', _cus.lastName) 
        firstName               = body.get('firstName', _cus.firstName)
        city                    = body.get('city', _cus.city) 
        distric                 = body.get('distric', _cus.distric) 
        street                  = body.get('street', _cus.street)
        address                 = body.get('address', _cus.address) 
        phone                   = body.get('phone', _cus.phone)
        birthDay                 = body.get('birthDay', _cus.birthDay) 
        acc_point               = body.get('acc_point', _cus.acc_point)
        sample_string           = body.get('new_password', '')
        password                = _cus.password
        if(sample_string != ''):
            ConirmNewPas        = body.get('confirm_new_password', '')
            Newpas              = body.get('new_password', '')
            if Newpas == '' or Newpas == None:
                return jsonify({"message": "Mật khẩu không được để trống."}), 401
            if  len(str(Newpas)) <6:
                return jsonify({"message": "Mật khẩu phải chứa ít nhấ 6 ký tự."}), 401
            tmp                 =  hashlib.md5(body.get('old_password', '').encode())
            pasOld              = tmp.hexdigest()
            if(pasOld !=  _cus.password):
                return jsonify({
                    'message': "Bạn nhập sai mật khẩu cũ !"
                }), 406
            if(Newpas !=  ConirmNewPas):
                return jsonify({
                    'message': "Xác nhận mật khẩu sai !"
                }), 406
            pas = hashlib.md5(Newpas.encode())
            password = pas.hexdigest()
        else:
            password = _cus.password
        customer = Customer(id, email, password, image, gender, lastName, firstName, city, distric, street, address, phone, birthDay, acc_point)
        result = customerController.update_customer_byId(customer)
        return jsonify(result)
    #delete profile
    if(request.method == 'DELETE'):
        check = customerController.get_customer_byId(id)
        if check['id'] == '':
            return jsonify({"message":"Xóa thất bại.Không tìm thấy tài khoản này."}), 404
        result = customerController.delete_customer_byId(id)
        return  jsonify({"message":"Xóa thành công."}), 200
       

@app.route('/customer/register', methods=['POST'])
def customerRegister():
    #register
    customerController  = CustomerController()
    body                = request.json
    email               = body.get('email', '')
    image               = 'http://127.0.0.1:5000/image/customer/default.png'
    gender              = body.get('gender', '')
    lastName            = body.get('lastName', '') 
    firstName           = body.get('firstName', '')
    city                = body.get('city', '97') 
    distric             = body.get('distric', '974') 
    street              = body.get('street', '32249')
    address             = body.get('address', '') 
    phone               = body.get('phone', '')
    birthDay             = body.get('birthDay', '') 
    acc_point           = body.get('acc_point', '')
    pas                 = body.get('password', '')
    tmp                 = hashlib.md5(pas.encode())
    password            = tmp.hexdigest()
    if pas == '' or pas == None:
        return jsonify({"message": "Mật khẩu không được để trống."}), 401
    if  len(str(pas)) <6:
        return jsonify({"message": "Mật khẩu phải chứa ít nhấ 6 ký tự."}), 401
    forgotPassword      = ForgotPassword()
    if forgotPassword.checkMailCustommerExit(email) == 0:
        customer        = Customer('', email, password, image, gender, lastName, firstName, city, distric, street, address, phone, birthDay, acc_point, ok='ok')
        customerController.add_customer(customer)
        return jsonify({"message": "Đăng ký thành công"})
    return jsonify({"message": "Email đã tồn tại!"}), 401

@app.route('/customer/forgotpassword', methods=['POST'])
def forgotPassword():
    forgotPassword  = ForgotPassword()
    body            = request.json
    email           = body.get('email', '')
    # check eamil is exit, check limit 
    id              = forgotPassword.checkMailCustommerExit(email)
    if( id != 0 and forgotPassword.checkLimitMailSend()):
        code        = id_generator()
        forgotPassword.saveCodeCustomer(code, id)
        msg         = Message(str(code)+' là mã xác nhận LTP_Xshop của bạn', recipients=[email])
        msg.html    = """<div style="text-align: left;"><h1> """+str(code)+""" là mã xác nhận tài tài khoản của bạn </h1><h1 style="color:rgb(2, 84, 87);">LTP Xshop</h1><p>Chúng tôi đã nhận được yêu cầu đặt lại mật khẩu của bạn.Nhập mã đặt lại mật khẩu sau đây</p><h1 style="color:rgb(255, 0, 0);">Lưu ý:<h2>Mã này có giá trị trong 30 phút, tính từ lúc bạn gửi yêu cầu</h2></h1><i>Tin nhắn này được gửi tới """+str(email)+""" theo yêu cầu của bạn.LTP_Xshop, Inc., Attention: Community Support, 1 LTP xshop Way, Menlo Park, CA 94025</i></div>"""
        mail.send(msg)
        return jsonify({"message":"Vui lòng kiểm tra mail của bạn, để nhận mã xác thực gồm 6 chữ số."}), 200
    if forgotPassword.checkMailCustommerExit(email) == 0:
        return jsonify({"message":"Email bạn vừa nhập không có trong hệ thống."}), 406
    return jsonify({"message":"Người dùng hàng ngày đã vượt quá hạn ngạch gửi, thử lại sau 24h."}), 503


#-------------- END CUSTOMER ----------------


#-------------- PRODUCT ---------------------

@app.route('/product/getAllProduct', methods=['GET'])
def GetAllProduct():
    productController   = ProductControler()
    result              = productController.get_all_product()
    return jsonify(result)

@app.route('/product/getProductBySuppliers/<id>', methods=['GET'])
def GetProductBySuppliers(id):
    productController   = ProductControler()
    result              = productController.get_product_by_suppliers(id)
    return jsonify(result)

@app.route('/product/listNewProduct', methods=['GET'])
def getProductNew():
    productController   = ProductControler()
    result              = productController.get_new_hot_product()
    return jsonify(result)

@app.route('/product/getProductMostSold', methods=['GET'])
def getProductMostSold():
    productController   = ProductControler()
    result              = productController.get_most_sold_product()
    return jsonify(result)

@app.route('/product/getProductById/<int:id>', methods=['GET'])
def getProductById(id):
    productController   = ProductControler()
    result              = productController.get_product_by_id(id)
    return jsonify(result)

@app.route('/product', methods=['POST'])
@jwt_required()
def insertProduct():
    body        = request.json
    proName     = body.get("proName", "")
    content     = body.get("content", "")
    proPrice    = body.get("proPrice", "")
    proSale     = body.get("proSale", "")
    supplierId  = body.get("supplierId", "")
    categoryId  = body.get("categoryId", "")
    proDes      = body.get("proDes", "")
    ''' 
        imageColor: [
            {
                "image": "url image color 1",
                "detail": [
                    "img": "detail 1.1",
                    "img": "detail 1.2",
                    "img": "detail 1.3",
                    ...
                ]
            },
            {
                "image": "url image color 2",
                "detail": [
                    "img": "detail 2.1",
                    "img": "detail 2.2",
                    "img": "detail 2.3",
                    ...
                ]
            },
            ...
        ]
    '''
    imageColor  = body.get("imageColor", []) 
    ''' 
        listsize: [
            {"size"  : "40",
            "number": "2"},
            {"size"  : "40",
            "number": "2"},
            ...
        ]
    '''
    listsize            = body.get("listsize", [])
    productController   = ProductControler()
    result              = productController.insert_product(proName, content, proPrice, proSale, supplierId, categoryId, proDes, imageColor, listsize)
    return jsonify(result), 200

@app.route('/product/<int:id>',methods=['PUT', 'DELETE'])
@jwt_required()
def functionProduct(id):
    productController = ProductControler()
    if request.method == 'DELETE':
        result        = productController.delete_product_by_id(id)
        return jsonify(result), 200
    if request.method == 'PUT':
        body        = request.json
        proName     = body.get("proName", "")
        content     = body.get("content", "")
        proPrice    = body.get("proPrice", "")
        proSale     = body.get("proSale", "")
        supplierId  = body.get("supplierId", "")
        categoryId  = body.get("categoryId", "")
        proDes      = body.get("proDes", "")
        ''' 
            imageColor: [
                {
                    "image": "url image color 1",
                    "detail": [
                        "img": "detail 1.1",
                        "img": "detail 1.2",
                        "img": "detail 1.3",
                        ...
                    ]
                },
                {
                    "image": "url image color 2",
                    "detail": [
                        "img": "detail 2.1",
                        "img": "detail 2.2",
                        "img": "detail 2.3",
                        ...
                    ]
                },
                ...
            ]
        '''
        imageColor  = body.get("imageColor", []) 
        ''' 
            listsize: [
                {"size"  : "40",
                "number": "2"},
                {"size"  : "40",
                "number": "2"},
                ...
            ]
        '''
        listsize            = body.get("listsize", [])
        productController   = ProductControler()
        result              = productController.update_product(id, proName, content, proPrice, proSale, supplierId, categoryId, proDes, imageColor, listsize)
        return jsonify(result), 200


@app.route('/product/upload_image', methods=['POST'])
@jwt_required()
def upload_file_product():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({
            'message': "No file part"
        })
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return jsonify({
            'message': "No selected file"
        })
    else:
        file.filename   = str(datetime.now())+".png"
        filename        = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_PRODUCT'], filename))
        url             = os.path.join(app.config['UPLOAD_FOLDER_PRODUCT'], filename)

    return jsonify({"url_image": "http://127.0.0.1:5000//image/product/"+str(filename)}), 200

@app.route('/search/<name>', methods=['GET'])
def search(name):
    productController   = ProductControler()
    result              = productController.get_product_by_name(name)
    return jsonify(result)

#-------------- END PRODUCT -----------------
#-------------- ORDER -----------------------
@app.route('/order', methods=['POST'])
@jwt_required()
def confirmOrder():
    curent_user = get_jwt_identity()
    id          = curent_user['id']
    #infor
    body        = request.json
    codeOrder   = id_generator()
    city        = body.get("city", "")
    district    = body.get("district", "")
    street      = body.get("street", "")
    address     = body.get("address", "")
    shiperId    = '1'
    phone       = body.get("phone", "")
    note        = body.get("note", "")
    name        = body.get("name", "")
    # list product
    '''
        product:[
            {
                "id":1,
                "price":500000,
                "sale":43,
                "image":2,
                "size":2,
                "quantity":1
            },
            {
                "id":1,
                "price":120000,
                "sale":43,
                "image":2,
                "size":2,
                "quantity":1
            }
        ]
    '''
    products    = list(body.get("products"))
    order       = orderController()
    result      = order.runOrder(id, codeOrder, city, district, street, address, phone, note, shiperId, name, products)
    return jsonify(result)

@app.route('/orderAll', methods=['GET'])
@jwt_required()
def orderAll():
    orderContro = orderController()
    result      = orderContro.orderALL()
    return jsonify(result), 200


@app.route('/order/<int:id>', methods=['DELETE'])
@jwt_required()
def DeleteOrder():
    order   = orderController()
    res     = order.deleteOrder(id)
    return jsonify(res), 200


@app.route('/order/history', methods=['GET'])
@jwt_required()
def orderHistory():
    curent_user = get_jwt_identity()
    id          = curent_user['id']
    orderContro = orderController()
    result      = orderContro.orderHistory(id)
    return jsonify(result), 200

@app.route('/order/status', methods=['PUT'])
@jwt_required()
def updateStatusOrder():
    body        = request.json
    id          = body.get("id", "")
    status      = body.get("status", "")
    order       = orderController()
    id_status_old = order.getStatusOrder(id)
    if int(id_status_old) == 6:
        return jsonify({"message": "Đơn hàng của bạn đã được thanh toán, không thể cập nhật lại."}), 403
    if int(id_status_old) == 7:
        return jsonify({"message": "Đơn hàng của bạn đã bị hủy, không thể cập nhật lại."}), 403
    if int(status) < int(id_status_old):
        return jsonify({"message": "Bạn không thể cập nhật trạng thái đơn hàng đi ngược."}), 403
    
    res         = order.updateStatusOrder(id, status)
    return jsonify(res), 200

#-------------- END ORDER -------------------

#-------------- PROCESS ADDRESS -------------
@app.route('/city', methods=['GET'])
def getCity():
    city        = City()
    result      = city.getAllCity()
    return jsonify(result)
@app.route('/district/<int:id>', methods=['GET'])
def getDistrict(id):
    district    = District()
    result      = district.getDistrict(id)
    return jsonify(result)
@app.route('/streets/<int:id>', methods=['GET'])
def getStreets(id):
    street      = Streets()
    result      = street.getStreets(id)
    return jsonify(result)
#-------------- END PROCESS ADDRESS ---------
@app.route('/supplier', methods=['GET'])
def supplier():
    orther      = OrtherController()
    return jsonify(orther.getSupplier())

@app.route('/category', methods=['GET'])
def category():
    orther      = OrtherController()
    return jsonify(orther.getCategory())

@app.route('/statusOrder', methods=['GET'])
def statusOrder():
    orther      = OrtherController()
    return jsonify(orther.getStatusOrder())


@app.route('/image/customer/<path>', methods=['GET'])
def get_image_customer(path):
    url = PATH+"\images\customer//"+path
    return send_file(url, mimetype='image/gif')

@app.route('/image/admin/<path>', methods=['GET'])
def get_image_admin(path):
    url = PATH+"\images//admin//"+path
    return send_file(url, mimetype='image/gif')

@app.route('/image/product/<path>', methods=['GET'])
def get_image_product(path):
    url = PATH+"\images\product//"+path
    return send_file(url, mimetype='image/gif')


#-------------- resetPass ---------------
@app.route('/customer/checkCode', methods=['POST'])
def checkCodeC():
    body           = request.json
    forgotPassword = ForgotPassword()
    id             = forgotPassword.checkCode(body.get('code',""))
    if id != 0:
        return jsonify({"message":"Xác thực thành công"}), 200
    return jsonify({"message":"Mã xác thực sai,hoặc đã hết hiệu lực."}), 202

@app.route('/setPacustomer/ressword', methods=['POST'])
def resetPasswordC():
    forgotPassword      = ForgotPassword()
    body                = request.json
    password            = body.get('newPass','')
    confirmPass         = body.get('confirmPass','')
    id                  = forgotPassword.checkCode(body.get('code',''))
    customerController  = CustomerController()
    _cus                = customerController.customer_ID(id)
    if id == 0:
        return jsonify({"message":"Mã xác thực sai,hoặc đã hết hiệu lực."}), 202
    if password == '' or password == None:
        return jsonify({"message": "Mật khẩu không được để trống."}), 401
    if  len(str(password)) <6:
        return jsonify({"message": "Mật khẩu phải chứa ít nhấ 6 ký tự."}), 401
    if password != confirmPass:
        return jsonify({"message": "Xác nhận mật khẩu không hợp lệ."}), 401
    tmp               =  hashlib.md5(password.encode())
    password = tmp.hexdigest()
    customer = Customer(id, _cus.email, password, _cus.image, _cus.gender, _cus.lastName, _cus.firstName, _cus.city, _cus.distric, _cus.street, _cus.address, _cus.phone, _cus.birthDay, _cus.acc_point)
    result = customerController.update_customer_byId(customer)
    return jsonify(result)

@app.route('/admin/checkCode', methods=['POST'])
def checkCode():
    body           = request.json
    forgotPassword = ForgotPassword()
    id             = forgotPassword.checkCodeA(body.get('code',""))
    if id != 0:
        return jsonify({"message":"Xác thực thành công"}), 200
    return jsonify({"message":"Mã xác thực sai,hoặc đã hết hiệu lực."}), 202

@app.route('/admin/resetPassword', methods=['POST'])
def resetPassword():
    forgotPassword      = ForgotPassword()
    body                = request.json
    password            = body.get('newPass','')
    confirmPass         = body.get('confirmPass','')
    id                  = forgotPassword.checkCodeA(body.get('code',''))
    adminController     = AdminController()
    _ad                 = adminController.get_admin_ID(id)
    if id == 0:
        return jsonify({"message":"Mã xác thực sai,hoặc đã hết hiệu lực."}), 202
    if password == '' or password == None:
        return jsonify({"message": "Mật khẩu không được để trống."}), 401
    if  len(str(password)) <6:
        return jsonify({"message": "Mật khẩu phải chứa ít nhấ 6 ký tự."}), 401
    if password != confirmPass:
        return jsonify({"message": "Xác nhận mật khẩu không hợp lệ."}), 401
    tmp                 =  hashlib.md5(password.encode())
    password            = tmp.hexdigest()
    admin               = Admin(id, _ad.email, password, _ad.image, _ad.gender, _ad.lastName, _ad.firstName, _ad.city, _ad.distric, _ad.street, _ad.address, _ad.phone, _ad.birthDay, _ad.roleId)
    result              = adminController.update_admin_byId(admin)
    return jsonify(result)
    


#-------------- End ResetPass -----------




def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_url_image_customer(name_image):
    return "http://127.0.0.1:5000//image/customer/"+str(name_image)
def create_url_image_admin(name_image):
    return "http://127.0.0.1:5000//image/admin/"+str(name_image)
def create_url_image_product(name_image):
    return "http://127.0.0.1:5000//image/product/"+str(name_image)



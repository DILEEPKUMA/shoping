from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
from flask import jsonify
# from flask.passlib.apps import custom_app_context as pwd_context
from bson.objectid import ObjectId
from datetime import datetime
import smtplib, ssl

db_connection = MongoClient('mongodb://localhost:27017')#localhost connection
db = db_connection.products_db
app = Flask(__name__)
@app.route('/user_details', methods=['POST', 'GET','DELETE','PUT'])
def user_details():
    if request.method == 'POST':
        data = request.get_json()
        user_details_db =db.user_details
        existing_product = user_details_db.find_one({'user_mob_no' : data['user_mob_no']})
        if existing_product is None:
            user_name = data['user_name']
            user_mob_no=data['user_mob_no']
            address=data['address']
            is_active = True
            shoping_history = data['shoping_history']
            balance_amount = data['balance_amount']
            redeem_amount = data['redeem_amount']
            create_product_date=datetime.utcnow()
            # update_date=data['update_date']
            product_inseretd=user_details_db.insert_one({'user_name':user_name,'user_mob_no' : user_mob_no,'address':address,
                'is_active':is_active,'shoping_history':shoping_history,'balance_amount':balance_amount,
                 'redeem_amount':redeem_amount,'create_product_date':create_product_date})
            user_id_post = str(user_details_db.inserted_id)
            print(user_id_post)
            session['user_id_post'] = user_id_post
            return ('all new user added')
        else:
            return ('That user id number already exists!')

@app.route('/product_details', methods=['POST', 'GET','DELETE','PUT'])
def product_details():
    if request.method == 'POST':
        data = request.get_json()
        product_details_db =db.product_details
        existing_product = product_details_db.find_one({'product_id' : data['product_id']})
        if existing_product is None:
            product_name = data['product_name']
            price=data['price']
            category=data['category']
            product_id = data['product_id']
            lock_ID = data['lock_ID']
            create_product_date=datetime.utcnow()
            # update_date=data['update_date']
            product_inseretd=product_details_db.insert_one({'product_name':product_name,'price' : price,'category':category,
                'lock_ID':lock_ID,'product_id':product_id,'create_product_date':create_product_date})
            session['product_id'] = product_id
            product_id_post = str(product_details_db.inserted_id)
            session['product_id_post'] = product_id_post
            return ('all new products added')
        else:
            return ('That product id number already exists!')

    if request.method == 'DELETE':
        data = request.get_json()
        product_details_db =db.product_details
        product_del = ObjectId(session['product_id'])
        record_del = product_details_db.delete_one({'_id': product_del})
        return "sucessful Deleted"

    if request.method == 'GET':
        data = request.get_json()
        product_details_db =db.product_details
        if session.get('product_id') == True:
            product_get = ObjectId(session['product_id'])
            print(product_get)
        elif data != {}:
            records_get = product_details_db.find_one({'_id': product_id_post})
        else:
            records_get = product_details_db.find({'product_ID': str(session['product_id'])})
            return str(records_get)

    if request.method == 'PUT':
        data = request.get_json()
        product_details_db =db.product_details
        product_id_put = ObjectId(session['product_id'])
        product_details_db.update_one({'_id': product_id_put},
            {
                "$set":
                    {'product_name': data['product_name'],'price' : data['price'],'category':data['category'],
                'lock_ID':data['lock_ID'],'product_id':data['product_id'],'create_product_date':datetime.utcnow()}
            }
                                    )
        return "updated sucessfully"

@app.route('/lock_details', methods=['POST', 'GET','DELETE'])
def lock_details():
    if request.method == 'POST':
        data = request.get_json()
        lock_details_db =db.lock_details
        existing_lock_id = lock_details_db.find_one({'lock_ID' : data['lock_ID']})
        if existing_lock_id is None:
            charge_percentage=data['charge_percentage']
            wifi_router_name = data['wifi_router_name']
            lock_ID = data['lock_ID']
            create_product_date=datetime.utcnow()
            # update_date=data['update_date']
            lock_details_db.insert_one({'charge_percentage':charge_percentage,
                'wifi_router_name':wifi_router_name,'lock_ID':lock_ID,'create_product_date':create_product_date})
            session['lock_ID'] = data['lock_ID']
            new_lock_id = str(lock_details_db.inserted_id)
            session['new_lock_id'] = new_lock_id

            return ('all new lock id added')
        else:
            return ('That lock id number already exists!')

    if request.method == 'DELETE':
        data = request.get_json()
        lock_details_db =db.lock_details
        lock_ID_del = ObjectId(session['new_lock_id'])
        record_del = lock_details_db.delete_one({'_id': lock_ID_del})
        return "sucessful Deleted"

    if request.method == 'GET':
        data = request.get_json()
        lock_details_db = db.lock_details
        if session.get('shop_id') == True:
            product_get = ObjectId(session['shop_id'])
            print(product_get)
        else:
            product_get = ObjectId(data['shop_id'])

        if data != {}:
            records_get = lock_details_db.find_one({'_id': new_lock_id})
        else:
            records_get = lock_details_db.find({'product_ID': str(session['product_id'])})
        return str(records_get)


@app.route('/product_lock_details', methods=['POST', 'DELETE'])
def product_lock_details():
    if request.method == 'POST':
        data = request.get_json()
        tbl_prod_lock_db =db.tbl_prod_lock_details
        existing_prod_lock = tbl_prod_lock_db.find_one({'lock_ID' : data['lock_ID']})
        if existing_prod_lock is None:
            product_id=data['product_id']
            shop_id = data['shop_id']
            lock_ID = data['lock_ID']
            create_product_date=datetime.utcnow()
            # update_date=data['update_date']
            tbl_prod_lock=tbl_prod_lock_db.insert_one({'product_id':product_id,
                'shop_id':shop_id,'lock_ID':lock_ID,'create_product_date':create_product_date})
            session['product_id'] = data['product_id']
            tbl_prod_lock_id = str(tbl_prod_lock.inserted_id)
            session['tbl_prod_lock_id'] = tbl_prod_lock_id
            return ('all new lock id added')
        else:
            return ('That lock id number already exists!')

    if request.method == 'DELETE':
        data = request.get_json()
        tbl_prod_lock_db =db.lock_details
        tbl_prod_lock_del = ObjectId(session['tbl_prod_lock_id'])
        record_del = tbl_prod_lock_db.delete_one({'_id': tbl_prod_lock_del})
        return "sucessful Deleted"

@app.route('/shop_details', methods=['POST', 'GET','DELETE','PUT'])
def shop_details():
    if request.method == 'POST':
        data = request.get_json()
        shop_db =db.shop_details
        existing_shop_details = shop_db.find_one({'shop_login_id' : data['shop_login_id']})
        if existing_shop_details is None:
            shop_login_id=data['shop_login_id']
            shop_password=data['shop_password']
            shop_email=data['shop_email']
            shop_name = data['shop_name']
            shop_incharge = data['shop_incharge']
            primary_mob = data['primary_mob']
            secondary_mob = data['secondary_mob']
            country=data['country']
            state=data['state']
            city=data['city']
            zipcode=data['zipcode']
            create_date=datetime.now()
            # update_date=data['update_date']
            inserted_shop_id=shop_db.insert_one({'shop_login_id':shop_login_id,'shop_password':shop_password,'shop_email':shop_email,
            'shop_name':shop_name,'shop_incharge':shop_incharge,'primary_mob':primary_mob,'secondary_mob':secondary_mob,
            'country':country,'state':state,'city':city,'zipcode':zipcode,'create_date':create_date})
            shop_id = str(inserted_shop_id.inserted_id)
            session['shop_id'] = shop_id
            session['shop_incharge'] = shop_incharge


            return ('all new shops id added')
        else:
            return ('That shop id number already exists!')

    if request.method == 'DELETE':
        data = request.get_json()
        shop_db =db.shop_id_details
        shop_id_del = ObjectId(session['shop_id'])
        record_del = shop_db.delete_one({'_id': shop_id_del})
        return "sucessful Deleted"

    if request.method == 'GET':
        data = request.get_json()
        shop_db =db.shop_id_details
        shop_id=''
        if session.get('shop_id') == True:
            shop_id = ObjectId(session['shop_id'])
            print(shop_id)
        else:
            if data != {}:
                shop_id = ObjectId(data['shop_id'])
                print(shop_id)
        zipcode = ''
        city = ''
        state = ''
        country = ''
        if shop_id == '':

            if zipcode != '':
                shop_records = shop_db.find({'zipcode': str(session['zipcode'])})
                print(shop_records)
            elif city != '':
                shop_records = shop_db.find({'city': str(session['city'])})
                print(shop_records)
            elif state != '':
                shop_records = shop_db.find({'state': str(session['state'])})
                print(shop_records)
            elif country != '':
                shop_records = shop_db.find({'country': str(session['country'])})
                print(shop_records)
        else:
            shop_records = shop_db.find({'shop_ID': str(session['shop_id'])})
            return str(shop_records)
    if request.method == 'PUT':
        data = request.get_json()
        shop_db =db.shop_id_details
        shop_id_put = ObjectId(session['shop_id'])
        shop_db.update_one({'_id': shop_id_put},
                                     {
                                         "$set":
                                             {'shop_id': data['shop_id'], 'shop_name': data['shop_name'],
                                              'shop_incharge': data['shop_incharge'], 'primary_mob': data['primary_mob'],
                                              'secondary_mob': data['secondary_mob'],
                                              'create_product_date':datetime.utcnow()
                                             }
                                     }
                                     )
        return "updated sucessfully"

@app.route('/shop_login', methods=['POST'])
def shop_login():
    if request.method == 'POST':
        data = request.get_json()
        shop_login_db =db.shop_login_details
        shop_login = shop_login_db.find_one({'shop_login_id' : data['shop_login_id'],'shop_password':data['shop_password']})
        shop_login_object_id = str(shop_login.get('_id'))
        if shop_login:
            # print(data['user_name'])
            session['shop_login_id'] = data['shop_login_id']
            session['shop_login_object_id'] = shop_login_object_id
            return ('successful login')
        else:
            return ('incorrect credential')


def send_email(receiver_email,message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "dileepkumar.gvd@gmail.com"  # Enter your address
    password = "Venkatesh123"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        # return("message sent to destination :", receiver_email)
    return 'success'

@app.route('/forget_password', methods=['GET','POST'])
def forget_password():
    if request.method == 'POST':
        # shop_incharge_name= session['shop_incharge']
        receiver_email = "rebeldileep.1996@gmail.com"  # Enter receiver address
        message = """\
        Subject: Hi there

        \nhi  incharge name here,\n
        you are request to reset the  password please click the link\n
        <a href="http://127.0.0.1:5000/forget_password/session['shop_id']" class="click">click here</a>"""
        data = request.get_json()
        shop_db = db.shop_details
        cursor = shop_db.find_one({'shop_email': data['shop_email']})
        # print(cursor)
        # shop_email=data['shop_email']
        if cursor == None:
            return("mail is not available")
        else:
            status_message=send_email(receiver_email,message)
            return (status_message)
    return ''

@app.route('/change_password', methods=['PUT'])
def change_password():
    if request.method == 'PUT':

        data = request.get_json()
        shop_db = db.shop_details
        shop_row_details = shop_db.find_one({'shop_login_id': data['shop_login_id']})
        if shop_row_details:
            confirm_password = data['confirm_password']
            new_password = data['new_password']
            if confirm_password == new_password:
                shop_db.update_one({'shop_login_id': data['shop_login_id']},
                                   {
                                       "$set":
                                           { 'shop_password': new_password  }
                                   }
                                   )
                return ("successfully password changed")

        return 'Invalid password combination'

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
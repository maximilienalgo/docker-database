# compose_flask/app.py
from flask import Flask
import flask_sqlalchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from sqlalchemy.sql import func
from sqlalchemy import *

app = Flask(__name__)
# config = {
#     'host' : 'db',
#     'port' : '3307',
#     'user' : 'root',
#     'password': 'root',
#     'database' : 'classicmodels'
# }
#
# db_user = config.get('user')
# db_pwd = config.get('password')
# db_host = config.get('host')
# db_port = config.get('port')
# db_name = config.get('database')
engine = create_engine('mysql+pymysql://root:root@db:3306/classicmodels')

Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

Customer = Base.classes.customers
Employee = Base.classes.employees
Offices = Base.classes.offices
OrderDetail = Base.classes.orderdetails
Order = Base.classes.orders
Payment = Base.classes.payments
ProductLine = Base.classes.productlines
Product = Base.classes.products


@app.route('/')
def hello():
    session = Session()
    result = []
    for instance in session.query(Customer).order_by(Customer.customerNumber):
        print(instance.customerName)
        result.append(instance.customerName)

    return jsonify(result)


def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in
            row.__table__.columns}


@app.route('/1')
def offices():
    session = Session()
    result = []
    for instance in session.query(Offices).order_by(Offices.country, Offices.state, Offices.city):
        result.append(to_dict(instance))
    return jsonify(result)

@app.route('/2')
def count_employees():
    session = Session()
    r = session.query(func.count(Employee.employeeNumber)).first()
    print(r[0])
    return str(r[0])

@app.route('/payment')
def total_payment():
    session = Session()
    for instance in session.query(func.sum(Payment.amount)).all():
        return jsonify({'total': str(instance[0])})

@app.route('/voitures')
def voitures():
    session = Session()
    r = session.query(func.count(ProductLine.productLine)).filter(ProductLine.productLine.contains('Cars'))
    print(r[0])
    return str(r[0])

@app.route('/totalOctobre')
def total_octobre():
    session = Session()
    for instance in session.query(func.sum(Payment.amount)).filter(Payment.paymentDate == '2004-10-28'):
        return jsonify({'total': str(instance[0])})

@app.route('/sup100k')
def sup100k():
    session = Session()
    result = []
    for instance in session.query(Payment).filter(Payment.amount >= 100000):
        result.append({"amount": str(instance.amount), "checkNumber": instance.checkNumber})
    return jsonify(result)


@app.route('/7')
def seven():
    session = Session()
    result = []
    for instance in session.query(ProductLine).all():
        productLine = {'name': instance.productLine, "products": [], 'count': 0}
        for pinstance in session.query(Product).filter(Product.productLine == instance.productLine):
            productLine["products"].append({"name": pinstance.productName})
        productLine['count'] = len(productLine["products"])
        result.append(productLine)
    return jsonify(result)


@app.route('/9')
def min_amount():
    session = Session()
    result =  session.query(func.min(Payment.amount))
    return jsonify({'min': str(result[0])})

@app.route('/10')
def mean():
    session = Session()
    result = []
    mean = session.query(func.avg(Payment.amount)).scalar()
    for instance in session.query(Payment).filter(Payment.amount >= mean*2):
        result.append({"amount": str(instance.amount), "checkNumber": instance.checkNumber})
    return jsonify(result)

@app.route('/12')
def distinct():
    result = []
    session = Session()
    r = session.query(func.count(Product.productCode)).first()
    print(r[0])
    for instance in session.query(Product.productName, Product.productCode).distinct():
        result.append({"modelCode": str(instance.productCode), "modelName": instance.productName})
    result.append({"nbmodel" : str(r[0])})
    return jsonify(result)

@app.route('/13')
def treize():
    result = []
    session = Session()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
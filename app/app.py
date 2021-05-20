# compose_flask/app.py
from flask import Flask
import flask_sqlalchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

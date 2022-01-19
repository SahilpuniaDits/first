from flask import Flask, request, jsonify, make_response,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
# from marshmallow_sqlalchemy import ModelSchema
import datetime
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/flaskapi'
db = SQLAlchemy(app)
ma = Marshmallow(app)



#Table
class Employee(db.Model):
   _tablename_ = "employee"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   email = db.Column(db.String(50), nullable = False)
   mobile = db.Column(db.Integer)
   department = db.Column(db.String(20))
   joining_date = db.Column(db.Date)
   designation = db.Column(db.String(50))
   experience = db.Column(db.String(100))
   level = db.Column(db.Integer)
   left_date = db.Column(db.Date)
   dob = db.Column(db.Date)
   created = db.Column(db.DateTime)
   updated = db.Column(db.DateTime)
   
   
   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, name, email, mobile, department, joining_date, designation, experience, level, left_date, dob):
       self.name = name
       self.email = email
       self.mobile = mobile
       self.department = department
       self.joining_date = joining_date
       self.designation = designation
       self.experience = experience
       self.level = level
       self.left_date = left_date
       self.dob = dob
       
      

   def __repr__(self):
       return f"{self.id}"


db.create_all()


class employeeSchema(ma.Schema):
   class Meta(ma.Schema.Meta):
       model = Employee
       sqla_session = db.session
   id = fields.Number(dump_only=True)
   name = fields.String(required=True)
   email = fields.String(required=True)
   mobile = fields.Integer(required=True)
   department = fields.String(required=True)
   joining_date = fields.Date(required=True)
   designation = fields.String(required=True)
   experience = fields.String(required=True)
   level = fields.Integer(required=True)
   left_date = fields.Date(required=True)
   dob = fields.Date(required=True)
   

   
# @app.route('/api/employee', methods=['POST'])
# def create_employee():
#    data = request.get_json()
#    employee_schema = employeeSchema()
#    employee = employee_schema.load(data)
#    result = employee_schema.dump(employee.create())
#    return make_response(jsonify({"employee": result}), 200)


# employee post 

@app.route('/api/employee', methods=['POST'])
def add_employee():
    #get data from request
    name = request.json['name']
    email = request.json['email']
    mobile = request.json['mobile']
    department = request.json['department']
    joining_date = request.json['joining_date']
    designation = request.json['designation']
    experience = request.json['experience']
    level = request.json['level']
    left_date = request.json['left_date']
    dob = request.json['dob']
    
    

    #Instantiate new user
    employee = Employee(name, email, mobile, department,
                        joining_date, designation, experience, level, left_date, dob)
    #add new user
    db.session.add(employee)
    #commit the change to reflect in database
    db.session.commit()
    #return the response
    # or you can use: return jsonify(user_schema.dump(new_user))
    return employeeSchema.jsonify(employee)


@app.route('/api/employee', methods=['GET'])
def index():
   get_employee = Employee.query.all()
   employee_schema = employeeSchema(many=True)
   employee = employee_schema.dump(get_employee)
   return make_response(jsonify({"employee": employee}))


@app.route('/api/employee/<id>', methods=['GET'])
def get_employee_by_id(id):
   get_employee = Employee.query.get(id)
   todo_schema = employeeSchema()
   employee = todo_schema.dump(get_employee)
   return make_response(jsonify({"employee": employee}))


@app.route('/api/employee/<id>', methods=['PUT'])
def update_employee_by_id(id):
   data = request.get_json()
   get_employee = Employee.query.get(id)
   if data.get('name'):
       get_employee.name = data['name']
   if data.get('mobile'):
       get_employee.mobile = data['mobile']
       
   if data.get('department'):
       get_employee.department = data['department']
   if data.get('joining_date'):
       get_employee.joining_date = data['joining_date']
   if data.get('designation'):
       get_employee.designation = data['designation']
   if data.get('experience'):
       get_employee.experience = data['experience']
   if data.get('level'):
       get_employee.level = data['level']
   if data.get('left_date'):
       get_employee.left_date = data['left_date']
   if data.get('dob'):
       get_employee.dob = data['dob']
       
       
   db.session.add(get_employee)
   db.session.commit()
   employee_schema = employeeSchema(
       only=['id', 'name', 'mobile', 'department', 'joining_date', 'designation', 'experience', 'level', 'left_date', 'dob'])
   employee = employee_schema.dump(get_employee)

   return make_response(jsonify({"employee": employee}))


@app.route('/api/employee/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
   get_employee = Employee.query.get(id)
   db.session.delete(get_employee)
   db.session.commit()
   return make_response("", 204)


# if __name__ == '__main__':
#     app.run(debug=True)
class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(52), index=True)
    password_hash = db.Column(db.String(128))
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
  


db.create_all()

@app.route('/api/users', methods=['POST'])
def new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    print(email,password,"<<<<<<<<<<<<<<<<<")
    if email is None or password is None:
        abort(400)  # missing arguments
        print(email,"**************")
    if User.query.filter_by(email=email).first() is not None:
        abort(400)  # existing user
    user = User(email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': user.email}), 201




# @app.route('/api/login',methods=['POST'])
# @auth.login_required
# def get_resource(email,password):
#     # email = request.json['email']
#     # password = request.json['password']
#     user = User.query.filter_by(email = email).first()
#     if user.password_hash == pwd_context.encrypt(password):
#     # if not user or not user.verify_password(password):
#         return jsonify({ 'data': 'Hello, %s!' % user.email })
#     # user = user
#     return False

# @auth.verify_password
# def verify_password(email, password):
#     user = User.query.filter_by(email = email).first()
#     if user.password_hash == pwd_context.encrypt(password):
#     # if not user or not user.verify_password(password):
#         return True
#     # user = user
#     return False

@app.route('/api/login', methods=['POST'])    
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    passs = (pwd_context.verify(password, user.password_hash))
    
    if passs == True:
        
        
        
        return jsonify({'User': user.email, 'status':'successfully logged In'}), 201, 
    else:
        return jsonify({'status': 'Incorrect email or password'})

if __name__ == '__main__':
    app.run(debug=True)
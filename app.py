from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres.efnrejuwcbrarhvjddcv:Tanoj%40190605@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create the database connection object
db=SQLAlchemy(app)

api=Api(app)

user_fields = {
    'id': fields.Integer,
    'task_name': fields.String,
    'task_description': fields.String,
    'task_status': fields.String
}

# Create a request parser
user_args = reqparse.RequestParser()
user_args.add_argument('task_name', type=str, help='Name of the Task',required=True)
user_args.add_argument('task_description', type=str, help='Description of the Task',required=True)
user_args.add_argument('task_status', type=str, help='Status of the Task',required=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_description = db.Column(db.String(100), nullable=False)
    task_status = db.Column(db.String(100), nullable=False)


class task_edit(Resource):
    @marshal_with(user_fields)
    def get(self,task_id):
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404,message='Task not found')
        return task, 200

    @marshal_with(user_fields)
    def put(self,task_id):
        args = user_args.parse_args()
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404,message='Task not found')
        task.task_name = args['task_name']
        task.task_description = args['task_description']
        task.task_status = args['task_status']
        db.session.commit()
        return task, 200

    def delete(self,task_id):
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404,message='Task not found')
        db.session.delete(task)
        db.session.commit()
        return 'Successfully deleted task', 204


class task(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        task = Task(task_name=args['task_name'],task_description=args['task_description'],task_status=args['task_status'])
        if Task.query.filter_by(task_name=args['task_name']).first():
            abort(409,message='Task already exists')

        db.session.add(task)
        db.session.commit()
        return task, 201

    @marshal_with(user_fields)
    def get(self):
        tasks = Task.query.all()
        return tasks, 200


api.add_resource(task,'/task')
api.add_resource(task_edit,'/task/<int:task_id>')
if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
        print('Database created!')

    app.run(debug=True)
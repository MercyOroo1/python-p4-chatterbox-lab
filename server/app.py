from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET'])
def messages():
    messages = Message.query.order_by('created_at').all()
    return jsonify ([{
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at,
        "updated_at": message.updated_at
    }for message in messages]),200
# getting messages by id
@app.route('/messages/<int:id>', methods = ['GET'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message: 
        return jsonify({
            'msg': 'message does not exist'
        })
    return jsonify ({
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at,
        "updated_at": message.updated_at
    })
# Adding messages
@app.route('/messages', methods = ['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body = data['body'], username = data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        'id':new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at,
        'updated_at': new_message.updated_at
    })

@app.route('/messages/<int:id>', methods = ['PATCH'])
def update_message(id):
    data = request.get_json()
    message = db.session.get(Message, id)
    if not message:
        return jsonify ({'msg':'message not found'})
    message.body = data['body']
    db.session.commit()
    return jsonify({
        'body': message.body
    })
@app.route('/messages/<int:id>', methods = ['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify ({'msg': 'message not found'})
    db.session.delete(message)
    db.session.commit()
    return jsonify({'msg':'message has been succesfully deleted !'})
if __name__ == '__main__':
    app.run(port=5555)

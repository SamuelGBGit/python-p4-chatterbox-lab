# server/app.py

from flask import request, jsonify
from flask_cors import CORS

from config import app, db
from models import Message

CORS(app)


@app.route('/')
def home():
    return jsonify({"message": "Chatterbox API running"}), 200


# GET /messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200


# POST /messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    message = Message(
        body=data['body'],
        username=data['username']
    )

    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), 201


# PATCH /messages/<id>
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()

    if 'body' in data:
        message.body = data['body']

    db.session.commit()

    return jsonify(message.to_dict()), 200


# DELETE /messages/<id>
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({}), 204


if __name__ == '__main__':
    app.run(port=5000, debug=True)
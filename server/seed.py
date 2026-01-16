# server/seed.py

from config import app, db
from models import Message

with app.app_context():
    Message.query.delete()

    messages = [
        Message(body="Hello world!", username="Ian"),
        Message(body="Chatterbox is live!", username="Abdullahi"),
        Message(body="Flask + React 🔥", username="Flatiron")
    ]

    db.session.add_all(messages)
    db.session.commit()

    print("Database seeded!")
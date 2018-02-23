# -*- encoding: utf-8 -*-
from uuid import uuid4
from wownder import db

__all__ = ["ChatRoom", "ChatMessage"]


class ChatRoom(db.Model):
    __tablename__ = 'chat_room'

    id = db.Column(db.String(33), primary_key=True, nullable=False, unique=True)
    char_1_id = db.Column(db.Integer, db.ForeignKey('char.id'), index=True, nullable=False)
    char_2_id = db.Column(db.Integer, db.ForeignKey('char.id'), index=True, nullable=False)

    char_1 = db.relationship("Char", foreign_keys=[char_1_id])
    char_2 = db.relationship("Char", foreign_keys=[char_2_id])

    __table_args__ = (db.Index('chars_un', char_1_id, char_2_id, unique=True),)

    messages = db.relationship("ChatMessage", back_populates="room", lazy="dynamic")

    def __init__(self, **kwargs):
        if not kwargs.get('id'):
            kwargs.update({'id': uuid4().hex})
        super(ChatRoom, self).__init__(**kwargs)

    @classmethod
    def create(cls, char_1, char_2):
        # Always keep lesser on char_1 to keep unique constraint working.
        ids = [char_1.id, char_2.id]
        ids.sort()
        char_1_id, char_2_id = ids
        return cls(char_1_id=char_1_id, char_2_id=char_2_id)

    def recipient(self, sender):
        return self.char_2 if self.char_1_id == sender.id else self.char_1

    def new_msgs_count(self, sender):
        return self.messages.filter_by(recipient_id=sender.id, read=False).count()

    def create_msg(self, sender, msg):
        return ChatMessage(room_id=self.id, sender_id=sender.id, recipient_id=self.recipient(sender).id, message=msg)


class ChatMessage(db.Model):
    __tablename__ = 'chat_message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.String(33), db.ForeignKey('chat_room.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('char.id'), index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('char.id'), index=True)
    message = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False, index=True)

    sender = db.relationship("Char", uselist=False, foreign_keys=[sender_id])
    recipient = db.relationship("Char", uselist=False, foreign_keys=[recipient_id])
    room = db.relationship("ChatRoom", back_populates="messages", uselist=False)

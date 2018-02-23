# -*- coding: utf-8 -*-
import os
import colander
import sqlalchemy
from sqlalchemy import or_

import logging

from flask import (
    Blueprint,
    jsonify,
    request,
    abort,
    current_app as app
)

from flask_login import current_user, logout_user

from wownder import db
from wownder.bnlogin import requires_bn_login_api
from wownder.views.schemas.profile import ProfileSchema
from wownder.models import User, Profile, Char, PvPCharStats, ChatRoom, ChatMessage

logger = logging.getLogger(__file__)

api = Blueprint('api', __name__, url_prefix='/api')


def get_current_user_char(uuid):
    char = current_user.chars.filter_by(uuid=uuid).first()
    if not char:
        abort(404)
    return char


def get_char_room(char, room_id):
    room = char.chat_rooms.filter_by(id=room_id).first()
    if not room:
        abort(404)
    return room


@api.after_request
def set_headers(_response):
    _cors_headers = {
        'Access-Control-Allow-Origin': app.config['CORS_ORIGIN'],
        'Access-Control-Allow-Methods': "GET, POST, PUT",
        'Access-Control-Max-Age': 3600,
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if isinstance(_response, tuple):
        _response, _status_code = _response
    else:
        _status_code = _response.status_code
    for k, v in _cors_headers.items():
        _response.headers[k] = v
    _response.status_code = _status_code
    return _response


@api.route('/logout')
def logout():
    logout_user()
    return jsonify({})


@api.route("/stats")
@requires_bn_login_api
def get_stats():
    """
    This is just to help keep track of users on live server during the initial tests.
    Should be removed after people really start using it.
    """
    if current_user.battletag == os.getenv('ADMIN_TAG'):
        return jsonify({'count': User.query.count(),
                        'tags': [u.battletag for u in User.query]})
    return jsonify({}), 403


@api.route("")
@requires_bn_login_api
def is_logged_in():
    return jsonify({})


@api.route("/chars")
@requires_bn_login_api
def api_get_chars():
    region = request.args.get('region')
    chars = current_user.chars.filter_by(region=region) if region else current_user.chars
    return jsonify([dict(c) for c in chars.order_by(Char.name)])


@api.route("/chars/message-stats")
@requires_bn_login_api
def api_get_chars_message_stats():
    region = request.args.get('region')
    query = current_user.chars.filter_by(region=region) if region else current_user.chars
    chars = []
    for c in query.order_by(Char.name):
        rooms_count = ChatRoom.query.filter(
            or_(ChatRoom.char_1_id == c.id, ChatRoom.char_2_id == c.id)
        ).count()
        total_unread_count = ChatMessage.query.filter_by(recipient_id=c.id, read=False).count()
        chars.append(dict(c, rooms_count=rooms_count, total_unread_count=total_unread_count))
    chars.sort(key=lambda x: x['rooms_count'], reverse=True)
    chars.sort(key=lambda x: x['total_unread_count'], reverse=True)

    return jsonify(chars)


@api.route("/chars/<uuid>")
@requires_bn_login_api
def api_get_char(uuid):
    return jsonify(dict(get_current_user_char(uuid)))


@api.route("/chars/<uuid>/profile", methods=['GET'])
@requires_bn_login_api
def get_char_profile(uuid):
    char = get_current_user_char(uuid)
    return jsonify(dict(char.profile) if char.profile else {"char_uuid": char.uuid})


@api.route("/chars/<uuid>/profile", methods=['PUT'])
@requires_bn_login_api
def create_or_update_profile(uuid):
    schema = ProfileSchema()
    try:
        data = schema.deserialize(request.json)
    except colander.Invalid as exc:
        return jsonify(exc.asdict()), 400

    char = get_current_user_char(uuid)

    if not char.profile:
        Profile.create_for_char(char)

    for k, v in data.items():
        setattr(char.profile, k, v) if v is not None else True

    db.session.commit()
    return jsonify(dict(char.profile))


@api.route("/chars/<uuid>/profile/matches")
@requires_bn_login_api
def find_matches(uuid):
    char = get_current_user_char(uuid)
    from wownder.models import Profile

    matches = Profile.query.filter(
        Profile.char_id != char.id,
        # Char.user_id != current_user.id,
        Profile.char_id == Char.id,
        Profile.faction == char.profile.faction,
        Char.region == char.region
    )

    if request.args.get('arena') == '3s':
        matches = matches.filter(
            Profile.listed_3s.is_(True),
            PvPCharStats.b3_current_rating < char.stats.b3_current_rating + 300,
            PvPCharStats.b3_current_rating > char.stats.b3_current_rating - 300,
            PvPCharStats.char_id == Char.id,
            Profile.char_id == Char.id
        ).order_by(PvPCharStats.b3_current_rating.desc())

    else:
        matches = matches.filter(
            Profile.listed_2s.is_(True),
            PvPCharStats.b2_current_rating < char.stats.b2_current_rating + 300,
            PvPCharStats.b2_current_rating > char.stats.b2_current_rating - 300,
            PvPCharStats.char_id == Char.id,
            Profile.char_id == Char.id
        ).order_by(PvPCharStats.b2_current_rating.desc())

    if char.profile.role == "Healer":
        matches = matches.filter(
            Profile.role != "Healer"
        )

    return jsonify([dict(m.char, profile=dict(m)) for m in matches])


@api.route("/chars/<uuid>/chat/rooms")
@requires_bn_login_api
def get_char_chat_rooms(uuid):
    char = get_current_user_char(uuid)
    return jsonify(
        [dict(
            id=r.id, owner_id=char.uuid, news=r.new_msgs_count(char),
            recipient=dict(r.recipient(char))
        ) for r in char.chat_rooms]
    )


@api.route("/chars/<uuid>/chat/rooms", methods=['POST'])
@requires_bn_login_api
def create_chat_room(uuid):
    char = get_current_user_char(uuid)
    data = request.json
    # TODO: User Colander
    if 'recipient_uuid' not in data:
        return jsonify({}), 400
    recipient = Char.query.filter_by(uuid=data['recipient_uuid']).first()
    if not recipient:
        abort(400)

    db.session.add(ChatRoom.create(char, recipient))
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        logger.info("Integrity Error")
        db.session.rollback()

    return jsonify({}), 201


@api.route("/chars/<uuid>/chat/rooms/<room_id>", methods=['POST'])
@requires_bn_login_api
def post_msg_on_char_room(uuid, room_id):
    char = get_current_user_char(uuid)
    room = get_char_room(char, room_id)
    if 'message' not in request.json:
        return jsonify({}), 400

    db.session.add(room.create_msg(char, request.json['message']))
    db.session.commit()
    return jsonify({})


@api.route("/chars/<uuid>/chat/rooms/<room_id>")
@requires_bn_login_api
def get_char_chat_room(uuid, room_id):
    char = get_current_user_char(uuid)
    room = get_char_room(char, room_id)

    messages = room.messages.order_by(ChatMessage.id.desc()).limit(100).all()
    messages.reverse()
    conversation = []
    for m in messages:
        _msg = {
            'id': m.id,
            'type': 'sent' if m.sender.id == char.id else 'received',
            'message': m.message,
            'read': m.read
        }
        conversation.append(_msg)
    return jsonify({'conversation': conversation})


@api.route("/chars/<uuid>/chat/rooms/<room_id>/messages", methods=['POST'])
@requires_bn_login_api
def set_msgs_read(uuid, room_id):
    char = get_current_user_char(uuid)
    room = get_char_room(char, room_id)

    if 'ids' not in request.json:
        return jsonify({}), 400

    _msgs = room.messages.filter_by(read=False, sender_id=room.recipient(char).id)
    _msgs.filter(ChatMessage.id.in_(request.json['ids'])).update({ChatMessage.read: True}, synchronize_session='fetch')

    db.session.commit()
    return jsonify({})

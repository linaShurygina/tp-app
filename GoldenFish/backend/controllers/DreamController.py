from flask import Blueprint, jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from backend.models.Dream import Dream
from backend.schemas import DreamSchema, GiftSchema
from backend.storage.DreamStorage import DreamStorage
from backend.app import docs


wishes = Blueprint('wishes', __name__)

dream_storage = DreamStorage()

# USER'S WISHES
@wishes.route('/mywishes', methods=['GET'])
@cross_origin()
@jwt_required
@marshal_with(DreamSchema(many=True))
def get_dreams():
    try:
        user_id = get_jwt_identity()
        dreams = dream_storage.get_unfulfilled_dreams(user_id)
    except Exception as e:
        return {'message': str(e)}, 400
    return dreams


@wishes.route('/mywishes', methods=['POST'])
@cross_origin()
@jwt_required
@use_kwargs(DreamSchema)
@marshal_with(DreamSchema)
def put_dream(**kwargs):
    try:
        user_id = get_jwt_identity()
        new_dream = Dream(owner_id=user_id, **kwargs)
        dream_storage.save(new_dream)
    except Exception as e:
        return {'message': str(e)}, 400
    return new_dream


@wishes.route('/mywishes/<int:dream_id>', methods=['GET'])
@cross_origin()
@jwt_required
@marshal_with(DreamSchema)
def get_dream(dream_id):
    try:
        user_id = get_jwt_identity()
        dream = dream_storage.get_by_id(user_id, dream_id)
    except Exception as e:
        return {'message': str(e)}, 400
    return dream


@wishes.route('/mywishes/<int:dream_id>', methods=['PUT'])
@cross_origin()
@jwt_required
@use_kwargs(DreamSchema)
@marshal_with(DreamSchema)
def update_dream(dream_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        dream = dream_storage.get_by_id(user_id, dream_id)
        dream_storage.update(dream, **kwargs)
    except Exception as e:
        return {'message': str(e)}, 400
    return dream


@wishes.route('/mywishes', methods=['PUT'])
@cross_origin()
@jwt_required
@use_kwargs(DreamSchema)
@marshal_with(DreamSchema)
def set_fulfilled():
    try:
        params = request.get_json()
        user_id = get_jwt_identity()
        dream = dream_storage.get_by_id(user_id, params['dream_id'])
        dream.set_fulfilled()
        dream_storage.update(dream)
    except Exception as e:
        return {'message': str(e)}, 400
    return '', 204


@wishes.route('/mywishes/<int:dream_id>', methods=['DELETE'])
@cross_origin()
@jwt_required
@marshal_with(DreamSchema)
def delete_dream(dream_id):
    try:
        user_id = get_jwt_identity()
        dream = dream_storage.get_by_id(user_id, dream_id)
        dream_storage.remove(dream)
    except Exception as e:
        return {'message': str(e)}, 400
    return '', 204

# USER'S FULFILLED WISHES
@wishes.route('/fulfilled', methods=['GET'])
@cross_origin()
@jwt_required
@marshal_with(DreamSchema(many=True))
def get_fulfilled():
    try:
        user_id = get_jwt_identity()
        dreams = dream_storage.get_fulfilled_dreams(user_id)
    except Exception as e:
        return {'message': str(e)}, 400
    return dreams

# USER'S GIFT LIST
@wishes.route('/gifts', methods=['GET'])
@cross_origin()
@jwt_required
@marshal_with(DreamSchema(many=True))
def get_gifts():
    try:
        user_id = get_jwt_identity()
        gifts = dream_storage.get_gifts(user_id)
    except Exception as e:
        return {'message': str(e)}, 400
    return gifts


@wishes.route('/gifts', methods=['PUT'])
@cross_origin()
@jwt_required
@use_kwargs(DreamSchema)
@marshal_with(DreamSchema)
def delete_from_gifts(dream_id):
    try:
        user_id = get_jwt_identity()
        gift = dream_storage.get_by_id(user_id, dream_id)
        gift.set_giver(None)
    except Exception as e:
        return {'message': str(e)}, 400
    return '', 204


@wishes.errorhandler(422)
def error_handlers(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_dreams, blueprint='wishes')
docs.register(get_dream, blueprint='wishes')
docs.register(update_dream, blueprint='wishes')
docs.register(put_dream, blueprint='wishes')
docs.register(delete_dream, blueprint='wishes')
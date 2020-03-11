from flask import jsonify

from ..utils import senseless_print

from ...main import app
from ...core.database import users

@app.route('/face', methods=['POST'])
def route_users():
    users_data = []
    for user in users:
        user_data = {
            'name': user.name,
            'email': user.email,
        }
        users_data.append(user_data)
    senseless_print()
    return jsonify(users_data)

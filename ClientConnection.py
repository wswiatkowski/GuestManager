import json

from flask import Flask, request, Response
from flask_api import status

from DbConnection import DbManager

app = Flask(__name__)
db = DbManager()


def parse_output(input):
    ret = [{"invitee": None, "email": None}]
    for elem in input:
        for j in range(len(elem)):
            if ret[-1]["email"] is not None:
                ret.append({"invitee": None, "email": None})
            if j % 2 == 0:
                ret[-1]["invitee"] = elem[j]
            else:
                ret[-1]["email"] = elem[j]
    return json.dumps(ret)


@app.route('/invitation', methods=['POST'])
def update_user():
    dct = request.get_json()

    try:
        ret = db.update_user(dct['invitee'], dct['email'])
    except NameError as e:
        return e.message, status.HTTP_409_CONFLICT

    return Response(str(parse_output(ret)), status.HTTP_201_CREATED, mimetype='application/json;charset=utf-8')


@app.route('/invitation', methods=['PUT'])
def create_user():
    dct = request.get_json()

    ret = db.create_user(dct['invitee'], dct['email'])

    return Response(str(parse_output(ret)), status.HTTP_201_CREATED, mimetype='application/json;charset=utf-8')


@app.route('/invitation', methods=['DELETE'])
def delete_user():
    dct = request.get_json()

    db.delete_user(dct['invitee'], dct['email'])

    return Response("Invitee {name} deleted.".format(name=dct['invitee']), status.HTTP_200_OK, mimetype='application/'
                                                                                                        'plain;charset'
                                                                                                        '=utf-8')


@app.route('/invitation', methods=['GET'])
def get_users():
    ret = db.get_users()

    return Response(str(parse_output(ret)), status.HTTP_200_OK, mimetype='application/json;charset=utf-8')

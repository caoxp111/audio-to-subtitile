from flask import jsonify


def success_response(result):
    return jsonify({"code": 1, "message": "success", "result": result})


def failed_response2(code, message):
    return jsonify({"code": code, "message": message, "result": None})


def failed_response1(message):
    return failed_response2(0, message)


def ws_response(socketio, namespace, event, socket_id, data):
    socketio.emit(event, data, namespace=namespace, to=socket_id)

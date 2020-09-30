from flask import jsonify

def page_not_found(e):
    return jsonify({'message':'Page not found', 'error': True}), 404


def method_not_allowed(e):
    return jsonify({'message':'The method is not allowed for the requested URL', 'error': True}), 405


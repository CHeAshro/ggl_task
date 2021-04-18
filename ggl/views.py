
from flask import abort, jsonify, request, Blueprint

from ggl.models import db, Task

bp = Blueprint('task', __name__)


@bp.route('/tasks', methods=['GET'])
def task_list():

    return jsonify(result=[task.to_json() for task in Task.query.all()])


@bp.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()

    try:
        name = data['name']
    except (TypeError, KeyError):
        abort(400)

    task = Task(name=name)
    db.session.add(task)
    db.session.commit()

    return jsonify(result=task.to_json())

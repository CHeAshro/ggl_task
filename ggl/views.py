
from flask import jsonify, Blueprint

from ggl.models import db, Task

bp = Blueprint('task', __name__)


@bp.route('/tasks', methods=['GET'])
def task_list():

    return jsonify(result=[task.to_json() for task in Task.query.all()])


from ggl.tests.base import app, client, db
from ggl.models import Task


def test_task_to_json():
    task = Task(id=1, name='task_01', status=True)
    expect_result = {
        'id': 1,
        'name': 'task_01',
        'status': 1,
    }
    assert expect_result == task.to_json()

    task.status = False
    expect_result = {
        'id': 1,
        'name': 'task_01',
        'status': 0,
    }
    assert expect_result == task.to_json()

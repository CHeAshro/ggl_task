
import json

import pytest

from ggl.app import create_app
from ggl.models import Task


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from ggl.app import db

    with app.app_context():
        db.create_all()

        yield db

        db.drop_all()
        db.session.commit()


def test_task_list(app, client, db):
    url = '/tasks'

    result = client.get(url)
    assert 200 == result.status_code
    assert {'result': []} == result.get_json()

    db.session.add(Task(name='task_01', status=False))
    db.session.add(Task(name='task_02', status=True))
    db.session.commit()

    result = client.get(url)
    expect_result = {
        'result': [
            {'id': 1, 'name': 'task_01', 'status': 0},
            {'id': 2, 'name': 'task_02', 'status': 1},
        ]
    }
    assert expect_result == result.get_json()


def test_task_create(app, client, db):
    url = '/task'

    result = client.post(url)
    assert 400 == result.status_code

    result = client.post(url, content_type='application/json')
    assert 400 == result.status_code

    result = client.post(url, data=json.dumps({}), content_type='application/json')
    assert 400 == result.status_code

    post_data = {
        'name': 'task_01',
    }
    result = client.post(url, data=json.dumps(post_data), content_type='application/json')
    assert 200 == result.status_code

    result_data = result.get_json()
    assert post_data['name'] == result_data['result']['name']
    assert 0 == result_data['result']['status']

    id = result_data['result']['id']
    task = Task.query.get(id)
    assert task.to_json() == result_data['result']


def test_task_edit(app, client, db):
    task = Task(name='task_01', status=False)
    db.session.add(task)
    db.session.commit()

    url = f'/task/{task.id}'

    result = client.put(url)
    assert 400 == result.status_code

    result = client.put(url, content_type='application/json')
    assert 400 == result.status_code

    result = client.put(url, data=json.dumps({}), content_type='application/json')
    assert 400 == result.status_code

    post_data = {
        'id': task.id,
        'name': 'task_edit',
        'status': 1,
    }

    data = post_data.copy()
    data['id'] = 10000
    result = client.put(f'/task/{data["id"]}', data=json.dumps(data), content_type='application/json')
    assert 404 == result.status_code

    data = post_data.copy()
    data['status'] = 'error_status'
    result = client.put(url, data=json.dumps(data), content_type='application/json')
    assert 400 == result.status_code

    result = client.put(url, data=json.dumps(post_data), content_type='application/json')
    assert 200 == result.status_code

    result_data = result.get_json()
    assert task.id == result_data['id']
    assert post_data['name'] == result_data['name']
    assert post_data['status'] == result_data['status']

    db.session.refresh(task)
    assert task.to_json() == result_data


def test_task_delete(app, client, db):
    task = Task(name='task_01', status=False)
    db.session.add(task)
    db.session.commit()

    result = client.delete('/task/10000')
    assert 404 == result.status_code

    result = client.delete(f'/task/{task.id}')
    assert 200 == result.status_code

    assert not db.session.query(Task.id).filter_by(id=task.id).scalar()

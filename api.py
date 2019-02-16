from flask import (
    Blueprint, jsonify, flash, g, request
)

from .db import get_db


VERSION = 'v1'


api_projects_bp = Blueprint('projects', __name__, url_prefix='/api/{}/projects'.format(VERSION))


@api_projects_bp.route('/', methods=('GET', ))
def list_projects():
    db = get_db()
    projects = db.execute('SELECT * FROM Projects', ()).fetchall()
    return jsonify({"error": None, "result": [dict(p) for p in projects]})


@api_projects_bp.route('/<name>', methods=('GET', ))
def project_info(name):
    db = get_db()
    project_info = db.execute('SELECT * FROM Projects WHERE name = ?', (name, )).fetchone()
    if project_info is None:
        return jsonify({"error": "No project '{}' found".format(name), "result": None})
    return jsonify({"error": None, "result": dict(project_info)})


@api_projects_bp.route('/create', methods=('POST', ))
def create_project():
    project_name = request.form['project_name']
    description = request.form['description']
    db = get_db()
    error = None
    project_info = db.execute('SELECT * FROM Projects WHERE name = ?', (project_name, )).fetchone()
    if project_info is not None:
        error = "Project '{}' already exists".format(name)
        return jsonify({"error": error, "result": None})
    else:
        db.execute(
            'INSERT INTO Projects (name, description) VALUES (?, ?)',
            (project_name, description)
        )
        db.commit()
        project_info = db.execute('SELECT * FROM Projects WHERE name = ?', (project_name, )).fetchone()
        return jsonify({"error": None, "result": dict(project_info)})

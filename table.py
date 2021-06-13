from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskwebtable.auth import login_required
from flaskwebtable.db import get_db

bp = Blueprint('table', __name__)

@bp.route('/')
def index():
    db = get_db()
    entries = db.execute(
        'SELECT e.id, field1, field2, created, author_id, username'
        ' FROM entries e JOIN user u ON e.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('table/index.html', entries=entries)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        field1 = request.form['field1']
        field2 = request.form['field2']
        error = None

        if not field1:
            error = 'Field 1 is required.'
        
        if not field2:
            error = 'Field 2 is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO entries (field1, field2, author_id)'
                ' VALUES (?, ?, ?)',
                (field1, field2, g.user['id'])
            )
            db.commit()
            return redirect(url_for('table.index'))

    return render_template('table/create.html')
    

def get_entry(id, check_author=True):
    entry = get_db().execute(
        'SELECT e.id, field1, field2, created, author_id, username'
        ' FROM entries e JOIN user u ON e.author_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()

    if entry is None:
        abort(404, f"Entry id {id} doesn't exist.")

    if check_author and entry['author_id'] != g.user['id']:
        abort(403)

    return entry


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_entry(id)

    if request.method == 'POST':
        field1 = request.form['field1']
        field2 = request.form['field2']
        error = None

        if not field1:
            error = 'Field 1 is required.'
        
        if not field2:
            error = 'Field 2 is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE entries SET field1 = ?, field2 = ?'
                ' WHERE id = ?',
                (field1, field2, id)
            )
            db.commit()
            return redirect(url_for('table.index'))

    return render_template('table/update.html', entry=entry)
    

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_entry(id)
    db = get_db()
    db.execute('DELETE FROM entries WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('table.index'))
from app import app
from flask import redirect , url_for
from flask_security import login_required


@app.route('/')
@login_required
def login_success():
    return redirect(url_for('admin/user'))

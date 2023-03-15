
from flask import Blueprint, render_template, session
from flask import request
from tools.decorators import is_login
from tools.params import data as xz
from tools.forms import *

bp = Blueprint("userprofile", __name__)


@bp.route("/userprofile/", methods=['GET', 'POST'])
@is_login
def userprofile():
    if request.method == 'GET':
        data = dict(
            title="个人资料",
            user=CRUD.user(session.get('name')),
            xz=xz['xingzuo']
        )
        return render_template("userprofile.html", data=data)
    else:
        res = dict(code=0)
        form = UserProfileEditForm(request.form)
        if form.validate():
            if CRUD.save_user(form):
                res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        return res

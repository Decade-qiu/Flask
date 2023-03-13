# from flask import Blueprint, request, render_template, g, redirect, url_for
# from .forms import QuestionForm, AnswerForm
# from model.models import QuestionModel, AnswerModel
# from exts import db
# from decorators import login_required
#
# bp = Blueprint("qa", __name__, url_prefix="/")
#
#
# # http://127.0.0.1:5000
# @bp.route("/")
# def index():
#     questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
#     return render_template("index.html", questions=questions)
#
#
# @bp.route("/qa/public", methods=['GET', 'POST'])
# @login_required
# def public_question():
#     if request.method == 'GET':
#         return render_template("public_question.html")
#     else:
#         form = QuestionForm(request.form)
#         if form.validate():
#             title = form.title.data
#             content = form.content.data
#             question = QuestionModel(title=title, content=content, author=g.user)
#             db.session.add(question)
#             db.session.commit()
#             # todo: 跳转到这篇问答的详情页
#             return redirect("/")
#         else:
#             print(form.errors)
#             return redirect(url_for("qa.public_question"))
#
#
# @bp.route("/qa/detail/<qa_id>")
# def qa_detail(qa_id):
#     question = QuestionModel.query.get(qa_id)
#     return render_template("detail.html", question=question)
#
#
# # @bp.route("/answer/public", methods=['POST'])
# @bp.post("/answer/public")
# @login_required
# def public_answer():
#     form = AnswerForm(request.form)
#     if form.validate():
#         content = form.content.data
#         question_id = form.question_id.data
#         answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
#         db.session.add(answer)
#         db.session.commit()
#         return redirect(url_for("qa.qa_detail", qa_id=question_id))
#     else:
#         print(form.errors)
#         return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))
#
#
# @bp.route("/search")
# def search():
#     # /search?q=flask
#     # /search/<q>
#     # post, request.form
#     q = request.args.get("q")
#     questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
#     return render_template("index.html", questions=questions)
#
# # url传参
# # 邮件发送
# # ajax
# # orm与数据库
# # Jinja2模板
# # cookie和session原理
# # 搜索
#
# # 前端
# # 部署
#
# # 《Flask全栈开发》：Flask基础增强+前端
# # 《Flask实战》：Flask+Vue前后端分离的论坛系统，WebSocket实战
#
# # 简单项目：
# # 复杂的项目：
#

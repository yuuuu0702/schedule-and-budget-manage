from flask import Flask, jsonify, request, send_from_directory
from datetime import date
import json

from project import Project
from transaction import Transaction, TransactionType

app = Flask(__name__)

projects = []


# JSON読み込み
def load_projects():
    global projects

    try:
        with open("projects.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        projects = [
            Project.from_dict(p)
            for p in data
        ]

    except FileNotFoundError:
        projects = []


# JSON保存
def save_projects():
    with open(
        "projects.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            [p.to_dict() for p in projects],
            f,
            ensure_ascii=False,
            indent=4
        )


# index.html表示
@app.route("/")
def index():
    return send_from_directory(
        ".",
        "index.html"
    )


# プロジェクト一覧取得
@app.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(
        [p.to_dict() for p in projects]
    )


# プロジェクト作成
@app.route("/projects", methods=["POST"])
def create_project():

    data = request.json

    project = Project(
        data["name"]
    )

    projects.append(project)

    save_projects()

    return jsonify(
        project.to_dict()
    )


# 取引一覧取得
@app.route(
    "/projects/<int:project_id>/transactions",
    methods=["GET"]
)
def get_transactions(project_id):

    if not (0 <= project_id < len(projects)):
        return jsonify({
            "error": "project not found"
        }), 404

    project = projects[project_id]

    return jsonify(
        [
            t.to_dict()
            for t in project.transactions
        ]
    )


# 取引追加
@app.route(
    "/projects/<int:project_id>/transactions",
    methods=["POST"]
)
def add_transaction(project_id):

    if not (0 <= project_id < len(projects)):
        return jsonify({
            "error": "project not found"
        }), 404

    project = projects[project_id]

    data = request.json

    transaction = Transaction(
        transaction_date=date.fromisoformat(
            data["date"]
        ),
        amount=data["amount"],
        transaction_type=TransactionType(
            data["type"]
        ),
        category=data["category"],
        memo=data.get(
            "memo",
            ""
        )
    )

    project.add_transaction(
        transaction
    )

    save_projects()

    return jsonify(
        transaction.to_dict()
    )


# 集計取得
@app.route(
    "/projects/<int:project_id>/summary",
    methods=["GET"]
)
def get_summary(project_id):

    if not (0 <= project_id < len(projects)):
        return jsonify({
            "error": "project not found"
        }), 404

    project = projects[project_id]

    return jsonify({
        "income": project.get_income_total(),
        "expense": project.get_expense_total(),
        "balance": project.get_balance()
    })


if __name__ == "__main__":
    load_projects()
    app.run(debug=True)
from flask import Flask, jsonify, request
from flask import send_from_directory
from datetime import date
import json

from project import Project
from transaction import Transaction, TransactionType

app = Flask(__name__)

# メモリ上のデータ
projects = []

# JSON読み込み
def load_projects():
    global projects
    try:
        with open("projects.json","r",encoding = "utf-8") as f:
            data = json.load(f)
        projects = [Project.from_dict(p) for p in data]
        
    except FileNotFoundError:
        projects = []


def save_projects():
    with open("projects.json","w",encoding = "utf-8") as f:
        json.dump(
            [p.to_dict() for p in projects ],
            f,
            ensure_ascii = False,
            indent = 4
        )
    

@app.route("/")
def index():
    return send_from_directory(".","index.html")
#プロジェクト一覧取得
@app.route("/projects",method=["GET"])
def get_projects():
    return jsonify([p.to_dict() for p in projects])

# プロジェクト作成
def create_project():
    data = request.json

    project = Project(data["name"])
    projects.append(project)

    save_projects()

    return jsonify(project.to_dict())


# 取引追加
@app.route("/projects/<int:project_id>/transactions",method = ["POST"])
def add_transaction(project_id):
    data = request.json
    project = projects[project_id]

    t = Transaction(
        transaction_date=date.fromisoformat(data["date"]),
        amount = data["amount"],
        transaction_type = TransactionType(data["date"]),
        category = data["category"],
        memo=data.get("memo","") 
    )

    project.add_transaction(t)
    save_projects()
    
    return jsonify(t.to_dict())


# 収支サマリー
@app.route("/projects/<int:project_id>summary",methods=["GET"])
def summary(project_id):
    p = projects[project_id]

    return jsonify({
        "名前":p.name,
        "収入":p.get_income_total(),
        "支出":p.get_expense_total(),
        "残高":p.get_balance()
    }) 

if __name__ == "__main__":
    load_projects()
    app.run(debug = True)
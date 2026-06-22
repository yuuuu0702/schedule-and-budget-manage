"""
ERモデルメモ
ユーザー_user
    アカウント id
        google google_id
        ユーザ名 user_name

        プロジェクト project
            イベントOR月 event_type
                日付
                    初日から最終日の日付
                        出費 expense
                            金額
                            理由
                        収入 income
                            LP work_income
                                開始時間 start
                                終了時間 up
                            その他 other_income
"""

from datetime import date
import json
from project import Project
from transaction import Transaction
from transaction import TransactionType

# メイン処理
def main():        
    projects = []
    app = True
    current_project = None
    
    while app :

        while True:
            print("\n ===== 家計簿 =====")
            print("1. プロジェクトを追加")
            print("2. プロジェクトを削除")
            print("3. プロジェクトを選択")
            print("4. 終了")

            choice = input("選択:")

            if choice == "1":
                name = input("プロジェクト名を入力:")
                projects.append(Project(name))
            
            elif choice == "2":
                if len(projects)==0:
                    print("プロジェクトがありません。")
                    continue
                for i,project in enumerate(projects):
                    print(f"{i}:{project.name}")
                j = int(input("選択:"))
                if 0 <= j < len(projects):
                    del projects[j]

            elif choice == "3":
                if len(projects)==0:
                    print("プロジェクトがありません。")
                    continue
                for i,project in enumerate(projects):
                    print(f"{i}:{project.name}")
                j = int(input("選択:"))
                if 0 <= j < len(projects):
                    current_project = projects[j]
                    break
                else:
                    print("存在しない番号です。")
            
            elif choice == "4":
                app = False
                break
            
            else:
                print("適切な値を入力してください。")

        while app:

            print("\n ===== 家計簿 =====")
            print("1. 取引追加")
            print("2. 取引削除")
            print("3. 一覧表示")
            print("4. 集計表示")
            print("5. 戻る")

            choice = input("選択:")

            if choice == "1":
                project_add = input_transaction()
                current_project.add_transaction(project_add)
            
            elif choice == "2":
                current_project.show_transactions()
                
                try:
                    i = int(input("削除する項目の番号を選んでください。"))
                    break

                except ValueError:
                    print("適切な数字を入力してください。")

                current_project.remove_transaction(i)
                break
 
            elif choice == "3":
                current_project.show_transactions()
            
            elif choice == "4":
                print("収入:",current_project.get_income_total())
                print("支出:", current_project.get_expense_total())
                print("残高:",current_project.get_balance())
            
            elif choice == "5":
                break

            else :
                print("適切な値を入力してください。")
            



def input_transaction():

    while True:

        dates = date.today()
        
        try:
            amount = int(input("金額:"))       
        except ValueError:
            print("数字を入力してください。")
            continue
        
        try:
            select_type = int(input("0: income, 1: expense  :"))
        except ValueError:
            print("適切な値を入力してください。")
            continue

        if select_type == 0:
            transaction_type = TransactionType.INCOME
            break
        elif select_type == 1:
            transaction_type = TransactionType.EXPENSE
            break
        else:
            print("0か1を入力してください。")

    category = input("カテゴリ:")
    memo = input("メモ:")

    return Transaction(dates,amount,transaction_type,category,memo)


if __name__ =="__main__":
    main()
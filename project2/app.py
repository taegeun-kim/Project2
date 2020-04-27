import os
import pymysql
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect, abort, session, jsonify

app = Flask(__name__, 
            static_folder="static",
            template_folder="views")
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key = 'project2'

db = pymysql.connect(
    user='root',
    passwd='taiginv',
    host='localhost',
    db='web2',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

def get_menu():
    cursor = db.cursor()
    cursor.execute("select id, item from field")
    menu = [f"<li><a href='/{e['id']}'>{e['item']}</a></li>"
            for e in cursor.fetchall()]
    return '\n'.join(menu)

@app.route("/")
def index():    
    title = 'Welcome ' + session['user']['name'] if 'user' in session else 'Welcome'
        
    content = 'Welcome Python Class...'
    return render_template('template.html',title=title, content=content)

@app.route("/login", methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute(f"""
            select id, name, profile, password from reader 
            where name = '{request.form['id']}'""")
        user = cursor.fetchone()
        
        if user is None:
            message = "회원이 아닙니다."
        else:
            cursor.execute(f"""
            select id, name, profile, password from reader 
            where name = '{request.form['id']}' and 
                  password = SHA2('{request.form['pw']}', 256)""")
            user = cursor.fetchone()
            
            if user is None:
                message = "<p>패스워드를 확인해 주세요</p>"
            else:
                # 로그인 성공에는 메인으로
                session['user'] = user
                return redirect(f"/main")
    return render_template('login.html', message=message)

@app.route("/<title>")
def html(title):
    print("*******************************8")

    menu=get_menu()
    title = title
    cursor = db.cursor()
    cursor.execute(f"select description from field where id = '{session['user']['id']}'")
    #content = cursor.fetchone()
    
    message = ['']
    print("!!!!!",request.method)
    if session['user']['id'] == 1 :
        if request.method == 'POST':
            print("********************")
            date = request.form["date"]
            url = f"https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=105&date={date}"
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            headline=soup.select('.ranking_headline > a')
            bs4_result = []
            for t in enumerate(headline) :
                bs4_result.append(t['title'])
            message = bs4_result
    
    return render_template('bs4.html', 
                           message=message, title=title, menu=menu)

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

# @app.route("/favicon.ico")
# def favicon():
#     return abort(404)

# @app.route("/dbtest")
# def dbtest():
#     cursor = db.cursor()
#     cursor.execute("select * from topic")
#     return str(cursor.fetchall())


# @app.route("/<id>")
# def content(id):
#     cursor = db.cursor()
#     cursor.execute(f"select * from topic where id = '{id}'")
#     topic = cursor.fetchone()
    
#     if topic is None:
#         abort(404)

#     return render_template('template.html',
#                            id=topic['id'],
#                            title=topic['title'],
#                            content=topic['description'],
#                            menu=get_menu())

# @app.route("/delete/<id>")
# def delete(id):
#     cursor = db.cursor()
#     cursor.execute(f"delete from topic where id='{id}'")
#     db.commit()
    
#     return redirect("/")

# @app.route("/create", methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         cursor = db.cursor() 
#         sql = f"""
#             insert into topic (title, description, created, author_id)
#             values ('{request.form['title']}', '{request.form['desc']}',
#                     '{datetime.now()}', '{session['user']['id']}')
#         """
#         cursor.execute(sql)
#         db.commit()

#         return redirect('/')
    
#     return render_template('create.html', 
#                            message='', 
#                            menu=get_menu())



app.run(port=8010)
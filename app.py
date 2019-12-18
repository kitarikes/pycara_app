import pyrebase
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyAInt6Z0EXxsRgA8W3QfItFpHlhqSy5jdw",
    "authDomain": "challecara-app.firebaseapp.com",
    "databaseURL": "https://challecara-app.firebaseio.com",
    "projectId": "challecara-app",
    "storageBucket": "challecara-app.appspot.com",
    "messagingSenderId": "393001281058",
    "appId": "1:393001281058:web:d47fd2dacfaaa7a1ae0c7b",
    "measurementId": "G-W581ZTLB6F"
}

"""
#科目データ--------------------------------------------------
data = {'math': 0 ,
        'english': 0 , 
        'history': 0 ,
        'chemistry': 0}
#----------------------------------------------------------
"""

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
username = ''

# user認証関連--------------------------------------------------

#ユーザー新規登録
@app.route("/sign_up_do", methods=["POST"])
def sign_up_do():
        if request.method == "POST":
                try:
                        data = {'math': 0 ,
                        'english': 0 , 
                        'history': 0 ,
                        'chemistry': 0}
                        result = request.form
                        user = auth.create_user_with_email_and_password(result  ['email'], result['password'])
                        auth.send_email_verification(user['idToken'])
                        auth.refresh(user['refreshToken'])
                        username = result['email'].split('@')[0]
                        db.child("users").child(result['email'].split('@')[0])  .set(data)
                        db.child('users').child(username).set(data)
                        message = '新規作成完了しました！このままログインして下さい。'
                        return render_template('login/sign_in.html', message=message)
                except:
                        error = '既に使われているメールアドレスか、入力に誤りがあります。'
                        return render_template('login/sign_up.html', error=error)
        else:
                render_template('login/sign_up.html')

@app.route("/sign_up")
def sign_up():
    return render_template('login/sign_up.html')


#ログイン
@app.route("/sign_in")
def sign_in():
        return render_template('login/sign_in.html')

@app.route("/sign_in_do", methods=['POST'])
def sign_in_do():
        try:

                result = request.form
                auth.sign_in_with_email_and_password(result['email'], result    ['password'])
                #sign_in したusernameを取得
                global username
                username = result['email'].split('@')[0]
                global data
                data = db.child('users').child(username).get().val()
                print(data)
                return redirect('/mypage') #変更
        except:
                return redirect('/sign_in')


#ログアウト
@app.route("/sign_out")
def sign_out():
        username = ''
        return redirect('/sign_in')
 
#------------------------------------------------------------

#教科リストの表示とお気に入り機能--------------------------------
@app.route("/subject", methods=['GET','POST'])
def sub_home():
        if username == '':
                return redirect('/sign_in')

        elif request.method == "GET":
                k = data.keys()
                sub_list = db.child('users').child(username).get().val()
                
                return render_template('subject/list.html', k=k, sub_list=sub_list, username = username)
        else:
                result = request.form

#お気に入り反映-------------------------------------------------
                a = result.to_dict().keys()
                for i in a:
                        sub_name = i
                data[sub_name] = int(result[sub_name])
                db.child('users').child(username).set(data)
#--------------------------------------------------------------

                k = data.keys()
                sub_list = db.child('users').child(username).get().val()
                
                return render_template('subject/list.html', k=k, sub_list=sub_list, username = username)
                
#お気に入り機能-------------------------------------------------


#教科ごとの画像表示
@app.route('/subject/<sub_name>')
def subject_detail(sub_name):
        a = []
        ans = []
        k =[]
        try:
                my_dic = db.child("subject_url").child(sub_name).get().val()
                for key, value in my_dic.items():
                        a.append(key)
                        ans.append(value)
                for i in ans:
                        k.append(i['url'])
        except:
                pass


        return render_template('subject/show.html', k = k, sub_name=sub_name)       

#教科ごとの画像upload form
@app.route('/subject/<sub_name>/upload', methods=['GET', 'POST'])
def upload(sub_name):
        if request.method == "GET":
                return render_template('subject/upload.html',   sub_name=sub_name)

        else:
                subject = sub_name
                f = request.files["s_file"]
                storage.child("images").child(subject).child(f.filename).put(f)
                url = storage.child("images/"+subject+"/"+f.filename).get_url(token=None)
                data = {"url":url}
                db.child("subject_url").child(subject).push(data)
                return redirect("/subject/"+subject)

#追加-----------------------------------------------------------------
@app.route('/')
def home():
        return render_template('home.html' , username=username)
      


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
        if username == '':
                return redirect('/sign_in')
        elif request.method == "GET":
                k = data.keys()
                sub_list = db.child('users').child(username).get().val()
                return render_template('mypage.html', k=k, sub_list=sub_list,username = username)

        else:
                result = request.form
                print(result)
                a = result.to_dict().keys()
                for i in a:
                        sub_name = i
                data[sub_name] = int(result[sub_name])
                print(data)
                db.child('users').child(username).set(data)
                k = data.keys()
                sub_list = db.child('users').child(username).get().val()
                
                return render_template('mypage.html', k=k, sub_list=sub_list, username = username)
#-----------------------------------------------------------------------------

app.run(host="localhost", debug=True)


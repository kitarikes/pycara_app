import pyrebase
from flask import Flask, render_template, request

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

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
# login関連--------------------------------------------------
@app.route("/sign_up_do", methods=["POST"])
def sign_up_do():
        if request.method == "POST":
                result = request.form
                user = auth.create_user_with_email_and_password(result['email'], result['password'])
                auth.send_email_verification(user['idToken'])
                auth.refresh(user['refreshToken'])
                data = {"name": result['email'].split('@')[0]}
                db.child("users").child(result['email'].split('@')[0]).set(data)
                return 'finished!!'
        else:
                render_template('login/sign_up.html')

@app.route("/sign_up")
def sign_up():
    return render_template('login/sign_up.html')

@app.route("/sign_in")
def sign_in():
        return render_template('login/sign_in.html')

@app.route("/sign_in_do", methods=['POST'])
def sign_in_do():
        result = request.form
        auth.sign_in_with_email_and_password(result['email'], result['password'])
        return ''
#------------------------------------------------------------

@app.route('/mypage', methods=["GET", "POST"])
def mypage():
        if request.method == "GET":
                print(1)
        return ''


#お気に入り機能----------------------------------------------
@app.route("/pre", methods=['GET','POST'])
def home():
        username = 'hogehogehoge'
        if request.method == "GET":
                dict = db.child('subject_url').get().val()
                k = []
                for key, value in dict.items():
                        k.append(key)

                sub_list = db.child('users').child(username).get().val()
                
                return render_template('subject/show.html', k=k, sub_list=sub_list)
        else:
                result = request.form

#お気に入り反映-------------------------------------------------
                a = result.to_dict().keys()
                for i in a:
                        sub_name = i
                db.child('users').child(username).set({sub_name : int(result[sub_name])})
#--------------------------------------------------------------

                dict = db.child('subject_url').get().val()
                k = []
                for key, value in dict.items():
                        k.append(key)

                sub_list = db.child('users').child(username).get().val()
                
                return render_template('subject/show.html', k=k, sub_list=sub_list)
                
#お気に入り機能----------------------------------------------


#画像アップロード関連----------------------------------------
@app.route("/pre_upload")
def img_up():
        return render_template('img/pre_upload.html')

@app.route("/pre_upload_do", methods=['POST'])
def up():
        subject = "math"
        f = request.files["s_file"]
        print(f)
        storage.child("images").child(subject).child(f.filename).put(f)
        url = storage.child("images/math/"+f.filename).get_url(token=None)
        data = {"url":url}
        db.child("subject_url").child("math").push(data)

        return ''

@app.route('/show')
def show():
        my_dic = db.child("subject_url").child("math").get().val()
        a = []
        ans = []
        for key, value in my_dic.items():
                a.append(key)
                ans.append(value)
        k =[]
        for i in ans:
                k.append(i['url'])



        return render_template('show.html', k = k)
#------------------------------------------------------------

@app.route('/')
def pre1():
        username='hogehogehoge'
        sub_list = db.child('users').child(username).get().val()
        print(sub_list['English'])
        return ''





app.run(host="localhost", debug=True)


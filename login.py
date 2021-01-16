from flask import Flask,render_template,url_for,request,session,redirect
import pymongo
import bcrypt
app=Flask(__name__,template_folder='templates')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return render_template('index.html')    

@app.route('/login', methods=['POST'])
def login():
    mycol=mydb["users"]
    login_user = mycol.find_one({'name' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username']=request.form['username']
            return redirect(url_for('index'))
        return 'Invalid username/password combination'  
    return 'Invalid username'      

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method =='POST':
        mycol=mydb["users"]
        existing_user = mycol.find_one({'name' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
            mycol.insert({'name':request.form['username'],'password' : hashpass})
            session['username']=request.form['username']
            return redirect(url_for('index'))
        return'That username already exists!'
    return render_template('register.html')        
        
if __name__=='__main__':
    app.secret_key='mysecret'
    app.run(debug=True)
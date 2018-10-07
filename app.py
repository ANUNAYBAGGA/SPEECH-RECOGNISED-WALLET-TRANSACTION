from flask import Flask,render_template,redirect,url_for,request
from pymongo import MongoClient
import speech_re as sr




app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.transact
@app.route('/',methods=['GET','POST'])
def main():
    error = ""
    if request.method=="POST":
        if request.form.get('login')=='login':

            user = request.form['username']
            passw = request.form['password']
            acc = db.account.find_one({"username":user})
            if acc==None:
                error = "Invalid Credentials"
                return render_template('index.html',data = error)
            if passw==acc["password"]:
                print("LOGGED IN")
                global username
                username = user
                global Password
                Password = passw
                global name
                name = acc["name"]
                global bal
                bal = int(acc["balance"])
                return redirect(url_for('home'))
            else:
                error = "Invalid Credentials"
                return render_template('index.html',data = error)
    return render_template('index.html',data = error)

@app.route('/home',methods=['GET','POST'])
def home():
    if username=="modi":
        if request.method=="POST":


            if request.form.get('log')=='log':

                return redirect(url_for('log'))
        
            if request.form.get('voice')=='voice':
                sound = sr.recog()
                use = sound[0]
                amt = sound[1]
                z = db.account.find_one({"username":use})

                if z!=None and bal>=amt:
                    temp = bal
                    temp = temp-amt
                    print(temp)
                    db.account.update({"username":username},{"$set":{"balance":temp}})
                    global bal
                    bal = temp

                    temp1 = z["balance"]
                    temp1 = int(temp1)
                    db.account.update({"username":use},{"$set":{"balance":temp1+amt}})
                    db.transfer.insert({"from":username , "to":use , "amt":amt})
                return render_template('profile.html',name = name , balance = bal)

            if request.form.get('send')=='send':
                use = request.form['username_send']
                amt = request.form['amount']
                amt = int(amt)
                print(use,amt)
                z = db.account.find_one({"username":use})

                if z!=None and bal>=amt:
                    temp = bal
                    temp = temp-amt
                    print(temp)
                    db.account.update({"username":username},{"$set":{"balance":temp}})
                    global bal
                    bal = temp

                    temp1 = z["balance"]
                    temp1 = int(temp1)
                    db.account.update({"username":use},{"$set":{"balance":temp1+amt}})
                    db.transfer.insert({"from":username , "to":use , "amt":amt})
        return render_template('profile.html',name = name , balance = bal)
    if username=="obama":
        if request.method=="POST":
            if request.form.get('log')=='log':

                return redirect(url_for('log'))
            if request.form.get('voice')=='voice':
                sound = sr.recog()
                use = sound[0]
                amt = sound[1]
                z = db.account.find_one({"username":use})

                if z!=None and bal>=amt:
                    temp = bal
                    temp = temp-amt
                    print(temp)
                    db.account.update({"username":username},{"$set":{"balance":temp}})
                    global bal
                    bal = temp

                    temp1 = z["balance"]
                    temp1 = int(temp1)
                    db.account.update({"username":use},{"$set":{"balance":temp1+amt}})
                    db.transfer.insert({"from":username , "to":use , "amt":amt})
                return render_template('profile2.html',name = name , balance = bal)
            if request.form.get('send')=='send':
                use = request.form['username_send']
                amt = request.form['amount']
                amt = int(amt)
                print(use,amt)
                z = db.account.find_one({"username":use})
                if z!=None and  bal>=amt:
                    temp = bal
                    temp = temp-amt
                    print(temp)
                    db.account.update({"username":username},{"$set":{"balance":temp}})
                    global bal
                    bal = temp
                    temp = db.account.find_one({"username":use})
                    temp1 = z["balance"]
                    temp1 = int(temp1)
                    db.account.update({"username":use},{"$set":{"balance":temp1+amt}})
                    db.transfer.insert({"from":username , "to":use , "amt":amt})
        return render_template('profile2.html',name = name , balance = bal)

@app.route("/log",methods = ["GET","POST"] )
def log():
    if username=="modi":
        dataI = db.transfer.find({"to":username})
        dataD = db.transfer.find({"from":username})
        return render_template('check_log.html',name = name , balance = bal , data1 = dataI , data2 = dataD)
    if username=="obama":
        dataI = db.transfer.find({"to":username})
        dataD = db.transfer.find({"from":username})
        return render_template('check_log1.html',name = name , balance = bal , data1 = dataI , data2 = dataD)



if __name__=='__main__':
    task = 0
    app.run(debug=True)

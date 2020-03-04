from flask import Flask,render_template,request,url_for,redirect
import requests
from datetime import datetime,timedelta
import pyrebase


config = {
 "apiKey": "AIzaSyCIXDU8UNMYEMDbPljFF6M4RtX6JOBY6Qs",
    "authDomain": "streetlightmanagement-675be.firebaseapp.com",
    "databaseURL": "https://streetlightmanagement-675be.firebaseio.com",
    "projectId": "streetlightmanagement-675be",
    "storageBucket": "streetlightmanagement-675be.appspot.com",
    "messagingSenderId": "761700878889",
    "appId": "1:761700878889:web:1fdb6764dcb35956142a38",
    "measurementId": "G-9TMR495E17"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

app = Flask(__name__,template_folder='Templates')
# res2 = []
class arrange:
    arrangebh3 = "regular"
    arrangebh6 = "regular"


@app.route("/",methods=["GET","POST"])
def dashboard():
    arrange2 = arrange.arrangebh3
    arrange1 = arrange.arrangebh6
    traffic=50
    msg = "In DayTime no arrangement can be done."
    labels=['LED1','LED2','LED3','LED4','LED5']
    colors = ['#ff0000', '#0000ff', '#ffffe0', '#FFA500','#808080']
    den = "Traffic Density is Low"
    bright = "Default Brightness : 50%"
    power = []
    powerbh6 = [50,60,20,55,60]
    powerbh3 = [50, 55, 20, 35, 40]
    bh6 = [1, 1, 0, 0, 0]
    bh6r = bh6
    bh6e = [1,0,1,0,1]
    bh3 = [0, 0, 1, 1, 1]
    newpow = []
    bh3r = bh3
    bh3e = [1,0,1,0,1]
    resfinl = ["Status Ok","Status Ok","Status Ok","Status Ok","Status Ok"]
    timeset1 = ""
    timerise1 = ""
    timenow = datetime.strptime(datetime.now().strftime("%H:%M:%S %p"),"%H:%M:%S %p").time()
    timenow = timedelta(hours=timenow.hour,minutes=timenow.minute)
    r = requests.get('https://api.sunrise-sunset.org/json?lat=31.326015&lng=75.576180&date=today')
    x = r.json()
    timerise = (datetime.strptime(x['results']['sunrise'], "%H:%M:%S %p").time())
    timerise1 = timedelta(hours=timerise.hour, minutes=timerise.minute) + timedelta(hours=5, minutes=30)
    timeset = (datetime.strptime(x['results']['sunset'], "%H:%M:%S %p").time())
    timeset1 = timedelta(hours=timeset.hour, minutes=timeset.minute) + timedelta(hours=5, minutes=30)
    print(timenow)
    if request.method=="POST":
        # arrange2 = arrange.arrangebh3
        # arrange1 = arrange.arrangebh6
        area = request.form["area"]
        print(request.form["area"])
        print(timeset1)
        if((timenow>timerise1) and (timenow<timeset1)):
            bright = "Default Brightness : 50% Enable At Night"
            res = []
            if (traffic > 50):
                den = "Traffic Density is High"
            if(area=="BH-6"):
                for i in range(0,5):
                    if(bh6[i]==1):
                        res.append("Status Error")
                    else:
                        res.append("Status Ok")
                resfinl = res
            elif(area=="BH-3"):
                for i in range(0,5):
                    if(bh3[i]==1):
                        res.append("Status Error")
                    else:
                        res.append("Status Ok")
                resfinl = res
        elif((timenow>timerise1 and timenow>timeset1) or (timenow<timerise1 and timenow<timeset1)):
            res = []
            if (area == "BH-6"):
                for i in range(0,5):
                    if (bh6[i] == 1 and arrange1=="regular"):
                        res.append("Status Ok")
                    if(bh6[i] == 0 and arrange1=="regular"):
                        res.append("Status Error")
                    if(arrange1=="even" and i%2==0 and bh6[i]==1):
                        res.append("Status Ok")
                    if(arrange1=="even" and i%2==0 and bh6[i]==0):
                        res.append("Status Error")
                    if (arrange1 == "even" and i % 2 != 0 and bh6[i] == 1):
                        res.append("Status Error")
                    if (arrange1 == "even" and i % 2 != 0 and bh6[i] == 0):
                        res.append("Status Ok")
                resfinl = res

            elif (area == "BH-3"):
                for i in range(0,5):
                    if (bh3[i] == 1 and arrange2 == "regular"):
                        res.append("Status Ok")
                    if (bh3[i] == 0 and arrange == "regular"):
                        res.append("Status Error")
                    if (arrange2 == "even" and i % 2 == 0 and bh3[i] == 1):
                        res.append("Status Ok")
                    if (arrange2 == "even" and i % 2 == 0 and bh3[i] == 0):
                        res.append("Status Error")
                    if (arrange2 == "even" and i % 2 != 0 and bh3[i] == 1):
                        res.append("Status Error")
                    if (arrange2 == "even" and i % 2 != 0 and bh3[i] == 0):
                        res.append("Status Ok")

        if(area=="BH-6"):
            power = powerbh6
        else:
            power = powerbh3

            if (traffic > 50):
                den = "Traffic Density is High"
                bright = "Adjusting Lights to 70%"
                newpow = []
                for i in range(0, 5):
                    newpow.append(power[i] * 2)
                power = newpow

            elif ((timenow < timerise1 and timenow < timeset1) and traffic <= 50):
                bright = "Adjusting Lights to 40%"
                newpow = []
                for i in range(0, 5):
                    newpow.append(power[i] * 2)
                power = newpow
                resfinl = res
    return render_template("dashboard.html",res=resfinl,arrange1=arrange1,arrange2 = arrange2,power=power,labels=labels,colors=colors,msg=msg,den = den,bright=bright)

@app.route("/changearray",methods = ["GET","POST"])
def changearray():
    if(request.method=="POST"):
        area = request.form["area1"]
        if(area == "BH-3"):
            arrange.arrangebh3 = request.form["arrange1"]
            if(arrange.arrangebh3 == "even"):
                db.child("Led-Arrange").push({"even":"1"})
            # print(arrange.arrangebh3)
        else:
            arrange.arrangebh6 = request.form["arrange1"]
        if(request.form["submit"]):
            return redirect(url_for("dashboard"))
    return render_template("changearray.html")

if(__name__) == "__main__":
    app.run(debug=True)
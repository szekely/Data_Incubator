import os,pickle
from flask import Flask,render_template,request,redirect
from bokeh.plotting import figure,output_file
from bokeh.io import output_notebook, show
app = Flask(__name__)

app.vars={}

base=os.getcwd()
print base
try:
    enrollment=pickle.load(open(os.path.join(base,'Enrollment_Pickle.p'),'rb'))
except:
    print "Failed to load enrollment data"
try:
    completion=pickle.load(open(os.path.join(base,'Completion_Pickle.p'),'rb'))
except:
    print "Failed to load completion data"
CIP_nums=[13.0,14.0,26.0,27.0,40.0,51.0401,51.1201,52.0,22.0101]
CIP_names=['Education','Engineering','Biological Sciences/Life Sciences','Mathematics','Physical Sciences','Dentistry','Medicine','Business Management and Administrative Services','Law']

app.CIP_names=CIP_names
app.slide=0
colors=[]

@app.route('/first',methods=['GET','POST'])
def first():
    if request.method=='GET':
        app.slide=1
        return render_template('Graph1_firstly.html')
    else:
        #request was a POST
        for x in ['Enrollment','Completion']:
            try:
                app.vars[x]=request.form[x]
            except:
                app.vars[x]=0
        return redirect('/main')

@app.route('/main')
def main():
    if app.slide==2: return render_template('end.html')
    return redirect('/next')

@app.route('/next',methods=['GET','POST'])
def next():  #remember the function name does not need to match the URL
    if request.method=='GET':
        app.slide=2
        return render_template('Graph1_second.html',ans1=app.CIP_names[0],ans2=app.CIP_names[1],ans3=app.CIP_names[2],
            ans4=app.CIP_names[3],ans5=app.CIP_names[4],ans6=app.CIP_names[5],
            ans7=app.CIP_names[6],ans8=app.CIP_names[7],ans9=app.CIP_names[8])
    elif request.method=='POST':
        app.vars['CIPs']=[]
        for x in range(9):
            try:
                app.vars['CIPs'].append(request.form[app.CIP_names[x]])
            except:
                app.vars['CIPs'].append(0)
        output_file("barplot.html")
        colors=['pink','red','gold','olive','green','darkturquoise','blue','lavender','indigo']
        p = figure(title="Graph of enrollment vs completion")

        if app.vars['Enrollment']=='Enrollment':
            for c in [x for x in range(9) if app.vars['CIPs'][x]!=0]:
                p.circle(x=range(1998,2016,2), y=[enrollment[str(yr)+'_'+str(CIP_nums[c])] for yr in range(1998,2016,2)], size=10, alpha=0.3,
                         color=colors[c], legend=CIP_names[c])
        if app.vars['Completion']=='Completion':
            for c in [x for x in range(9) if app.vars['CIPs'][x]!=0]:
                p.triangle(x=range(1999,2016), y=[completion[str(yr)+'_'+str(CIP_nums[c])] for yr in range(1999,2016)], size=10, alpha=0.3,
                         color=colors[c], legend=CIP_names[c])

        p.legend.location = "top_left"
        show(p)
        return redirect('/main')

if __name__ == "__main__":
    app.run(port=33507,debug=False)
    
#For C
#git rm --cached . -r
#git add .
#git commit -m "some name"
#git push heroku master

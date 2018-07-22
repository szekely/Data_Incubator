import os,traceback,pickle
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask,render_template,request,redirect
app = Flask(__name__)

base='D:\Data_incubator'
file=open(os.path.join(base,'CIPs.txt'),'r')
CIP_lines=file.readlines()
file.close()
CIPs=[line.split(')')[1].split('.')[0] for line in CIP_lines]
CIP_nums=[13.0,14.0,26.0,27.0,40.0,51.0401,51.1201,52.0,22.0101]
try:
    enrollment=pickle.load(open(os.path.join(base,'Enrollment_Pickle.p'),'rb'))
except:
    enrollment=dict(zip([str(yr)+'_'+str(cip) for yr in range(1998,2016,2) for cip in CIP_nums],[0]*len(CIP_nums)*len(range(1998,2016,2))))
    for yr in range(1998,2016,2):
        if 'ef'+str(yr)+'cp_rv.csv' in os.listdir(base):
            filename=os.path.join(base,'ef'+str(yr)+'cp_rv.csv')
        elif yr==1998:
            filename=os.path.join(base,'ef98_acp.csv')
        else:
            filename=os.path.join(base,'ef'+str(yr)+'cp.csv')
        enrol_raw=pd.read_csv(filename,na_values=['A','B','D','H'])
        if 'LINE' in enrol_raw.columns.values.tolist():
            enrol=enrol_raw.dropna(subset=['LINE','CIPCODE'])
            length=enrol['LINE'].keys()
            subset=['LINE','CIPCODE']
        elif 'line' in enrol_raw.columns.values.tolist():
            enrol=enrol_raw.dropna(subset=['line','cipcode'])
            length=enrol['line'].keys()
            subset=['line','cipcode']
        else:
            print 'failed to find good enrollment headers'
        for x in length:
            if enrol[subset[0]][x] in [9,11,23,25,'9','11','23','25']:
                if enrol[subset[1]][x] in CIP_nums:
                    try:
                        enrollment[str(yr)+'_'+str(enrol[subset[1]][x])]+=int(enrol['EFTOTLT'][x])
                    except:
                        enrollment[str(yr)+'_'+str(enrol[subset[1]][x])]+=int(int(enrol['efrace15'][x])+int(enrol['efrace16'][x]))
    pickle.dump(enrollment,open(os.path.join(base,'Enrollment_Pickle.p'),'wb'))
try:
    completion=pickle.load(open(os.path.join(base,'Completion_Pickle.p'),'rb'))
except:
    completion=dict(zip([str(yr)+'_'+str(cip) for yr in range(1999,2016) for cip in CIP_nums],[0]*len(CIP_nums)*len(range(1999,2016))))
    for yr in range(1999,2016):
        if 'c'+str(yr)+'a_rv.csv' in os.listdir(base):
            filename=os.path.join(base,'c'+str(yr)+'_a_rv.csv')
        elif yr==1999:
            filename=os.path.join(base,'c9798_a.csv')
        else:
            filename=os.path.join(base,'c'+str(yr)+'_a.csv')
        degrees_raw=pd.read_csv(filename,na_values=['A','B','D','H'])
        if 'AWLEVEL' in degrees_raw.columns.values.tolist():
            degrees=degrees_raw.dropna(subset=['AWLEVEL','CIPCODE'])
            length=degrees['AWLEVEL'].keys()
            subset=['AWLEVEL','CIPCODE']
        elif 'awlevel' in degrees_raw.columns.values.tolist():
            degrees=degrees_raw.dropna(subset=['awlevel','cipcode'])
            length=degrees['awlevel'].keys()
            subset=['awlevel','cipcode']
        else:
            print 'failed to find good enrollment headers'
        for x in length:
            if degrees[subset[0]][x] in [9,10,11,17,18,19]:
                if int(str(degrees[subset[1]][x]).split('.')[0]) in CIP_nums:
                    if 'crace15' in degrees_raw.columns.values.tolist():
                        completion[str(yr)+'_'+str(float(str(degrees[subset[1]][x]).split('.')[0]))]+=int(degrees['crace15'][x]+degrees['crace16'][x])
                    elif 'CRACE15' in degrees_raw.columns.values.tolist():
                        completion[str(yr)+'_'+str(float(str(degrees[subset[1]][x]).split('.')[0]))]+=int(degrees['CRACE15'][x]+degrees['CRACE16'][x])
                    elif 'CTOTALT' in degrees_raw.columns.values.tolist():
                        completion[str(yr)+'_'+str(float(str(degrees[subset[1]][x]).split('.')[0]))]+=degrees['CTOTALT'][x]
                elif degrees[subset[1]][x] in CIP_nums:
                    if 'crace15' in degrees_raw.columns.values.tolist():
                        completion[str(yr)+'_'+str(degrees[subset[1]][x])]+=int(degrees['crace15'][x]+degrees['crace16'][x])
                    elif 'CRACE15' in degrees_raw.columns.values.tolist():
                        try:
                            completion[str(yr)+'_'+str(float(str(degrees[subset[1]][x]).split('.')[0]))]+=int(degrees['CRACE15'][x]+degrees['CRACE16'][x])
                        except:
                            completion[str(yr)+'_'+str(float(str(degrees[subset[1]][x])))]+=int(degrees['CRACE15'][x]+degrees['CRACE16'][x])
                    elif 'CTOTALT' in degrees_raw.columns.values.tolist():
                        completion[str(yr)+'_'+str(degrees[subset[1]][x])]+=degrees['CTOTALT'][x]
    pickle.dump(completion,open(os.path.join(base,'Completion_Pickle.p'),'wb'))
try:
    enrollment_race=pickle.load(open(os.path.join(base,'Race_Enrollment_Pickle.p'),'rb'))
except:
    enrollment_race=dict(zip([str(yr)+'_'+str(cip)+'_'+rc for yr in range(1998,2016,2) for cip in CIP_nums for rc in ['American Indian or Alaska Native','Asian','Black or African American','Hispanic','Native Hawaiian or Other Pacific Islander','White']],[0]*len(CIP_nums)*len(range(1998,2016,2)*6)))
    rcs=['American Indian or Alaska Native','Asian','Black or African American','Hispanic','Native Hawaiian or Other Pacific Islander','White']
    for yr in range(1998,2016,2):
        if 'ef'+str(yr)+'cp_rv.csv' in os.listdir(base):
            filename=os.path.join(base,'ef'+str(yr)+'cp_rv.csv')
        elif yr==1998:
            filename=os.path.join(base,'ef98_acp.csv')
        else:
            filename=os.path.join(base,'ef'+str(yr)+'cp.csv')
        enrol_raw=pd.read_csv(filename,na_values=['A','B','D','H'])
        if 'LINE' in enrol_raw.columns.values.tolist():
            enrol=enrol_raw.dropna(subset=['LINE','CIPCODE'])
            length=enrol['LINE'].keys()
            subset=['LINE','CIPCODE']
        elif 'line' in enrol_raw.columns.values.tolist():
            enrol=enrol_raw.dropna(subset=['line','cipcode'])
            length=enrol['line'].keys()
            subset=['line','cipcode']
        else:
            print 'failed to find good enrollment headers'
        if 'EFAIANT' in enrol_raw.columns.values.tolist():
            if yr==2008:
                races=['EFRACE05','EFRACE06','EFRACE07','EFRACE08','EFRACE03','EFRACE04','EFRACE09','EFRACE10','EFRACE06','EFRACE07','EFRACE11','EFRACE12']
            else:
                races=['EFAIANT','EFASIAT','EFBKAAT','EFHISPT','EFNHPIT','EFWHITT']
        elif 'EFRACE05' in enrol_raw.columns.values.tolist():
            races=['EFRACE05','EFRACE06','EFRACE07','EFRACE08','EFRACE03','EFRACE04','EFRACE09','EFRACE10','EFRACE06','EFRACE07','EFRACE11','EFRACE12']
        elif 'efrace05' in enrol_raw.columns.values.tolist():
            races=[item.lower() for item in ['EFRACE05','EFRACE06','EFRACE07','EFRACE08','EFRACE03','EFRACE04','EFRACE09','EFRACE10','EFRACE06','EFRACE07','EFRACE11','EFRACE12']]
        else:
            print 'Issues with race'
        for x in length:
            if enrol[subset[0]][x] in [9,11,23,25,'9','11','23','25']:
                if enrol[subset[1]][x] in CIP_nums:
                    if len(races)>6:
                        rcr=0
                        for y in range(0,12,2):
                            try:
                                enrollment_race[str(yr)+'_'+str(enrol[subset[1]][x])+'_'+rcs[rcr]]+=int(enrol[races[y]][x]+enrol[races[y+1]][x])
                                rcr+=1
                            except ValueError:
                                rcr+=1
                                continue
                    else:
                        for y in range(6):
                            try:
                                enrollment_race[str(yr)+'_'+str(enrol[subset[1]][x])+'_'+rcs[y]]+=enrol[races[y]][x]
                            except ValueError:
                                continue
    pickle.dump(enrollment_race,open(os.path.join(base,'Race_Enrollment_Pickle.p'),'wb'))
try:
    completion_race=pickle.load(open(os.path.join(base,'Race_Completion_Pickle.p'),'rb'))
except:
    completion_race=dict(zip([str(yr)+'_'+str(cip)+'_'+race for yr in range(1999,2016) for cip in CIP_nums for race in ['American Indian or Alaska Native','Asian','Black or African American','Hispanic','Native Hawaiian or Other Pacific Islander','White']],[0]*len(CIP_nums)*len(range(1999,2016)*6)))
    rcs=['American Indian or Alaska Native','Asian','Black or African American','Hispanic','Native Hawaiian or Other Pacific Islander','White']
    for yr in range(1999,2016):
        if 'c'+str(yr)+'a_rv.csv' in os.listdir(base):
            filename=os.path.join(base,'c'+str(yr)+'_a_rv.csv')
        elif yr==1999:
            filename=os.path.join(base,'c9798_a.csv')
        else:
            filename=os.path.join(base,'c'+str(yr)+'_a.csv')
        degrees_raw=pd.read_csv(filename,na_values=['A','B','D','H'])
        if 'AWLEVEL' in degrees_raw.columns.values.tolist():
            degrees=degrees_raw.dropna(subset=['AWLEVEL','CIPCODE'])
            length=degrees['AWLEVEL'].keys()
            subset=['AWLEVEL','CIPCODE']
        elif 'awlevel' in degrees_raw.columns.values.tolist():
            degrees=degrees_raw.dropna(subset=['awlevel','cipcode'])
            length=degrees['awlevel'].keys()
            subset=['awlevel','cipcode']
        else:
            print 'failed to find good enrollment headers'
        if 'CAIANT' in degrees_raw.columns.values.tolist():
            if yr in range(2008,2011):
                races=['CRACE05','CRACE06','CRACE07','CRACE08','CRACE03','CRACE04','CRACE09','CRACE10','CRACE07','CRACE08','CRACE11','CRACE12']
            else:
                races=['CAIANT','CASIAT','CBKAAT','CHISPT','CNHPIT','CWHITT']
        elif 'CRACE05' in degrees_raw.columns.values.tolist():
            races=['CRACE05','CRACE06','CRACE07','CRACE08','CRACE03','CRACE04','CRACE09','CRACE10','CRACE07','CRACE08','CRACE11','CRACE12']
        elif 'crace05' in degrees_raw.columns.values.tolist():
            races=[item.lower() for item in ['CRACE05','CRACE06','CRACE07','CRACE08','CRACE03','CRACE04','CRACE09','CRACE10','CRACE07','CRACE08','CRACE11','CRACE12']]
        else:
            print 'Issues with race'
        for x in length:
            if degrees[subset[0]][x] in [9,10,11,17,18,19]:
                if len(races)>6:
                    rcr=0
                    for y in range(0,12,2):
                        if int(str(degrees[subset[1]][x]).split('.')[0]) in CIP_nums:
                            try:
                                completion_race[str(yr)+'_'+str(float(str(degrees[subset[1]][x]).split('.')[0]))+'_'+rcs[rcr]]+=int(degrees[races[y]][x]+degrees[races[y+1]][x])
                            except ValueError:
                                continue
                        elif degrees[subset[1]][x] in CIP_nums:
                            try:
                                completion_race[str(yr)+'_'+str(degrees[subset[1]][x])+'_'+rcs[rcr]]+=int(degrees[races[y]][x]+degrees[races[y+1]][x])
                            except ValueError:
                                continue
                        rcr+=1
                else:
                    for y in range(6):
                        if int(str(degrees[subset[1]][x]).split('.')[0]) in CIP_nums:
                            completion_race[str(yr)+'_'+str(float(str(degrees[subset[1]][x]).split('.')[0]))+'_'+rcs[y]]+=degrees[races[y]][x]
                        elif degrees[subset[1]][x] in CIP_nums:
                            completion_race[str(yr)+'_'+str(degrees[subset[1]][x])+'_'+rcs[y]]+=degrees[races[y]][x]
    pickle.dump(completion_race,open(os.path.join(base,'Race_Completion_Pickle.p'),'wb'))

app.enrollment=enrollment
app.completion=completion
app.enrollment_race=enrollment_race
app.completion_race=completion_race

colors=['r.','rx','ro','rv','r^','r<','r>','rs','r*']
CIP_names=['Education','Engineering','Biological Sciences/Life Sciences','Mathematics','Physical Sciences','Dentistry','Medicine','Business Management and Administrative Services','Law']
#for c in range(len(CIP_nums)):
#    y=[enrollment[str(yr)+'_'+str(CIP_nums[c])] for yr in range(1998,2016,2)]
#    x=range(1998,2016,2)
#    n, bins, patches = plt.hist(x,len(range(1998,2016,2)),histtype='bar',align='mid',color='green')
#    plt.plot(x,y,colors[c],label=CIP_names[c])
#colors=['b.','bx','bo','bv','b^','b<','b>','bs','b*']
#for c in range(len(CIP_nums)):
#    y=[completion[str(yr)+'_'+str(CIP_nums[c])] for yr in range(1999,2016)]
#    x=range(1999,2016)
#    n, bins, patches = plt.hist(x,len(range(1998,2016,2)),histtype='bar',align='mid',color='green')
#    plt.plot(x,y,colors[c],label=CIP_names[c])
#plt.xlabel('Year')
#plt.ylabel('Enrollment and Completion')
#plt.title('Graph of enrollment vs completion')
#plt.legend(CIP_names)
#plt.grid(False)
#plt.show()
markers=['.','x','o','v','^','<','>','s','*']
colors=['b','g','r','c','m','y']
#rcs=['American Indian or Alaska Native','Asian','Black or African American','Hispanic','Native Hawaiian or Other Pacific Islander','White']
rcs=['American Indian or Alaska Native','Asian','Black or African American','Hispanic','Native Hawaiian or Other Pacific Islander']
for c in range(len(CIP_nums)):
    for r in range(len(rcs)):
        y=[completion_race[str(yr)+'_'+str(CIP_nums[c])+'_'+rcs[r]] for yr in range(1999,2016)]
        print y
        x=range(1999,2016)
    #    n, bins, patches = plt.hist(x,len(range(1998,2016,2)),histtype='bar',align='mid',color='green')
        plt.plot(x,y,colors[r]+markers[c],label=CIP_names[c])
plt.xlabel('Year')
plt.ylabel('Completion')
plt.title('Graph of completion by race')
plt.legend(rcs)
plt.grid(False)
plt.show()
for c in range(len(CIP_nums)):
    for r in range(len(rcs)):
        y=[enrollment_race[str(yr)+'_'+str(CIP_nums[c])+'_'+rcs[r]] for yr in range(1998,2016,2)]
        print y
        x=range(1998,2016,2)
    #    n, bins, patches = plt.hist(x,len(range(1998,2016,2)),histtype='bar',align='mid',color='green')
        plt.plot(x,y,colors[r]+markers[c],label=CIP_names[c])
plt.xlabel('Year')
plt.ylabel('Enrollment')
plt.title('Graph of enrollment by race')
plt.legend(rcs)
plt.grid(False)
plt.show()

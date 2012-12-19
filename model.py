import MySQLdb
import os
import pickle
from itertools import izip, chain
from collections import OrderedDict
from sklearn import linear_model
from sklearn import ensemble
from sklearn import tree
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt


db_train = MySQLdb.connect("localhost","root","password","kiva" )
db_test = MySQLdb.connect("localhost","root","password","kiva_test" )
cursor_train = db_train.cursor()
cursor_test = db_test.cursor()

train_x = []
train_y = []
test_x = []
test_y = []
sectormap = {"Agriculture":1,"Arts":2,"Clothing":3,"Construction":4,"Education":5,"Entertainment":6,"Food":7,"Health":8,"Housing":9,"Manufacturing":10,"Personal Use":11,"Retail":12,"Services":13,"Transportation":14,"Wholesale":15}

x = []
y = []
x1 = []
y1 = []

def loadtraindata():
    # Download the file
    cursor_train.execute("select loan_amount,paid_amount,funded_amount,disbursal_amount,sector,partner_id,gender,funded_date from loan where rand()<=0.5")
    data = cursor_train.fetchall()
    loan_amount = 0
    paid_amount = 0 
    funded_amount = 0 
    disbursal_amount = 0 
    for row in data:
        temp = [] 
        if row[0] != None:
            loan_amount = row[0]
        temp.append(loan_amount)
        if row[1] != None:
            paid_amount = row[1]
        temp.append(paid_amount)
        if row[2] != None:
            funded_amount = row[2]
        temp.append(funded_amount)
        if row[3] != None:
            disbursal_amount = row[3]
        temp.append(disbursal_amount)
        temp.append(sectormap.get(row[4]))
        temp.append(row[5])
        if row[6] == 'F':
            temp.append(1)
        else :
            temp.append(0)
        train_x.append(temp)
        funded_date = row[7]
        if funded_date == None:
            train_y.append(0)
        else :
            train_y.append(1)
            
    print "Number of train records:", len(train_x)
    #print train_x
   
def loadtestdata():
    # Download the file
    cursor_test.execute("select loan_amount,paid_amount,funded_amount,disbursal_amount,sector,partner_id,gender,funded_date from loan where rand()<=0.5")
    data = cursor_test.fetchall()
    loan_amount = 0
    paid_amount = 0 
    funded_amount = 0 
    disbursal_amount = 0 

    for row in data:
        temp = [] 
        if row[0] != None:
            loan_amount = row[0]
        temp.append(loan_amount)
        if row[1] != None:
            paid_amount = row[1]
        temp.append(paid_amount)
        if row[2] != None:
            funded_amount = row[2]
        temp.append(funded_amount)
        if row[3] != None:
            disbursal_amount = row[3]
        temp.append(disbursal_amount)
        temp.append(sectormap.get(row[4]))
        temp.append(row[5])
        if row[6] == 'F':
            temp.append(1)
        else :
            temp.append(0)
        test_x.append(temp)
        funded_date = row[7]
        if funded_date == None:
            test_y.append(0)
        else :
            test_y.append(1)
            
    print "Number of test records:", len(test_x)
    #print test_x
    
def getProbabilities(clf,test_x):
    global problabels 
    problabels = {}
    probabilities =  clf.predict_proba(test_x)
    print "length:", len(probabilities)# ,"::probabilities:", probabilities 
    i = 0
    try:
        for line in probabilities:
            if len(line)==2:
                problabels[i] = line[1] 
                i += 1
    except IndexError:
        print "Error when i is:",i
        print "prob:",len(problabels)
    problabels = OrderedDict(sorted(problabels.items(), key=lambda x: -x[1]))
    print "Model: ",type(clf), "No of test records:",len(problabels)
    
    
def calculateAccuracy(th,test_y):
    bullseyes = 0;
    accuracy = 0;
    if th == 0:
        th = 0.5
    for k,v in problabels.iteritems():
        #print "key, val:", k, v
        
        predictedLabel = 0;    
        if v >= th:
            predictedLabel = 1
        #print "predictedLabel:", predictedLabel, "test_y[k]",test_y[k]
        if(test_y[k] == predictedLabel):
            bullseyes +=1;
    if len(problabels) != 0 :
        accuracy = float(bullseyes)/(len(problabels))
    print "Accuracy :"+ str(accuracy)
    return accuracy

def fitmodel():

    clflogistic = linear_model.LogisticRegression().fit(train_x, train_y)
    getProbabilities(clflogistic,train_x)
    calculateAccuracy(0,train_y)
    
    clfTree = tree.DecisionTreeClassifier().fit(train_x, train_y)
    getProbabilities(clfTree,train_x)
    calculateAccuracy(0,train_y)
    
def comparemodels():
    count = 1
    while count < 20: 
        print "-----------------------------------------------------------------------"
        print "Evaluating for :" , count * 5, "%"
        print "-----------------------------------------------------------------------"
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        train_x, train_y, test_size=count*0.05, random_state=0)
        print 'Training data#: ',len(X_train), ' Test data#: ',len(X_test)
        count += 1
        clflogistic = linear_model.LogisticRegression().fit(X_train, y_train)
        #print "Score: ", clflogistic.score(X_test,y_test)
        getProbabilities(clflogistic,X_test)
        accuracy = calculateAccuracy(0,y_test)
        x.append(count*5)
        y.append(accuracy)

        clfTree = tree.DecisionTreeClassifier().fit(X_train, y_train)
        #print "Score: ", clfTree.score(X_test,y_test)
        getProbabilities(clfTree,X_test)
        accuracy = calculateAccuracy(0,y_test)
        x1.append(count*5)
        y1.append(accuracy)
        print "-----------------------------------------------------------------------"

    plt.plot(x, y, c='r', label="Logit")
    plt.plot(x1, y1, c='g', label= "Tree")
    plt.xlabel("% Training Set") # set the x axis label 
    plt.ylabel("Accuracy") # set the y axis label 
    plt.legend() # place a legend on the current axes
    plt.show()
    

    
    
loadtraindata();
loadtestdata();
fitmodel();
comparemodels()

db_train.close()
db_test.close()

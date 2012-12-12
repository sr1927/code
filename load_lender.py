import MySQLdb
import lender
import json
import sys
import os
import random

dirname = "C:\\Documents and Settings\\rangas1\\Desktop\\Stern\\PracticalDataScience\\project\\data\\lenders\\"

#filename = "C:\\Documents and Settings\\rangas1\\Desktop\\Stern\\PracticalDataScience\\project\\data\\lenders\\1.json"
data = []

def readfile(filename):
    try :
        filehandle = open(dirname+filename,"r")
    except IOError : 
        print "Data file read error. Please check whether data file was downloaded and stored properly."
        raise
    rawdata = json.load(filehandle)
    #print str(data["lenders"])
    global data
    data = rawdata["lenders"]
    print len(data)


def insertrecord(data):
    db_train = MySQLdb.connect("localhost","root","password","kiva" )
    db_test = MySQLdb.connect("localhost","root","password","kiva_test" )
    db_train.autocommit(True) 
    db_test.autocommit(True) 
    cursor_train = db_train.cursor()
    cursor_test = db_test.cursor()
    
    print type(data)
    for line in data:
        lender_id = line["lender_id"]
        print lender_id
        if lender_id == None:
            continue;
        name = line["name"]
        image_id = line["image"]["id"]
        template_id = line["image"]["template_id"]
        whereabouts = line["whereabouts"]
        country_code = line["country_code"]
        uid = line["uid"]
        member_since = line["member_since"]
        personal_url = line["personal_url"]
        occupation = line["occupation"]
        loan_because = line["loan_because"]
        occupational_info = line["occupational_info"]
        loan_count = line["loan_count"]
        invitee_count = line["invitee_count"]
        inviter_id = line["inviter_id"]       

        try:
            #cursor.execute("""INSERT INTO lender values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""",(lender_id,name,image_id,template_id,whereabouts,country_code,lender_uid,member_since,personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count))
            if(random.random() > 0.7):
                cursor_test.execute("""INSERT INTO lender values (%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,%s,%s,%s)""",(lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count))
                db_test.commit()
            else:
                cursor_train.execute("""INSERT INTO lender values (%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,%s,%s,%s)""",(lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count))
                db_train.commit()
        except UnicodeEncodeError:
            print 'Unicode char', lender_id
        except NameError as e:
            print "**********************************Rolling back*************"
            print sys.exc_info()[0]
            print e
            db_test.rollback()
            db_train.rollback()

    db_test.close()
    db_train.close()

for filename in os.listdir(dirname):
    print  filename
    readfile(filename)
    insertrecord(data)

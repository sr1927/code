import os
import httplib2
import json
import MySQLdb
import sys
import random

db_train = MySQLdb.connect("localhost","root","password","kiva" )
db_test = MySQLdb.connect("localhost","root","password","kiva_test" )
db_train.autocommit(True) 
db_test.autocommit(True) 
cursor_train = db_train.cursor()
cursor_test = db_test.cursor()

app_idstr = "&app_id=edu.stern.nyu.pds-f2012"
h = httplib2.Http()
for count in range(2,500):
    resp, content = h.request("http://api.kivaws.org/v1/lenders/newest.json?page="+str(count)+app_idstr)
    assert resp.status == 200
    print resp
    print content
    data = json.loads(content)
    print len(data)
    print len(data["lenders"])
    ids = ""
    count = 0
    for lender in data["lenders"]:
        count += 1
        lender_id = lender["lender_id"]
        if count != 50:
            ids += lender_id +","
        else:
            ids += lender_id 
    app_idstring = "?app_id=edu.stern.nyu.pds-f2012"
    requeststr = "http://api.kivaws.org/v1/lenders/"+ids+".json"+app_idstring
    print requeststr
    resp, content = h.request(requeststr)
    data = json.loads(content)
    print data["lenders"]
    print type(data["lenders"])

    for line in data["lenders"]:
        lender_id = line["lender_id"]
        print lender_id
        if line.has_key("name"):
            name = line["name"]
        else :
            name = None
        if line.has_key("image") :
            image_id = line["image"]["id"]
        else :
            image_id = ""
            
        template_id = line["image"]["template_id"]
        whereabouts = line["whereabouts"]
        if line.has_key("country_code") :
            country_code = line["country_code"]
        else:
            country_code = None
            
        uid = line["uid"]
        member_since = line["member_since"]
        personal_url = line["personal_url"]
        occupation = line["occupation"]
        loan_because = line["loan_because"]
        occupational_info = line["occupational_info"]
        loan_count = line["loan_count"]
        invitee_count = line["invitee_count"]
        if line.has_key("inviter_id") :
            inviter_id = line["inviter_id"]       
        else:
            inviter_id = None
        
        try:
            #cursor.execute("""INSERT INTO lender values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""",(lender_id,name,image_id,template_id,whereabouts,country_code,lender_uid,member_since,personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count))
            if(random.random() > 0.7):
                cursor_test.execute("""INSERT INTO lender values (%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,%s,%s,%s)""",(lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count))
                #print lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count
                db_test.commit()
            else:
                cursor_train.execute("""INSERT INTO lender values (%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,%s,%s,%s)""",(lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count))
                #print lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count
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
    

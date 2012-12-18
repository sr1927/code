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
for count in range(70,400):
    resp, content = h.request("http://api.kivaws.org/v1/loans/newest.json?page="+str(count)+app_idstr)
    assert resp.status == 200
    print resp
    print content
    data = json.loads(content)
    print len(data)
    print len(data["loans"])
    ids = ""
    count = 0
    for lender in data["loans"]:
        count += 1
        loan_id = str(lender["id"])
        if count != 10:
            ids += loan_id +","
        else:
            ids += loan_id 
            break
    app_idstring = "?app_id=edu.stern.nyu.pds-f2012"
    requeststr = "http://api.kivaws.org/v1/loans/"+ids+".json"+app_idstring
    print requeststr
    resp, content = h.request(requeststr)
    data = json.loads(content)
    print content
    print data["loans"]
    print type(data["loans"])

    for line in data["loans"]:
        funded_date = ""
        paid_date = ""
        loan_id = line["id"]
        print loan_id
        name = line["name"]
        status = line["status"]
        funded_amount = line["funded_amount"]
        paid_amount = None
        if line.has_key("paid_amount"):
            paid_amount = line["paid_amount"]
        image_id = line["image"]["id"]
        template_id = line["image"]["template_id"]
        activity = line["activity"]
        sector = line["sector"]
        uses = line["use"]
        country_code = line["location"]["country_code"]
        town = None
        if line["location"].has_key("town"):
            town = line["location"]["town"]
        geolevel = line["location"]["geo"]["level"]
        geopairs = line["location"]["geo"]["pairs"]
        geotype = line["location"]["geo"]["type"]
        partner_id = line["partner_id"]
        disbursal_amount = line["terms"]["disbursal_amount"]
        disbursal_currency = line["terms"]["disbursal_currency"]
        disbursal_date = line["terms"]["disbursal_date"]
        disbursal_date = None
        if disbursal_date != None:
            disbursal_date = disbursal_date[:10]
        loan_amount = line["terms"]["loan_amount"]
        nonpayment = line["terms"]["loss_liability"]["nonpayment"]
        currency_exchange = line["terms"]["loss_liability"]["currency_exchange"]
        posted_date = line["posted_date"]
        posted_date = None
        if posted_date!= None:
            posted_date = posted_date[:10]
        funded_date = None
        paid_date = None
        if line.has_key("funded_date"):
            funded_date = line["funded_date"]
        if funded_date != None:
            funded_date = funded_date[:10]
        if line.has_key("paid_date"):
            paid_date = line["paid_date"]
        if paid_date != None:
            paid_date = paid_date[:10]
        loan_amount = line["loan_amount"]
        journal_entries = line["journal_totals"]["entries"]
        journal_bulk_entries = line["journal_totals"]["bulkEntries"]
        if len(line["borrowers"]) == 1:
            gender = line["borrowers"][0]["gender"]
        elif len(line["borrowers"]) > 1:
            gender = 'N'
        
        try:
            if(random.random() > 0.7):
                cursor_test.execute("""INSERT INTO loan values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,date(%s),date(%s),%s,date(%s),%s,%s,%s,%s)""",(loan_id,name ,status,funded_amount ,paid_amount,image_id,template_id, activity,sector,uses,country_code,town ,geolevel,geopairs,geotype ,partner_id ,disbursal_amount,disbursal_currency,disbursal_date,loan_amount,nonpayment,currency_exchange ,posted_date,funded_date,None,paid_date,None,journal_entries, journal_bulk_entries,gender))
                db_test.commit()
            else:
                cursor_test.execute("""INSERT INTO loan values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,date(%s),date(%s),%s,date(%s),%s,%s,%s,%s)""",(loan_id,name ,status,funded_amount ,paid_amount,image_id,template_id, activity,sector,uses,country_code,town ,geolevel,geopairs,geotype ,partner_id ,disbursal_amount,disbursal_currency,disbursal_date,loan_amount,nonpayment,currency_exchange ,posted_date,funded_date,None,paid_date,None,journal_entries, journal_bulk_entries,gender))
                db_train.commit()
        except UnicodeEncodeError:
            print 'Unicode char', loan_id
        except NameError as e:
            print "**********************************Rolling back*************"
            print sys.exc_info()[0]
            print e
            db_test.rollback()
            db_train.rollback()
        except :
            continue

db_test.close()
db_train.close()
    

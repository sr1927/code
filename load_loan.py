import MySQLdb
import lender
import json
import sys
import os
import random

dirname = "C:\\Documents and Settings\\rangas1\\Desktop\\Stern\\PracticalDataScience\\project\\data\\loans\\"

#filename = "C:\\Documents and Settings\\rangas1\\Desktop\\Stern\\PracticalDataScience\\project\\data\\loans\\1.json"
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
    data = rawdata["loans"]
    print len(data)


def insertrecord(data):

    db_train = MySQLdb.connect("localhost","root","password","kiva" )
    db_test = MySQLdb.connect("localhost","root","password","kiva_test" )
    db_train.autocommit(True) 
    db_test.autocommit(True) 
    cursor_train = db_train.cursor()
    cursor_test = db_test.cursor()

    for line in data:
        loan_id = line["id"]
        print loan_id
        name = line["name"]
        status = line["status"]
        funded_amount = line["funded_amount"]
        paid_amount = line["paid_amount"]
        image_id = line["image"]["id"]
        template_id = line["image"]["template_id"]
        activity = line["activity"]
        sector = line["sector"]
        uses = line["use"]
        country_code = line["location"]["country_code"]
        town = line["location"]["town"]
        geolevel = line["location"]["geo"]["level"]
        geopairs = line["location"]["geo"]["pairs"]
        geotype = line["location"]["geo"]["type"]
        partner_id = line["partner_id"]
        disbursal_amount = line["terms"]["disbursal_amount"]
        disbursal_currency = line["terms"]["disbursal_currency"]
        disbursal_date = line["terms"]["disbursal_date"]
        if disbursal_date != None:
            disbursal_date = disbursal_date[:10]
        loan_amount = line["terms"]["loan_amount"]
        nonpayment = line["terms"]["loss_liability"]["nonpayment"]
        currency_exchange = line["terms"]["loss_liability"]["currency_exchange"]
        posted_date = line["posted_date"]
        if posted_date!= None:
            posted_date = posted_date[:10]
        funded_date = line["funded_date"]
        if funded_date != None:
            funded_date = funded_date[:10]
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
                cursor_train.execute("""INSERT INTO loan values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,date(%s),%s,%s,%s,date(%s),date(%s),%s,date(%s),%s,%s,%s,%s)""",(loan_id,name ,status,funded_amount ,paid_amount,image_id,template_id, activity,sector,uses,country_code,town ,geolevel,geopairs,geotype ,partner_id ,disbursal_amount,disbursal_currency,disbursal_date,loan_amount,nonpayment,currency_exchange ,posted_date,funded_date,None,paid_date,None,journal_entries, journal_bulk_entries,gender))
                db_train.commit()
        except UnicodeEncodeError:
            print 'Unicode char', id
        except NameError as e:
            print "**********************************Rolling back*************"
            print sys.exc_info()[0]
            print e
            db.rollback()
        except :
            print "Error:", sys.exc_info()[0]
            
    db_test.close()
    db_train.close()

for filename in os.listdir(dirname):
    print  filename
    readfile(filename)
    insertrecord(data)

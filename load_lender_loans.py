import MySQLdb
import httplib2
import json
import _mysql_exceptions

db = MySQLdb.connect("localhost","root","password","kiva" )

cursor = db.cursor()

cursor.execute("SELECT lender_id from lender")
data = cursor.fetchall()
app_idstr = "?app_id=edu.stern.nyu.pds-f2012"
h = httplib2.Http()

for row in data:
    print "id: %s " % row[0]
    lender_id = str(row[0])
    resp, content = h.request("http://api.kivaws.org/v1/lenders/"+lender_id+"/loans.json"+app_idstr)
    if resp.status != 200:
        continue;
    print resp
    print content
    data = json.loads(content)
    print len(data)
    print len(data["loans"])
    for loan in data["loans"]:
        if loan.has_key("id"):
            loan_id = loan["id"]
            print "Loan id ", loan_id 
            try:
                cursor.execute("""INSERT INTO LENDER_LOANS values(%s,%s)""",(lender_id,loan_id))
                db.commit()
            except :
                print "foriegn key violation, continuing"
db.close()

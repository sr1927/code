import MySQLdb
import httplib2
import json
import _mysql_exceptions

db = MySQLdb.connect("localhost","root","password","kiva" )

cursor = db.cursor()

cursor.execute("SELECT id from loan")
data = cursor.fetchall()
app_idstr = "&app_id=edu.stern.nyu.pds-f2012"
h = httplib2.Http()

for row in data:
    print "id: %s " % row[0]
    loan_id = str(row[0])
    resp, content = h.request("http://api.kivaws.org/v1/loans/"+loan_id+"/lenders.json")
    print resp
    print content
    data = json.loads(content)
    print len(data)
    print len(data["lenders"])
    for lender in data["lenders"]:
        if lender.has_key("lender_id"):
            lender_id = lender["lender_id"]
            print "lender_id ", lender_id 
            try:
                cursor.execute("""INSERT INTO LOAN_LENDERS values(%s,%s)""",(loan_id,lender_id))
                db.commit()
            except :
                print "foriegn key violation, continuing"
db.close()

import os
import httplib2
import json

dirname = "C:\\Documents and Settings\\rangas1\\Desktop\\Stern\\PracticalDataScience\\project\\data\\lenders\\"

#for filename in os.listdir(dirname):
#    print  filename

app_id = "edu.stern.nyu.pds-f2012"
h = httplib2.Http()
resp, content = h.request("http://api.kivaws.org/v1/lenders/newest.json?page=1")
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

requeststr = "http://api.kivaws.org/v1/lenders/"+ids+".json"
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
        
    print lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since[:10],personal_url,occupation,loan_because,occupational_info,loan_count,invitee_count

from WordCloudMaker import WordCloudMaker
import urllib2
import MySQLdb

def getText():
    text = ""
    cursor = db.cursor()
    cursor.execute("SELECT uses from loan where uses is not null limit 10000")
    data = cursor.fetchall()
    for row in data:
        text += row[0]
    return text 
    
def getLenderText():
    text = ""
    cursor = db.cursor()
    cursor.execute("SELECT loan_because from lender where loan_because is not null limit 10000")
    data = cursor.fetchall()
    for row in data:
        text += row[0]
    return text 


db = MySQLdb.connect("localhost","root","password","kiva" )

client = WordCloudMaker("nq5xaswr9unlh2i12zrmx70rul1cnn", "lwftyt5nyzmorfuorqo63tsevegyjd")

text = getText()
response = client.makeWordCloud(400,text,600)
print ("_____________________________________________________________________________________")
# now you can do something with the response.
print response.body
print response.body["url"]

text = getLenderText()
response = client.makeWordCloud(400,text,600)
print ("_____________________________________________________________________________________")
# now you can do something with the response.
print response.body
print response.body["url"]

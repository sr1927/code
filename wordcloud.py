from WordCloudMaker import WordCloudMaker
import urllib2
import MySQLdb

def getText():
    text = ""
    db = MySQLdb.connect("localhost","root","password","kiva" )

    cursor = db.cursor()

    cursor.execute("SELECT uses from loan")
    data = cursor.fetchall()
    for row in data:
        text += row[0]

    return text 
    
client = WordCloudMaker("nq5xaswr9unlh2i12zrmx70rul1cnn", "lwftyt5nyzmorfuorqo63tsevegyjd")

text = getText()

response = client.makeWordCloud(400,text,600)
print ("_____________________________________________________________________________________")
# now you can do something with the response.
print response.body
print response.body["url"]


import MySQLdb
import httplib2
import json
import _mysql_exceptions
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


db = MySQLdb.connect("localhost","root","password","kiva" )

cursor = db.cursor()
cursor1 = db.cursor()
cursor.execute("select * from loan_lenders limit 1000")
data = cursor.fetchall()
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=0,llcrnrlat=-80,urcrnrlon=360,urcrnrlat=80,projection='mill')

for row in data:
    cursor1.execute("select latitude,longitude from country where iso_code=(select country from loan where id ='"+str(row[0])+"')")
    loancountry = cursor1.fetchall()
    #print loancountry
    cursor1.execute("select latitude,longitude from country where iso_code=(select country_code from lender where lender_id ='"+str(row[1])+"')")
    lendercountry = cursor1.fetchall()
    #print lendercountry
    loanlat=0 ;loanlon=0; lenderlat=0;lenderlon=0
    for row in loancountry:
        loanlat = row[0]; loanlon = row[1]
    for row in lendercountry:
        lenderlat = row[0]; lenderlon = row[1]
    # draw great circle route between NY and London
    if loanlat!=0 and loanlon!=0 and lenderlat!=0 and lenderlon!=0:
        print "drawing", loanlat,loanlon,lenderlat,lenderlon
        m.drawgreatcircle(loanlon,loanlat,lenderlon,lenderlat,linewidth=1,color='b')
    
m.drawcoastlines()
m.fillcontinents()
# draw parallels
m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
ax.set_title('Loan Country plot')
plt.show()

db.close()
    
from flask import Flask, url_for
app = Flask(__name__)

import pyodbc

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/sql/<lat>/<long>')	
def api_sql(lat,long):
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=prashantvikramsingh.database.windows.net;DATABASE=Zillow;UID=prashant;PWD=Pvs758993@')
	cursor = cnxn.cursor()
	cursor.execute("SELECT top 10 * FROM [dbo].[distance] ("+lat+","+long+") order by distance")
	rows = cursor.fetchall()
	s='ParcelID		Latitude		Longitude		Distance'+'\n\n'
	#print(rows)
	for row in rows:
	
		s+= str(row[0])+'		'+str(row[1])+'		'+str(row[2])+'		'+str(row[3]) +'\n'
		#return 'Helloooooo'
			#return 'You are reading ' + articleid
	return s 
	
if __name__ == '__main__':
    app.run()
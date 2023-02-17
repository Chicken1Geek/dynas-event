import sqlite3 as sqlite
from datetime import datetime,timezone
dbConn = sqlite.connect('main.db',check_same_thread=False)
sql = dbConn.cursor()

ticketTableQuery = 'create table if not exists ticket (ticketId text,name text,email text,pcontact integer,contact integer,food text,transport text,status text)'

logTableQuery = 'create table if not exists log (time text,user text,ticketId text,event text)'

for query in [ticketTableQuery,logTableQuery]:
	sql.execute(query)

def run(query):
	a = sql.execute(query).fetchall()
	dbConn.commit()
	return a

def createTicket(name,email,pcontact,contact,transport,food):
	ticketId = str(pcontact)[-4:] + name[:3]
	query = f"""insert into ticket (ticketId,name,email,pcontact,contact,food,transport,status) values('{ticketId}','{name}','{email}',{pcontact},{contact},'{food}','{transport}','tv'); """
	sql.execute(query)
	dbConn.commit()
	return ticketId
	
def getAllTicket(status):
	data = sql.execute(f"""select * from ticket where status == '{status}' """).fetchall()
	result = []
	for i in data:
		result.append(Ticket(i))
	return result

def getTicket(ticketId):
	data = sql.execute(f"""select * from ticket where ticketId == '{ticketId}'""").fetchone()
	return Ticket(data)

def Ticket(data):
	result = {}
	j = 0
	for i in ['ticketId','name','email','pcontact','contact','food','transport','status']:
		result[i] = data[j]
		j+=1
	return result

def updateTicket(ticketId,status):
	query = f"""update ticket set status='{status}' where ticketId == '{ticketId}'"""
	sql.execute(query)
	dbConn.commit()

def log(ticketId,event,user):
	with open('log.txt','at') as file:
		log = f'{datetime.now(timezone.utc)} - {ticketId} - {event} - {user}\n'
		file.write(log)

#run('delete from ticket')
#createTicket('sjs','jj',9737,3278,'sjsj','sss')
#print(getAllTicket())
#print(updateTicket('3737sjs','uwuw'))

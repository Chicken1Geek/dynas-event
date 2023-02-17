from flask import Flask , request
from flask_cors import CORS
import db
import validators
app = Flask('Dynas Backend api')
CORS(app)

# Api
@app.route('/api/create')
def createTicketEndpoint():
	args = request.args.to_dict()
	if len(args) == 6:
		for i in list(args.values()):
			if i == '':
				return 'You have not filled one or more fields',403
	else:
		return 'You have not filled one or more fields',403

	if not validators.email(args['email']):
		return 'Bad email address',403
	
	for i in ['pcontact','contact']:
		if len(args[i]) != 10:
			return 'Invalid Mobile Number' , 403
	id = db.createTicket(args['name'],args['email'],int(args['pcontact']),int(args['contact']),args['food'],args['transport'])
	db.log(id,'create','app')
	return id,200

@app.route('/api/list')
def listTickets():
	args = request.args.to_dict()['view']
	return db.getAllTicket(args)

@app.route('/api/status')
def ticketStatus():
	args = request.args.to_dict()['ticketId']
	return db.getTicket(args)

@app.route('/api/do')
def doTicket():
	args = request.args.to_dict()
	if args['action'] == 'verify':
		status = 'tp'
	else:
		status = 'v'
	db.updateTicket(args['ticketId'],status)
	db.log(args['ticketId'],'update',args['user'])
	return ' ',200

@app.route('/api/run')
def runSql():
	args = request.args.to_dict()['sql']
	return db.run(args)

	
app.run(host='0.0.0.0',port='8080')
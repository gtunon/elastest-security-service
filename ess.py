"""
Author: Avinash Sudhodanan
Project: ElasTest
Description: The following code is the API backend of the ElasTest Security Service
How to run: Download the file and execute "python <filename>" in the commandprompt
Language: Python 2.7 (supposed to work also for python 3 but not properly tested at the moment)
"""
from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask_httpauth import HTTPBasicAuth
import subprocess
import time
from pprint import pprint
from zapv2 import ZAPv2
import os

target = '0.0.0.0' #indicates in which IP address the API listents to
por = 8000 #indicates the port in
api_version='r3' #represents the current version of the API
zap=ZAPv2() #call to the OWAZP ZAP python API library (https://github.com/zaproxy/zaproxy/wiki/ApiPython)
app = Flask(__name__, static_url_path = "")

auth = HTTPBasicAuth() #for securing api calls using HTTP basic authentication

secjobs=[] #setting empty secjobs list when api starts

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def make_public_secjob(secjob):
    new_secjob = {}
    for field in secjob:
        new_secjob[field] = secjob[field]
    return new_secjob

@app.route('/', methods = ['GET'])
def get_gui():
    return render_template('ess.html')

@app.route('/ess/api/'+api_version+'/secjobs', methods = ['GET'])
def get_secjobs():
    return jsonify( { 'secjobs': map(make_public_secjob, secjobs) } )

@app.route('/ess/api/v0.1/secjobs/<int:secjob_id>', methods = ['GET'])
def get_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    return jsonify( { 'secjob': make_public_secjob(secjob[0]) } )


@app.route('/ess/api/'+api_version+'/secjobs', methods = ['POST'])
def create_secjob():
    if not request.json or not 'name' in request.json:
        abort(400)
    secjob = {
        'id': secjobs[-1]['id'] + 1,
        'name': request.json['name'],
        'vulns': request.json['vulns'],
        'tJobId': request.json['tJobId'],
        'maxRunTimeInMins': request.json['maxRunTimeInMins']
    }
    secjobs.append(secjob)
    return jsonify( { 'secjob': make_public_secjob(secjob) } ), 201

@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>', methods = ['PUT'])
def update_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    
    if not request.json:
        abort(400)
    print 'id' in request.json
    if 'id' in request.json and type(request.json['id']) != int:
        abort(400)
    
    if 'maxRunTimeInMins' in request.json and type(request.json['maxRunTimeInMins']) != int:
        abort(400)
    
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'tJobId' in request.json and type(request.json['tJobId']) != int:
        abort(400)
    if 'vulns' in request.json and type(request.json['vulns']) != list:
        abort(400)
    if 'name' in request.json['vulns'] and type(request.json['vulns']['name']) != unicode:
        abort(400)
    if 'version' in request.json['vulns'] and type(request.json['vulns']['version']) != int:
        abort(400)
    if 'vulnType' in request.json['vulns'] and type(request.json['vulns']['vulnType']) != unicode:
        abort(400)
    
    secjob[0]['maxRunTimeInMins'] = request.json.get('maxRunTimeInMins', secjob[0]['maxRunTimeInMins'])
    secjob[0]['name'] = request.json.get('name', secjob[0]['name'])
    secjob[0]['tJobId'] = request.json.get('maxRunTimeInMins', secjob[0]['maxRunTimeInMins'])
    secjob[0]['vulns'] = request.json.get('vulns', secjob[0]['vulns'])
    return jsonify( { 'secjob': make_public_secjob(secjob[0]) } )
    
@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>', methods = ['DELETE'])
def delete_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    secjobs.remove(secjob[0])
    return jsonify( { 'result': True } )

@app.route('/ess/api/'+api_version+'/tjobs/<int:tjob_id>/exec', methods = ['GET'])
def execute_tjob(tjob_id):
    if tjob_id==1:
        proc = subprocess.Popen("docker run dockernash/tjob-tomato-norm:v1", stdout=subprocess.PIPE, shell=True)
    #proc.wait()
    	(result,err) =proc.communicate()
    	proc.wait()
    	print type(result)
    	print len(result)
    	if "OK" in result:
             return jsonify( { 'result': "tJob execution successful" } )
    	else:
#TODO detech child process from parent
             return jsonify( { 'result': "tJob execution successful"})
    elif tjob_id==11:
        proc = subprocess.Popen("docker run dockernash/tjob-tomato-mal:v1", stdout=subprocess.PIPE, shell=True)
        #proc.wait()
        (result,err) =proc.communicate()
        proc.wait()
        print type(result)
        print len(result)
        if "OK" in result:
             return jsonify( { 'result': "tJob execution successful" } )
        else:
#TODO detach child process from parent
             return jsonify( { 'result': "tJob execution successful" } )
    else:
        return jsonify( { 'result': "No tJob found with the provided id" })    

@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>/exec', methods = ['GET'])
def execute_secjob(secjob_id):
    time.sleep(5)
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    if secjob[0]["id"]==1:
             return jsonify( { 'result': "Attack tJob found with id 11 (visit http://127.0.0.1/ess/api/v1.0/tjobs/11/exec for executing it)" } )
    else:
             return jsonify( { 'result': "No tJobs found for tJobId mentioned in the secJob description" })

if __name__ == '__main__':
	app.run(host=target, port=por)

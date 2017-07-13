#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

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

secjobs = [{"id": 1,"name": "secTest1","vulns": [{"vulnType": "Logical","name": "Replay Attack","version": 1}],"tJobId": "1","maxRunTimeInMins": "10"}]

def make_public_secjob(secjob):
    new_secjob = {}
    for field in secjob:
        new_secjob[field] = secjob[field]
    return new_secjob
    
@app.route('/ess/api/v1.0/secjobs', methods = ['GET'])
def get_secjobs():
    return jsonify( { 'secjobs': map(make_public_secjob, secjobs) } )

@app.route('/ess/api/v1.0/secjobs/<int:secjob_id>', methods = ['GET'])
def get_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    return jsonify( { 'secjob': make_public_secjob(secjob[0]) } )

@app.route('/ess/api/v1.0/secjobs', methods = ['POST'])
def create_secjob():
    if not request.json or not 'name' in request.json:
        abort(400)
    secjob = {
        'id': secjobs[-1]['id'] + 1,
        'title': request.json['name'],
        'vulns': request.json['vulns'],
        'tJobId': request.json['tJobId'],
        'maxRunTimeInMins': request.json['maxRunTimeInMins']
    }
    secjobs.append(secjob)
    return jsonify( { 'secjob': make_public_secjob(secjob) } ), 201

@app.route('/ess/api/v1.0/secjobs/<int:secjob_id>', methods = ['PUT'])
def update_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    secjob[0]['title'] = request.json.get('title', secjob[0]['title'])
    secjob[0]['description'] = request.json.get('description', secjob[0]['description'])
    secjob[0]['done'] = request.json.get('done', secjob[0]['done'])
    return jsonify( { 'secjob': make_public_secjob(secjob[0]) } )
    
@app.route('/ess/api/v1.0/secjobs/<int:secjob_id>', methods = ['DELETE'])
def delete_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    secjobs.remove(secjob[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)

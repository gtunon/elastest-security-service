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
import requests
import json
from requests.exceptions import ProxyError

torm_api="etm:8091" #TORM API URL in production mode
#torm_api="localhost:37000" #TORM API URL in dev mode
tormurl="http://"+torm_api+"/" #TORM API full URL
target = '0.0.0.0' #indicates in which IP address the API listens to
por = 80 #indicates the port
api_version='r4' #represents the current version of the API
zap=ZAPv2() #call to the OWAZP ZAP python API library (https://github.com/zaproxy/zaproxy/wiki/ApiPython)
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth() #for securing api calls using HTTP basic authentication

secjobs=[] #setting empty secjobs list when api starts

#To be used while implementing HTTPBasicAuth
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

#method for creating a dummy project
@app.route('/test/project/', methods = ['GET'])
def create_dummy_project():
    req=requests.Session()
    project_creation_check=req.post(tormurl+"api/project/",json={"id": 0, "name": "UnitTest TJob Project"})
    if project_creation_check.status_code==200:
        return jsonify(project_creation_check.text)
    else:
        abort(404)



#method for creating a dummy tjob
@app.route('/test/tjb/<int:project_id>/', methods = ['GET'])
def create_dummy_tjob(project_id):
    req=requests.Session()
    rqbody={
  "id": 0,
  "name": "ESS UnitTest TJob",
  "execDashboardConfig": "{\"showAllInOne\":true,\"allMetricsFields\":{\"fieldsList\":[{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_cpu_totalUsage\",\"activated\":false,\"type\":\"cpu\",\"subtype\":\"totalUsage\",\"unit\":\"percent\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_memory_usage\",\"activated\":false,\"type\":\"memory\",\"subtype\":\"usage\",\"unit\":\"percent\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_memory_maxUsage\",\"activated\":false,\"type\":\"memory\",\"subtype\":\"maxUsage\",\"unit\":\"bytes\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_blkio_read_ps\",\"activated\":false,\"type\":\"blkio\",\"subtype\":\"read_ps\",\"unit\":\"bytes\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_blkio_write_ps\",\"activated\":false,\"type\":\"blkio\",\"subtype\":\"write_ps\",\"unit\":\"bytes\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_blkio_total_ps\",\"activated\":false,\"type\":\"blkio\",\"subtype\":\"total_ps\",\"unit\":\"bytes\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_net_rxBytes_ps\",\"activated\":false,\"type\":\"net\",\"subtype\":\"rxBytes_ps\",\"unit\":\"amount/sec\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_net_rxErrors_ps\",\"activated\":false,\"type\":\"net\",\"subtype\":\"rxErrors_ps\",\"unit\":\"amount/sec\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_net_rxPackets_ps\",\"activated\":false,\"type\":\"net\",\"subtype\":\"rxPackets_ps\",\"unit\":\"amount/sec\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_net_txBytes_ps\",\"activated\":false,\"type\":\"net\",\"subtype\":\"txBytes_ps\",\"unit\":\"amount/sec\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_net_txErrors_ps\",\"activated\":false,\"type\":\"net\",\"subtype\":\"txErrors_ps\",\"unit\":\"amount/sec\"},{\"component\":\"\",\"stream\":\"et_dockbeat\",\"streamType\":\"composed_metrics\",\"name\":\"et_dockbeat_net_txPackets_ps\",\"activated\":false,\"type\":\"net\",\"subtype\":\"txPackets_ps\",\"unit\":\"amount/sec\"}]},\"allLogsTypes\":{\"logsList\":[{\"component\":\"test\",\"stream\":\"default_log\",\"streamType\":\"log\",\"name\":\"test_default_log_log\",\"activated\":true},{\"component\":\"sut\",\"stream\":\"default_log\",\"streamType\":\"log\",\"name\":\"sut_default_log_log\",\"activated\":true}]}}",
  "execDashboardConfigModel": {
    "showAllInOne": True,
    "allMetricsFields": {
      "fieldsList": [
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_cpu_totalUsage",
          "activated": False,
          "type": "cpu",
          "subtype": "totalUsage",
          "unit": "percent"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_memory_usage",
          "activated": False,
          "type": "memory",
          "subtype": "usage",
          "unit": "percent"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_memory_maxUsage",
          "activated": False,
          "type": "memory",
          "subtype": "maxUsage",
          "unit": "bytes"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_blkio_read_ps",
          "activated": False,
          "type": "blkio",
          "subtype": "read_ps",
          "unit": "bytes"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_blkio_write_ps",
          "activated": False,
          "type": "blkio",
          "subtype": "write_ps",
          "unit": "bytes"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_blkio_total_ps",
          "activated": False,
          "type": "blkio",
          "subtype": "total_ps",
          "unit": "bytes"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_net_rxBytes_ps",
          "activated": False,
          "type": "net",
          "subtype": "rxBytes_ps",
          "unit": "amount/sec"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_net_rxErrors_ps",
          "activated": False,
          "type": "net",
          "subtype": "rxErrors_ps",
          "unit": "amount/sec"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_net_rxPackets_ps",
          "activated": False,
          "type": "net",
          "subtype": "rxPackets_ps",
          "unit": "amount/sec"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_net_txBytes_ps",
          "activated": False,
          "type": "net",
          "subtype": "txBytes_ps",
          "unit": "amount/sec"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_net_txErrors_ps",
          "activated": False,
          "type": "net",
          "subtype": "txErrors_ps",
          "unit": "amount/sec"
        },
        {
          "component": "",
          "stream": "et_dockbeat",
          "streamType": "composed_metrics",
          "name": "et_dockbeat_net_txPackets_ps",
          "activated": False,
          "type": "net",
          "subtype": "txPackets_ps",
          "unit": "amount/sec"
        }
      ]
    },
    "allLogsTypes": {
      "logsList": [
        {
          "component": "test",
          "stream": "default_log",
          "streamType": "log",
          "name": "test_default_log_log",
          "activated": True
        },
        {
          "component": "sut",
          "stream": "default_log",
          "streamType": "log",
          "name": "sut_default_log_log",
          "activated": True
        }
      ]
    }
  },
  "imageName": "dockernash/test-tjob-ess",
  "project": {
    "id": int(project_id),
    "name": "UnitTest TJob Project",
    "suts": [],
    "tjobs": []
  },
  "tjobExecs": [],
  "parameters": [],
  "commands": "python tjob-request.py",
  "resultsPath": "",
  "esmServicesString": "[{\"id\":\"a1920b13-7d11-4ebc-a732-f86a108ea49c\",\"name\":\"EBS\",\"selected\":false,\"config\":{}},{\"id\":\"fe5e0531-b470-441f-9c69-721c2b4875f2\",\"name\":\"EDS\",\"selected\":false,\"config\":{}},{\"id\":\"af7947d9-258b-4dd1-b1ca-17450db25ef7\",\"name\":\"ESS\",\"selected\":false,\"config\":{}},{\"id\":\"29216b91-497c-43b7-a5c4-6613f13fa0e9\",\"name\":\"EUS\",\"selected\":false,\"config\":{\"webRtcStats\":{\"name\":\"webRtcStats\",\"type\":\"boolean\",\"label\":\"Gather WebRTC Statistics\",\"default\":false,\"value\":false}}},{\"id\":\"bab3ae67-8c1d-46ec-a940-94183a443825\",\"name\":\"EMS\",\"selected\":false,\"config\":{}}]",
  "esmServices": [
    {
      "id": "a1920b13-7d11-4ebc-a732-f86a108ea49c",
      "name": "EBS",
      "selected": False,
      "config": {}
    },
    {
      "id": "fe5e0531-b470-441f-9c69-721c2b4875f2",
      "name": "EDS",
      "selected": False,
      "config": {}
    },
    {
      "id": "af7947d9-258b-4dd1-b1ca-17450db25ef7",
      "name": "ESS",
      "selected": False,
      "config": {}
    },
    {
      "id": "29216b91-497c-43b7-a5c4-6613f13fa0e9",
      "name": "EUS",
      "selected": False,
      "config": {
        "webRtcStats": {
          "name": "webRtcStats",
          "type": "boolean",
          "label": "Gather WebRTC Statistics",
          "default": False,
          "value": False
        }
      }
    },
    {
      "id": "bab3ae67-8c1d-46ec-a940-94183a443825",
      "name": "EMS",
      "selected": False,
      "config": {}
    }
  ],
  "esmServicesChecked": 0
}
    tjob_creation_check=req.post(tormurl+"api/tjob/",json=rqbody)
    if tjob_creation_check.status_code==200:
        return jsonify(tjob_creation_check.text)
    else:
        abort(404)


#method for creating new secjob
def make_public_secjob(secjob):
    new_secjob = {}
    for field in secjob:
        new_secjob[field] = secjob[field]
    return new_secjob

@app.route('/gui/scripts.js', methods = ['GET'])
def get_scripts_gui():
    return render_template('scripts.js')

@app.route('/scripts.js', methods = ['GET'])
def get_scripts():
    return render_template('scripts.js')


@app.route('/gui/', methods = ['GET'])
def get_webgui():
    return render_template('ess.html')

@app.route('/', methods = ['GET'])
def load_gui():
    return render_template('ess.html')

@app.route('/health/', methods = ['GET'])
def get_health():
	try:
		urls=zap.core.urls
		return jsonify( {'status': "up", "context": {"message":"ZAP is Ready"}})
	except ProxyError:
		return jsonify( {'status': "down", "context": {"message":"ZAP is not Ready"}})

@app.route('/ess/api/'+api_version+'/secjobs/', methods = ['GET'])
def get_secjobs():
    return jsonify( { 'secjobs': map(make_public_secjob, secjobs) } )

@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>/', methods = ['GET'])
def get_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    return jsonify( { 'secjob': make_public_secjob(secjob[0]) } )


@app.route('/ess/api/'+api_version+'/secjobs/', methods = ['POST'])
def create_secjob():
    req=requests.Session()
    tjob_check=req.get(tormurl+"api/tjob/"+str(request.json['tJobId']))
    if tjob_check.status_code==200:
        if not request.json or not 'name' in request.json:
    	       abort(400)
        if len(secjobs)!=0:
    	    secjob = {
    		'id': secjobs[-1]['id'] + 1,
    		'name': request.json['name'],
    		'vulns': request.json['vulns'],
    		'tJobId': request.json['tJobId'],
    		'maxRunTimeInMins': request.json['maxRunTimeInMins']
    	    }
        else:
    	    secjob = {
    		'id': 1,
    		'name': request.json['name'],
    		'vulns': request.json['vulns'],
    		'tJobId': request.json['tJobId'],
    		'maxRunTimeInMins': request.json['maxRunTimeInMins']
    	    }
        secjobs.append(secjob)
        return jsonify( { 'secjob': make_public_secjob(secjob) } ), 201
    elif tjob_check.status_code==400:
        abort(404)

@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>/', methods = ['PUT'])
def update_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)

    if not request.json:
        abort(400)
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

@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>/', methods = ['DELETE'])
def delete_secjob(secjob_id):
    secjob = filter(lambda t: t['id'] == secjob_id, secjobs)
    if len(secjob) == 0:
        abort(404)
    secjobs.remove(secjob[0])
    return jsonify( { 'result': True } )

@app.route('/ess/api/'+api_version+'/tjobs/<int:tjob_id>/exec/', methods = ['GET'])
def execute_tjob(tjob_id):
	payload={"tJobParams": []}
	req=requests.Session()
	tjob_check=req.get(tormurl+"api/tjob/"+str(tjob_id))
	if tjob_check.status_code==200:
		r= req.post("http://"+torm_api+"/api/tjob/"+str(tjob_id)+"/exec", json=payload)

		if "IN PROGRESS" in str(json.loads(r.text)["result"]):
			return jsonify( {'result': "IN PROGRESS","instance":str(json.loads(r.text)["id"])})
		else:
			return jsonify( {'result': "FAILED","instance":"", "message":"TJob execution could not start"})
	elif tjob_check.status_code==400:
		return jsonify( {'result': "FAILED","instance":"", "message":"No tjob found with the entered tjob id"})

@app.route('/ess/api/'+api_version+'/tjobs/<int:tjob_id>/exec/<instance>/', methods = ['GET'])
def get_tjob_exec_inst(tjob_id,instance):
	s=requests.Session()
	exec_resp=s.get(tormurl+"api/tjob/"+str(tjob_id)+"/exec/"+str(instance))
	if len(exec_resp.text)!=0:
		print(instance)
		print(str(json.loads(exec_resp.text)["result"]))
		return jsonify( {'result': str(json.loads(exec_resp.text)["result"])})
	else:
		return jsonify( {'result': "FAILED"})

@app.route('/ess/api/'+api_version+'/secjobs/<int:secjob_id>/exec/', methods = ['GET'])
def execute_secjob(secjob_id):
#Logic for insec URLs
    all_tjob_urls=list(set(zap.core.urls()))
    insecure_urls=[]
    insecure_cookies=[]
    for url in all_tjob_urls:
    	if not url.startswith("https"):
    		insecure_urls.append(url)
#Logic for insec URLs
    all_tjob_messages=zap.core.messages()
    urls=[]
    results=[]
    resulthttponly={"url":"","method":"","inseccookies":[]}
    cookies=[]
    insecure_cookies=[]
    inSecureFlag=None
    nonHttpOnlyFlag=None
    nonSameSiteFlag=None
    for message in all_tjob_messages:
    	result={"url":"","method":"","allcookies":[], "insecurecookies":[], "nonhttponlycookies":[], "nonsamesitecookies":[]}
    	if message["requestHeader"].split()[1].startswith("https"):
            result["method"]=message["requestHeader"].split()[0]
            result["url"]=message["requestHeader"].split()[1]
            for field in message["responseHeader"].split("\r\n"):
                if(field.startswith("Set-Cookie")):
                    result["allcookies"].append(field.lstrip("Set-Cookie: ").split(";")[0])
                    inSecureFlag=False
                    nonHttpOnlyFlag=False
                    nonSameSiteFlag=False
                    for attributes in field.lstrip("Set-Cookie: ").split(";"):
                    	if attributes.strip().lower().startswith("secure"):
                    		inSecureFlag=True
                    	if attributes.strip().lower().startswith("httponly"):
                    		nonHttpOnlyFlag=True
                    	if attributes.strip().lower().startswith("samesite"):
                    		nonSameSiteFlag=True
                    if inSecureFlag==False:
                    	result["insecurecookies"].append(field.lstrip("Set-Cookie:").strip().split(";")[0])
                    if nonHttpOnlyFlag==False:
                    	result["nonhttponlycookies"].append(field.lstrip("Set-Cookie:").strip().split(";")[0])
                    if nonSameSiteFlag==False:
                    	result["nonsamesitecookies"].append(field.lstrip("Set-Cookie:").strip().split(";")[0])
    	if len(result["insecurecookies"])!=0 or len(result["nonhttponlycookies"])!=0 or len(result["nonsamesitecookies"])!=0:
    		results.append(result.copy())
    return jsonify({"insecurls":insecure_urls,"inseccookieinfo":results})

#Start Sipder Scan with ZAP
@app.route('/ess/api/'+api_version+'/startspider/', methods = ['POST'])
def start_spider():
    scan_url=str(request.json['url'])
    try:
        zap.urlopen(scan_url)
        time.sleep(2)
        zap.spider.scan(scan_url)
        return jsonify( { 'status': "Started Spidering" } )
    except:
        return jsonify( { 'status': "ZAP Exception" } )


#Start Active Scan with ZAP
@app.route('/ess/api/'+api_version+'/startascan/', methods = ['POST'])
def start_ascan():
    scan_url=str(request.json['url'])
    try:
        time.sleep(5)
        zap.ascan.scan(scan_url)
        return jsonify( { 'status': "Started Active Scanning" } )
    except:
        return jsonify( { 'status': "ZAP Exception" } )

#Check spider scan progress of ZAP
@app.route('/ess/api/'+api_version+'/zap/getstatus/spider/', methods = ['GET'])
def get_status_spider():
    try:
        return jsonify( { 'status': zap.spider.status() } )
    except:
        return jsonify( { 'status': "ZAP Exception" } )

#Check active scan progress of ZAP
@app.route('/ess/api/'+api_version+'/zap/getstatus/ascan/', methods = ['GET'])
def get_status_ascan():
    try:
        return jsonify( { 'status': zap.ascan.status() } )
    except:
        return jsonify( { 'status': "ZAP Exception" } )

#Get Active Scan Report from ZAP
@app.route('/ess/api/'+api_version+'/zap/getscanresults/', methods = ['GET'])
def get_scan_report():
    try:
        return jsonify( { 'status': "Started Active Scanning","report":zap.core.alerts() } )
    except:
        return jsonify( { 'status': "ZAP Exception" } )

def isZapReady():
	zap=ZAPv2()
	try:
		urls=zap.core.urls
		return "Ready"
	except ProxyError:
		return "NotReady"

if __name__ == '__main__':
	sleeps=[10,10,10,10,10]
	ready=False
	for slp in sleeps:
		if isZapReady()=="Ready":
			ready=True
			break
		else:
			time.sleep(slp)
	if ready==True:
		app.run(host=target, port=por)

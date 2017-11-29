import unittest
import requests
import os
import sys

def e2etests():
	tormurl=sys.argv[1]
	print tormurl
	#proxyurl="http://" + "localhost" + ":8080/"
	
	#def test_send_request(self):
	#	s=requests.Session()
	#	response=s.get(tormurl)
	#	assert "ElasTest Torm" in response.text
		
if __name__=="__main__":
	e2etests()	

import pprint
import requests
import os
import sys

#function that calls all other tests
def e2etests():
	tormurl=sys.argv[1]
	#To check whether the TORM URL has been read correctly	
	print "TORM URL is: "+tormurl
	#To check whether the TORM preloader page can successfully retrieved
	tests=["test_load_torm_home_preloader(tormurl)","test_load_torm_api_info(tormurl+\"/api/context/services/info\")","test_create_new_project(tormurl+\"/api/project\")"]	
	numtests=len(tests)
	testssuccess=0
	testsfailed=0	
	testsrun=0
	testsleft=numtests

	if numtests!=0:
		for i in range(len(tests)):
			testsrun+=1
			print "~~~~~~~~~~~~~~~"
			print "Running test "+str(testsrun)+" out of "+str(testsleft)
			status=eval(tests[i])
			if status=="success":
				testssuccess+=1
				print "Status: Success"
			if status=="failed":
				testsfailed+=1
				print "Status: Failed"
			
	print "##############"
	print "_TESTS SUMMARY_"
	print "TOTAL TESTS RAN: "+str(testsrun)
	print "TOTAL TESTS SUCCEEDED: "+str(testssuccess)
	print "TOTAL TESTS FAILED: "+str(testsfailed)
	#status=test_load_torm_api_info(tormurl+"api/context/services/info") 

def test_load_torm_home_preloader(tormurl):
		s=requests.Session()
		r = s.get(tormurl)
		print(r.text)
		try:
			assert "Loading ElasTest..." in r.text
		except AssertionError:
		        print "Test to load TORM home page prealoader failed"
			return "failed"
		return "success"

def test_load_torm_api_info(tormapiinfourl):
		s=requests.Session()
		r = s.get(tormapiinfourl)
		print(r.text)
		try:
			assert "elasticSearchUrl" in r.text
		except AssertionError:
		        print "Call to load elasticSearchUrl failed"
			return "failed"
		return "success"

def test_create_new_project(tormapicreateprojecturl):
		s=requests.Session()
		payload={"id": 0,"name": "E2E test ESS"}
		r = s.post(tormapicreateprojecturl,json=payload)
		print(r.text)
		try:
			assert "E2E test ESS" in r.text
		except AssertionError:
		        print "New Project creation"
			return "failed"
		return "success"

		
if __name__=="__main__":
	e2etests()	

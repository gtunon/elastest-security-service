##############################
# Author: Avinash Sudhodanan #
##############################
from selenium import webdriver
import pprint
import os
import sys
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#function that calls all other tests
projectId=0
tjobId=0
essip=""
def e2etests():
	tormurl=sys.argv[1]
	#To check whether the TORM URL has been read correctly
	if tormurl[-1]!='/':
		tormurl=tormurl+'/'

	print("TORM URL is: "+tormurl)
	#List of all the tests to be run. Append to this list the new tests
	#tests=["test_load_torm_home_preloader(tormurl,driver)","test_load_torm_home_full(tormurl+\"/api/context/services/info\",driver)","test_service_launch(tormurl,driver)","test_create_new_project(tormurl+\"/api/project\",driver)","test_create_new_tjob(tormurl+\"/api/tjob\")","test_run_tjob(tormurl,driver)"]
	tests=["test_load_torm_homepage(tormurl,driver)","test_service_launch(tormurl,driver)","test_zap_active_scan(tormurl,driver)"]
	#setup Chrome WebDriver
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('--no-sandbox')
	#driver = webdriver.Firefox() #for testing with GUI locally
	driver = webdriver.Chrome(chrome_options=options)

	numtests=len(tests)
	testssuccess=0
	testsfailed=0
	testsrun=0
	testsleft=numtests
	#Check if the number of tests is empty
	if numtests!=0:
		#Iterate through each test in the list of tests
		for i in range(len(tests)):
			testsrun+=1
			print("~~~~~~~~~~~~~~~")
			print("Running test "+str(testsrun)+" out of "+str(testsleft))
			status=eval(tests[i])
			#Check if the last test executed successfully.
			if status=="success":
				testssuccess+=1
				print("Status: Success")
			if status=="failed":
				testsfailed+=1
				print("Status: Failed")
				#A failed test will prevent the execution of future tests. This behavior is debatable.
				break
	driver.close()
	print("##############")
	print("_TESTS SUMMARY_")
	print("TOTAL TESTS RAN: "+str(testsrun))
	print("TOTAL TESTS SUCCEEDED: "+str(testssuccess))
	print("TOTAL TESTS FAILED: "+str(testsfailed))

# Function to check whether the TORM preloader page can successfully retrieved
def test_load_torm_homepage(tormurl,driver):
		driver.get(tormurl)
		try:
			element = WebDriverWait(driver, 240).until(
				EC.presence_of_element_located((By.ID, "nav_support_services"))
			)
			print("\ta. TORM home page preloader loaded successfully")
		except:
			print("\ta. Test to load TORM home page prealoader failed")
			return "failed"
		return "success"


#Launch ESS service
def test_service_launch(tormurl,driver):
		try:
			driver.get(tormurl+"#/support-services")
			time.sleep(10)
			print("\ta. Loaded TSS page")
			element = driver.find_element_by_class_name("mat-select-trigger")
			element.click()
			print("\tb. Clicked TSS Options")
			options = driver.find_elements_by_tag_name("md-option")
			for option in options:
				if option.text=="ESS":
					option.click()
					print("\tc. Selected ESS from the list of TSSes")
			element=driver.find_element_by_id("create_instance")
			element.click()
			print("\td. Initiated ESS launch")
			element = WebDriverWait(driver, 540).until(
		        EC.visibility_of_element_located((By.ID, "view_service"))
		    )
			element.click()
			print("\te. ESS launch successful")
		except:
			print("Failed to click Test Support Services Tab because: "+str(sys.exc_info()[0]))
			return "failed"
		return "success"

# Function to test the scanning feature
def test_zap_active_scan(tormurl,driver):
		try:
			element = driver.find_element_by_xpath("/html/body/etm-app/etm-etm/td-layout-nav/div/div/td-layout-manage-list/md-sidenav-container/div[4]/div/div/esm-service-detail/div/div/md-card/md-card-content/div[1]/md-list/div[1]/md-list-item[1]/div/a")
			driver.get(element.text)
			print("\ta. ESS GUI loaded successfully")
			element = driver.find_element_by_id("scan-url")
			element.send_keys("http://example.com")
			print("\tb. Entered example.com URL")
			element = driver.find_element_by_id("start-scan")
			element.click()
			print("\tc. Started scanning example.com")
			element = WebDriverWait(driver, 540).until(
		        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/ul/li[3]/div[2]/ul/ul/li[1]/div[1]/i"))
		    )
			print("\td. Scanned example.com and generated report")
		except:
			print("Scanning of http://example.com failed")
			return "failed"
		return "success"
"""
# Function to make REST API calls to create a project in TORM
def test_create_new_project(tormapicreateprojecturl,driver):

# Create a new tjob as part of a project
def test_create_new_tjob(tormapicreatetjoburl,driver):

# Function to test the running of the tjob
def test_run_tjob(tormurl,driver):
"""
if __name__=="__main__":
	e2etests()

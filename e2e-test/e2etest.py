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
	tests=["test_load_torm_homepage(tormurl,driver)","test_create_exec_tjob(tormurl,driver)"]
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
				print("Test Status: Success")
			if status=="failed":
				testsfailed+=1
				print("Test Status: Failed")
				#A failed test will prevent the execution of future tests. This behavior is debatable.
				break
	#driver.close()
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

def test_create_exec_tjob(tormurl,driver):
		try:
			element = driver.find_element(By.XPATH, '/html/body/etm-app/etm-etm/td-layout-nav/div/div/td-layout-manage-list/md-sidenav-container/div[4]/div/div/app-tjob-execs-manager/etm-projects-manager/div/div/div/md-card/md-card-content/td-data-table/div/table/tbody/tr/td[2]/div')
			element.click()
			print("\ta. Hello World Project Clicked")
		except:
			print("\tERROR:: Hello World Project Click failed because ")
			return "failed"

		try:
			element = driver.find_element(By.XPATH, '//*[@id="tJobs"]/div/table/tbody/tr/td[7]/div/button[2]/span/md-icon')
			element.click()
			print("\ta. Hello World TJob Edit Button Clicked")
		except:
			print("\tERROR:: Hello World TJob Edit Button Click failed because "+E)
			return "failed"
		time.sleep(10)
		try:
			element = driver.find_element(By.ID, 'md-input-3')
			element.clear()
			print("\tb. Hello World TJob Results Path Cleared")
		except:
			print("\tERROR:: Hello World TJob Results Path Clearing failed")
			return "failed"

		try:
			element = driver.find_element(By.ID, 'md-input-5')
			element.clear()
			print("\tc. Hello World TJob Docker Image Cleared")
		except:
			print("\tERROR:: Hello World TJob Docker Image Clearing failed")
			return "failed"

		try:
			element.send_keys("dockernash/test-tjob-ess")
			print("\td. ESS Test TJob Docke Image Set")
		except:
			print("\tERROR:: ESS Test TJob Docke Image Setting failed")
			return "failed"

		try:
			element = driver.find_element(By.ID, 'commands')
			element.clear()
			print("\te. Hello World TJob Commands Cleared")
		except:
			print("\tERROR:: Hello World TJob Commands Clearing failed")
			return "failed"

		try:
			element.send_keys("python fteaching-tjob.py example")
			print("\tf. ESS Test TJob Commands Set")
		except:
			print("\tERROR:: ESS Test TJob Commands Setting failed")
			return "failed"

		try:
			element = driver.find_element(By.XPATH, '/html/body/etm-app/etm-etm/td-layout-nav/div/div/td-layout-manage-list/md-sidenav-container/div[4]/div/div/etm-tjob-form/md-card/md-card-content/form/td-expansion-panel[2]/div[2]/div/div[3]/div/md-checkbox/label/div')
			element.click()
			print("\tg. Set ESS as TSS for the Test Tjob")
		except:
			print("\tERROR:: Setting ESS as TSS for the Test Tjob failed")
			return "failed"

		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/etm-tjob-form/md-card/md-card-actions/button[1]/span')
			element.click()
			print("\th. Saved the Test Tjob")
		except:
			print("\tERROR:: Attempt to Saved the Test Tjob failed")
			return "failed"
		time.sleep(10)
		try:
			element = driver.find_element(By.XPATH, '/html/body/etm-app/etm-etm/td-layout-nav/div/div/td-layout-manage-list/md-sidenav-container/div[4]/div/div/etm-project-manager/div[2]/div[1]/etm-tjobs-manager/md-card/md-card-content/td-data-table/div/table/tbody/tr/td[7]/div/button[1]')
			element.click()
			print("\ti. Launched the Test Tjob")
		except:
			print("\tERROR:: Launching the Test Tjob failed")
			return "failed"
		time.sleep(10)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="resultMsgText"]')
			while(element.text!="Executing Test" or element.text!="Failed" or element.text!="Finish"):
				print("\tWaiting for tjob execution to complete")
		except:
			print("\tERROR:: Could not fetch the status of tjob execution")
			return "failed"


		return "success"
if __name__=="__main__":
	e2etests()

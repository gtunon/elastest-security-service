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
	#tests=["test_load_torm_homepage(tormurl,driver)","test_create_exec_tjob(tormurl,driver)"]
	tests=["test_load_torm_homepage(tormurl,driver)"]
	
	#Guio: Use an if. If not you won't be able to execute externaly to ElasTest
	if eusUrl!=null:
		print("EUS URL is: "+str(eusUrl))
		driver = webdriver.Remote(command_executor=eusUrl, desired_capabilities=capabilities)
	
	else:
	#	driver = webdriver.Firefox() #for testing with GUI locally
	#	or...
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
			print("\tERROR: Test to load TORM home page prealoader failed")
			return "failed"
		return "success"

def test_create_exec_tjob(tormurl,driver):
		time.sleep(4)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="projects"]/div/table/tbody/tr[7]/td[2]/div')
			element.click()
			print("\tb. ESS Demo Project Clicked")
		except:
			print("\tERROR:: ESS Demo Project Click failed because ")
			return "failed"
		time.sleep(4)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="newTJobBtn"]/span')
			element.click()
			print("\tc. New TJob Creation Button Clicked")
		except:
			print("\tERROR:: New TJob Creation Button Click failed")
			return "failed"
		time.sleep(4)

		try:
			element = driver.find_element(By.XPATH, '//*[@id="md-input-1"]')
			element.send_keys("ESS Demo TJob")
			print("\td. ESS Demo TJob Name Set")
		except:
			print("\tERROR:: ESS Demo TJob Name Setting Failed")
			return "failed"

		try:
			element = driver.find_element(By.ID, 'md-input-3')
			element.clear()
			print("\te. ESS Demo TJob Results Path Cleared")
		except:
			print("\tERROR:: ESS Demo TJob Results Path Clearing failed")
			return "failed"

		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/etm-tjob-form/md-card/md-card-content/form/div[1]/div/md-select/div')
			element.click()
			element = driver.find_element(By.XPATH, '//*[@id="md-option-0"]')
			element.click()
			print("\tf. SuT setting to None")
		except:
			print("\tERROR:: SUT setting to None failed")
			return "failed"
		try:
			element = driver.find_element(By.ID, 'md-input-5')
			element.clear()
			print("\tg. ESS Demo TJob Docker Image Cleared")
		except:
			print("\tERROR:: ESS Demo TJob Docker Image Clearing failed")
			return "failed"

		try:
			element.send_keys("dockernash/test-tjob-ess")
			print("\th. ESS Test TJob Docke Image Set")
		except:
			print("\tERROR:: ESS Test TJob Docker Image Setting failed")
			return "failed"

		try:
			element = driver.find_element(By.ID, 'commands')
			element.clear()
			print("\ti. ESS Demo TJob Commands Cleared")
		except:
			print("\tERROR:: ESS Demo TJob Commands Clearing failed")
			return "failed"

		try:
			element.send_keys("python fteaching-tjob.py example")
			print("\tj. ESS Test TJob Commands Set")
		except:
			print("\tERROR:: ESS Test TJob Commands Setting failed")
			return "failed"

		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/etm-tjob-form/md-card/md-card-content/form/td-expansion-panel[2]/div[2]/div/div[4]/div/md-checkbox')
			element.click()
			print("\tk. Set ESS as TSS for the Test Tjob")
		except:
			print("\tERROR:: Setting ESS as TSS for the Test Tjob failed")
			return "failed"
		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/etm-tjob-form/md-card/md-card-content/form/td-expansion-panel[2]/div[2]/div/div[5]/div/md-checkbox')
			element.click()
			print("\tl. Set EUS as TSS for the Test Tjob")
		except:
			print("\tERROR:: Setting EUS as TSS for the Test Tjob failed")
			return "failed"
		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/etm-tjob-form/md-card/md-card-actions/button[1]/span')
			element.click()
			print("\tm. Saved the Test Tjob")
		except:
			print("\tERROR:: Attempt to Saved the Test Tjob failed")
			return "failed"
		time.sleep(4)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="tJobs"]/div/table/tbody/tr/td[8]/div/button[1]/span/md-icon')
			element.click()
			print("\tn. Launched the Test Tjob")
		except:
			print("\tERROR:: Launching the Test Tjob failed")
			return "failed"
		time.sleep(4)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="resultMsgText"]')
			printed=True
			while(element.text!="Executing Test" or element.text!="Failed" or element.text!="Finish"):
				if(printed==True):
					print("\to. Waiting for tjob execution to complete")
					printed=False
				else:
					continue
		except:
			print("\tp. TJob Execution must have finished")
		time.sleep(4)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/etm-tjob-exec-view/etm-tjob-exec-manager/div/div/md-card/md-card-title/div/a/span[2]')
			element.click()
			print("\tq. Selecting Finished TJob succeeded")
		except:
			print("\tERROR: Selecting TJob failed")
			return "failed"
		try:
			element = driver.find_element(By.XPATH, '//*[@id="menusideLeft"]/md-sidenav-container/div[4]/div/div/app-tjob-manager/auto-height-grid/normal-height-row/div/md-card/md-card-content/div/span[5]/div/button[3]/span/md-icon')
			element.click()
			print("\tr. Clicking Delete Button of Finished TJob Succeeded")
		except:
			print("\tERROR: Clicking Delete Button of Finished TJob Failed")
			return "failed"
		time.sleep(10)
		try:
			element = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-5"]/md-dialog-container/td-confirm-dialog/td-dialog/div/div[2]/td-dialog-actions/button[2]/span')
			element.click()
			print("\ts. Clicking Delete Confirmation Button Succeeded")
		except:
			print("\tERROR: Clicking Delete Confirmation Button Failed")
			print("Unexpected error:", sys.exc_info()[0])

		try:
			element = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-4"]/md-dialog-container/td-confirm-dialog/td-dialog/div/div[2]/td-dialog-actions/button[2]/span')
			element.click()
			print("\ts. Clicking Delete Confirmation Button Succeeded")
		except:
			print("\tERROR: Clicking Delete Confirmation Button Failed")
			print("Unexpected error:", sys.exc_info()[0])

		try:
			element = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-3"]/md-dialog-container/td-confirm-dialog/td-dialog/div/div[2]/td-dialog-actions/button[2]/span')
			element.click()
			print("\ts. Clicking Delete Confirmation Button Succeeded")
		except:
			print("\tERROR: Clicking Delete Confirmation Button Failed")
			print("Unexpected error:", sys.exc_info()[0])

		try:
			element = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-2"]/md-dialog-container/td-confirm-dialog/td-dialog/div/div[2]/td-dialog-actions/button[2]/span')
			element.click()
			print("\ts. Clicking Delete Confirmation Button Succeeded")
		except:
			print("\tERROR: Clicking Delete Confirmation Button Failed")
			print("Unexpected error:", sys.exc_info()[0])

		try:
			element = driver.find_element(By.XPATH, '//*[@id="cdk-overlay-1"]/md-dialog-container/td-confirm-dialog/td-dialog/div/div[2]/td-dialog-actions/button[2]/span')
			element.click()
			print("\ts. Clicking Delete Confirmation Button Succeeded")
		except:
			print("\tERROR: Clicking Delete Confirmation Button Failed")
			print("Unexpected error:", sys.exc_info()[0])

		time.sleep(50)
		return "success"

if __name__=="__main__":
	e2etests()

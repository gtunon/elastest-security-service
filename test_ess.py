import unittest
import ess

api_version='r3'
class TestESS(unittest.TestCase):

    def setUp(self):
        ess.app.testing = True
        self.app = ess.app.test_client()
    def test_get_password(self):
        with ess.app.app_context():
            self.assertEqual(ess.get_password('miguel'),'python')
            self.assertEqual(ess.get_password('avinash'),None)

    def test_get_scripts_gui(self):
        with ess.app.app_context():
            rv = self.app.get('/gui/scripts.js')
            self.assertTrue("ElasTest ESS GUI JavaScript File" in rv.data)

    def test_get_scripts(self):
        with ess.app.app_context():
            rv = self.app.get('/scripts.js')
            self.assertTrue("ElasTest ESS GUI JavaScript File" in rv.data)

    def test_get_webgui(self):
        with ess.app.app_context():
            rv = self.app.get('/gui/')
            self.assertTrue("ElasTest Security Service" in rv.data)

    def test_load_gui(self):
        with ess.app.app_context():
            rv = self.app.get('/')
            self.assertTrue("ElasTest Security Service" in rv.data)

    def test_get_health(self):
        with ess.app.app_context():
            rv = self.app.get('/health/')
            self.assertTrue("ZAP is Ready" in rv.data)


    def test_isZapReady(self):
        with ess.app.app_context():
            self.assertEqual(ess.isZapReady(),'Ready')
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_create_dummy_project(self):
        with ess.app.app_context():
            rv = self.app.get('/test/project/')
            print rv.data
            #self.assertTrue("ElasTest Security Service" in rv.data)
"""
    def test_create_secjob(self):
        with ess.app.app_context():
            rv = self.app.post('/ess/api/'+api_version+'/secjobs/',data={
    		'id': 0,
    		'name': "UnitTest SecJob",
    		'vulns': [],
    		'tJobId': "1",
    		'maxRunTimeInMins': 10
    	    })
            print rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_get_secjobs():
        api_version='r3'
        with ess.app.app_context():
            rv = self.app.get('/ess/api/'+api_version+'/secjobs/')
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_get_secjob(secjob_id):
        with ess.app.app_context():
            rv = self.app.get('')
            rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)


    def test_execute_tjob(tjob_id):
        with ess.app.app_context():
            rv = self.app.get('')
            rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_get_tjob_exec_inst(tjob_id,instance):
        with ess.app.app_context():
            rv = self.app.get('')
            rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_execute_secjob(secjob_id):
        with ess.app.app_context():
            rv = self.app.get('')
            rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_update_secjob(secjob_id):
        with ess.app.app_context():
            rv = self.app.get('')
            rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)

    def test_delete_secjob(secjob_id):
        with ess.app.app_context():
            rv = self.app.get('')
            rv.data
            #self.assertTrue("ZAP is Ready" in rv.data)
"""
if __name__=="__main__":
    unittest.main()

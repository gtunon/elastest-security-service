node('docker') {
    stage "Container Prep"
        echo("The node is up")
        def mycontainer = docker.image('elastest/ci-docker-compose-py-siblings:latest')
        mycontainer.pull()
        mycontainer.inside("-u jenkins -v /var/run/docker.sock:/var/run/docker.sock:rw") {
            git 'https://github.com/elastest/elastest-security-service'

	     stage "prepare tests"
     		pip install flask
		pip install flask-httpauth
		pip install coverage
		pip install python-owasp-zap-v2.4

            stage "Tests"
                echo ("Starting tests")
		sh 'coverage run test_ess.py'

            stage "Build image - Package"
                echo ("Building")
                def myimage = docker.build 'elastest/ess:latest'

            stage "Run image"
                myimage.run()

            stage "Publish"
                echo ("Publishing")
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'elastestci-dockerhub',
                    usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
                    sh 'docker login -u "$USERNAME" -p "$PASSWORD"'
                    myimage.push()
                }

	    stage "Cobertura"
                def codecovArgs = "-v -t $COB_ESS_TOKEN"
                echo "$codecovArgs"                
                def exitCode = sh(
                    returnStatus: true,
                    script: "curl -s https://codecov.io/bash | bash -s - $codecovArgs")
                    if (exitCode != 0) {
                        echo( exitCode +': Failed to upload code coverage to codecov')
                    }
        }
}

# ElasTest Security Service (ESS)

The ElasTest Security Service (ESS) is an ElasTest service for identifying security issues in the System Under Test (SuT) by analyzing the HTTP traffic of the SuT. ESS creates security tests (that mimics attacker's behavior) from the HTTP traffic generated as a result of the tJobs associated to a SuT. These security tests represent malicious attacker behaviors such as modifying URL parameters, replaying requests [and much more](https://pdfs.semanticscholar.org/270c/cf24e8be8421515f5121600f248e841f424d.pdf?_ga=2.125276362.151869347.1515086898-1552517986.1515086898).

## Features
The current version of ESS (v0.5.0) has the following features.
- A web-based GUI for creating security jobs for detecting security vulnerabilties from tJobs defined in [ElasTest TORM](https://github.com/elastest/elastest-torm)
- Detect the insecure http connection involved in tJobs that are not protected with SSL/TLS
- Detect cookies that can be stolen using [SSL Stripping attacks](https://paladion.net/ssl-stripping-revisiting-http-downgrading-attacks/)
- Detect cookies that can be stolen using the [Cross-Site Scripting attack](https://en.wikipedia.org/wiki/Cross-site_scripting)
- Detect cookies that facilitates [Cross-Site Request Forgery attacks](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

The future versions of the ESS is expected to support the detection of the following types of vulnerabilities/attacks:
- Logical vulnerability
- Denial-of-Service
- Improper/Missing authentication

## How to run

ESS can be launched from the ElasTest TORM web-ui. The steps for doing it is as follows.
1. From the side panel of the web-ui of TORM, click the _Test Support Services_ option, select ESS from the dropdown list of services and clicking the _Create Instance_ button. Then, wait until the ESS instance has been completely launched (meaning the circular spinner that appeared under the _Options_ column of the launched instance stopped spinning).
2. Click the icon with the shape of an eye corresponding to the _View Service Detail Option_. From the displayed details, scroll down to see the web-ui of ESS. Alternately, the ESS web-ui can be viewed in another tab by clicking on the link corresponding to the option _URL gui:_. For instance, if the value of _URL gui:_ is http://172.18.0.12:80/gui/, either click this link or load the URL http://172.18.0.12:80/gui/ in a new tab.

## Basic usage
###Creating a tJob that proxies through ESS
For analyzing a tJob through ESS, all HTTP communications of the tJob must pass through the Man-in-the-Middle (MitM in short) proxy service of the ESS. Currently the ESS makes use of the [OWASP ZAP](https://github.com/zaproxy/zaproxy) and [MITM proxy](https://mitmproxy.org/) for this purpose. An example of how to create such a tJob is explained below.
1. Write a program that makes HTTP connections through an IP address provided as a run-time argument. A proxy server must be listening at this IP address at port 8080. An example of such a script is provided [here](https://github.com/avinash-sudhodanan/sample-ess-tjob/blob/master/tjob-request.py).
2. Create a docker container with the above mentioned program and the required libraries. Make available this container in a public/private docker repository. For instance, container we created for the program shown [here](https://github.com/avinash-sudhodanan/sample-ess-tjob/blob/master/tjob-request.py) is [hosted at docker hub] (https://hub.docker.com/r/dockernash/sample-ess-tjob/).
3. From ElasTest, launch an instance of ESS. If an ESS instance has already been launched, read the next point, otherwise continue reading. An ESS instance can be launched by visiting the ElasTest home page in a web browser, clicking the _Test Support Services_ option from the side panel, selecting ESS from the dropdown list of services and clicking the _Create Instance_ button.
4. After an instance of ESS has been completely launch (meaning the circular spinner that appeared under the _Options_ column of the launched instance), click the icon with the shape of an eye corresponding to the _View Service Detail Option_. From the displayed details, note down the IP address of the running ESS instance which is mentioned corresponding to _URL gui:_. For instance, if the value of _URL gui:_ is http://172.18.0.12:80/gui/, then the IP address of ESS is _172.18.0.12_.
5. Click on the option _Project_ from the side-panel of TORM and create a new project. 
6. After creating the project, create a tJob under it with the following values for the corresponding fields 
+__TJob Name__: Any value,
+__Select a SuT__: None,
+__Environment docker image__: _dockernash/sample-ess-tjob_,
+__Commands__: _python tjob-request.py_ <IP Address of the launched ESS instance>
and click the _SAVE_ button. In the page that appears after clicking the _SAVE_ button, note the id of the newly-created tJob.

###Analysing a tJob using ESS
To analyse a previously-created tJob using ESS, following the steps below.
1. Visit the URL of the gui of ESS (see section __How to run__ for details).
2. Click on the option _Create New SecJob_, provide a desired secJob name, the id of the newly-created tjob, an optional description and click on the _CREATE_ button.
3. If the secJob creation has been successful, an unobtrusive alert saying "SecJob Creation Successful" should appear.
4. Now click on the _View & Execute SecJobs_ option from the web-gui where a summary of the recently-created secJob (see previous step) will be displayed. On the right side of this summary, there should be an option to run the secJob. Click on it.
5. Upon clicking the run button, you should see two progress bars indicating the secJob execution status. The first progress bar corresponds to the status of the automatic execution of the tJob by the ESS. After the successful execution of the tJob, the second progress bar will display the status of the analysis of the HTTP traffic generated as a result of the tJob execution by the ESS. After the analysis is completed, the results of the analysis will be available. The results are explained below.
6. The first result is that of the insecure URLs involved in the tJob execution that are not protected with [SSL/TLS](https://en.wikipedia.org/wiki/HTTPS). 
7. The second result indicates the details of the cookies involved in the tJob execution that are set over the _https_-protected channel but without using the [_secure_ attribute](https://en.wikipedia.org/wiki/Secure_cookies). Cookies set in this way ar einsecure and can be stolen by an attacker through protocol downgrade attacks such as [SSL-stripping](https://paladion.net/ssl-stripping-revisiting-http-downgrading-attacks/). 
8. The third result indicates the details of cookies set without the [HttpOnly](https://en.wikipedia.org/wiki/HTTP_cookie#HttpOnly_cookie) attribute. Cookies set in this way can be stolen by an attacker if there is a [cross-site scripting](https://en.wikipedia.org/wiki/Cross-site_scripting) vulnerability in the web site associated to the cookie. Cross-Site Scripting is one of the the [most common web applications vulnerabilities](https://www.owasp.org/images/7/72/OWASP_Top_10-2017_%28en%29.pdf.pdf).
9. The fourth result provides the details of the Cookies set without the [_SameSite_](https://en.wikipedia.org/wiki/HTTP_cookie#SameSite_cookie) attribute facilitates [cross-site request forgery attacks](https://en.wikipedia.org/wiki/Cross-site_request_forgery). Although the _SameSite_ attribute has been introduced recently, it is an important future direction to prevent cross-site request forgery attacks. Another reason why ESS performs this check is to spread awareness about this new cookie attribute that aims to secure the web.

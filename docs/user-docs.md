# ElasTest Security Service (ESS)

The ElasTest Security Service (ESS) is an ElasTest service for identifying security vulnerabilities in Web applications. ESS creates security tests that mimics the behavior of malicious users to probe a Web application to discover vulnerabilities. ESS is based on [OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project), a prominent open source web vulnerability scanner. ESS not only supports the detection of the common web application vulnerabilities such as cross-site scripting, SQL injection etc., but also [replay attacks](https://pdfs.semanticscholar.org/270c/cf24e8be8421515f5121600f248e841f424d.pdf?_ga=2.125276362.151869347.1515086898-1552517986.1515086898) and cross-site script inclusion.

## Features
The current version of ESS (v0.5.0) has the following features.
1. A web-based GUI for providing the details of the Web application under test
2. Support for detecting [common Web application security weaknesses](https://www.owasp.org/index.php/Top_10-2017_Top_10)
2. Supports the detection of insecure cookies that (1) can be stolen using [SSL Stripping attacks](https://paladion.net/ssl-stripping-revisiting-http-downgrading-attacks/), (2) can be stolen using [Cross-Site Scripting attacks](https://en.wikipedia.org/wiki/Cross-site_scripting), (3) facilitates [Cross-Site Request Forgery attacks](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

The future releases of ESS will support the detection of:
1. Vulnerabilities enabling cross-site sctipt inclusion attacks
2. Vulnerabilities enabling replay attacks

## How to launch ESS

ESS can be launched from the ElasTest TORM web-ui. The steps for doing it is as follows.
1. From the side panel of the web-ui of TORM, click the _Test Support Services_ option, select ESS from the dropdown list of services and clicking the _Create Instance_ button. Then, wait until the ESS instance has been completely launched (meaning the circular spinner that appeared under the _Options_ column of the launched instance stopped spinning).
2. Click the icon with the shape of an eye corresponding to the _View Service Detail Option_. From the displayed details, scroll down to see the web-ui of ESS. Alternately, the ESS web-ui can be viewed in another tab by clicking on the link corresponding to the option _URL gui:_. For instance, if the value of _URL gui:_ is http://172.18.0.12:80/gui/, either click this link or load the URL http://172.18.0.12:80/gui/ in a new tab.

## Basic usage
### Scanning a web site using ESS
A tester can launch ESS from the "Test Support Services" tab of the ElasTest Web-GUI. The steps are as follows:
1. Start TORM and load the Web-GUI of TORM in the Web browser
![][TORM GUI]
2. Click on the "Test Support Services" side panel option
![][Click TSS]
3. From the drop down list, select "ESS" and click the button "Create Instance"
![][Launch ESS]
4. Wait until the ESS instance is completely ready
![][Load ESS]
5. Click on the "View Icon" and see the Web-GUI of ESS
![][ESS GUI]
6. Enter the URL of the Web site that must be tested using ESS
![][Enter SUT URL]
7. Wait until the Spidering and Active Scan completes
![][ESS Progress]
8. Check the results generated
9. ![][ESS Results]
 
[TORM GUI]: https://pocemon.000webhostapp.com/ESS%20GUI.PNG
[Click TSS]: https://pocemon.000webhostapp.com/Click%20TSS.png
[Launch ESS]: https://pocemon.000webhostapp.com/Select%20ESS.png
[Load ESS]: 
[ESS GUI]: 
[Enter SUT URL]: https://pocemon.000webhostapp.com/Start%20Scan.png
[ESS Progress]: https://pocemon.000webhostapp.com/Progress.png
[ESS Results]: https://pocemon.000webhostapp.com/Result.png



# ElasTest Security Service (ESS)

The ElasTest Security Service (ESS) is an ElasTest service for identifying security issues in the System Under Test (SuT) by mimicking attacker behavior. Thus, when finding security issues, the focus is not in generating test cases that capture normal user behavior with the SuT. Instead, ESS focuses on generating test cases that check the SuT reaction to abnormal behavior (e.g. modifying URL parameters, using incorrect requests, or replaying authorization requests).

## Features
The final version of ESS is expected to support the detection of the following types of vulnerabilities/attacks:
1. Logical vulnerability
2. Denial-of-Service
3. Improper/Missing authentication

The current version of ESS (v0.1) has the following features.

- Create a secJob from a tJob
- Update and Delete secJobs
- Execute a tJob associated to the secJob
- Show the mockup of the creation of a malicious tJob that exposes a replay attack vulnerability in TomatoCart (an open source e-commerce web application)

## How to run

ESS can be installed by running the following commands

## Basic usage

When ElasTest TORM is started, it is accessible in the following URL:
- Linux: http://localhost:8091/
- Windows: http://\<docker-host>:8091/ (where \<docker-host> is obtained executing the command `docker-machine ip`)

EUS web interface is accessible from the option EUS in the sidebar of the main ElasTest TORM web interface.

![EUS main graphical web interface](imgs/main-gui.png)</p>


## Development documentation

### Architecture

ESS is implemented in two parts:
* ESS Web client Application
* ESS Server Application

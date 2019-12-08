# AttachmentChecker
<h3>Goal - Automate check your emails for malicious attachments.</h3>

<h4>Step 1 - Enviroment, est. 1 hour</h4>

* Set up a new enviroment for development on a VM - We will use Ubuntu 18.04.3 LTS. - 1 hour.
* Make sure that the new enviroment is disconnected from your computer, because we will download the suspicious attachments to the enviroment, and we would like to avoid lateral movement.

<h4>Step 2 - Developement, est. 25 hours</h4>

* Create a flask server that will be our CNC on the new enviroment. - 5 hours.
* Create an email-reader API using python's imap library, in order to read the email's attachments. - 10 hours.
* Create a virustotal communicator, in order to send the suspicious attachments to validation at virustotal. - 10 hours.

<h4>Step 3 - Testing, est. 1 hour</h4>

* Set the CNC to alert on malicious attachments.
* Send 2 types of files to yourself, malicious and not malicious, and see if the CNC alert on the malicious file.


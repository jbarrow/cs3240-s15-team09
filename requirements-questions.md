* What security precautions should we use when encrypting files? 
* Should the user who created the group be the default admin?
* Is there a maximum file size? Is there a maximum number of files that you can attach to a report?
* What types of systems should we expect to see: are they location-based, type of event-based, etc?
* If the server fails or crashes, how should that error be reported to the user? 
* likewise, what should the system do if it cannot complete a request? How is this different if they are viewing private vs. public information (is it different at all)?
* How do folders work across named groups? If a user is a part of multiple named groups, can they set which folders/reports are available to which groups?
* What kinds of authenication do you want for the system? Different types of security requirements for data stored in the database vs. when the data is being transmitted to and from the database? 
* How do you want us to handle requests to see private reports? Should private reports be available when searching for reports?
* for private reports, if they can be visible through a search, what information should be available/unencrypted in the search results -i.e. title, date, etc.? 
* How should the user transmit keys for encryption and decryption? Do we handle this? Will the system be responsible for  generating a key and then pass on the responsibility of protecting the key to the user?
* How does connecting to the system work? Is there an identity verification stage that the users need to go through to get approved? What information does the user need to supply in order to get an account?
* How do you designate administrators and how does the administrator pass on the responsiblity of administrator if they no longer want to be an admin? 
* Is there additional information you need to supply if you want to be an admin?
* Can you search for named groups and request to be a part of the group? How should this be handled?
* 

###  How to use, and what to do (for me)  ###
The two components of an End-to-End encrypted chatroom in a network.

The server ip and port so far are hardcoded (both in the server and client files),
such that these need to be adjusted before running the file.

The client connects by giving a "name" and a password. 
The password generates a key in a keyfile to en- and decrypt the messages
when sent and recieved.

So far, having the wrong password breaks the application...

How to use:
Change IP and Port as desired and correct for server in both 
server AND client file. 
Run both server and as many client files as wanted/needed (must be from different IPs).
Enter a name and the "correct" password for all clients.
Enjoy encrypted chatting!


To-Do:
1. remove hardcoded IP for server and make it more interactive on 
	1.1. server
	1.2. client

2. Handling wrong passwords better
	2.1. what breaks, server or client? --> client?
	2.2. how to exclude clients with wrong passwords, without disrupting others?
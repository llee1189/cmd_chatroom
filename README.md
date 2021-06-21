server.py and users.py is a pairing of code that allows client-server based messaging. At the moment, users can also whisper other users and request from the server the current users in the chatroom.
Originally, I planned to have a /disconnect command, but the usage of it seemed redundant with the code mainly purposed in CMD (the user might as well exit out of CMD instead of disconnecting where there's no other options afterwards). 
From the server side, all chats and who connects and disconnects is told.

# Installation
The process was tested on Ubuntu Linux 14.04 and may require appropriate changes for different distributions of Linux
Code was tested on Python 2.7.11

## Dependecies:
* Mindy chatbot engine (included in repo)
* Neo4J NoSql Graph database (requires Java Runtime)
* NLTK
* PractNLPTools
* dateparser
* yelp
* twilio

To install Neo4J go to the https://neo4j.com/download/?ref=home and download community edition. Unpack and run "neo4j console start" from "bin" directory
next, install Python library for interfacing with Neo4J

    pip install neo4j-driver

NLTK can be installed:

    sudo pip install -U nltk

    sudo python -m nltk.downloader -d /usr/local/share/nltk_data all

PractNLPTools:

    git clone https://github.com/biplab-iitb/practNLPTools

cd practNLPTools

    sudo python setup.py install

dateparser

    sudo pip install dateparser

Install python yelp library

    sudo pip install python-yelp-v2


Obtain API key from [yelp.com/developers](https://www.yelp.com/developers/manage_api_keys) and edit `yelp_API_key`  in config.py

Install python twilio library
	
	pip install twilio

# Overview

This code relies on chatbot engine for both admin interface and user interaction. Engine use rules, that are defined in json files: rules.json (for admin) and user.json (for processing sms messages).  


# Usage
## Admin panel
run python admit-bot.py

example commands that are understood by admin panel:

* create new event owner with phone 1-234-567-8901 named "John Smith"
* create new event named "Great Music Event" that will be held at 11-06-2016  10:00am to 11:00am
* create new place with the name "Best Restaurant"
* set owner to "John Smith" for event with id  2
* show all events with owners
* set place to "Best Restaurant" for event with id =2
* show all events with owners and places
* set default reply "Hello, and welcome to our event" for event with id = 2
* remove event with id = 6
* set event name to "Best music event" for event with id = 2
* show all subscribers for event "Great Music Event"

testing user behavior in admin panel
* @feedback "Great Music Event" |user-phone=1-234-567-6523
* @a "Best Restaurant" feedback |message_time=11-06-2016 10:30 am
* @subscribe "Great Super Event" |user_phone=1-1-234-567-8906
* @subsribers send message to "We are glad to see" to all subscribers for event with id=7

see screencast admin-demo2.mp4 and subscribe_test_demo.mp4 for demonstration of how system works. There is also second interactive script chat_user_test.py, it accepts only user messages, not admin commands.
Currently syntax for sending messages to subscriber require event owner to use event id. This may need to be changed in the future.

## Integration

<code python>
import user_api

#call when SMS is recieved
answer = user_api.process_message(input_data, data)
 '''Args:
        message - string containing message recieved from user
        data - dictionary with additional data
            {'user_phone':<phone_string>,message_time:<date_time_string>}
    Returns:
        list of messages to be send [
            {'user_phone'':<phone_string>,'message':<message_string>}]'''

</code>

SUBSCRIBE:

the process of sending to user list of interesting places:

@subscribe "Great Super Event" |user_phone=1-1-234-567-8906

answer:  $EventMessage \n The night is still young. Looking for more booze and fun? Let us know where do you wanna go next, we will find you the best spots nearby!

@subscriber no
answer: Thank you for feedback.

OR

@subscriber yes
answer: OK, write to 'show best spaces' or 'show me 'bars' ('clubs' ect.)'

@subscriber show best spaces

User get lists of different intresting places. Or user choose category and get list.

OWNER:

if owner wants to send a message to subscribers , it sends the following message :
@subsribers send message to "We are glad to see u" to all subscribers for event with id=7


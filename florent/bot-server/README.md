# Installation
The process was tested on Ubuntu Linux 14.04 and may require appropriate changes for different distributions of Linux
Code was tested on Python 2.7.11

# # Dependecies:
*Mindy chatbot engine (included in repo)
*Neo4J NoSql Graph database (requires Java Runtime)
*NLTK 
*PractNLPTools

To install Neo4J go to the https://neo4j.com/download/?ref=home and download community edition. Unpack and run "neo4j console start" from "bin" directory

NLTK can be installed:

sudo pip install -U nltk

sudo python -m nltk.downloader -d /usr/local/share/nltk_data all

PractNLPTools:

git clone https://github.com/biplab-iitb/practNLPTools

cd practNLPTools

sudo python setup.py install

# Usage
## Admin panel
run python admit-bot.py

example commands that are understood by admin panel:

* create new event owner with phone 1-234-567-8901 named "John Smith"
* create new event named "Great Music Event" that will be held at 11-06-2016  10:00am to 12:00am
* create new place with the name "Best Restaurant"
* set owner to "John Smith" for event with id  2
* show all events with owners
* set place to "Best Restaurant" for event with id =2
* show all events with owners and places
* set reply "Hello, and welcome to our event" for event with id = 2
* remove event with id = 6
* set event name to "Best music event" for event with id = 2
* show all subscribers for event "Great Music Event"

testing user behavior in admin panel
* @a "Best Restaurant" feedback |message_time=11-06-2016 10:30 am
* @subscribe "Great Music Event" |phone=1-1-234-567-8906

## Integration

<code python>
import user_api

#call when SMS is recieved
answer = user_api.process_user_message(input_data, data)
 '''Args:
        message - string containing message recieved from user
        data - dictionary with additional data
            {'user_phone':<phone_string>,message_time:<date_time_string>}
    Returns:
        list of messages to be send [
            {'user_phone'':<phone_string>,'message':<message_string>}]'''

</code>

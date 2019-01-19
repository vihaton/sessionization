__author__ = "Vili Hätönen"

import sys
import json

from sessio import *
from event_types import *

#TODO stream start and end
#TODO pause and play
#TODO track playtime
#TODO ad count

#closedsessions = {} #to move data from the open ones, prevents extra work
opensessions = {}
lts = -1 # the Latest TimeStamp for checking timeouts

def check_timeouts():
    global lts

    topop = []
    for k in opensessions.keys():
        s = opensessions[k]
        if lts >= 60 + int(s.sc["session_end"]): #if the latest event on this session was over a minute ago
            topop.append(k)      #add this to ones to be closed

    # close the timed out sessions
    for k in topop:
        opensessions.pop(k).print_this()

def process_event(event):
    global lts
    lts = event["timestamp"]

    #TODO if event is about starting a session then the previous session is closed

    #does event belong to some S
    if event["user_id"] in opensessions.keys():
        #update the session
        s = opensessions[event["user_id"]]
        s.add_event(event)
        opensessions[event["user_id"]] = s

    else:   #create new session
        opensessions[event["user_id"]] = Sessio(event) # assumes that one user can have one session open

def parse_input(line):
    try:
        #TODO check for valid structure of input
        return json.loads(line)
    except:
        print("The input was invalid:\n\t", line)

def main():
    for line in sys.stdin:
        event = parse_input(line)
        process_event(event)
        check_timeouts()

    print("open sessions in the end:")
    for s in opensessions.values():
        s.print_this()

if __name__ == "__main__":
    main()
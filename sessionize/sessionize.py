__author__ = "Vili Hätönen"

import sys
import json

from sessionize.sessio import Sessio
from sessionize.event_types import EventType

#TODO stream start and end
#TODO pause and play
#TODO track playtime
#TODO ad count

#closedsessions = {} #to move data from the open ones, prevents extra work
opensessions = {}
lts = -1 # the Latest TimeStamp for checking timeouts

def output_sessions(topop: list):
    # remove the closed sessions
    for k in topop:
        opensessions.pop(k).print_this()


def end_sessions():
    global lts

    #TODO should we automatically open a new session if an old one timeouts?
    topop = []
    for k in opensessions.keys():
        s = opensessions[k]
        if lts >= 60 + int(s.sc["session_end"]):    #if the latest event on this session was over a minute ago
            topop.append(k)
        elif s.state == "closed":                   #stream was closed
            topop.append(k)

    output_sessions(topop)

def process_event(event):
    global lts
    lts = event["timestamp"]
    uid = event["user_id"]

    #TODO if event is about starting a session then the previous session is closed

    # Has this user already a session open?
    # (this assumes that one user can have one session open)
    if event["user_id"] in opensessions.keys():
        s = opensessions[uid]

        # if this is start stream then close the old session and start new
        if event["event_type"] == EventType.stream_start:
            output_sessions([uid])
            opensessions[uid] = Sessio(event) 
        else:
            # we continue an existing session
            s.add_event(event)
        
    else:   # no existing session, create a new one
        opensessions[uid] = Sessio(event)

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
        end_sessions()

    print("open sessions in the end:")
    for s in opensessions.values():
        s.print_this()

if __name__ == "__main__":
    main()
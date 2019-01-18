import sys
import json

#closedsessions = {} #to move data from the open ones, prevents extra work
opensessions = {}
"""
{
  "timestamp": 123,
  "event_type": "track_heartbeat",
  "user_id": "A",
  "content_id": "T1001"
}
"""
class Sessio(object):
    sc = ""

    def __init__(self, event):
        global sc
        sc = {} # session content
        sc["user_id"] = event["user_id"]
        sc["content_id"] = event["content_id"]
        sc["session_start"] = event["timestamp"]
        sc["session_end"] = -1
        sc["total_time"] = 0
        sc["track_playtime"] = 0
        sc["event_count"] = 0
        sc["ad_count"] = 0

    def print_this(self):
        print(sc)

    def add_event(self, event):
        #TODO add all other status updates
        sc["event_count"] += 1

def process_event(event):
    #TODO if event is about starting a session then the previous session is closed

    #does event belong to some S
    if event["user_id"] in opensessions.keys():
        #update the session
        s = opensessions[event["user_id"]]
        s.add_event(event)

    else:   #create new session
        opensessions[event["user_id"]] = Sessio(event) # assumes that one user can have one session open

def parse_input(line):
    try:
        #TODO check for valid structure of input
        return json.loads(line)
    except:
        print("The input was invalid")

def main():
    for line in sys.stdin:
        event = parse_input(line)
        process_event(event)
        print("***\n")
        for s in opensessions.values():
            s.print_this()


if __name__ is "__main__":
    main()
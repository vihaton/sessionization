import sys
import json
__author__ = "Vili Hätönen"

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

    def __init__(self, event):
        self.sc = {} # session content
        self.sc["user_id"] = event["user_id"]
        self.sc["content_id"] = event["content_id"]
        self.sc["session_start"] = event["timestamp"]
        self.sc["session_end"] = -1
        self.sc["total_time"] = 0
        self.sc["track_playtime"] = 0
        self.sc["event_count"] = 1
        self.sc["ad_count"] = 0

    def print_this(self):
        print(self.sc)

    def add_event(self, event):
        #TODO add all other status updates
        self.sc["event_count"] += 1

def process_event(event):
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
        print("\n***")
        for s in opensessions.values():
            s.print_this()

if __name__ == "__main__":
    main()
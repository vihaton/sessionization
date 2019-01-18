import sys
import json

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

    def __init__(self, user_id, content_id, session_start):
        global sc
        sc = {} # session content
        sc["user_id"] = user_id
        sc["content_id"] = content_id
        sc["session_start"] = session_start
        sc["session_end"] = -1
        sc["total_time"] = 0
        sc["track_playtime"] = 0
        sc["event_count"] = 0
        sc["ad_count"] = 0

    def print_this(self):
        print(sc)

def process_event(event):
    #do stuff to address event to an session
    print(event)

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
    
    s = Sessio(123, 321, 1)
    s.print_this()

if __name__ is "__main__":
    main()
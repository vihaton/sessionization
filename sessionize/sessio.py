__author__ = "Vili Hätönen"

from . import EventType

class Sessio(object):

    def __init__(self, event):
        self.sc = {} # session content
        self.state = "open" # just for debugging, no actual use in this app
        self.paused = 0
        self.sc["user_id"] = event["user_id"]
        self.sc["content_id"] = event["content_id"]
        ts = event["timestamp"]
        self.sc["session_start"] = ts
        self.sc["session_end"] = ts
        self.sc["total_time"] = 0
        self.sc["track_playtime"] = 0
        self.sc["event_count"] = 1
        self.sc["ad_count"] = 0

    def print_this(self):
        print(self.sc)

    def add_event(self, event):
        self.sc["event_count"] += 1
        et = event["event_type"]
        ts = event["timestamp"]
        prev_ts = self.sc["session_end"]

        if et == "ad_start":
            self.state = "open/ad"
            self.sc["ad_count"] = 1

        elif et == EventType.ad_end:
            self.state = "open"

        elif et == EventType.track_start:
            self.state = "open/playing"

        elif et == EventType.pause:
            self.state = "open/paused"
            
        elif et == EventType.play:
            self.state = "open/playing"
            # the time paused is current time - latest event time + previous pauses, bc "play must happen after pause event"
            self.paused += ts - prev_ts
            
        elif et == EventType.track_heartbeat:
            self.sc["track_playtime"] += ts - prev_ts

        elif et == EventType.track_end:
            self.state = "open/end"
            self.sc["track_playtime"] += ts - prev_ts

        elif et == EventType.stream_end:
            self.state = "closed"

        self.sc["session_end"] = ts #stores the stamp of latest event

         # this is the way total time is approximated in the instructions, 
         # ie. exclude the 60s wait for timeout
        self.sc["total_time"] = ts - self.sc["session_start"] - self.paused

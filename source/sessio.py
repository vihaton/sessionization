__author__ = "Vili Hätönen"

class Sessio(object):

    def __init__(self, event):
        self.sc = {} # session content
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
        ts = event["timestamp"]
        self.sc["session_end"] = ts
        self.sc["total_time"] = ts - self.sc["session_start"] # this is the way total time is approximated in the instructions, ie. exclude the 60s wait for timeout

        #TODO add all other status updates
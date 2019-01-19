__author__ = "Vili Hätönen"

import enum

#Does this bring any benefits? Maybe protects from typos... worth it?
class EventType(enum.Enum):
    stream_start = "stream_start"
    ad_start = "ad_start"
    ad_end = "ad_end"
    track_start = "track_start"
    track_heartbeat = "track_heartbeat"
    pause = "pause"
    play = "play"
    track_end = "track_end"
    stream_end = "stream_end"	


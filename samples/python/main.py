from clamp_fsm import ClampFSM
from clamp_fsm_def import ClampFSMDef

if __name__ == "__main__":
    with open("1.txt", "w", encoding="utf8") as f:
        fsm = ClampFSM(f)
        fsm.post_event(ClampFSMDef.EventId.TO_TIGHT)
        fsm.post_event(ClampFSMDef.EventId.TRIGGER)
        fsm.post_event(ClampFSMDef.EventId.TO_LOOSE)
        fsm.post_event(ClampFSMDef.EventId.TRIGGER)

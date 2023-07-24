'''clamp_fsm'''

from clamp_fsm_def import ClampFSMDef


class ClampFSM (ClampFSMDef):
    '''ClampFSM'''

    def __init__(self, context):
        super().__init__()

        self.__context = context

    def _TIGHT_on_enter(self):
        print("ClampFSM::TightOnEnter")
        self.__context.write("TightOnEnter\n")

    def _TIGHT_on_exit(self):
        print("ClampFSM::TightOnExit")
        self.__context.write("TightOnExit\n")

    def _TIGHT_on_event_TRIGGER(self):
        print("ClampFSM::TightOnEvent_Trigger")
        self.__context.write("TightOnEvent_Trigger\n")

    def _LOOSE_on_enter(self):
        print("ClampFSM::LooseOnEnter")
        self.__context.write("LooseOnEnter\n")

    def _LOOSE_on_exit(self):
        print("ClampFSM::LooseOnExit")
        self.__context.write("LooseOnExit\n")

    def _LOOSE_on_event_TRIGGER(self):
        print("ClampFSM::LooseOnEvent_Trigger")
        self.__context.write("LooseOnEvent_Trigger\n")

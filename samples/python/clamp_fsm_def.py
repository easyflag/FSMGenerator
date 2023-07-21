'''clamp_fsm_def'''

from abc import abstractmethod
from enum import Enum

from fsm_base import FSMNode, FSMBase


class ClampFSMDef(FSMBase):
    '''ClampFSMDef'''

    class EventId(Enum):
        '''EventId'''

        TO_TIGHT = 1
        TO_LOOSE = 2
        TRIGGER = 3

    class StateId(Enum):
        '''StateId'''

        TIGHT = 1
        LOOSE = 2

    def __init__(self):
        super().__init__()
        self._fsm_name = "ClampFSM"
        self.__init_TIGHT()
        self.__init_LOOSE()

    @abstractmethod
    def _TIGHT_on_enter(self):
        pass

    @abstractmethod
    def _TIGHT_on_exit(self):
        pass

    @abstractmethod
    def _TIGHT_on_event_TRIGGER(self):
        pass

    @abstractmethod
    def _LOOSE_on_enter(self):
        pass

    @abstractmethod
    def _LOOSE_on_exit(self):
        pass

    @abstractmethod
    def _LOOSE_on_event_TRIGGER(self):
        pass

    def __init_TIGHT(self):
        node = FSMNode()
        node.state_id = self.StateId.TIGHT
        node.entry_action = self._TIGHT_on_enter
        node.exit_action = self._TIGHT_on_exit
        node.event_actions[self.EventId.TRIGGER] = self._TIGHT_on_event_TRIGGER
        node.transitions[self.EventId.TO_LOOSE] = self.StateId.LOOSE
        self._fsm_nodes[self.StateId.TIGHT] = node

    def __init_LOOSE(self):
        node = FSMNode()
        node.state_id = self.StateId.LOOSE
        node.entry_action = self._LOOSE_on_enter
        node.exit_action = self._LOOSE_on_exit
        node.event_actions[self.EventId.TRIGGER] = self._LOOSE_on_event_TRIGGER
        node.transitions[self.EventId.TO_TIGHT] = self.StateId.TIGHT
        self._fsm_nodes[self.StateId.LOOSE] = node

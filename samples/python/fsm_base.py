'''fsm_base'''

from abc import ABC


class FSMNode():
    '''FSMNode'''

    def __init__(self):
        self.state_id = 0
        self.entry_action = None
        self.exit_action = None
        self.event_actions = {}
        self.transitions = {}


class FSMBase(ABC):
    '''FSMBase'''

    def __init__(self):
        self._fsm_name = ""
        self._fsm_nodes = {}
        self._current_state_id = 0

    def current_state_id(self):
        '''current_state_id'''

        return self._current_state_id

    def post_event(self, event_id):
        '''post_event'''

        self.__handle_event(event_id)

    def __handle_event(self, event_id):
        if event_id in self._fsm_nodes[self._current_state_id].event_actions:
            self.__do_event_action(event_id)

        self.__handle_transition(event_id)

    def __handle_transition(self, event_id):
        if event_id in self._fsm_nodes[self._current_state_id].transitions:
            self.__do_exit_action()
            self.__go_to_state(
                self._fsm_nodes[self._current_state_id].transitions[event_id])

    def __do_event_action(self, event_id):
        self._fsm_nodes[self._current_state_id].event_actions[event_id]()

    def __do_entry_action(self):
        self._fsm_nodes[self._current_state_id].entry_action()

    def __do_exit_action(self):
        self._fsm_nodes[self._current_state_id].exit_action()

    def __go_to_state(self, state_id):
        print(self._fsm_name, "go to state:", state_id)

        self._current_state_id = state_id
        self.__do_entry_action()

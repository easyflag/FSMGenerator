class FSMNode():
    id = 0

    entryAction = None
    exitAction = None
    eventActions = {}

    transitions = {}


class FSMBase():
    def __init__(self) -> None:
        self._fsm_name = ""
        self._fsm_node_tab = {}
        self._current_state_id = 0

    def current_state_id(self):
        return self._current_state_id

    def post_event(self, event_id):
        self.__handle_event(event_id)

    def __handle_event(self, event_id):
        if self._fsm_node_tab[self._current_state_id].eventActions.contains(event_id):
            self.__do_event_action(event_id)

        self.__handle_transition(event_id)

    def __handle_transition(self, event_id):
        if self._fsm_node_tab[self._current_state_id].transitions.contains(event_id):
            self.__do_exit_action()
            self.__go_to_state(
                self._fsm_node_tab[self._current_state_id].transitions[event_id])

    def __do_event_action(self, event_id):
        self._fsm_node_tab[self._current_state_id].eventActions[event_id]()

    def __do_entry_action(self):
        self._fsm_node_tab[self._current_state_id].entryAction()

    def __do_exit_action(self):
        self._fsm_node_tab[self._current_state_id].exitAction()

    def __go_to_state(self, state_id):
        print(self._fsm_name, "go to state:", state_id)

        self._current_state_id = state_id
        self.__do_entry_action()

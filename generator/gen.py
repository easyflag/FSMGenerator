'''gen'''

from argparse import ArgumentParser
import xml.parsers.expat
from jinja2 import Environment, FileSystemLoader


class FSMEvent():
    '''FSMEvent'''

    def __init__(self):
        self.id = 0
        self.name = ''


class FSMState():
    '''FSMState'''
    class Action():
        '''Action'''

        def __init__(self):
            self.event = ''
            self.describe = ''

    class Transition():
        '''Transition'''

        def __init__(self):
            self.event = ''
            self.next_state = ''

    def __init__(self):
        self.id = 0
        self.name = ''
        self.entry_action = None
        self.exit_action = None
        self.event_actions = []
        self.transitions = []


class FSMXML():
    '''FSMXML'''

    def __init__(self, filename):
        self.name = ''
        self.events = []
        self.states = []
        self.first_state = ''

        element_stack = []

        def start_element(name, attrs):
            element_stack.append(name)
            element_chain = '.'.join(element_stack)
            if element_chain == 'state_machine':
                self.name = attrs['name']
            elif element_chain == 'state_machine.events.event':
                event = FSMEvent()
                event.id = attrs['id']
                event.name = attrs['name']
                self.events.append(event)
            elif element_chain == 'state_machine.states.state':
                state = FSMState()
                state.id = attrs['id']
                state.name = attrs['name']
                self.states.append(state)
            elif element_chain == 'state_machine.states.state.entry_action':
                action = FSMState.Action()
                self.states[-1].entry_action = action
            elif element_chain == 'state_machine.states.state.exit_action':
                action = FSMState.Action()
                self.states[-1].exit_action = action
            elif element_chain == 'state_machine.states.state.event_actions.event_action':
                action = FSMState.Action()
                self.states[-1].event_actions.append(action)
            elif element_chain == 'state_machine.states.state.transitions.transition':
                transition = FSMState.Transition()
                self.states[-1].transitions.append(transition)

        def end_element(name):
            element_stack.pop()

        def char_data(str):
            if str == '\n' or str.strip() == '':
                return

            element_chain = '.'.join(element_stack)
            if element_chain == 'state_machine.states.state.entry_action.describe':
                self.states[-1].entry_action.describe = str
            elif element_chain == 'state_machine.states.state.exit_action.describe':
                self.states[-1].exit_action.describe = str
            elif element_chain == 'state_machine.states.state.event_actions.event_action.event':
                self.states[-1].event_actions[-1].event = str
            elif element_chain == 'state_machine.states.state.event_actions.event_action.describe':
                self.states[-1].event_actions[-1].describe = str
            elif element_chain == 'state_machine.states.state.transitions.transition.event':
                self.states[-1].transitions[-1].event = str
            elif element_chain == 'state_machine.states.state.transitions.transition.next_state':
                self.states[-1].transitions[-1].next_state = str
            elif element_chain == 'state_machine.first_state':
                self.first_state = str

        with open(filename, mode='rb') as file:
            parser = xml.parsers.expat.ParserCreate()
            parser.StartElementHandler = start_element
            parser.EndElementHandler = end_element
            parser.CharacterDataHandler = char_data
            parser.ParseFile(file)


class Generator():
    def __init__(self, template):
        self.__template = template

    def gen(self, fsm, filename):
        env = Environment(loader=FileSystemLoader('./'))
        template = env.get_template(self.__template)
        content = template.render(name='22')
        print(content)


if __name__ == '__main__':
    paser = ArgumentParser(description=__doc__)
    paser.add_argument('input', help='the definiton file')
    paser.add_argument('output', help='the output directory')

    args = paser.parse_args()
    print(args)

    fsm = FSMXML(args.input)
    gen = Generator('cpp_qt.j2')
    gen.gen(fsm, args.output)

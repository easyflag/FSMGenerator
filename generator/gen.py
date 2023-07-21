'''gen'''

from argparse import ArgumentParser
import xml.parsers.expat


class FSMXML(object):
    def __init__(self, filename):
        self.name = ''
        self.events = []
        self.states = []

        element_stack = []

        def start_element(name, attrs):
            element_stack.append(name)
            element_chain = '.'.join(element_stack)
            if element_chain == 'state_machine':
                self.name = attrs['name']

        def end_element(name):
            element_stack.pop()

        with open(filename, mode='rb') as file:
            parser = xml.parsers.expat.ParserCreate()
            parser.StartElementHandler = start_element
            parser.EndElementHandler = end_element
            parser.ParseFile(file)


if __name__ == "__main__":
    paser = ArgumentParser(description=__doc__)
    paser.add_argument("input", help="the definiton file")
    paser.add_argument("output", help="the output directory")

    args = paser.parse_args()
    print(args)

    FSMXML(args.input)

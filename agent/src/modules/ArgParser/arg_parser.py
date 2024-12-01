import argparse
import sys

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def add_argument(self, name, type=str, help=None, choices=None):
        """
        Add a new argument to the parser.

        Args:
            name (str): The name of the argument.
            type (type, optional): The type of the argument. Defaults to str.
            help (str, optional): A help message for the argument. Defaults to None.
            required (bool, optional): Whether the argument is required. Defaults to False.
        """
        if choices:
            self.parser.add_argument(name, type=type, help=help, choices=choices)
        else:
            self.parser.add_argument(name, type=type, help=help)

    def add_positional_argument(self, name, type=str, help=None, choices=None):
        """
        Add a new positional argument to the parser.

        Args:
            name (str): The name of the argument.
            type (type, optional): The type of the argument. Defaults to str.
            help (str, optional): A help message for the argument. Defaults to None.
        """
        if choices:
            self.parser.add_argument(name, type=type, help=help, choices=choices)
        else:
            self.parser.add_argument(name, type=type, help=help)

    def add_optional_argument(self, name, type=str, help=None, required=False, action=None):
        """
        Add a new optional argument to the parser.

        Args:
            name (str): The name of the argument.
            type (type, optional): The type of the argument. Defaults to str.
            help (str, optional): A help message for the argument. Defaults to None.
            required (bool, optional): Whether the argument is required. Defaults to False.
            action (str, optional): The basic type of action to be taken when this argument is encountered at the command line. 
                Options include 'store', 'store_const', 'store_true', 'store_false', 'append', 'append_const', 'count', 
                'help', 'version', 'store_action' and 'extend_action'. Defaults to None.
        """
        if action in ['store_true', 'store_false']:
            self.parser.add_argument(f"--{name}", action=action, help=help)
        else:
            self.parser.add_argument(f"--{name}", type=type, action=action, help=help, required=required)

    def parse_args(self):
        """
        Parse the command line arguments.

        Returns:
            Namespace: The parsed arguments.
        """
        return self.parser.parse_args()

# Test basic functionality
if __name__ == "__main__":
    sys.argv.append('input_file_location')
    sys.argv.append('--output_file=output_file_location')
    sys.argv.append('--verbose')

    parser = ArgumentParser()
    parser.add_positional_argument("input_file", type=str, help="The path to the input file")
    parser.add_optional_argument("output_file", type=str, help="The path to the output file", required=True)
    parser.add_optional_argument("verbose", action="store_true", help="Increase verbosity")

    args = parser.parse_args()

    assert(args.input_file == "input_file_location")
    assert(args.output_file == "output_file_location")
    assert(args.verbose == True)
    print("PASSED")
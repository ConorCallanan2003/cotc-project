import argparse
import sys
import threading

class ArgumentParser:
    
    _instance = None
    _lock = threading.Lock()
    _parser = None
    _parsed_args = None
    
    def __new__(cls):
        with cls._lock:
            if cls._instance == None:
                cls._instance = super(ArgumentParser, cls).__new__(cls)
                cls._parser = argparse.ArgumentParser()
                
        return cls._instance

    @classmethod
    def add_argument(cls, name, arg_type=str, help=None, choices=None):
        assert type(cls._parser) == argparse.ArgumentParser, "Parser is not initialized"
        if choices:
            cls._parser.add_argument(name, type=arg_type, help=help, choices=choices)
        else:
            cls._parser.add_argument(name, type=arg_type, help=help)

    @classmethod
    def add_positional_argument(cls, name, arg_type=str, help=None, choices=None):
        assert type(cls._parser) == argparse.ArgumentParser, "Parser is not initialized"
        if choices:
            cls._parser.add_argument(name, type=arg_type, help=help, choices=choices)
        else:
            cls._parser.add_argument(name, type=arg_type, help=help)

    @classmethod
    def add_optional_argument(cls, name, arg_type=str, help=None, required=False, action=None):
        assert type(cls._parser) == argparse.ArgumentParser, "Parser is not initialized"
        if action in ['store_true', 'store_false']:
            cls._parser.add_argument(f"--{name}", action=action, help=help)
        else:
            cls._parser.add_argument(f"--{name}", type=arg_type, action=action, help=help, required=required)
            

    @classmethod
    def parseArgs(cls):
        assert type(cls._parser) == argparse.ArgumentParser, "Parser is not initialized"
        cls._parsed_args = cls._parser.parse_args()
    
    @classmethod
    def getArg(cls, key: str):
        assert type(cls._parser) == argparse.ArgumentParser, "Parser is not initialized"
        assert cls._parsed_args is not None, "Args have not been parsed"
        return cls._parsed_args.__getattribute__(key)

# Test basic functionality
if __name__ == "__main__":
    sys.argv.append('input_file_location')
    sys.argv.append('--output_file=output_file_location')
    sys.argv.append('--verbose')

    parser = ArgumentParser()
    parser.add_positional_argument("input_file", type=str, help="The path to the input file")
    parser.add_optional_argument("output_file", type=str, help="The path to the output file", required=True)
    parser.add_optional_argument("verbose", action="store_true", help="Increase verbosity")

    args = ArgumentParser.parseArgs()

    assert(args.input_file == "input_file_location")
    assert(args.output_file == "output_file_location")
    assert(args.verbose == True)
    print("PASSED")
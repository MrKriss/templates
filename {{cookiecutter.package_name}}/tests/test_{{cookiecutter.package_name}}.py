""" Example test for cli arguments 

"""

import os

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def test_cli_with_custom_arguments(capfd):
    
    # Pull out the functions we need to create a parser object, and trigger the entry point 
    from mypackage.command_line import get_parser, main
    import shlex 

    # The package is designed to read either from stdin, or from a file specified with the -i flag
    # We can parse in our own arguments as if they were on the command line as follows:

    # First create parser object using utility function from command_line.py 
    parser = get_parser()

    test_input_filepath = os.path.join(TEST_DIR, 'test.csv')

    # This can take multiple arguments just like they would be parsed on the command line 
    # note that paths to file must be quoted in case they contain spaces 
    argument_str = '-i "{input_file}"'.format(input_file=test_input_filepath)

    # Split argument string into a list 
    my_arguments_list = shlex.split(argument_str)

    # Add arguments to the parser
    parser = parser.parse_args(my_arguments_list)

    # Trigger the main entry point, now with custom arguments
    main(parser)
    
    # Capture stdout and stderr
    out, err = capfd.readouterr()

    target = """ TESTS NEED WRITING """
    assert out == target






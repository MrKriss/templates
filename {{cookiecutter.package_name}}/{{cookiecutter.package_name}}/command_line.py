#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""{{cookiecutter.package_description}}"""

import os
import sys 
import argparse 

from .utils import create_logger, read_and_update_config


def main(args):
    """The main function of the file that executes all other processes"""

    # Use this utility to read defaults from a config file and then overwrite them 
    # with values passed into the cli as arguments
    config = read_and_update_config(args)

    logger = create_logger(config)
    logger.info("============================= Started New Run ===================================")

    # Write results to stdout. to_csv will also accept a file object so works by passing 
    # in reference to stdout
    # results_df.to_csv(args.output, index=False)


def command_line_entry_point():
    """This is the function that gets executed first from command line"""

    # Parse Arguments
    args = get_parser().parse_args()
    # Run program
    main(args)


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)

    # Optional positional input and output files
    # if not present, will default to stdio
    parser.add_argument(
        '-i', '--input', nargs='?',
        type=argparse.FileType('r', encoding='utf-8'),
        default=sys.stdin,
        help='Specify a file to read from for the input. Defaults to stdin if not specified.'
    )

    parser.add_argument(
        '-o', '--output', nargs='?',
        type=argparse.FileType('w', encoding='utf-8'),
        default=sys.stdout,
        help='Specify a file to write to for the output. Defaults to stdout if not specified.'
    )

    # Useful generic options
    parser.add_argument(
        "-c", "--config",
        dest='config_filepath',
        help="Specify a ini configuration file to use for setting algorithm parameters."
    )

    # Other Algorithm specific parameters are passed via a key value interface
    parser.add_argument(
        "-a", "--args", nargs='*', dest='cli_args',
        help=("Collection of key-value arguments to pass to the algorithm."
              "Accepts a space separated list of key value pairs. e.g.\n"
              "   --args key1=value1 key2=value2\n"
              "The key name follows the associated config ini file hierarchy with the format:\n"
              "   <SECTION_NAME>.<PARAMETER_NAME>"))
    return parser


if __name__ == '__main__':
    # If executed directly, this script will kick off the same entry point 
    # as if the command line utility was invoked
    command_line_entry_point()

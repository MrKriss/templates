""" Utility Functions """

import os
import logging
import logging.config
import configparser

from . import PKG_DIR


def create_logger(config):
    """ Return the configured logger """

    logger = logging.getLogger(__name__)

    filename = config.get('logging', 'filename')
    dirs = os.path.dirname(filename)
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)

    # Use a timed rotating file handle for the logfile which appends to daily log file for last 7 days
    # https://docs.python.org/2/library/logging.handlers.html?highlight=rotatingfilehandle#timedrotatingfilehandler
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'when': 'D',
                'interval': 1,
                'utc': True,
                'formatter': 'standard',
                'backupCount': 7,
                'filename': filename,
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': config.get('logging', 'level').upper(),
                'propagate': True
            }
        }
    })

    return logger


def read_and_update_config(args):
    """Return config updated with command line arguments.

    If no configfile is specified, the default config file will be specified:
    'default_config.ini'

    Any parameters parsed using the command line via --args always take precedence over those in a
    config file, even if it was also parsed via --config.

    Parameters
    ----------
    args: argparse object
        The argparse argument namespace object.

    Returns
    -------
    parameters:
        A configparser configuration object.

    """

    # Read in default config values
    parameters = configparser.ConfigParser()
    if args.config_filepath:
        parameters.read(args.config_filepath)
    else:
        parameters.read(os.path.join(PKG_DIR, 'default_config.ini'))

    # Pass extra arguments from the command line, and override configfile values if necessary
    if args.cli_args:
        cli_parameters = args.cli_args
        for item in cli_parameters:
            key, value = item.split('=')

            # Check if arg has named section
            if len(key.split('.')) == 1:
                # key should be in DEFAULT section
                section = 'DEFAULT'
                option = key
                if key not in parameters.defaults().keys():
                    raise ValueError('Unable to update parameter: %s in DEFAULT section\n'
                                     '\tNo such parameter exists: %s' % (key, key))
            else:
                section, option = key.split('.')
                # Check that option is in config and update
                if not parameters.has_option(section, option):
                    raise ValueError('Unable to update parameter: %s in %s section\n'
                                     '\tNo such parameter exists: %s' % (option, section, option))

            parameters.set(section, option, value)

    return parameters

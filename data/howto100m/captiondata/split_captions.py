import pandas as pd
import argparse
import sys
import logging
import os


def config_logger(verbose=False, logdir="./"):
    """Configure general logger and severity
    :param: verbose, boolean if DEBUG activated
    :return:
    """
    nameofscript = "split_captions"

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(logdir + nameofscript + ".log")

    # Create formatters and add it to handlers
    c_format = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
    )
    f_format = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
    )
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger = logging.getLogger()

    if verbose:
        logger.setLevel(logging.DEBUG)
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)


def parse_args():
    """Parse the scripts args"""
    parser = argparse.ArgumentParser(description="Split captions into train, test, val captions")
    optional = parser._action_groups.pop()
    # Manage required args
    # required = parser.add_argument_group('required arguments')
    # Manage optional args
    optional.add_argument(
        "--logdir",
        "-L",
        dest="logdir",
        action="store",
        default="./",
        help="Logdir to be used.",
    )
    optional.add_argument(
        "--verbose",
        "-v",
        dest="verbose",
        action="store_true",
        default=False,
        help="Activate verbose",
    )
    optional.add_argument(
        "--input-file",
        "-i",
        dest="input_file",
        action="store",
        type=argparse.FileType('rb'),
        help="Input file to be used",
    )
    optional.add_argument(
        "--execute",
        "-e",
        dest="execute",
        action="store_true",
        default=False,
        help="Activate clean operation",
    )
    parser._action_groups.append(optional)

    return parser.parse_args()


def process_json(input_file):
    df = pd.read_json(input_file)
    df = df.T
    file_name = os.path.basename(input_file.name).split(".", 1)[0]
    file_path = os.path.dirname(os.path.abspath(input_file.name))
    # Generate train
    logging.info("Generating train")
    train=df.sample(frac=0.6,random_state=200)
    # Generate test
    logging.info("Generating test")
    pre_test=df.drop(train.index)
    test=pre_test.sample(frac=0.2,random_state=200)
    # Generate val
    logging.info("Generating val")
    val=pre_test.drop(test.index)

    # Write train
    train = train.T
    train.to_json(f"{file_path}/{file_name}_train.json")
    # Write test
    test = test.T
    test.to_json(f"{file_path}/{file_name}_test.json")
    # Write val
    val = val.T
    val.to_json(f"{file_path}/{file_name}_val.json")


def main(args):
    logging.debug("Starting processing")
    process_json(input_file=args.input_file)
    logging.debug("End of processing")

if __name__ == "__main__":
    args = parse_args()
    config_logger(args.verbose, args.logdir)
    global verbose
    verbose = args.verbose

    main(args)

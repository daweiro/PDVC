import pandas as pd
import itertools
import argparse
import sys
import logging


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
        "--output-file",
        "-o",
        dest="output_file",
        action="store",
        type=argparse.FileType('wb'),
        help="Output file to be used",
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


def process_json(input_file, output_file):
    df = pd.read_json(input_file)
    logging.debug("First load:%s", df)
    df = df.T
    logging.debug("After transpo:%s", df)
    df['timestamps'] = df[["start", "end"]].apply(lambda x: [[start, end] for start, end in itertools.zip_longest(x[0], x[1], fillvalue=-1)], axis=1)
    logging.info("After timestamps: %s", df)
    df['duration'] =  df["end"].apply(lambda x: x[-1])
    logging.info("After duration: %s", df)
    df = df.rename(columns={'text': 'sentences'})
    logging.info("After sentences: %s", df)
    df = df.drop('start', axis=1)
    df = df.drop('end', axis=1)
    logging.info("Final result: %s", df)
    df = df.T
    df.to_json(output_file)

def main(args):
    logging.debug("Starting processing")
    process_json(input_file=args.input_file, output_file=args.output_file)
    logging.debug("End of processing")

if __name__ == "__main__":
    args = parse_args()
    config_logger(args.verbose, args.logdir)
    global verbose
    verbose = args.verbose

    main(args)

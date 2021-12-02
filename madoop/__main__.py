"""A light weight MapReduce framework for education.

Andrew DeOrio <awdeorio@umich.edu>

"""
import argparse
import sys
import pkg_resources
from .mapreduce import mapreduce
from .exceptions import MadoopError


def main():
    """Parse command line arguments and options then call mapreduce()."""
    parser = argparse.ArgumentParser(
        description='A light weight MapReduce framework for education.'
    )

    optional_args = parser.add_argument_group('optional arguments')
    version = pkg_resources.get_distribution("madoop").version
    optional_args.add_argument(
        '--version', action='version',
        version=f'Madoop {version}'
    )

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-input', dest='input', required=True)
    required_args.add_argument('-output', dest='output', required=True)
    required_args.add_argument('-mapper', dest='mapper', required=True)
    required_args.add_argument('-reducer', dest='reducer', required=True)

    args, _ = parser.parse_known_args()

    try:
        mapreduce(
            input_dir=args.input,
            output_dir=args.output,
            map_exe=args.mapper,
            reduce_exe=args.reducer,
        )
    except MadoopError as err:
        sys.exit(f"Error: {err}")


if __name__ == '__main__':
    main()

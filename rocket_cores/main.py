import argparse
import asyncio

from .fetch_data import fetch_data_interactive


def main():
    parser = argparse.ArgumentParser(
        description="Fetches the most resued first stages of rocket + total lifted mass in kgs."
    )
    parser.add_argument(
        "--cores",
        type=int,
        default=0,
        help="Number of most reused cores fetched from api",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset from first element in cores",
    )

    parser.add_argument(
        "--only-successful",
        action="store_true",
        help="Only successful launches counts.",
    )
    parser.add_argument(
        "--no-future-launches",
        action="store_false",
        help="Future launches does not count.",
    )

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        fetch_data_interactive(
            args.only_successful, args.no_future_launches, args.cores, args.offset
        )
    )

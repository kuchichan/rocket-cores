import argparse
import asyncio
from typing import List, Tuple

import aiohttp

from .core import get_cores, get_cores_ids, get_reuse_count
from .payload import calculate_payload_for_cores, format_payload_query, get_payloads


async def fetch_core_info(
    only_successful, future_launches, limit
) -> List[Tuple[str, int, int]]:
    async with aiohttp.ClientSession() as session:
        response_cores = await get_cores(session, limit)
        core_ids = get_cores_ids(response_cores)
        core_reuse_count = get_reuse_count(response_cores)
        query = format_payload_query(future_launches=future_launches)
        response_launches = await get_payloads(
            session,
            core_ids,
            query,
            only_successful=only_successful,
            future_launches=future_launches,
        )
        total_masses_for_each_core = calculate_payload_for_cores(
            response_launches, future_launches=future_launches
        )

        return list(zip(core_ids, core_reuse_count, total_masses_for_each_core))


def present_data(data: List[Tuple[str, int, int]]) -> None:
    print("\nThe most reused rocket cores:\n")
    print("_" * 37)
    print("|core id|reuse count|mass total [kg]|")
    print("|" + "-" * 7 + "+" + "-" * 11 + "+" + "-" * 15 + "|")
    for id_, r_count, mass in data:
        print(f"|{id_:^7}|{r_count:^11}|{mass:^15}|")
    print("=" * 37)


def main():
    parser = argparse.ArgumentParser(
        description="Fetches the most resued first stages of rocket + total lifted mass in kgs."
    )
    parser.add_argument(
        "--cores",
        type=int,
        default=5,
        help="Number of most reused cores fetched from api",
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
    result = loop.run_until_complete(
        fetch_core_info(args.only_successful, args.no_future_launches, args.cores)
    )
    present_data(result)

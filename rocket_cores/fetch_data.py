import asyncio
from typing import List, Tuple

import aiohttp

from .constants import MAX_CORE_LIMIT
from .core import fetch_core_info
from .payload import fetch_launches_data


def present_data(data: List[Tuple[str, int, int]], cursor: int = 0) -> None:
    print(f"\nThe most reused rocket cores: {cursor+1}, {cursor + 10}\n")
    print("_" * 40)
    print("|core id   |reuse count|mass total [kg]|")
    print("|" + "-" * 10 + "+" + "-" * 11 + "+" + "-" * 15 + "|")
    for id_, r_count, mass in data:
        print(f"|{id_:^10}|{r_count:^11}|{mass:^15}|")
    print("=" * 40)


def get_input():
    result = ""
    while result not in ("n", "q"):
        result = input('Fetch next page? ("n" to fetch next page, "q" to quit): ')
    return result


async def fetch_data_interactive(
    only_successful: bool, future_launches: bool, limit: int, offset: int = 0
) -> None:
    async with aiohttp.ClientSession() as session:
        core_ids, reuse_count = await fetch_core_info(session, limit, offset)
        core_list_length = len(core_ids)

        if core_list_length > MAX_CORE_LIMIT:
            cursor = 0
            while cursor <= core_list_length:
                masses = await fetch_launches_data(
                    session,
                    core_ids[cursor : cursor + 10],
                    only_successful=only_successful,
                    future_launches=future_launches,
                )
                present_data(
                    list(
                        zip(
                            core_ids[cursor : cursor + MAX_CORE_LIMIT],
                            reuse_count[cursor : cursor + MAX_CORE_LIMIT],
                            masses,
                        )
                    ),
                    cursor,
                )
                cursor += MAX_CORE_LIMIT
                if cursor >= core_list_length:
                    break
                result = get_input()
                if result == "q":
                    break
                await asyncio.sleep(10)  # blocked by api
        else:
            masses = await fetch_launches_data(
                session,
                core_ids,
                only_successful=only_successful,
                future_launches=future_launches,
            )
            present_data(list(zip(core_ids, reuse_count, masses)))

        print("Goodbye!")


async def fetch_data_automatically(
    only_successful: bool, future_launches: bool, limit: int, offset: int = 0
) -> List[Tuple[str, int, int]]:
    async with aiohttp.ClientSession() as session:
        core_ids, reuse_count = await fetch_core_info(session, limit, offset)
        core_list_length = len(core_ids)

        if core_list_length < MAX_CORE_LIMIT:
            masses = await fetch_launches_data(
                session,
                core_ids,
                only_successful=only_successful,
                future_launches=future_launches,
            )
            return list(zip(core_ids, reuse_count, masses))

        cursor = 0
        result = []
        while cursor <= core_list_length:
            masses = await fetch_launches_data(
                session,
                core_ids[cursor : cursor + 10],
                only_successful=only_successful,
                future_launches=future_launches,
            )
            result.extend(
                list(
                    zip(
                        core_ids[cursor : cursor + MAX_CORE_LIMIT],
                        reuse_count[cursor : cursor + MAX_CORE_LIMIT],
                        masses,
                    )
                )
            )
            cursor += MAX_CORE_LIMIT
            await asyncio.sleep(11)  # blocked by api

        return result

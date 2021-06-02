import asyncio
from typing import Any, Dict, List

from aiohttp import ClientSession

from .constants import GRAPHQL_API_URL, PAYLOAD_QUERY


def format_payload_query(future_launches: bool = True):
    return PAYLOAD_QUERY.format(
        launches_type="launches" if future_launches else "launchesPast"
    )


def calculate_payload_for_cores(
    responses: List[Dict[str, Any]], future_launches: bool
) -> List[int]:
    launch_key = "launches" if future_launches else "launchesPast"
    return [
        round(
            sum(
                payload["payload_mass_kg"]
                for el in response["data"][launch_key]
                for payload in el["rocket"]["second_stage"]["payloads"]
                if payload["payload_mass_kg"] is not None
            )
        )
        for response in responses
    ]


async def get_payload_for_id(
    session: ClientSession,
    id_: str,
    query: str,
    only_successful: bool,
    future_launches: bool,
) -> Dict[str, Any]:
    launch_key = "launches" if future_launches else "launchesPast"

    async with session.post(
        url=GRAPHQL_API_URL, json={"query": query, "variables": {"id": id_}}
    ) as resp:
        result = await resp.json()
        errors = result.get("errors")

        if errors:
            raise ValueError(errors[0]["message"])

        if only_successful:
            return {
                "data": {
                    launch_key: [
                        launch
                        for launch in result["data"][launch_key]
                        if launch["launch_success"]
                    ]
                }
            }
        return result


async def get_payloads(
    session: ClientSession,
    ids: List[str],
    query: str,
    *,
    only_successful: bool = False,
    future_launches: bool = True
):
    tasks = [
        asyncio.create_task(
            get_payload_for_id(session, id_, query, only_successful, future_launches)
        )
        for id_ in ids
    ]
    results = await asyncio.gather(*tasks)
    return list(results)


async def fetch_launches_data(
    session, core_ids, only_successful, future_launches
) -> List[int]:
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
    return total_masses_for_each_core

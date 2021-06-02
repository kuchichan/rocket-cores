from typing import Any, Dict, List, Tuple

from aiohttp.client import ClientSession

from .constants import CORE_QUERY, CORE_QUERY_LIMIT, GRAPHQL_API_URL


def get_cores_ids(response: Dict[str, Any]) -> List[str]:
    return [el["id"] for el in response["data"]["cores"]]


def get_reuse_count(response: Dict[str, Any]) -> List[int]:
    return [el["reuse_count"] for el in response["data"]["cores"]]


async def get_cores(session: ClientSession, limit: int) -> Dict[str, Any]:
    json: Dict[str, Any] = (
        {"query": CORE_QUERY}
        if not limit
        else {"query": CORE_QUERY_LIMIT, "variables": {"lim": limit}}
    )
    async with session.post(
        url=GRAPHQL_API_URL,
        json=json,
    ) as resp:
        result = await resp.json()
        errors = result.get("errors")
        if errors:
            raise ValueError(errors[0]["message"])
        return result


async def fetch_core_info(session, limit) -> Tuple[List[str], List[int]]:
    response_cores = await get_cores(session, limit)
    core_ids = get_cores_ids(response_cores)
    core_reuse_count = get_reuse_count(response_cores)

    return core_ids, core_reuse_count

from typing import Any, Dict, List

from aiohttp.client import ClientSession

from .constants import CORE_QUERY, GRAPHQL_API_URL


def get_cores_ids(response: Dict[str, Any]) -> List[str]:
    return [el["id"] for el in response["data"]["cores"]]


def get_reuse_count(response: Dict[str, Any]) -> List[int]:
    return [el["reuse_count"] for el in response["data"]["cores"]]


async def get_cores(session: ClientSession, limit: int) -> Dict[str, Any]:
    async with session.post(
        url=GRAPHQL_API_URL, json={"query": CORE_QUERY, "variables": {"lim": limit}}
    ) as resp:
        result = await resp.json()
        errors = result.get("errors")
        if errors:
            raise ValueError(errors[0]["message"])
        return result

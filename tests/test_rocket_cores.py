import asyncio

import pytest

from rocket_cores.constants import CORE_QUERY_LIMIT, GRAPHQL_API_URL
from rocket_cores.core import get_cores, get_cores_ids, get_reuse_count
from rocket_cores.payload import (
    calculate_payload_for_cores,
    format_payload_query,
    get_payload_for_id,
)

fake_core_data = {
    "data": {
        "cores": [
            {"id": "B1049", "reuse_count": 6},
            {"id": "B1051", "reuse_count": 5},
            {"id": "B1048", "reuse_count": 4},
            {"id": "B1046", "reuse_count": 3},
            {"id": "B1056", "reuse_count": 3},
            {"id": "B1059", "reuse_count": 3},
        ]
    }
}

fake_launch_data = {
    "data": {
        "launches": [
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": True,
            },
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": True,
            },
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": True,
            },
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": True,
            },
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": True,
            },
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": True,
            },
            {
                "rocket": {"second_stage": {"payloads": [{"payload_mass_kg": 1}]}},
                "launch_success": False,
            },
        ]
    }
}

fake_error_data = {"errors": [{"message": "Hey, dont do that!"}]}


@pytest.fixture
async def fake_session_cores(mocker):
    async def get_json(data):
        await asyncio.sleep(0.01)
        return data

    def get_value(data):
        fake_response = mocker.Mock()
        fake_response.json.return_value = get_json(data)
        return fake_response

    def spawn(data):
        session = mocker.MagicMock()
        session.post = mocker.MagicMock(spec=["url", "json"])
        session.post.return_value.__aenter__.return_value = get_value(data)
        return session

    return spawn


@pytest.mark.asyncio
async def test_fake_session_cores(fake_session_cores):
    fake_session = fake_session_cores(fake_core_data)

    async with fake_session.post(
        url="URL", json={"query": CORE_QUERY_LIMIT, "variables": 10}
    ) as s:
        result = s
        assert await result.json() == fake_core_data
        fake_session.post.assert_called_with(
            url="URL", json={"query": CORE_QUERY_LIMIT, "variables": 10}
        )


@pytest.mark.asyncio
async def test_get_cores_calls_post_with_given_limit_and_url(fake_session_cores):
    fake_session = fake_session_cores(fake_core_data)
    limit = 5
    result = await get_cores(fake_session, limit)

    assert result == fake_core_data
    fake_session.post.assert_called_with(
        url=GRAPHQL_API_URL,
        json={"query": CORE_QUERY_LIMIT, "variables": {"lim": limit, "offset": 0}},
    )


@pytest.mark.asyncio
async def test_get_cores_raises_a_value_error_if_errors(fake_session_cores):
    fake_session = fake_session_cores(fake_error_data)
    limit = 5
    with pytest.raises(ValueError, match="Hey, dont do that!"):
        await get_cores(fake_session, limit)


def test_get_cores_ids_extracts_id_from_given_json():
    expected = ["B1049", "B1051", "B1048", "B1046", "B1056", "B1059"]
    result = get_cores_ids(fake_core_data)

    assert expected == result


def test_get_resue_count_extract_reuse_count_from_given_json():
    expected = [6, 5, 4, 3, 3, 3]
    result = get_reuse_count(fake_core_data)

    assert expected == result


@pytest.mark.asyncio
async def test_get_payload_for_id_calls_post_with_given_url_and_id(fake_session_cores):
    fake_session = fake_session_cores(fake_launch_data)
    query = format_payload_query()
    result = await get_payload_for_id(
        fake_session, "aaaa", query, only_successful=False, future_launches=True
    )

    assert result == fake_launch_data
    fake_session.post.assert_called_with(
        url=GRAPHQL_API_URL, json={"query": query, "variables": {"id": "aaaa"}}
    )


@pytest.mark.asyncio
async def test_get_payload_only_for_successful_flights(fake_session_cores):
    fake_session = fake_session_cores(fake_launch_data)
    query = format_payload_query()
    result = await get_payload_for_id(
        fake_session, "aaaa", query, only_successful=True, future_launches=True
    )

    assert (
        len(result["data"]["launches"]) == len(fake_launch_data["data"]["launches"]) - 1
    )
    assert all(launch["launch_success"] for launch in result["data"]["launches"])


def test_calculate_payload_returns_total_number_of_payloads():
    result = calculate_payload_for_cores([fake_launch_data] * 5, future_launches=True)
    assert result == [7, 7, 7, 7, 7]

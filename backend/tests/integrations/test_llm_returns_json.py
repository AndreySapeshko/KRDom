# import pytest
#
# from backend.llm.open_router_client import get_open_router_client
#
#
# @pytest.mark.llm
# @pytest.mark.asyncio
# async def test_llm_returns_json():
#     client = get_open_router_client()
#
#     data = {"ping": "pong"}
#
#     result = await client.llm_complete_json(
#         prompt="Return the same object back as JSON.",
#         input_data=data
#     )
#
#     assert result["ping"] == "pong"

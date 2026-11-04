"""EveryPlate transport routing and shared recipe-detail behavior (no live account)."""

from unittest.mock import AsyncMock

from custom_components.hellofresh.client import HelloFreshClient
from custom_components.hellofresh.models import HelloFreshRecipe, HelloFreshWeek


class _Response:
    status = 200
    headers = {}

    def __init__(self, payload):
        self.payload = payload

    async def json(self, **_kwargs):
        return self.payload

    async def text(self):
        return ""


async def test_everyplate_login_and_refresh_use_er_on_everyplate_host() -> None:
    calls = []

    class Session:
        async def post(self, url, **kwargs):
            calls.append((url, kwargs))
            if url.endswith("/gw/auth/token"):
                return _Response({"access_token": "app-token"})
            return _Response(
                {
                    "access_token": "made-up-access",
                    "refresh_token": "made-up-refresh",
                    "expires_in": 1800,
                    "refresh_expires_in": 5184000,
                }
            )

    client = HelloFreshClient(
        session=Session(), country="everyplate_us", username="cook@example.com", password="made-up"
    )
    await client._async_login(force=True)
    assert [url for url, _ in calls] == [
        "https://www.everyplate.com/gw/auth/token",
        "https://www.everyplate.com/gw/login",
    ]
    assert calls[-1][1]["params"] == {"country": "ER", "locale": "en-US"}
    calls.clear()
    await client._async_refresh_access_token(force=True)
    assert calls[0][0] == "https://www.everyplate.com/gw/refresh"
    assert calls[0][1]["params"] == {"country": "ER", "locale": "en-US"}


async def test_everyplate_recipe_details_skip_cookbook_and_keep_regional_params() -> None:
    client = HelloFreshClient(session=None, country="everyplate_us")
    get = AsyncMock(return_value=_Response({"id": "recipe1", "name": "Pasta", "steps": []}))
    client._async_api_get = get
    client._async_search_favorites = AsyncMock(side_effect=AssertionError("No EveryPlate cookbook"))
    detail = await client.async_get_recipe_detail("recipe1")
    assert detail.name == "Pasta"
    assert detail.is_favorite is None
    assert get.await_args.kwargs["params"] == {"country": "ER", "locale": "en-US"}
    client._async_search_favorites.assert_not_awaited()


async def test_everyplate_poll_does_not_request_cookbook_even_when_option_is_true() -> None:
    client = HelloFreshClient(session=None, country="everyplate_us", enable_favorites=True)
    client._async_list_cookbook = AsyncMock(side_effect=AssertionError("No EveryPlate cookbook"))
    await client._async_apply_favorites(
        [
            HelloFreshWeek(
                week_id="2026-W46",
                display_name="Week 46",
                recipes=[HelloFreshRecipe(recipe_id="recipe1", name="Pasta")],
            )
        ]
    )
    client._async_list_cookbook.assert_not_awaited()
    assert client._extract_currency_code({}) == "USD"
    assert client._extract_currency_code({"currency": "CAD"}) == "CAD"

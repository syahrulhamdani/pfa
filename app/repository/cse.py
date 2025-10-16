"""Google Custom Search Engine API."""
import re
from dataclasses import dataclass, field
from typing import Any

import html2text
from httpx import (AsyncClient, HTTPError, HTTPStatusError, Limits,
                   RequestError, Response, Timeout)
from loguru import logger as _LOGGER
from tenacity import (RetryCallState, retry, retry_if_exception_type,
                      stop_after_attempt, wait_exponential)

from app.core.config import config as c
from app.models.cse import CSEItem, CSEResults


CSE_PARSING_RULE = {
    "zapfinance.co.id": {
        "parser": (
            lambda text: re.compile(
                r"###### Articles(.*?)#### Tuliskan Komentar Cancel reply", re.DOTALL
            ).search(text).group(1).strip()
        ),
        "excluded_url_pattern": [
            "course", "resource", "academy"
        ],
    },
    "pocketsmith.com": {
        "parser": (
            lambda text: "# " + re.compile(
                r"\n*#\s*(.*?)\* \* \*", re.DOTALL
            ).search(text).group(1).strip()
        ),
        "excluded_url_pattern": [],
    },
    "ynab.com": {
        "parser": (
            lambda text: "# " + re.compile(
                r"\n*#\s(.*?)Try", re.DOTALL
            ).search(text).group(1).strip()
        ),
        "excluded_url_pattern": [],
    },
}


@dataclass
class GoogleCSE:
    """Google Custom Search Engine instance."""
    cx: str = field(default=c.GOOGLE_CSE_ID)
    base_url: str = field(default=c.GOOGLE_CSE_URL)
    timeout: int = field(default=c.GOOGLE_CSE_TIMEOUT)
    max_connections: int = field(default=c.HTTP_MAX_CONNECTIONS)

    def __post_init__(self):
        limits = Limits(max_connections=self.max_connections)
        timeout = Timeout(timeout=self.timeout)
        self.client = AsyncClient(
            base_url=self.base_url,
            limits=limits,
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/108.0.0.0 Safari/537.36"
                )
            }
        )
        self.parser = html2text.HTML2Text()
        self.parser.ignore_links = True

    def _log_retry_attempt(self, retry_state: RetryCallState):
        _LOGGER.warning(
            "  [RETRY] Attempt {} failed. Waiting {:.1f}s before next retry...",
            retry_state.attempt_number,
            retry_state.idle_for
        )

    async def run(self, query: str) -> CSEResults:
        """Run end-to-end CSE search, which will search and then be parsed to markdown.

        Args:
            query (str): search query.

        Returns:
            CSEResults: clean search results.
        """
        async def _fetch_and_parse(cse_response: dict[str, Any]) -> CSEItem:
            _LOGGER.info("Fetching url: {}", cse_response["link"])
            for site, rule in CSE_PARSING_RULE.items():
                if site not in cse_response["link"]:
                    continue

                for part in rule["excluded_url_pattern"]:
                    if part in cse_response["link"]:
                        return CSEItem()

                try:
                    response = await self.client.get(cse_response["link"])
                    response.raise_for_status()
                except HTTPError as exc:
                    _LOGGER.exception(
                        "Request error using CSE ({}): {}",
                        cse_response["link"], exc
                    )
                    raise

                _LOGGER.debug("Parsing content from url: {}", cse_response["link"])
                raw_content = self.parser.handle(response.text)
                parser = rule["parser"]
                clean_content = parser(raw_content)

                _LOGGER.info("Done fetching url: {}", cse_response["link"])
                return CSEItem(
                    title=cse_response["title"],
                    link=cse_response["link"],
                    content=clean_content,
                )

        responses = await self.search(query=query)
        if int(responses["searchInformation"]["totalResults"]) == 0:
            _LOGGER.warning("No search result found for: '{}'", query)
            return CSEResults(results=[])

        _LOGGER.info("Got search result: {}", len(responses["items"]))
        results = []
        for item in responses["items"]:
            try:
                result = await _fetch_and_parse(item)
            except Exception as exc:
                _LOGGER.exception("Error parsing CSE item: {}", exc)
                continue
            results.append(result)
        return CSEResults(results=results)

    async def _search(self, query: str) -> Response:
        params = {
            "key": c.GOOGLE_CSE_API_KEY,
            "cx": self.cx,
            "q": query,
            "sort": "date",
        }
        response = await self.client.get("/", params=params)
        response.raise_for_status()
        return response

    async def search(self, query: str) -> dict[str, Any]:
        """Run CSE search.

        Args:
            query (str): search query.

        Returns:
            dict[str, Any]: response in JSON-format dictionary.
        """
        try:
            response = await self._search(query)
            return response.json()
        except RequestError as exc:
            _LOGGER.exception("Request error using CSE after retrying: {}", exc)
            return {"error": str(exc), "status_code": None}
        except HTTPError as exc:
            _LOGGER.exception("Error searching using CSE: {}", exc)
            return {"error": str(exc), "status_code": response.status_code}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.aclose()


    async def parse(self, response: Response) -> str:
        """Parse (article) response into readable format in string."""
        content = self.parser.handle(response.text)
        return content

import os
import time
from typing import Dict, Optional

import dotenv
import requests

dotenv.load_dotenv()

try:
    import cloudscraper  # type: ignore
except ImportError as exc:  # pragma: no cover
    cloudscraper = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

SCRAPER_TIMEOUT = float(os.getenv("SCRAPER_TIMEOUT", "15"))
SCRAPER_MAX_RETRIES = int(os.getenv("SCRAPER_MAX_RETRIES", "4"))
SCRAPER_BACKOFF = float(os.getenv("SCRAPER_BACKOFF", "1.5"))
SCRAPER_USER_AGENT = os.getenv(
    "SCRAPER_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
)
SCRAPER_ACCEPT_LANGUAGE = os.getenv("SCRAPER_ACCEPT_LANGUAGE", "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7")
SCRAPER_REFERER = os.getenv("SCRAPER_REFERER", "https://anime-sama.eu")
SCRAPER_COOKIES = os.getenv("SCRAPER_COOKIES", "")
SCRAPER_ACCEPT_ENCODING = os.getenv("SCRAPER_ACCEPT_ENCODING", "gzip, deflate")
SCRAPER_PRAGMA = os.getenv("SCRAPER_PRAGMA", "no-cache")
SCRAPER_CACHE_CONTROL = os.getenv("SCRAPER_CACHE_CONTROL", "no-cache")

_session: Optional[requests.Session] = None

INVALID_COOKIE_CHARS = {";"}


def _ensure_cloudscraper_available():
    if cloudscraper is None:
        raise RuntimeError(
            "cloudscraper doit être installé (ajoutez-le à requirements.txt) pour contourner Cloudflare"
        ) from _IMPORT_ERROR


def _parse_cookie_string(raw_cookie: str) -> Dict[str, str]:
    cookies: Dict[str, str] = {}
    for chunk in raw_cookie.split(";"):
        if "=" not in chunk:
            continue
        key, value = chunk.split("=", 1)
        key = key.strip()
        if not key:
            continue
        cookies[key] = value.strip()
    return cookies


def _build_session() -> requests.Session:
    _ensure_cloudscraper_available()
    session = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    session.headers.update(
        {
            "User-Agent": SCRAPER_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": SCRAPER_ACCEPT_LANGUAGE,
            "Accept-Encoding": SCRAPER_ACCEPT_ENCODING,
            "Pragma": SCRAPER_PRAGMA,
            "Cache-Control": SCRAPER_CACHE_CONTROL,
            "Referer": SCRAPER_REFERER,
            "Upgrade-Insecure-Requests": "1",
        }
    )

    cookies = SCRAPER_COOKIES.strip()
    if cookies:
        session.cookies.update(_parse_cookie_string(cookies))

    return session


def get_scraper_session(force_refresh: bool = False) -> requests.Session:
    global _session
    if _session is None or force_refresh:
        _session = _build_session()
    return _session


def fetch(
    url: str,
    *,
    method: str = "GET",
    timeout: Optional[float] = None,
    retries: Optional[int] = None,
    backoff: Optional[float] = None,
    **kwargs,
) -> requests.Response:
    """Perform an HTTP request with retry/backoff using the shared cloudscraper session."""

    timeout = timeout or SCRAPER_TIMEOUT
    retries = retries or SCRAPER_MAX_RETRIES
    backoff = backoff or SCRAPER_BACKOFF

    last_exception: Optional[Exception] = None

    for attempt in range(1, retries + 1):
        session = get_scraper_session()
        try:
            response = session.request(method.upper(), url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as http_err:
            last_exception = http_err
            status = http_err.response.status_code if http_err.response else None
            if status not in {403, 429} and (status is None or status < 500) or attempt == retries:
                raise
            get_scraper_session(force_refresh=True)
        except requests.RequestException as req_err:
            last_exception = req_err
            if attempt == retries:
                raise
        time.sleep(backoff ** attempt)

    if last_exception:
        raise last_exception

    raise RuntimeError(f"Impossible de récupérer l'URL {url}")

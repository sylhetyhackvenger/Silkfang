#!/usr/bin/env python3
import argparse
import asyncio
import hashlib
import io
import json
import math
import random
import re
import signal
import socket
import ssl
import sys
import tarfile
import time
import zipfile
from base64 import urlsafe_b64decode, b64decode
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag, parse_qs, urlencode, unquote

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

try:
    from curl_cffi.requests import AsyncSession
    HAS_CURL_CFFI = True
except ImportError:
    AsyncSession = None
    HAS_CURL_CFFI = False

try:
    import httpx
except ImportError:
    httpx = None

try:
    from bs4 import BeautifulSoup, Comment
except ImportError:
    print("FATAL: beautifulsoup4 is required. Install with: pip install beautifulsoup4 lxml")
    sys.exit(1)

try:
    from tldextract import extract
except ImportError:
    print("FATAL: tldextract is required. Install with: pip install tldextract")
    sys.exit(1)

try:
    import esprima
    HAS_ESPRIMA = True
except ImportError:
    esprima = None
    HAS_ESPRIMA = False

try:
    import dns.resolver
    import dns.zone
    import dns.query
    import dns.exception
    HAS_DNS = True
except ImportError:
    HAS_DNS = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
except ImportError:
    print("FATAL: rich is required. Install with: pip install rich")
    sys.exit(1)

console = Console()

TOOL_NAME = "SILKFANG"
AUTHOR = "SYLHETYHACKVENGER (THE-ERROR808)"

SEV_COLOR = {
    "critical": "bright_red",
    "high": "red",
    "medium": "yellow",
    "low": "cyan",
    "info": "white",
}

QUIET_TYPES = {
    "FETCHED", "INFO", "TECH-ID", "EXTERNAL-DOMAIN", "IMG",
    "PRELOAD", "META", "OG", "MICRODATA", "ICON", "HEARTBEAT",
    "HUD",
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Brave/122",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Brave/121",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.5",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Vivaldi/6.4",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; Applebot/0.1; +http://www.apple.com/go/applebot)",
    "curl/8.5.0",
    "curl/8.4.0",
    "curl/8.0.1",
    "python-httpx/0.27.0",
    "python-requests/2.31.0",
    "Wget/1.21.4",
    "Wget/1.21.3",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com)",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
    "TelegramBot (like TwitterBot)",
    "WhatsApp/2.23.20.0 A",
]

ACCEPT_VARIANTS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,application/xhtml+xml;q=0.9,application/xml;q=0.8,*/*;q=0.7",
    "application/json, text/plain, */*",
    "application/json",
    "text/css,*/*;q=0.1",
    "image/avif,image/webp,*/*",
    "text/html, */*; q=0.01",
    "*/*",
]

LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "en-CA,en;q=0.9,fr;q=0.8",
    "en-US,en;q=0.9,es;q=0.8",
    "en-US,en;q=0.9,de;q=0.8",
    "en-US,en;q=0.9,fr;q=0.8",
    "en-US,en;q=0.9,it;q=0.8",
    "en-US,en;q=0.9,ja;q=0.8",
    "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "en-US,en;q=0.9,pt;q=0.8",
    "en-US,en;q=0.9,nl;q=0.8",
    "en-US,en;q=0.9,ru;q=0.8",
    "en-US,en;q=0.9,ko;q=0.8",
    "en-US,en;q=0.9,pl;q=0.8",
    "en-US,en;q=0.9,tr;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8",
]

SEC_CH_UA_VARIANTS = [
    '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    '"Chromium";v="121", "Not(A:Brand";v="24", "Google Chrome";v="121"',
    '"Chromium";v="120", "Not(A:Brand";v="24", "Google Chrome";v="120"',
    '"Microsoft Edge";v="122", "Chromium";v="122", "Not(A:Brand";v="24"',
    '"Microsoft Edge";v="121", "Chromium";v="121", "Not(A:Brand";v="24"',
    '"Opera";v="107", "Chromium";v="121", "Not(A:Brand";v="24"',
    '"Brave";v="122", "Chromium";v="122", "Not(A:Brand";v="24"',
    '"Vivaldi";v="6.5", "Chromium";v="122", "Not(A:Brand";v="24"',
]

RE_URL = re.compile(r'https?://[^\s"\'<>\\`]+')
RE_PATH = re.compile(r'["\'`](/[a-zA-Z0-9_\-./?=&%]+)["\'`]')
RE_EMAIL = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
RE_PHONE = re.compile(
    r'(?<![\d\-])'
    r'(?:\+\d{1,3}[\s\-\.]?)'
    r'(?:\(?\d{2,4}\)?[\s\-\.]?)'
    r'\d{3,4}[\s\-\.]\d{3,4}'
    r'(?![\d\-])'
)
RE_WS = re.compile(r'wss?://[^\s"\'`]+')
RE_API_PATH = re.compile(r'/api/[a-zA-Z0-9_\-./]+')
RE_SOURCEMAP = re.compile(r'sourceMappingURL=([^\s*]+)')
RE_JWT = re.compile(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+')
RE_BASE64 = re.compile(r'[A-Za-z0-9+/]{40,}={0,2}')
RE_UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)
RE_MD5 = re.compile(r'\b[a-f0-9]{32}\b', re.I)
RE_SHA1 = re.compile(r'\b[a-f0-9]{40}\b', re.I)
RE_SHA256 = re.compile(r'\b[a-f0-9]{64}\b', re.I)
RE_BTC = re.compile(r'\b(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}\b')
RE_ETH = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
RE_XMR = re.compile(r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b')
RE_LTC = re.compile(r'\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b')
RE_DOGE = re.compile(r'\bD{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}\b')
RE_SOL = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
RE_LOREM = re.compile(r'lorem ipsum dolor sit amet', re.I)
RE_COMING_SOON = re.compile(r'(coming soon|under construction|staging|beta|maintenance|work in progress)', re.I)
RE_INTERNAL_ID = re.compile(r'data-(?:id|uid|user|order|product|session|token|account|tenant|customer)="([^"]+)"')
RE_AWS_S3 = re.compile(r'https?://([a-z0-9.\-]+)\.s3[.\-][a-z0-9\-]*\.?amazonaws\.com/?[^\s"\'<>]*')
RE_AZURE_BLOB = re.compile(r'https?://([a-z0-9]+)\.blob\.core\.windows\.net/?[^\s"\'<>]*')
RE_GCS = re.compile(r'https?://storage\.googleapis\.com/([a-z0-9_\-]+)')
RE_FIREBASE_STORAGE = re.compile(r'https?://firebasestorage\.googleapis\.com/v0/b/([a-z0-9\-]+)')
RE_GRAPHQL_ENDPOINT = re.compile(r'["\'](https?://[^"\']*/graphql[^"\']*)["\']')
RE_INTERNAL_IP = re.compile(r'\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b')
RE_SSN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
RE_CREDIT_CARD = re.compile(r'\b(?:\d[ -]*?){13,19}\b')
RE_IBAN = re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{4,30}\b')

RE_GA_UA = re.compile(r'UA-\d{4,10}-\d{1,4}')
RE_GA4 = re.compile(r'G-[A-Z0-9]{8,12}')
RE_GTM = re.compile(r'GTM-[A-Z0-9]{4,8}')
RE_FB_PIXEL = re.compile(r'fbq\([\'"]init[\'"],\s*[\'"](\d{10,20})[\'"]')
RE_HOTJAR = re.compile(r'hj\([\'"]\w+[\'"],\s*(\d+)')
RE_SEGMENT = re.compile(r'analytics\.load\([\'"]([A-Za-z0-9]{20,})')
RE_SENTRY = re.compile(r'https://([0-9a-f]{32})@([a-z0-9.\-]+)/?(\d+)?')
RE_INTERCOM = re.compile(r'intercomSettings\s*=\s*{[^}]*app_id[\'"]\s*:\s*[\'"]([a-z0-9]{8})')
RE_DRIFT = re.compile(r'drift\.load\([\'"]([a-z0-9]{16})')
RE_CRISP = re.compile(r'CRISP_WEBSITE_ID\s*=\s*[\'"]([a-f0-9\-]{36})')
RE_ZENDESK = re.compile(r'zE\([\'"]init[\'"],\s*[\'"]([a-f0-9\-]{36})')
RE_RECAPTCHA = re.compile(r'data-sitekey="(6L[a-zA-Z0-9_\-]{38})"')
RE_HCAPTCHA = re.compile(r'data-sitekey="([a-f0-9\-]{36})"')
RE_TURNSTILE = re.compile(r'data-sitekey="(0x4[A-Za-z0-9_\-]{30,})"')
RE_STRIPE_PK = re.compile(r'\b(pk_(?:test|live)_[0-9a-zA-Z]{20,})')
RE_STRIPE_SK = re.compile(r'\b(sk_(?:test|live)_[0-9a-zA-Z]{20,})')
RE_PAYPAL = re.compile(r'business=([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+)')
RE_SQUARE = re.compile(r'sq0[a-z]{3}-[0-9A-Za-z_\-]{22,}')
RE_BRAINTREE = re.compile(r'braintree[^"\']{0,30}tokenizationKey["\']?\s*[:=]\s*["\']([a-z0-9]{32})')
RE_ADYEN = re.compile(r'adyen[^"\']{0,30}clientKey["\']?\s*[:=]\s*["\']([a-z0-9]{16,})')
RE_FIREBASE = re.compile(r'apiKey["\']?\s*:\s*["\']([A-Za-z0-9_\-]{30,})["\'][^}]*projectId["\']?\s*:\s*["\']([a-z0-9\-]+)', re.I)
RE_FIREBASE_DB = re.compile(r'https?://([a-z0-9\-]+)\.firebaseio\.com')
RE_SUPABASE = re.compile(r'https://([a-z0-9]{20})\.supabase\.co')
RE_SUPABASE_KEY = re.compile(r'sb_[a-z0-9_\-]{30,}')
RE_AUTH0 = re.compile(r'([a-z0-9\-]+)\.auth0\.com')
RE_OKTA = re.compile(r'([a-z0-9\-]+)\.okta\.com')
RE_COGNITO = re.compile(r'([a-z0-9\-]+)\.auth\.[a-z0-9\-]+\.amazoncognito\.com')
RE_CLERK = re.compile(r'clerk\.([a-z0-9\-]+)\.(?:accounts|clerk)\.dev')
RE_FIREBASE_AUTH = re.compile(r'([a-z0-9\-]+)\.firebaseapp\.com')
RE_AUTH0_CLIENT = re.compile(r'client_id["\']?\s*[:=]\s*["\']([A-Za-z0-9]{32})["\'][^}]*domain["\']?\s*[:=]\s*["\']([a-z0-9\-]+\.auth0\.com)')
RE_MAPBOX = re.compile(r'\b(pk\.[A-Za-z0-9_\-]{60,})')
RE_MAPBOX_SK = re.compile(r'\b(sk\.[A-Za-z0-9_\-]{60,})')
RE_GOOGLE_MAPS = re.compile(r'AIza[0-9A-Za-z_\-]{35}')
RE_HERE_MAPS = re.compile(r'here[^"\']{0,20}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9_\-]{43})')
RE_PUSHER = re.compile(r'pusher[^"\']{0,20}key["\']?\s*[:=]\s*["\']([a-f0-9]{20})')
RE_PUBNUB = re.compile(r'pub(?:-cbn|-key)?["\']?\s*[:=]\s*["\'](pub-[a-z0-9\-]+)')
RE_ABLY = re.compile(r'ably[^"\']{0,20}key["\']?\s*[:=]\s*["\']([A-Za-z0-9_\-\.]{20,})')
RE_ALGOLIA = re.compile(r'algolia[^"\']{0,30}appId["\']?\s*:\s*["\']([A-Z0-9]{10})')
RE_ALGOLIA_KEY = re.compile(r'algolia[^"\']{0,30}apiKey["\']?\s*:\s*["\']([a-f0-9]{32})')
RE_TYPESENSE = re.compile(r'typesense[^"\']{0,30}apiKey["\']?\s*:\s*["\']([A-Za-z0-9]{20,})')
RE_MEILISEARCH = re.compile(r'meilisearch[^"\']{0,30}apiKey["\']?\s*:\s*["\']([A-Za-z0-9_\-]{30,})')
RE_LAUNCHDARKLY = re.compile(r'client-side-id["\']?\s*:\s*["\']([a-f0-9\-]{36})')
RE_OPTIMIZELY = re.compile(r'optimizely\.com/js/(\d{8,15})')
RE_DATADOG_RUM = re.compile(r'datadog-rum[^"\']{0,30}applicationId["\']?\s*:\s*["\']([a-f0-9\-]+)')
RE_NEW_RELIC = re.compile(r'NREUM\.init\(\{\s*licenseKey:\s*["\']([a-z0-9]{40})')
RE_ROLLBAR = re.compile(r'rollbar\.init\(\{[^}]*accessToken:\s*["\']([a-f0-9]{32})')
RE_HONEYBADGER = re.compile(r'Honeybadger\.configure\(\{[^}]*apiKey:\s*["\']([a-f0-9]{8})')
RE_BUGSNAG = re.compile(r'bugsnag[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([a-f0-9]{32})')
RE_SENTRY_DSN = re.compile(r'sentry[^"\']{0,30}dsn["\']?\s*[:=]\s*["\']([^"\']+)')
RE_RAYGUN = re.compile(r'raygun[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9_\-]{20,})')
RE_LOGRocket = re.compile(r'logrocket[^"\']{0,30}appId["\']?\s*[:=]\s*["\']([a-z0-9\/]+)')
RE_FULLSTORY = re.compile(r'fullstory[^"\']{0,30}org["\']?\s*[:=]\s*["\']([A-Z0-9]{8,})')
RE_AMPLITUDE = re.compile(r'amplitude[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([a-f0-9]{32})')
RE_MIXPANEL = re.compile(r'mixpanel[^"\']{0,30}token["\']?\s*[:=]\s*["\']([a-f0-9]{32})')
RE_POSTHOG = re.compile(r'posthog[^"\']{0,30}api_key["\']?\s*[:=]\s*["\'](phc_[A-Za-z0-9]{40,})')
RE_PLAUSIBLE = re.compile(r'plausible[^"\']{0,30}domain["\']?\s*[:=]\s*["\']([a-z0-9.\-]+)')
RE_MATOMO = re.compile(r'matomo[^"\']{0,30}siteId["\']?\s*[:=]\s*["\'](\d+)')
RE_UMAMI = re.compile(r'umami[^"\']{0,30}websiteId["\']?\s*[:=]\s*["\']([a-f0-9\-]{36})')
RE_CLARITY = re.compile(r'clarity[^"\']{0,30}projectId["\']?\s*[:=]\s*["\']([a-z0-9]{10})')
RE_HEAP = re.compile(r'heap[^"\']{0,30}appId["\']?\s*[:=]\s*["\'](\d+)')
RE_SEGMENT_WRITE = re.compile(r'segment[^"\']{0,30}writeKey["\']?\s*[:=]\s*["\']([A-Za-z0-9]{32})')
RE_RUDDERSTACK = re.compile(r'rudderstack[^"\']{0,30}writeKey["\']?\s*[:=]\s*["\']([A-Za-z0-9]{32})')
RE_MPARTICLE = re.compile(r'mparticle[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([a-z0-9]{24})')
RE_TEALIUM = re.compile(r'tealium[^"\']{0,30}account["\']?\s*[:=]\s*["\']([a-z0-9]{6,})')
RE_ONETRUST = re.compile(r'onetrust[^"\']{0,30}domainScript["\']?\s*[:=]\s*["\']([a-f0-9\-]{36})')
RE_COOKIEBOT = re.compile(r'cookiebot[^"\']{0,30}cbID["\']?\s*[:=]\s*["\']([a-f0-9\-]{36})')

RE_POSTMESSAGE = re.compile(r'postMessage\s*\(([^)]*)\)')
RE_ADDEVENTMESSAGE = re.compile(r'addEventListener\s*\(\s*[\'"]message[\'"]')
RE_ORIGIN_CHECK = re.compile(r'(?:event|e|ev)\.origin')
RE_DANGEROUS_SINKS = re.compile(r'\b(innerHTML|outerHTML|eval|Function|document\.write|document\.writeln|setTimeout|setInterval)\b')
RE_STORAGE_WRITE = re.compile(r'(?:localStorage|sessionStorage)\.setItem\s*\(\s*[\'"]([^\'"]+)[\'"]')
RE_FETCH_CALL = re.compile(r'(?:fetch|axios\.(?:get|post|put|delete|patch))\s*\(\s*[\'"`]([^\'"`]+)[\'"`]')
RE_REQUIRE_IMPORT = re.compile(
    r'(?:require\s*\(\s*|import\s+[^;]+?\bfrom\s+|import\s*\(\s*|import\s+)[\'"]([^\'"]+)[\'"]'
)
RE_CLIENT_ID = re.compile(r'client_id=([A-Za-z0-9_\-\.]{10,})')
RE_RESET_TOKEN = re.compile(r'(?:reset|token|recover)[_-]?token[=:]\s*[\'"]?([A-Za-z0-9_\-]{20,})', re.I)
RE_CSRF_HINT = re.compile(r'(?:csrf|xsrf|authenticity)[_-]?token', re.I)

RE_IDOR_NUM = re.compile(r'^\d{1,7}$')
RE_IDOR_UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

SENSITIVE_COMMENT_HINTS = re.compile(
    r'\b(todo|fixme|hack|bug|password|passwd|pwd|secret|token|api[_\-]?key|'
    r'admin|internal|debug|staging|backup|private|hidden|vulnerable|'
    r'xss|sqli|injection|bypass|auth|credential|apikey|aws|gcp|azure|'
    r'client[_\-]?secret|private[_\-]?key|salt|hash|jwt|oauth|bearer|'
    r'ssh|pem|cert|keystore|htpasswd|shadow|sudo|root)\b',
    re.IGNORECASE,
)

SECRET_PATTERNS = [
    (r'AKIA[0-9A-Z]{16}', "AWS-KEY"),
    (r'ASIA[0-9A-Z]{16}', "AWS-STS"),
    (r'AGPA[0-9A-Z]{16}', "AWS-IAM"),
    (r'AIDA[0-9A-Z]{16}', "AWS-USER"),
    (r'AROA[0-9A-Z]{16}', "AWS-ROLE"),
    (r'sk_live_[0-9a-zA-Z]{24,}', "STRIPE-LIVE"),
    (r'pk_live_[0-9a-zA-Z]{24,}', "STRIPE-PK"),
    (r'sk_test_[0-9a-zA-Z]{24,}', "STRIPE-TEST"),
    (r'rk_live_[0-9a-zA-Z]{24,}', "STRIPE-RESTRICTED"),
    (r'AIza[0-9A-Za-z_\-]{35}', "GOOGLE-API"),
    (r'xox[baprs]-[0-9a-zA-Z\-]{10,}', "SLACK-TOKEN"),
    (r'xoxa-[0-9a-zA-Z\-]{10,}', "SLACK-APP"),
    (r'ghp_[0-9A-Za-z]{36}', "GITHUB-PAT"),
    (r'gho_[0-9A-Za-z]{36}', "GITHUB-OAUTH"),
    (r'ghu_[0-9A-Za-z]{36}', "GITHUB-USER"),
    (r'ghs_[0-9A-Za-z]{36}', "GITHUB-SERVER"),
    (r'ghr_[0-9A-Za-z]{36}', "GITHUB-REFRESH"),
    (r'github_pat_[0-9A-Za-z_]{82}', "GITHUB-FINE"),
    (r'glpat-[0-9A-Za-z_\-]{20}', "GITLAB-PAT"),
    (r'glrt-[0-9A-Za-z_\-]{20}', "GITLAB-RUNNER"),
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----', "PRIVATE-KEY"),
    (r'-----BEGIN CERTIFICATE-----', "CERTIFICATE"),
    (r'SG\.[0-9A-Za-z_\-]{22}\.[0-9A-Za-z_\-]{43}', "SENDGRID"),
    (r'key-[0-9a-zA-Z]{32}', "MAILGUN"),
    (r'mailgun[^"\']{0,30}key["\']?\s*[:=]\s*["\']([a-z0-9]{32})', "MAILGUN-KEY"),
    (r'dop_v1_[a-f0-9]{64}', "DIGITALOCEAN"),
    (r'doo_v1_[a-f0-9]{64}', "DIGITALOCEAN-OAUTH"),
    (r'LTAI[A-Za-z0-9]{12,20}', "ALIBABA"),
    (r'cloudinary://\d{15}:[A-Za-z0-9_\-]{27,}@[a-z0-9]+', "CLOUDINARY"),
    (r'SK[0-9a-f]{32}', "TWILIO"),
    (r'AC[a-f0-9]{32}', "TWILIO-SID"),
    (r'hf_[A-Za-z0-9]{34}', "HUGGINGFACE"),
    (r'sk-ant-[A-Za-z0-9\-_]{90,}', "ANTHROPIC"),
    (r'sk-[A-Za-z0-9]{48}', "OPENAI"),
    (r'sk-proj-[A-Za-z0-9_\-]{48,}', "OPENAI-PROJECT"),
    (r'(?:"type"\s*:\s*"service_account")', "GCP-SA"),
    (r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}', "DISCORD"),
    (r'\d{8,10}:[a-zA-Z0-9_-]{35}', "TELEGRAM"),
    (r'sq0[a-z]{3}-[0-9A-Za-z_\-]{22,}', "SQUARE"),
    (r'eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}', "JWT"),
    (r'[a-zA-Z0-9_-]{32,45}', "HIGH-ENTROPY"),
    (r'lin_api_[A-Za-z0-9]{40}', "LINEAR"),
    (r'notion[^"\']{0,30}secret["\']?\s*[:=]\s*["\']([A-Za-z0-9]{43})', "NOTION"),
    (r'airtable[^"\']{0,30}key["\']?\s*[:=]\s*["\'](key[A-Za-z0-9]{14})', "AIRTABLE"),
    (r'pat[A-Za-z0-9]{14}\.[A-Za-z0-9]{64}', "AIRTABLE-PAT"),
    (r'figd_[A-Za-z0-9_\-]{40,}', "FIGMA"),
    (r'shp(at|ca|pa)_[a-f0-9]{32}', "SHOPIFY"),
    (r'shpat_[a-f0-9]{32}', "SHOPIFY-AT"),
    (r'shpss_[a-f0-9]{32}', "SHOPIFY-SS"),
    (r'shpca_[a-f0-9]{32}', "SHOPIFY-CA"),
    (r'shppa_[a-f0-9]{32}', "SHOPIFY-PA"),
    (r'cohere[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9]{40})', "COHERE"),
    (r'replicate[^"\']{0,30}token["\']?\s*[:=]\s*["\'](r8_[A-Za-z0-9]{37})', "REPLICATE"),
    (r'sk-or-v1-[a-f0-9]{64}', "OPENROUTER"),
    (r'gsk_[A-Za-z0-9]{52}', "GROQ"),
    (r'xai-[A-Za-z0-9]{80}', "XAI"),
    (r'pplx-[A-Za-z0-9]{48}', "PERPLEXITY"),
    (r'claude[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9_\-]{40,})', "CLAUDE"),
    (r'mistral[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9]{32})', "MISTRAL"),
    (r'deepgram[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9]{40})', "DEEPGRAM"),
    (r'elevenlabs[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([A-Za-z0-9]{32})', "ELEVENLABS"),
    (r'assemblyai[^"\']{0,30}apiKey["\']?\s*[:=]\s*["\']([a-f0-9]{32})', "ASSEMBLYAI"),
    (r'sk_live_[a-f0-9]{32}', "CLERK"),
    (r'sec_[A-Za-z0-9]{40}', "SUPABASE-SECRET"),
    (r'sb_[a-z0-9_\-]{30,}', "SUPABASE-KEY"),
    (r'vercel_[A-Za-z0-9]{24}', "VERCEL"),
    (r'netlify_[A-Za-z0-9]{40}', "NETLIFY"),
    (r'fly_[A-Za-z0-9]{40}', "FLY"),
    (r'railway_[A-Za-z0-9]{40}', "RAILWAY"),
    (r'render_[A-Za-z0-9]{40}', "RENDER"),
    (r'heroku_[A-Za-z0-9]{32}', "HEROKU"),
    (r'datadog_[A-Za-z0-9]{40}', "DATADOG"),
    (r'pagerduty_[A-Za-z0-9]{20}', "PAGERDUTY"),
    (r'opsgenie_[A-Za-z0-9]{40}', "OPSGENIE"),
    (r'slack_[A-Za-z0-9]{40}', "SLACK"),
    (r'discord_[A-Za-z0-9]{40}', "DISCORD-WEBHOOK"),
    (r'webhook[^"\']{0,30}https://discord\.com/api/webhooks/(\d+/[A-Za-z0-9_\-]+)', "DISCORD-HOOK"),
    (r'webhook[^"\']{0,30}https://hooks\.slack\.com/services/([A-Za-z0-9/]+)', "SLACK-HOOK"),
]

TARGET_TAGS = [
    ("a", "href"), ("area", "href"), ("link", "href"), ("script", "src"),
    ("form", "action"), ("img", "src"), ("iframe", "src"), ("frame", "src"),
    ("embed", "src"), ("object", "data"), ("source", "src"), ("track", "src"),
    ("input", "formaction"), ("button", "formaction"), ("video", "poster"),
    ("audio", "src"), ("video", "src"), ("picture", "src"),
    ("use", "href"), ("image", "href"), ("base", "href"),
]
DATA_ATTRS = [
    "data-href", "data-url", "data-src", "data-action",
    "data-endpoint", "data-api", "data-page", "data-load",
    "data-link", "data-target", "data-route", "data-path",
    "data-redirect", "data-location", "data-destination", "data-origin",
]

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp", ".tif", ".tiff",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".sfnt",
    ".mp4", ".mp3", ".avi", ".mov", ".wav", ".ogg", ".webm", ".flv", ".m4a", ".m4v",
    ".mkv", ".wmv", ".flac", ".aac", ".opus", ".m3u8", ".ts",
    ".pdf", ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".zst",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".iso", ".dmg", ".apk", ".msi",
    ".deb", ".rpm", ".pkg", ".img", ".vmdk", ".ova",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp",
    ".sql", ".db", ".sqlite", ".sqlite3", ".mdb",
    ".psd", ".ai", ".indd", ".sketch", ".fig", ".xd",
    ".stl", ".obj", ".fbx", ".blend", ".3ds",
    ".epub", ".mobi", ".azw", ".azw3",
    ".cer", ".crt", ".der", ".p12", ".pfx", ".pem", ".key", ".keystore", ".jks",
}

DEEP_ASSET_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff",
    ".pdf", ".docx", ".xlsx", ".pptx", ".zip", ".tar", ".tgz", ".gz",
    ".svg", ".ttf", ".otf", ".woff", ".woff2",
    ".doc", ".xls", ".ppt", ".odt", ".ods", ".odp",
    ".epub", ".mobi", ".sqlite", ".db",
    ".cer", ".crt", ".pem", ".key",
}

SENSITIVE_PATHS = [
    "/.env", "/.env.local", "/.env.production", "/.env.backup", "/.env.dev",
    "/.env.staging", "/.env.test", "/.env.old", "/.env.bak", "/.env.example",
    "/.git/config", "/.git/HEAD", "/.git/logs/HEAD", "/.git/index", "/.gitignore",
    "/.git/refs/heads/master", "/.git/refs/heads/main", "/.git/packed-refs",
    "/.svn/entries", "/.svn/wc.db", "/.hg/", "/.bzr/", "/.DS_Store",
    "/wp-login.php", "/wp-admin/", "/wp-json/wp/v2/users", "/xmlrpc.php",
    "/wp-config.php", "/wp-config.php.bak", "/wp-config.php~", "/wp-content/debug.log",
    "/wp-content/uploads/", "/wp-includes/version.php",
    "/administrator/", "/admin/", "/admin", "/admin.php", "/admin.html",
    "/login", "/login.php", "/login.html", "/signin", "/signin.php",
    "/dashboard", "/console", "/panel", "/cpanel", "/webadmin", "/manager",
    "/api", "/api/", "/api/v1", "/api/v2", "/api/v3", "/api/v4",
    "/api/docs", "/api/swagger.json", "/api/openapi.json", "/api/swagger.yaml",
    "/api/graphql", "/api/users", "/api/admin", "/api/config", "/api/health",
    "/api/status", "/api/me", "/api/profile", "/api/token", "/api/auth",
    "/graphql", "/graphiql", "/altair", "/playground", "/voyager", "/apollo",
    "/swagger-ui/", "/swagger-ui.html", "/swagger-ui/index.html",
    "/swagger.json", "/swagger.yaml", "/openapi.json", "/openapi.yaml",
    "/api-docs", "/api-docs/", "/docs", "/redoc", "/redoc.html",
    "/actuator", "/actuator/env", "/actuator/health", "/actuator/mappings",
    "/actuator/beans", "/actuator/heapdump", "/actuator/threaddump",
    "/actuator/metrics", "/actuator/loggers", "/actuator/info", "/actuator/auditevents",
    "/.well-known/security.txt", "/.well-known/openid-configuration",
    "/.well-known/change-password", "/.well-known/host-meta",
    "/.well-known/webfinger", "/.well-known/assetlinks.json",
    "/.well-known/apple-app-site-association", "/security.txt",
    "/server-status", "/server-info", "/phpinfo.php", "/info.php", "/php.php",
    "/test.php", "/debug.php", "/config.php", "/config.php.bak",
    "/config.json", "/config.yaml", "/config.yml", "/settings.py",
    "/web.config", "/app.config", "/appsettings.json", "/.htaccess", "/.htpasswd",
    "/backup.zip", "/backup.sql", "/backup.tar.gz", "/backup.rar", "/backup.7z",
    "/db.sql", "/dump.sql", "/site.tar.gz", "/www.zip", "/site.zip", "/db.sqlite",
    "/robots.txt", "/sitemap.xml", "/sitemap_index.xml", "/sitemap-news.xml",
    "/crossdomain.xml", "/clientaccesspolicy.xml", "/humans.txt",
    "/trace", "/debug", "/test", "/dev", "/staging", "/preview", "/old", "/new",
    "/jenkins/", "/.github/workflows/", "/.github/", "/Dockerfile",
    "/docker-compose.yml", "/docker-compose.yaml", "/.dockerignore",
    "/package.json", "/package-lock.json", "/yarn.lock", "/pnpm-lock.yaml",
    "/composer.json", "/composer.lock", "/Gemfile", "/Gemfile.lock",
    "/requirements.txt", "/Pipfile", "/Pipfile.lock", "/pyproject.toml",
    "/go.mod", "/go.sum", "/Cargo.toml", "/Cargo.lock", "/pom.xml",
    "/build.gradle", "/build.gradle.kts", "/Makefile", "/CMakeLists.txt",
    "/ads.txt", "/app-ads.txt", "/manifest.json", "/site.webmanifest",
    "/feed", "/rss", "/atom.xml", "/blog/feed", "/news/feed",
    "/sitemap-images.xml", "/sitemap-video.xml", "/status", "/health",
    "/healthz", "/readyz", "/livez", "/version", "/versions", "/changelog",
    "/CHANGELOG.md", "/README.md", "/LICENSE", "/SECURITY.md",
    "/.circleci/config.yml", "/.gitlab-ci.yml", "/.travis.yml", "/azure-pipelines.yml",
    "/.vscode/", "/.idea/", "/.editorconfig", "/.eslintrc", "/.eslintrc.json",
    "/.prettierrc", "/.babelrc", "/.browserslistrc", "/tsconfig.json",
    "/gulpfile.js", "/Gruntfile.js", "/webpack.config.js", "/vite.config.js",
    "/next.config.js", "/nuxt.config.js", "/svelte.config.js", "/astro.config.mjs",
]

HIGH_RISK_SENSITIVE = {
    "/.env", "/.env.local", "/.env.production", "/.env.backup", "/.env.dev",
    "/.env.staging", "/.env.test", "/.env.old", "/.env.bak",
    "/.git/config", "/.git/HEAD", "/.git/logs/HEAD", "/.git/index",
    "/.git/refs/heads/master", "/.git/refs/heads/main", "/.git/packed-refs",
    "/.svn/entries", "/.svn/wc.db", "/.hg/", "/.bzr/", "/.DS_Store",
    "/wp-config.php", "/wp-config.php.bak", "/wp-config.php~", "/wp-content/debug.log",
    "/config.php", "/config.php.bak", "/config.json", "/config.yaml", "/config.yml",
    "/web.config", "/app.config", "/appsettings.json", "/.htaccess", "/.htpasswd",
    "/backup.zip", "/backup.sql", "/backup.tar.gz", "/backup.rar", "/backup.7z",
    "/db.sql", "/dump.sql", "/site.tar.gz", "/www.zip", "/site.zip", "/db.sqlite",
    "/actuator/env", "/actuator/heapdump", "/actuator/threaddump",
    "/actuator/beans", "/actuator/mappings", "/actuator/metrics",
    "/server-status", "/server-info", "/phpinfo.php", "/info.php", "/php.php",
    "/test.php", "/debug.php",
    "/Dockerfile", "/docker-compose.yml", "/docker-compose.yaml", "/.dockerignore",
    "/package.json", "/package-lock.json", "/yarn.lock", "/pnpm-lock.yaml",
    "/composer.json", "/composer.lock", "/Gemfile", "/Gemfile.lock",
    "/requirements.txt", "/Pipfile", "/Pipfile.lock", "/pyproject.toml",
    "/go.mod", "/go.sum", "/Cargo.toml", "/Cargo.lock", "/pom.xml",
    "/build.gradle", "/build.gradle.kts", "/Makefile", "/CMakeLists.txt",
    "/.github/workflows/", "/.circleci/config.yml", "/.gitlab-ci.yml",
    "/.travis.yml", "/azure-pipelines.yml",
    "/.vscode/", "/.idea/",
    "/settings.py", "/.eslintrc", "/.eslintrc.json", "/.prettierrc",
    "/.babelrc", "/tsconfig.json", "/webpack.config.js", "/vite.config.js",
    "/next.config.js", "/nuxt.config.js", "/svelte.config.js", "/astro.config.mjs",
}

FUZZ_PATHS = [
    "admin", "api", "backup", "backups", "config", "db", "dev", "docs",
    "download", "downloads", "files", "internal", "login", "logs", "old", "private",
    "prod", "production", "public", "secret", "secrets", "staging", "test", "tests",
    "tmp", "temp", "upload", "uploads", "user", "users", "v1", "v2", "v3", "www",
    "assets", "static", "media", "images", "img", "css", "js", "fonts",
    "app", "application", "auth", "account", "accounts", "billing", "payments",
    "checkout", "cart", "order", "orders", "invoice", "invoices", "subscription",
    "profile", "settings", "preferences", "maintenance", "enterprise", "partner",
    "partners", "affiliate", "affiliates", "forgot", "reset", "recover", "mfa",
    "2fa", "otp", "verify", "verification", "register", "signup", "signin",
    "sitemap", "robots", "swagger", "redoc", "graphql", "playground", "apollo",
    "cgi-bin", "phpmyadmin", "pma", "mysql", "adminer", "webmail", "roundcube",
    "jenkins", "gitlab", "git", "svn", "nexus", "sonar", "sonarqube", "grafana",
    "kibana", "prometheus", "alertmanager", "traefik", "consul", "vault",
    "portainer", "rancher", "kubernetes", "k8s", "docker", "registry", "harbor",
    "monitor", "monitoring", "metrics", "stats", "analytics", "reports",
    "export", "import", "migrate", "migration", "sync", "webhook", "webhooks",
    "callback", "callbacks", "oauth", "saml", "sso", "ldap", "cas", "jwt",
    "debug", "trace", "profiler", "phpinfo", "info", "status", "health", "healthz",
    "version", "versions", "changelog", "release", "releases", "build", "builds",
]

PAGINATION_KEYS = (
    "page", "p", "pg", "offset", "start", "from", "pgno", "pageNo",
    "pageNum", "page_num", "pageno", "pageIndex", "page_index",
    "skip", "cursor", "after", "before", "index", "pos", "position",
    "n", "num", "no", "count", "limit", "per_page", "perpage", "size",
)
NON_PAGINATION_KEYS = {
    "locale", "lang", "language", "currency", "theme", "color", "tz", "timezone",
    "format", "version", "v", "ver", "ref", "source", "utm_source",
    "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "fbclid",
    "msclkid", "ref_src", "ref_url", "share", "share_token",
}

SEC_HEADERS = {
    "Strict-Transport-Security": "HSTS",
    "Content-Security-Policy": "CSP",
    "Content-Security-Policy-Report-Only": "CSP-RO",
    "X-Frame-Options": "XFO",
    "X-Content-Type-Options": "XCTO",
    "Referrer-Policy": "REF",
    "Permissions-Policy": "PERM",
    "Feature-Policy": "FEAT-POL",
    "Cross-Origin-Opener-Policy": "COOP",
    "Cross-Origin-Embedder-Policy": "COEP",
    "Cross-Origin-Resource-Policy": "CORP",
    "X-XSS-Protection": "XSS",
    "X-Permitted-Cross-Domain-Policies": "XPCDP",
    "X-Download-Options": "XDO",
    "X-DNS-Prefetch-Control": "XDPC",
    "Expect-CT": "EXPECT-CT",
    "Clear-Site-Data": "CSD",
    "Cache-Control": "CACHE",
    "Pragma": "PRAGMA",
    "Expires": "EXPIRES",
    "X-UA-Compatible": "XUA",
    "X-Robots-Tag": "ROBOTS",
    "X-Content-Duration": "XCD",
    "X-Content-Security-Policy": "XCSP",
    "X-WebKit-CSP": "XWCSP",
    "Public-Key-Pins": "PKP",
    "Public-Key-Pins-Report-Only": "PKP-RO",
    "Alt-Svc": "ALT-SVC",
    "NEL": "NEL",
    "Report-To": "REPORT-TO",
    "Server-Timing": "SRV-TIMING",
    "Timing-Allow-Origin": "TIMING-ORIGIN",
    "X-Edge-Request-ID": "EDGE-REQ",
    "X-Varnish": "VARNISH",
    "X-Cache": "XCACHE",
    "X-Cache-Hits": "XCACHE-HITS",
    "X-Served-By": "XSRV",
    "X-Timer": "XTIMER",
    "CF-Ray": "CF-RAY",
    "CF-Cache-Status": "CF-CACHE",
    "X-Akamai-Transformed": "AKAMAI",
    "X-Amz-Cf-Id": "AMZ-CF",
    "X-Amz-Cf-Pop": "AMZ-POP",
    "X-Fastly-Request-Id": "FASTLY",
    "X-Sucuri-Id": "SUCURI",
    "X-Iinfo": "IINFO",
    "X-Powered-By": "XPB",
    "X-AspNet-Version": "ASPNET",
    "X-AspNetMvc-Version": "ASPNETMVC",
    "X-Generator": "GENERATOR",
    "X-Drupal-Cache": "DRUPAL",
    "X-Drupal-Dynamic-Cache": "DRUPAL-DYN",
    "X-Varnish-Cache": "VARNISH-CACHE",
    "X-Backend-Server": "BACKEND",
    "X-Forwarded-For": "XFF",
    "X-Forwarded-Host": "XFH",
    "X-Forwarded-Proto": "XFP",
    "X-Real-IP": "XREAL",
    "X-Original-URL": "XOURI",
    "X-Rewrite-URL": "XRURI",
    "X-HTTP-Method-Override": "XMETH",
    "X-Request-ID": "XREQ",
    "X-Correlation-ID": "XCORR",
    "X-Trace-ID": "XTRACE",
    "X-Span-ID": "XSPAN",
    "X-B3-TraceId": "B3-TRACE",
    "X-B3-SpanId": "B3-SPAN",
    "Traceparent": "W3C-TRACE",
    "Tracestate": "W3C-STATE",
    "Server": "SRV",
    "Via": "VIA",
    "Age": "AGE",
    "ETag": "ETAG",
    "Last-Modified": "LASTMOD",
    "Accept-Ranges": "RANGES",
    "Content-Range": "CRANGE",
    "Content-Location": "CLOC",
    "Content-Disposition": "CDISP",
    "Content-Language": "CLANG",
    "Vary": "VARY",
    "DNT": "DNT",
    "Tk": "TK",
}

LIB_VERSION_PATTERNS = {
    "jquery": re.compile(r'jquery[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "jquery-ui": re.compile(r'jquery-ui[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "jquery-mobile": re.compile(r'jquery\.mobile[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "bootstrap": re.compile(r'bootstrap[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "foundation": re.compile(r'foundation[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "bulma": re.compile(r'bulma[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "tailwind": re.compile(r'tailwind[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "react": re.compile(r'react[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "react-dom": re.compile(r'react-dom[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "redux": re.compile(r'redux[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "vue": re.compile(r'vue[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "vuex": re.compile(r'vuex[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "angular": re.compile(r'angular[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "svelte": re.compile(r'svelte[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "ember": re.compile(r'ember[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "backbone": re.compile(r'backbone[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "knockout": re.compile(r'knockout[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "lodash": re.compile(r'lodash[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "underscore": re.compile(r'underscore[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "moment": re.compile(r'moment[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "dayjs": re.compile(r'dayjs[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "d3": re.compile(r'd3[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "chart.js": re.compile(r'chart(?:\.min)?[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "three": re.compile(r'three[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "gsap": re.compile(r'gsap[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "axios": re.compile(r'axios[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "socket.io": re.compile(r'socket\.io[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "handlebars": re.compile(r'handlebars[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "mustache": re.compile(r'mustache[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "requirejs": re.compile(r'require(?:\.min)?[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "modernizr": re.compile(r'modernizr[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "popper": re.compile(r'popper[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "alpine": re.compile(r'alpine[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
    "htmx": re.compile(r'htmx[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
}

WAF_SIGNATURES = {
    "Cloudflare": [("server", "cloudflare"), ("cf-ray", None), ("cf-cache-status", None)],
    "Akamai": [("server", "akamaighost"), ("x-akamai-transformed", None)],
    "Incapsula": [("x-iinfo", None), ("incap_ses", None), ("visid_incap", None)],
    "Sucuri": [("x-sucuri-id", None), ("server", "sucuri")],
    "AWS CloudFront": [("x-amz-cf-id", None), ("via", "cloudfront")],
    "AWS WAF": [("x-amzn-requestid", None), ("x-amzn-trace-id", None)],
    "Fastly": [("x-fastly-request-id", None), ("x-served-by", "cache-")],
    "F5 BIG-IP": [("server", "big-ip"), ("x-wa-info", None)],
    "Barracuda": [("server", "barracuda")],
    "ModSecurity": [("server", "mod_security"), ("x-mod-security", None)],
    "Imperva": [("x-cdn", "imperva"), ("x-iinfo", None)],
    "DDoS-Guard": [("server", "ddos-guard")],
    "FortiWeb": [("server", "fortiweb"), ("fortiweb", None)],
    "Citrix NetScaler": [("via", "ns-cache"), ("x-ns-cache", None)],
    "Radware": [("x-rdwr", None), ("server", "radware")],
    "Wallarm": [("server", "nginx-wallarm"), ("x-wallarm", None)],
    "Signal Sciences": [("x-sigsci-requestid", None), ("x-sigsci-tags", None)],
    "Rapid7": [("x-rapid7", None), ("server", "rapid7")],
    "StackPath": [("server", "stackpath"), ("x-sp-cache", None)],
    "KeyCDN": [("server", "keycdn"), ("x-cache", "keycdn")],
    "BunnyCDN": [("server", "bunnycdn"), ("cdn-pullzone", None)],
    "Gcore": [("server", "gcore"), ("x-gcore", None)],
    "Qrator": [("server", "qrator"), ("x-qrator", None)],
    "Vercel": [("server", "vercel"), ("x-vercel-id", None)],
    "Netlify": [("server", "netlify"), ("x-nf-request-id", None)],
    "Deno Deploy": [("server", "deno"), ("x-deno", None)],
    "Cloudflare Workers": [("server", "cloudflare"), ("cf-worker", None)],
    "Fastly Compute": [("x-fastly-request-id", None), ("x-compute-request", None)],
}

BOT_CHALLENGE_SIGNATURES = {
    "cloudflare": ["cf-mitigated", "just a moment", "__cf_chl", "checking your browser", "cf_chl_opt"],
    "datadome": ["datadome", "captcha-delivery", "dd_cookie"],
    "akamai": ["reference #", "akamai ghost", "_abck"],
    "perimeterx": ["_px", "perimeterx", "px-captcha"],
    "kasada": ["kasada", "x-kpsdk-ct", "x-kpsdk-cd"],
    "hcaptcha": ["hcaptcha", "h-captcha"],
    "recaptcha": ["recaptcha", "g-recaptcha", "grecaptcha"],
    "turnstile": ["turnstile", "cf-turnstile"],
    "arkose": ["arkose", "funcaptcha", "arkoselabs"],
    "aws-waf": ["aws-waf-token", "aws-waf"],
    "imperva": ["_incap_ses", "visid_incap", "incap_ses"],
    "f5": ["bigip", "ts_", "mr_"],
    "sucuri": ["sucuri", "x-sucuri"],
    "wordfence": ["wordfence", "wfwaf"],
    "shield": ["shield", "icwp"],
}

TAKEOVER_FINGERPRINTS = {
    "AWS S3": ["NoSuchBucket", "The specified bucket does not exist", "The specified key does not exist"],
    "GitHub Pages": ["There isn't a GitHub Pages site here", "For root URLs (like http://example.com/)"],
    "Heroku": ["No such app", "no such app"],
    "Azure": ["404 Web Site not found", "This web app is stopped", "This site is stopped"],
    "Shopify": ["Sorry, this shop is currently unavailable"],
    "Tumblr": ["There's nothing here.", "Whatever you were looking for doesn't currently exist at this address"],
    "Fastly": ["Fastly error: unknown domain", "Fastly error: unknown domain:"],
    "Ghost": ["The thing you were looking for is no longer here"],
    "Pantheon": ["The gods are wise", "The gods are wise, but do not know of the site"],
    "WordPress.com": ["Do you want to register", "doesn’t exist. Would you like to search for it?"],
    "Surge.sh": ["project not found"],
    "Bitbucket": ["Repository not found"],
    "Netlify": ["Not Found - Request ID", "Not found - Request ID"],
    "Vercel": ["The deployment could not be found", "DEPLOYMENT_NOT_FOUND"],
    "Read the Docs": ["The requested project was not found"],
    "Cargo Collective": ["<title>404 — File not found</title>"],
    "UserVoice": ["This UserVoice subdomain is currently available"],
    "Zendesk": ["Help Center Closed", "Oops, this help center no longer exists"],
    "Freshdesk": ["There is no helpdesk here"],
    "Tilda": ["Please renew your subscription", "This page is not published"],
    "Webflow": ["This site is not published", "The page you are looking for doesn't exist"],
    "Strikingly": ["Sorry, this page is not available", "This site is no longer available"],
    "Cargo": ["<title>404 — File not found</title>"],
    "Unbounce": ["The requested URL was not found on this server"],
    "Bigcartel": ["<h1>Oops! We couldn&#8217;t find that page.</h1>"],
    "Campaign Monitor": ["Double check the URL"],
    "Statuspage": ["Status page pushed", "This status page is not active"],
    "Intercom": ["This page is reserved for artistic purposes"],
    "Ngrok": ["Tunnel "],
    "Pageclip": ["The site does not exist", "This page does not exist"],
    "Canny": ["This Canny instance does not exist"],
    "Airee": ["The page you're looking for could not be found"],
    "Hatena": ["404 Not Found"],
    "SmartJobBoard": ["This job board website is either expired"],
    "Simplebooklet": ["We can't find this simplebooklet"],
    "Bitly": ["Bitly's link shortener"],
    "Pingdom": ["This is a special placeholder page"],
    "Helpjuice": ["No helpjuice content"],
    "Help Scout": ["The help center you are looking for doesn't exist"],
    "Chargify": ["This page is reserved for artistic purposes"],
    "Jetbrains": ["This space is not yet registered"],
    "Discourse": ["Site is not configured"],
    "Wix": ["Error ConnectYourDomain occurred"],
    "Sendgrid": ["This is a SendGrid"],
}

TAKEOVER_CNAME_HINTS = {
    "AWS S3": ["s3.amazonaws.com", "s3-website", ".s3.", "s3.dualstack"],
    "GitHub Pages": ["github.io", "github.com", "githubapp.com"],
    "Heroku": ["herokuapp.com", "herokussl.com", "herokudns.com"],
    "Azure": ["azurewebsites.net", "cloudapp.azure.com", "trafficmanager.net", "azure-api.net", "azurefd.net"],
    "Shopify": ["myshopify.com", "shopifypreview.com"],
    "Tumblr": ["tumblr.com", "tumblr.co"],
    "Fastly": ["fastly.net", "fastlylb.net"],
    "Ghost": ["ghost.io"],
    "Pantheon": ["pantheonsite.io", "pantheonsite.com"],
    "WordPress.com": ["wordpress.com", "wpcomstaging.com"],
    "Surge.sh": ["surge.sh"],
    "Bitbucket": ["bitbucket.io", "bitbucket.org"],
    "Netlify": ["netlify.app", "netlify.com"],
    "Vercel": ["vercel.app", "now.sh", "vercel-dns.com"],
    "Read the Docs": ["readthedocs.io", "readthedocs.org"],
    "Cargo Collective": ["cargocollective.com"],
    "UserVoice": ["uservoice.com"],
    "Zendesk": ["zendesk.com"],
    "Freshdesk": ["freshdesk.com"],
    "Tilda": ["tilda.ws", "tildacdn.com"],
    "Webflow": ["webflow.io", "webflow.com"],
    "Strikingly": ["strikingly.com", "strikinglydns.com"],
    "Unbounce": ["unbounce.com", "unbouncepages.com"],
    "Bigcartel": ["bigcartel.com"],
    "Campaign Monitor": ["createsend.com", "cmail1.com"],
    "Statuspage": ["statuspage.io"],
    "Intercom": ["intercom.io", "intercom.help"],
    "Ngrok": ["ngrok.io", "ngrok.com", "ngrok-free.app"],
    "Pageclip": ["pageclip.co"],
    "Canny": ["canny.io"],
    "Airee": ["airee.ru"],
    "SmartJobBoard": ["smartjobboard.com"],
    "Simplebooklet": ["simplebooklet.com"],
    "Bitly": ["bitly.com", "bit.ly"],
    "Pingdom": ["pingdom.com"],
    "Helpjuice": ["helpjuice.com"],
    "Help Scout": ["helpscoutdocs.com", "helpscout.net"],
    "Chargify": ["chargify.com"],
    "Jetbrains": ["jetbrains.space"],
    "Discourse": ["discourse.org", "discourse.group"],
    "Wix": ["wix.com", "wixsite.com"],
    "Sendgrid": ["sendgrid.net"],
    "HubSpot": ["hubspot.net", "hubspot.com", "hs-sites.com"],
    "Desk": ["desk.com"],
    "Kajabi": ["kajabi.com", "kajabi-app.com"],
    "Teamwork": ["teamwork.com"],
    "Tictail": ["tictail.com"],
    "Launchrock": ["launchrock.com"],
    "UptimeRobot": ["uptimerobot.com"],
    "AgileCRM": ["agilecrm.com"],
    "Sitemill": ["sitemill.com"],
    "Feedpress": ["feedpress.me"],
    "Surveygizmo": ["surveygizmo.com"],
    "Mashery": ["mashery.com"],
    "Divio": ["divio.io"],
    "Ngrok-free": ["ngrok-free.app"],
}

SEVERITY = {
    "SECRET": "critical", "JWT-VULN": "critical", "PRIVATE-KEY": "critical",
    "AWS-KEY": "critical", "STRIPE-SK": "critical", "PROTO-POLLUTION": "high",
    "POSTMESSAGE-FLAW": "high", "SUBDOMAIN-TAKEOVER": "critical",
    "DNS-ZONE-TRANSFER": "critical", "WEAK-JWT-SECRET": "critical",
    "POSTMESSAGE-WILDCARD": "high", "DOM-XSS": "high", "OPEN-REDIRECT": "high",
    "GRAPHQL": "high", "IDOR-CANDIDATE": "high", "CORS": "high",
    "CORS-PREFLIGHT": "high", "METHOD-RISK": "high", "EXIF-GPS": "high",
    "JSON-KEY": "high", "CACHE-POISONING": "high", "CACHE-DECEPTION": "high",
    "METHOD-OVERRIDE": "high", "FAT-GET": "high", "SENSITIVE-200": "high",
    "OPEN-S3": "high", "OPEN-AZURE": "high", "OPEN-GCS": "high",
    "INTERNAL-IP": "medium", "SSN": "critical", "CREDIT-CARD": "critical",
    "IBAN": "high", "GRAPHQL-ENDPOINT": "medium",
    "HSTS-WEAK": "medium", "CSP-WEAK": "medium", "HDR-": "medium",
    "COOKIE": "medium", "COOKIE-JWT": "medium", "HIDDEN-INPUT": "medium",
    "FORM-TARGET": "medium", "CSRF-MISSING": "medium", "PATH": "medium",
    "STORAGE-SENSITIVE": "medium", "SOURCE-MAP": "medium",
    "SUBDOMAIN": "info", "TECH-ID": "info", "TECH": "info", "DNS": "info",
    "TLS": "info", "EMAIL": "info", "COMMENT": "low",
    "JS-AST": "info", "FETCH": "info", "DOM-SINK": "low",
}


def severity_of(typ):
    for k, v in SEVERITY.items():
        if typ.startswith(k):
            return v
    return "info"


def shannon_entropy(s):
    if not s:
        return 0.0
    counts = Counter(s)
    length = len(s)
    ent = 0.0
    for c in counts.values():
        p = c / length
        ent -= p * math.log2(p)
    return ent


def is_high_entropy_string(s):
    if len(s) < 20 or len(s) > 200:
        return False
    if s.startswith(("http://", "https://", "/", "./", "../")):
        return False
    if s.isdigit() or s.isalpha():
        return False
    if " " in s:
        return False
    return shannon_entropy(s) > 4.2


def luhn_valid(number):
    try:
        digits = [int(d) for d in re.sub(r'\D', '', number)]
        if len(digits) < 13 or len(digits) > 19:
            return False
        checksum = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0
    except Exception:
        return False


def cookie_items(resp):
    try:
        jar = getattr(resp.cookies, "jar", None)
        if jar is not None:
            out = []
            for c in jar:
                out.append({
                    "name": c.name,
                    "value": c.value,
                    "domain": c.domain or "",
                    "path": c.path or "/",
                    "secure": bool(c.secure),
                    "httponly": bool(c.has_nonstandard_attr("HttpOnly")),
                    "samesite": bool(c.has_nonstandard_attr("SameSite")),
                })
            return out
    except Exception:
        pass
    try:
        out = []
        items = resp.cookies.items() if hasattr(resp.cookies, "items") else []
        for name, value in items:
            out.append({
                "name": name, "value": value, "domain": "", "path": "/",
                "secure": False, "httponly": False, "samesite": False,
            })
        return out
    except Exception:
        return []


class LiveStream:
    def __init__(self, silent=False, jsonl=False, quiet=False):
        self.silent = silent
        self.jsonl = jsonl
        self.quiet = quiet
        self.target = None
        self._seen = set()
        self._count = 0
        self._sev_counts = Counter()
        self._type_counts = Counter()
        self._listener = None

    def set_target(self, target):
        self.target = target

    def set_listener(self, fn):
        self._listener = fn

    def emit(self, typ, key, val):
        if self.quiet and typ in QUIET_TYPES:
            return
        key_s = str(key)
        val_s = str(val)
        t = (typ, key_s, val_s)
        if t in self._seen:
            return
        self._seen.add(t)
        self._count += 1
        sev = severity_of(typ)
        self._sev_counts[sev] += 1
        self._type_counts[typ] += 1

        if self._listener:
            try:
                self._listener(typ, key_s, val_s)
            except Exception:
                pass

        if self.jsonl or self.silent:
            try:
                print(json.dumps({
                    "type": typ, "url": key_s, "value": val_s,
                    "target": self.target or "", "severity": sev,
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }, ensure_ascii=False), flush=True)
            except Exception:
                pass
            return

        color = SEV_COLOR.get(sev, "white")
        ts = time.strftime("%H:%M:%S")
        short_type = typ[:22].ljust(22)
        console.print(
            f"[dim]{ts}[/] [bold {color}]{sev[:4].upper():<4}[/] "
            f"[{color}]{short_type}[/] [white]{key_s[:70]}[/] "
            f"[dim]→[/] [italic]{val_s[:80]}[/]",
            highlight=False,
        )

    @property
    def count(self):
        return self._count

    @property
    def sev_counts(self):
        return dict(self._sev_counts)

    @property
    def type_counts(self):
        return dict(self._type_counts)


class Stealth:
    def __init__(self, min_delay=0.5, max_delay=2.5, backoff_base=5.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.backoff_base = backoff_base
        self._rng = random.Random()
        self._host_state = defaultdict(lambda: {"backoff_until": 0.0, "failures": 0})
        self._lock = asyncio.Lock()
        self._last_request = defaultdict(float)
        self._ua_pool = USER_AGENTS[:]
        self._rng.shuffle(self._ua_pool)
        self._ua_index = 0

    def _next_ua(self):
        ua = self._ua_pool[self._ua_index % len(self._ua_pool)]
        self._ua_index += 1
        if self._ua_index >= len(self._ua_pool):
            self._rng.shuffle(self._ua_pool)
            self._ua_index = 0
        return ua

    def build_headers(self, url, accept=None, referer=None, is_ajax=False):
        ua = self._next_ua()
        ua_l = ua.lower()
        headers = {
            "User-Agent": ua,
            "Accept": accept or self._rng.choice(ACCEPT_VARIANTS),
            "Accept-Language": self._rng.choice(LANGUAGES),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": referer or f"{urlparse(url).scheme}://{urlparse(url).netloc}/",
        }
        if any(x in ua_l for x in ("chrome/", "edg/", "opr/", "brave", "vivaldi")):
            headers["sec-ch-ua"] = self._rng.choice(SEC_CH_UA_VARIANTS)
            headers["sec-ch-ua-mobile"] = "?0" if "mobile" not in ua_l else "?1"
            headers["sec-ch-ua-platform"] = (
                '"Windows"' if "windows" in ua_l else
                '"macOS"' if "macintosh" in ua_l else
                '"Linux"' if "linux" in ua_l else
                '"Android"' if "android" in ua_l else
                '"iOS"' if "iphone" in ua_l or "ipad" in ua_l else '"Unknown"'
            )
            headers["Sec-Fetch-Dest"] = "document" if not is_ajax else "empty"
            headers["Sec-Fetch-Mode"] = "navigate" if not is_ajax else "cors"
            headers["Sec-Fetch-Site"] = "same-origin" if referer else "none"
        if "firefox" in ua_l:
            headers["DNT"] = "1"
            headers["Sec-Fetch-Dest"] = "document"
            headers["Sec-Fetch-Mode"] = "navigate"
            headers["Sec-Fetch-Site"] = "none"
        if "safari" in ua_l and "chrome" not in ua_l:
            headers["DNT"] = "1"
        return {k: v for k, v in headers.items() if v is not None}

    async def wait(self, url):
        host = urlparse(url).hostname or "?"
        state = self._host_state[host]
        now = time.time()
        if now < state["backoff_until"]:
            await asyncio.sleep(state["backoff_until"] - now)
        async with self._lock:
            last = self._last_request[host]
            elapsed = time.time() - last
            min_spacing = 0.2 + self._rng.uniform(0.05, 0.35)
            if elapsed < min_spacing:
                await asyncio.sleep(min_spacing - elapsed)
            self._last_request[host] = time.time()
        if self.min_delay or self.max_delay:
            await asyncio.sleep(self._rng.uniform(self.min_delay, self.max_delay))

    async def mark_failure(self, url, status_code=None):
        host = urlparse(url).hostname or "?"
        state = self._host_state[host]
        state["failures"] += 1
        backoff = min(300.0, self.backoff_base * (2 ** (state["failures"] - 1)))
        state["backoff_until"] = time.time() + backoff

    async def mark_success(self, url):
        host = urlparse(url).hostname or "?"
        self._host_state[host]["failures"] = 0

    def get_host_backoff(self):
        now = time.time()
        return {h: max(0, s["backoff_until"] - now)
                for h, s in self._host_state.items() if s["backoff_until"] > now}


def banner():
    art = (
        "[bold cyan]╔══════════════════════════════════════════════════════════════════════╗[/]\n"
        "[bold cyan]║[/]   [bold white]███████╗██╗██╗     ██╗  ██╗███████╗ █████╗ ███╗   ██╗ ██████╗[/]      [bold cyan]║[/]\n"
        "[bold cyan]║[/]   [bold white]██╔════╝██║██║     ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝[/]      [bold cyan]║[/]\n"
        "[bold cyan]║[/]   [bold white]███████╗██║██║     █████╔╝ █████╗  ███████║██╔██╗ ██║██║  ███╗[/]     [bold cyan]║[/]\n"
        "[bold cyan]║[/]   [bold white]╚════██║██║██║     ██╔═██╗ ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║[/]     [bold cyan]║[/]\n"
        "[bold cyan]║[/]   [bold white]███████║██║███████╗██║  ██╗██║     ██║  ██║██║ ╚████║╚██████╔╝[/]     [bold cyan]║[/]\n"
        "[bold cyan]║[/]   [bold white]╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝[/]      [bold cyan]║[/]\n"
        f"[bold cyan]║[/]   [dim]Website Recon Engine & A Powerful Crawler[/]                          [bold cyan]║[/]\n"
        f"[bold cyan]║[/]   [dim]Author:[/] [bold magenta]{AUTHOR}[/]                           [bold cyan]║[/]\n"
        "[bold cyan]╚══════════════════════════════════════════════════════════════════════╝[/]"
    )
    console.print(art)


def warning():
    text = (
        "[bold red]⚠  LEGAL WARNING  ⚠[/]\n\n"
        "[white]SILKFANG performs [bold yellow]passive[/] and [bold red]ACTIVE[/] reconnaissance.[/]\n"
        "[white]Active probes: HTTP method fuzz, open-redirect injection, GraphQL introspection,\n"
        "path brute-forcing, cache poisoning probes, subdomain takeover checks, DNS zone transfer.[/]\n\n"
        "[white]Only use against systems you [bold]own[/] or have [bold]explicit written authorization[/] to test.[/]\n\n"
        "[bold red]The author assumes NO liability for misuse.[/]"
    )
    console.print(Panel(text, title="[bold red]AUTHORIZATION REQUIRED[/]",
                        border_style="red", padding=(1, 2)))


def get_consent():
    try:
        ans = console.input("[bold yellow]Do you have authorization? [green](y/N)[/]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return ans in ("y", "yes")


def wait_enter(msg="Press Enter to return to menu"):
    try:
        console.input(f"\n[bold cyan]{msg}...[/]")
    except (EOFError, KeyboardInterrupt):
        pass


def show_menu(current_target=None):
    console.print()
    t = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
    t.add_column(style="bold cyan")
    t.add_column(style="white")
    t.add_row("[1]", "OFFENSIVE   //  attack surface · DNS · subdomains · paths · secrets")
    t.add_row("[2]", "DEFENSIVE   //  headers · TLS · cookies · CORS · robots · email-auth")
    t.add_row("[3]", "ALL + FULL  //  everything + full-site crawl")
    t.add_row("[4]", "NEW TARGET  //  change the target URL")
    t.add_row("[5]", "QUIT")
    title = "[bold cyan]SELECT SCAN PROFILE[/]"
    if current_target:
        title += f"  [dim]target:[/] [white]{current_target}[/]"
    console.print(Panel(t, title=title, border_style="cyan"))


def registered_domain(url):
    try:
        ext = extract(url)
        return f"{ext.domain}.{ext.suffix}".lower() if ext.domain and ext.suffix else ""
    except Exception:
        return ""


def in_scope(url, scope, mode="rdn"):
    host = urlparse(url).hostname
    if not host:
        return False
    host = host.lower()
    if mode == "fqdn":
        return host == scope
    if mode == "rdn":
        try:
            u_ext = extract(url)
            s_ext = extract(scope)
            if not (u_ext.domain and u_ext.suffix and s_ext.domain and s_ext.suffix):
                return False
            return (u_ext.domain == s_ext.domain and u_ext.suffix == s_ext.suffix)
        except Exception:
            return False
    if mode == "dn":
        return host == scope or host.endswith("." + scope)
    return False


def path_in_scope(url, scope_regex):
    if not scope_regex:
        return True
    try:
        return re.search(scope_regex, url) is not None
    except re.error:
        return True


def ext_of(url):
    return Path(urlparse(url).path).suffix.lower()


def is_binary(url):
    return ext_of(url) in BINARY_EXT


def normalize(url, base):
    if not url:
        return None
    url = url.strip()
    if not url or url.startswith(("javascript:", "mailto:", "tel:", "data:", "blob:")):
        return None
    if url.startswith("#/") or url.startswith("#!"):
        base_no_frag, _ = urldefrag(base)
        return base_no_frag + url
    absolute = urljoin(base, url)
    parsed = urlparse(absolute)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return None
    if not (parsed.fragment.startswith("/") or parsed.fragment.startswith("!")):
        absolute, _ = urldefrag(absolute)
    return absolute


def base_url_of(url):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def safe_b64_decode(s):
    try:
        s2 = s + "=" * (-len(s) % 4)
        return b64decode(s2).decode("utf-8", errors="ignore")
    except Exception:
        return None


def looks_like_json(s):
    s = s.strip()
    return (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]"))


def analyze_image(data, url, stream):
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
        img = Image.open(io.BytesIO(data))
        stream.emit("ASSET-DIM", url, f"{img.width}x{img.height} {img.format}")
        exif = img.getexif()
        if exif:
            for tag_id, val in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    try:
                        gps = exif.get_ifd(0x8825)
                        gps_named = {GPSTAGS.get(k, k): v for k, v in gps.items()}
                        stream.emit("EXIF-GPS", url, str(gps_named)[:200])
                    except Exception:
                        pass
                elif tag in ("Make", "Model", "Software", "DateTime", "Artist",
                             "Copyright", "ImageDescription", "UserComment", "HostComputer",
                             "LensModel", "LensMake", "SerialNumber", "CameraOwnerName",
                             "BodySerialNumber", "ImageUniqueID", "OwnerName"):
                    stream.emit(f"EXIF-{tag.upper()}", url, str(val)[:120])
    except Exception:
        pass


def analyze_pdf(data, url, stream):
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        meta = reader.metadata or {}
        for k, v in meta.items():
            if isinstance(v, str) and v.strip():
                stream.emit("PDF-META", url, f"{k.lstrip('/')}={v[:100]}")
        stream.emit("PDF-PAGES", url, str(len(reader.pages)))
        return
    except Exception:
        pass
    head = data[:65536]
    for field in ("Author", "Creator", "Producer", "Title", "Subject",
                  "Keywords", "CreationDate", "ModDate", "Trapped"):
        m = re.search(rf'/{field}\s*\((.*?)\)'.encode(), head)
        if m:
            try:
                stream.emit("PDF-META", url, f"{field}={m.group(1).decode('latin-1', 'ignore')[:100]}")
            except Exception:
                pass


def analyze_office(data, url, stream):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if "docProps/core.xml" in z.namelist():
                core = z.read("docProps/core.xml").decode("utf-8", errors="ignore")
                for tag in ("creator", "lastModifiedBy", "title", "subject",
                            "description", "keywords", "company", "manager",
                            "category", "revision", "created", "modified"):
                    m = re.search(rf'<{tag}[^>]*>([^<]+)</{tag}>', core)
                    if m:
                        stream.emit("OFFICE-META", url, f"{tag}={m.group(1)[:100]}")
    except Exception:
        pass


def analyze_archive(data, url, stream):
    names = []
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = z.namelist()[:60]
    except Exception:
        try:
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as t:
                names = t.getnames()[:60]
        except Exception:
            pass
    for n in names:
        stream.emit("ARCHIVE-ENTRY", url, n[:150])


def analyze_svg(data, url, stream):
    try:
        text = data.decode("utf-8", errors="ignore")
        if "<script" in text.lower():
            stream.emit("SVG-SCRIPT", url, "embedded <script>")
        for m in re.findall(r'xlink:href="([^"]+)"', text):
            stream.emit("SVG-REF", url, m[:150])
    except Exception:
        pass


def analyze_font(data, url, stream):
    try:
        from fontTools.ttLib import TTFont
        f = TTFont(io.BytesIO(data), fontNumber=0, lazy=True)
        if "name" in f:
            for rec in f["name"].names:
                if rec.nameID in (1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20):
                    try:
                        val = rec.toUnicode()[:100]
                        stream.emit("FONT-META", url, f"name{rec.nameID}={val}")
                    except Exception:
                        pass
    except Exception:
        pass


def deep_analyze_asset(data, url, stream):
    ext = ext_of(url)
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"):
        analyze_image(data, url, stream)
    elif ext == ".pdf":
        analyze_pdf(data, url, stream)
    elif ext in (".docx", ".xlsx", ".pptx", ".odt", ".ods", ".odp", ".epub"):
        analyze_office(data, url, stream)
    elif ext in (".zip", ".tar", ".tgz", ".gz", ".doc", ".xls", ".ppt"):
        analyze_archive(data, url, stream)
    elif ext == ".svg":
        analyze_svg(data, url, stream)
    elif ext in (".ttf", ".otf", ".woff", ".woff2"):
        analyze_font(data, url, stream)


class StateStore:
    def __init__(self, fqdn, out_dir="output"):
        self.dir = Path(out_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f".silkfang-state-{fqdn}.jsonl"

    def load(self):
        try:
            if not self.path.exists():
                return None
            state = {"visited": [], "assets": [], "all_urls": [],
                     "results": [], "target": None, "mode": None, "timestamp": 0}
            with open(self.path) as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    k = rec.get("k")
                    v = rec.get("v")
                    if k in ("visited", "assets", "all_urls"):
                        state[k].append(v)
                    elif k == "result":
                        state["results"].append(tuple(v))
                    elif k == "meta":
                        state["target"] = v.get("target")
                        state["mode"] = v.get("mode")
                        state["timestamp"] = v.get("timestamp", 0)
            return state
        except Exception:
            return None

    def save(self, state):
        try:
            tmp = self.path.with_suffix(".tmp")
            with open(tmp, "w") as f:
                meta = {"target": state.get("target"),
                        "mode": state.get("mode"),
                        "timestamp": state.get("timestamp", time.time())}
                f.write(json.dumps({"k": "meta", "v": meta}) + "\n")
                for u in state.get("visited", []):
                    f.write(json.dumps({"k": "visited", "v": u}) + "\n")
                for u in state.get("assets", []):
                    f.write(json.dumps({"k": "assets", "v": u}) + "\n")
                for u in state.get("all_urls", []):
                    f.write(json.dumps({"k": "all_urls", "v": u}) + "\n")
                for r in state.get("results", []):
                    f.write(json.dumps({"k": "result", "v": list(r)}) + "\n")
            tmp.replace(self.path)
        except Exception:
            pass

    def clear(self):
        try:
            self.path.unlink()
        except Exception:
            pass


def analyze_postmessage(js_text, js_url, stream):
    if not RE_ADDEVENTMESSAGE.search(js_text):
        return
    if not RE_ORIGIN_CHECK.search(js_text):
        stream.emit("POSTMESSAGE-FLAW", js_url, "addEventListener('message') without origin check")
    for m in RE_POSTMESSAGE.findall(js_text):
        if "'*'" in m or '"*"' in m:
            stream.emit("POSTMESSAGE-WILDCARD", js_url, f"postMessage(..., '*') — {m[:120]}")


def analyze_dom_sinks(js_text, js_url, stream):
    sources = []
    for s in ("location.hash", "location.search", "location.href", "document.URL",
              "document.referrer", "window.name", "document.cookie",
              "location.pathname", "window.location", "history.state"):
        if s in js_text:
            sources.append(s)
    if not sources:
        return
    sinks = set(RE_DANGEROUS_SINKS.findall(js_text))
    for sink in sinks:
        if sink in ("innerHTML", "outerHTML", "document.write", "document.writeln",
                    "eval", "setTimeout", "setInterval"):
            for src in sources:
                stream.emit("DOM-XSS", js_url, f"{src} → {sink}")


def analyze_proto_pollution(js_text, js_url, stream):
    if "__proto__" not in js_text and "constructor.prototype" not in js_text:
        return
    if not re.search(r'\b(?:Object\.assign|deepMerge|\.merge\s*\(|\$\.extend|_\.merge|extend\s*\()', js_text):
        return
    for m in re.finditer(r'__proto__|constructor\.prototype', js_text):
        start = max(0, m.start() - 80)
        ctx = js_text[start:m.end() + 80]
        if re.search(r'\b(?:Object\.assign|merge|extend)\s*\(', ctx):
            stream.emit("PROTO-POLLUTION", js_url, ctx.replace("\n", " ")[:150])
            return


def analyze_storage(js_text, js_url, stream):
    for m in RE_STORAGE_WRITE.finditer(js_text):
        key = m.group(1)
        if any(x in key.lower() for x in ("token", "auth", "session", "jwt", "key",
                                          "secret", "user", "password", "credential",
                                          "api", "bearer", "oauth", "csrf", "xsrf")):
            stream.emit("STORAGE-SENSITIVE", js_url, key)


def analyze_fetch_calls(js_text, js_url, stream):
    for m in RE_FETCH_CALL.findall(js_text):
        stream.emit("FETCH", js_url, m[:150])


def analyze_sensitive_inline(html, url, stream):
    for m in RE_INTERNAL_IP.findall(html):
        stream.emit("INTERNAL-IP", m, url)
    for m in RE_SSN.findall(html):
        stream.emit("SSN", m[:12], url)
    for m in RE_CREDIT_CARD.findall(html)[:5]:
        if luhn_valid(m):
            stream.emit("CREDIT-CARD", m[:20], url)
    for m in RE_IBAN.findall(html)[:5]:
        if len(m) >= 15:
            stream.emit("IBAN", m[:30], url)
    for m in RE_AWS_S3.findall(html):
        stream.emit("AWS-S3-URL", m, url)
    for m in RE_AZURE_BLOB.findall(html):
        stream.emit("AZURE-BLOB", m, url)
    for m in RE_GCS.findall(html):
        stream.emit("GCS-BUCKET", m, url)
    for m in RE_FIREBASE_STORAGE.findall(html):
        stream.emit("FIREBASE-STORAGE", m, url)
    for m in RE_FIREBASE_DB.findall(html):
        stream.emit("FIREBASE-DB", m, url)
    for m in RE_GRAPHQL_ENDPOINT.findall(html):
        stream.emit("GRAPHQL-ENDPOINT", m[:150], url)
    for m in RE_DOGE.findall(html)[:3]:
        stream.emit("CRYPTO", "DOGE", m)
    for m in RE_LTC.findall(html)[:3]:
        stream.emit("CRYPTO", "LTC", m)
    for m in RE_SOL.findall(html)[:3]:
        if len(m) >= 32:
            stream.emit("CRYPTO", "SOL", m)


def audit_jwt(token, source, stream, crack_wordlist=None):
    parts = token.split(".")
    if len(parts) != 3:
        return
    try:
        hb = parts[0] + "=" * (-len(parts[0]) % 4)
        header = json.loads(urlsafe_b64decode(hb))
    except Exception:
        return
    alg = header.get("alg", "?")
    stream.emit("JWT", source, f"alg={alg}")
    if alg == "none":
        stream.emit("JWT-VULN", source, "alg=none")
    if "jwk" in header:
        stream.emit("JWT-VULN", source, "jwk header present")
    if "jku" in header:
        stream.emit("JWT-VULN", source, f"jku header present: {header['jku'][:80]}")
    if "kid" in header and any(c in str(header["kid"]) for c in ("../", "/", "\\")):
        stream.emit("JWT-VULN", source, f"kid injection: {header['kid'][:80]}")
    try:
        pb = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(urlsafe_b64decode(pb))
        if "exp" not in payload:
            stream.emit("JWT-WEAK", source, "no exp claim")
        for k in ("password", "pwd", "secret", "token", "api_key", "apikey"):
            if k in payload:
                stream.emit("JWT-SENSITIVE", source, f"{k}={str(payload[k])[:40]}")
    except Exception:
        pass
    if alg == "HS256" and crack_wordlist:
        import hmac
        signing_input = (parts[0] + "." + parts[1]).encode()
        try:
            sig_raw = parts[2] + "=" * (-len(parts[2]) % 4)
            sig = urlsafe_b64decode(sig_raw)
        except Exception:
            return
        try:
            words = Path(crack_wordlist).read_text().splitlines()
        except Exception:
            return
        for word in words[:10000]:
            if hmac.compare_digest(
                hmac.new(word.encode(), signing_input, hashlib.sha256).digest(), sig
            ):
                stream.emit("WEAK-JWT-SECRET", source, word)
                break


def parse_js_ast(js_text, js_url, stream):
    endpoints = set()
    if not HAS_ESPRIMA:
        for m in RE_URL.findall(js_text):
            endpoints.add(m)
        for m in RE_PATH.findall(js_text):
            endpoints.add(m)
        for ep in list(endpoints)[:300]:
            stream.emit("JS-AST", js_url, ep[:150])
        return endpoints

    try:
        try:
            ast = esprima.parseScript(js_text, tolerant=True)
        except Exception:
            ast = esprima.parseModule(js_text, tolerant=True)
    except Exception:
        for m in RE_URL.findall(js_text):
            endpoints.add(m)
        for m in RE_PATH.findall(js_text):
            endpoints.add(m)
        return endpoints

    def add(val):
        if not val or not isinstance(val, str):
            return
        if val.startswith(("/", "http://", "https://", "ws://", "wss://")):
            if len(val) < 500:
                endpoints.add(val)

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "Literal":
                add(node.get("value"))
            elif node.get("type") == "TemplateLiteral":
                for q in node.get("quasis", []):
                    raw = q.get("value", {}).get("raw", "")
                    if raw and raw.startswith(("/", "http")):
                        add(raw)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for i in node:
                walk(i)

    try:
        walk(ast)
    except Exception:
        pass
    for ep in list(endpoints)[:300]:
        stream.emit("JS-AST", js_url, ep[:150])
    return endpoints


def extract_dynamic_imports(js_text, js_url):
    imports = set()
    for m in RE_REQUIRE_IMPORT.findall(js_text):
        if not m.startswith(("http://", "https://", "/", "./", "../")):
            continue
        imports.add(urljoin(js_url, m))
    return imports


def mine_js_deep(text, js_url, stream):
    out = parse_js_ast(text, js_url, stream)
    for m in RE_WS.findall(text):
        stream.emit("WS", js_url, m[:100])
    if "sourceMappingURL" in text:
        sm = RE_SOURCEMAP.search(text)
        if sm:
            sm_url = urljoin(js_url, sm.group(1))
            stream.emit("SOURCEMAP", js_url, sm_url)
            stream.emit("SOURCE-MAP", sm_url, "source map exposed")
    for pat, label in SECRET_PATTERNS:
        try:
            for m in re.findall(pat, text)[:5]:
                if label == "HIGH-ENTROPY" and not is_high_entropy_string(m):
                    continue
                if label in ("CREDIT-CARD",) and not luhn_valid(m):
                    continue
                stream.emit("SECRET", label, m[:80])
        except re.error:
            continue
    for m in RE_JWT.findall(text):
        audit_jwt(m, js_url, stream)
    for lib, pat in LIB_VERSION_PATTERNS.items():
        for m in pat.findall(text)[:2]:
            stream.emit("LIB-VERSION", lib, m)
    analyze_postmessage(text, js_url, stream)
    analyze_dom_sinks(text, js_url, stream)
    analyze_proto_pollution(text, js_url, stream)
    analyze_storage(text, js_url, stream)
    analyze_fetch_calls(text, js_url, stream)
    analyze_sensitive_inline(text, js_url, stream)
    return out


def mine_json_deep(text, url, stream):
    out = set()
    try:
        data = json.loads(text)
    except Exception:
        return out
    SK = {"token", "apikey", "api_key", "secret", "password", "jwt",
          "access_token", "refresh_token", "authorization", "private_key",
          "aws_access_key_id", "aws_secret_access_key", "client_secret",
          "session", "api_token", "auth_token", "client_id", "connection_string",
          "database_url", "redis_url", "smtp_password", "smtp_user",
          "webhook_url", "webhook_secret", "encryption_key", "signing_key",
          "hmac_secret", "cookie_secret", "sentry_dsn", "stripe_key",
          "sendgrid_key", "twilio_sid", "firebase_key"}

    def walk(o, p=""):
        if isinstance(o, dict):
            for k, v in o.items():
                np = f"{p}.{k}" if p else k
                if k.lower() in SK and isinstance(v, str) and v:
                    stream.emit("JSON-KEY", url, f"{np}={v[:40]}")
                walk(v, np)
        elif isinstance(o, list):
            for i in o[:30]:
                walk(i, p)
        elif isinstance(o, str):
            if o.startswith(("http://", "https://", "/")):
                out.add(o)
    walk(data)
    return out


def parse_css(css_text, css_url, stream):
    out = set()
    for m in re.findall(r'url\(([^)]+)\)', css_text):
        u = m.strip().strip("'\"")
        if u and not u.startswith("data:"):
            out.add(urljoin(css_url, u))
            if any(e in u.lower() for e in (".woff", ".woff2", ".ttf", ".otf", ".eot")):
                stream.emit("FONT", u, css_url)
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
                if ext in u.lower():
                    out.add(urljoin(css_url, u))
    for m in re.findall(r'@import\s+(?:url\()?["\']?([^"\')\s]+)', css_text):
        out.add(urljoin(css_url, m))
    if "sourceMappingURL" in css_text:
        m = re.search(r'sourceMappingURL=([^\s*]+)', css_text)
        if m:
            stream.emit("SOURCE-MAP", urljoin(css_url, m.group(1)), "css source map")
    return out


def waf_fingerprint(resp, stream):
    h = resp.headers
    ck = cookie_items(resp)
    cookie_names = [c["name"].lower() for c in ck]
    for waf, sigs in WAF_SIGNATURES.items():
        for hdr, needle in sigs:
            if hdr in ("incap_ses", "visid_incap"):
                if any(hdr in c for c in cookie_names):
                    stream.emit("WAF", waf, f"cookie={hdr}")
                    return
            val = h.get(hdr, "").lower()
            if needle is None:
                if val:
                    stream.emit("WAF", waf, f"header={hdr}")
                    return
            elif needle in val:
                stream.emit("WAF", waf, f"header={hdr}")
                return


def detect_bot_challenge(resp):
    try:
        body = resp.text[:5000].lower() if hasattr(resp, "text") else ""
    except Exception:
        body = ""
    headers = {k.lower(): str(v).lower() for k, v in resp.headers.items()}
    for vendor, sigs in BOT_CHALLENGE_SIGNATURES.items():
        for sig in sigs:
            if sig in body or any(sig in h for h in headers.values()):
                return vendor
    if resp.status_code == 503 and "challenge" in body:
        return "unknown"
    return None


def fingerprint_tech(resp, html, stream):
    url = str(resp.url)
    h = resp.headers
    html_l = html.lower() if html else ""
    seen = set()

    def hit(tech):
        if tech not in seen:
            stream.emit("TECH-ID", url, tech)
            seen.add(tech)

    xpb = h.get("x-powered-by", "").lower()
    srv = h.get("server", "").lower()
    for needle, tech in [
        ("wp-content", "WordPress"), ("wp-includes", "WordPress"),
        ("/wp-json/", "WordPress"), ("csrfmiddlewaretoken", "Django"),
        ("__viewstate", "ASP.NET"), ("asp.net", "ASP.NET"),
        ("swagger-ui", "Swagger UI"), ("swaggeruibundle", "Swagger UI"),
        ("ng-version", "Angular"), ("ng-app", "Angular"),
        ("__next_data__", "Next.js"), ("_nuxt", "Nuxt"),
        ("vue.js", "Vue"), ("vue.runtime", "Vue"),
        ("data-reactroot", "React"), ("react-dom", "React"),
        ("jquery", "jQuery"), ("laravel_session", "Laravel"),
        ("phpsessid", "PHP"), ("jsessionid", "Java"),
        ("drupal", "Drupal"), ("joomla", "Joomla"),
        ("magento", "Magento"), ("shopify", "Shopify"),
        ("strapi", "Strapi"), ("ghost", "Ghost"),
        ("gatsby", "Gatsby"), ("svelte", "Svelte"),
        ("ember", "Ember"), ("backbone", "Backbone"),
        ("knockout", "Knockout"), ("alpine", "Alpine"),
        ("htmx", "HTMX"), ("astro", "Astro"),
        ("remix", "Remix"), ("solid", "Solid"),
        ("preact", "Preact"), ("lit", "Lit"),
        ("docusaurus", "Docusaurus"), ("hugo", "Hugo"),
        ("jekyll", "Jekyll"), ("eleventy", "Eleventy"),
        ("pelican", "Pelican"), ("grav", "Grav"),
        ("concrete5", "Concrete5"), ("modx", "MODX"),
        ("typo3", "TYPO3"), ("craft", "Craft CMS"),
        ("statamic", "Statamic"), ("contentful", "Contentful"),
        ("sanity", "Sanity"), ("prismic", "Prismic"),
    ]:
        if needle in html_l:
            hit(tech)
    for needle, tech in [
        ("express", "Express"), ("django", "Django"),
        ("flask", "Flask"), ("php", "PHP"), ("asp.net", "ASP.NET"),
        ("nginx", "Nginx"), ("apache", "Apache"), ("iis", "IIS"),
        ("cloudflare", "Cloudflare"), ("tomcat", "Tomcat"),
        ("jboss", "JBoss"), ("gunicorn", "Gunicorn"),
        ("uvicorn", "Uvicorn"), ("kestrel", "Kestrel"),
        ("caddy", "Caddy"), ("traefik", "Traefik"),
        ("envoy", "Envoy"), ("haproxy", "HAProxy"),
        ("varnish", "Varnish"), ("lighttpd", "Lighttpd"),
        ("openresty", "OpenResty"), ("litespeed", "LiteSpeed"),
        ("node", "Node.js"), ("deno", "Deno"),
        ("bun", "Bun"), ("puma", "Puma"),
        ("unicorn", "Unicorn"), ("passenger", "Passenger"),
        ("phusion", "Phusion"), ("werkzeug", "Werkzeug"),
        ("rails", "Rails"), ("laravel", "Laravel"),
        ("symfony", "Symfony"), ("codeigniter", "CodeIgniter"),
        ("cakephp", "CakePHP"), ("yii", "Yii"),
        ("zend", "Zend"), ("spring", "Spring"),
        ("quarkus", "Quarkus"), ("micronaut", "Micronaut"),
        ("vertx", "Vert.x"), ("netty", "Netty"),
    ]:
        if needle in xpb or needle in srv:
            hit(tech)
    for c in cookie_items(resp):
        n = c["name"].lower()
        if n.startswith("wp-"):
            hit("WordPress")
        elif n == "phpsessid":
            hit("PHP")
        elif n == "jsessionid":
            hit("Java")
        elif n == "laravel_session":
            hit("Laravel")
        elif n == "csrftoken":
            hit("Django")
        elif n.startswith("_next"):
            hit("Next.js")
        elif n.startswith("__cf"):
            hit("Cloudflare")
        elif n == "asp.net_sessionid":
            hit("ASP.NET")
        elif n.startswith("_shopify"):
            hit("Shopify")
        elif n.startswith("_ga"):
            hit("Google Analytics")
        elif n.startswith("_gid"):
            hit("Google Analytics")
        elif n.startswith("_fbp"):
            hit("Facebook Pixel")
        elif n.startswith("_hjid"):
            hit("Hotjar")
        elif n.startswith("__hs"):
            hit("HubSpot")
        elif n.startswith("_mkto"):
            hit("Marketo")
        elif n.startswith("_intercom"):
            hit("Intercom")
        elif n.startswith("__stripe"):
            hit("Stripe")
        elif n.startswith("__stripe_mid"):
            hit("Stripe")
        elif n.startswith("__stripe_sid"):
            hit("Stripe")


def extract_all(html, url, stream, page_css=None, page_js=None):
    if page_css is None:
        page_css = set()
    if page_js is None:
        page_js = set()
    found_links = set()
    external_domains = set()
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    base_tag = soup.find("base", href=True)
    effective_base = urljoin(url, base_tag["href"]) if base_tag else url
    if base_tag:
        stream.emit("META-BASE", url, base_tag["href"])

    for m in soup.find_all("meta"):
        for attr in ("name", "property", "http-equiv"):
            v = m.get(attr)
            if v:
                stream.emit("META", f"{attr}={v}", (m.get("content") or "")[:150])
        prop = m.get("property") or m.get("name") or ""
        if prop.startswith(("og:", "twitter:")):
            stream.emit("OG", prop, (m.get("content") or "")[:150])
        if prop.lower() == "generator":
            stream.emit("FRAMEWORK-VERSION", "generator", (m.get("content") or "")[:80])
        if prop.lower() in ("description", "keywords", "author", "robots", "canonical"):
            stream.emit("META-SEO", prop.lower(), (m.get("content") or "")[:150])
        if prop.lower() == "csrf-token":
            stream.emit("CSRF-TOKEN", url, (m.get("content") or "")[:80])
        if prop.lower() == "viewport":
            stream.emit("META-VIEWPORT", url, (m.get("content") or "")[:80])

    for m in soup.find_all("meta", attrs={"http-equiv": True}):
        if m.get("http-equiv", "").lower() == "refresh":
            mm = re.search(r"url=(.+)", m.get("content", ""), re.I)
            if mm:
                target = mm.group(1).strip().strip("'\"")
                stream.emit("META-REFRESH", url, target[:150])
                found_links.add(target)

    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")

            def walk_ld(o, p=""):
                if isinstance(o, dict):
                    for k, v in o.items():
                        np = f"{p}.{k}" if p else k
                        if isinstance(v, str):
                            if "@" in v and "." in v:
                                stream.emit("JSONLD-EMAIL", np, v[:120])
                            elif v.startswith(("http://", "https://", "/", "tel:")):
                                stream.emit("JSONLD-VALUE", np, v[:120])
                                if v.startswith(("/", "http")):
                                    found_links.add(v)
                        else:
                            walk_ld(v, np)
                elif isinstance(o, list):
                    for i in o[:20]:
                        walk_ld(i, p)
            walk_ld(data)
        except Exception:
            pass

    for el in soup.find_all(attrs={"itemprop": True}):
        prop = el.get("itemprop")
        content = (el.get("content") or el.get_text(strip=True) or
                   el.get("href") or el.get("src") or "")
        if prop and content:
            stream.emit("MICRODATA", prop, content[:150])

    for ph in set(RE_PHONE.findall(html)):
        if len(ph.strip(" -().+")) >= 8:
            stream.emit("PHONE", ph, url)

    for m in RE_BTC.findall(html):
        stream.emit("CRYPTO", "BTC", m)
    for m in RE_ETH.findall(html):
        stream.emit("CRYPTO", "ETH", m)
    for m in RE_XMR.findall(html):
        stream.emit("CRYPTO", "XMR", m)
    for m in RE_LTC.findall(html)[:3]:
        stream.emit("CRYPTO", "LTC", m)
    for m in RE_DOGE.findall(html)[:3]:
        stream.emit("CRYPTO", "DOGE", m)

    for el in soup.find_all(attrs=True):
        for k, v in el.attrs.items():
            if isinstance(v, str) and k.startswith("data-") and "id" in k.lower():
                stream.emit("INTERNAL-ID", k, v[:100])
    for m in RE_INTERNAL_ID.findall(html):
        stream.emit("INTERNAL-ID", "attr", m[:100])

    if RE_LOREM.search(html):
        stream.emit("DEV-BANNER", "lorem ipsum", url)
    for m in RE_COMING_SOON.findall(html)[:3]:
        stream.emit("DEV-BANNER", m.lower(), url)

    for m in RE_BASE64.findall(html)[:10]:
        dec = safe_b64_decode(m)
        if dec and (looks_like_json(dec) or dec.startswith("http")):
            stream.emit("BASE64", m[:40], dec[:100])

    for u in RE_UUID.findall(html)[:5]:
        stream.emit("UUID", u, url)
    for m in RE_MD5.findall(html)[:3]:
        stream.emit("HASH", "MD5", m)
    for m in RE_SHA1.findall(html)[:3]:
        stream.emit("HASH", "SHA1", m)
    for m in RE_SHA256.findall(html)[:3]:
        stream.emit("HASH", "SHA256", m)

    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        txt = str(c).strip()[:200]
        if txt and SENSITIVE_COMMENT_HINTS.search(txt):
            stream.emit("COMMENT", url, txt)

    for s in soup.find_all("script"):
        if s.string:
            page_js.add(s.string)
            for m in RE_PATH.findall(s.string):
                found_links.add(m)
            for m in RE_URL.findall(s.string):
                found_links.add(m)
    for s in soup.find_all("style"):
        if s.string:
            page_css.add(s.string)

    for el in soup.find_all("link"):
        rels = [r.lower() for r in (el.get("rel") or [])]
        href = el.get("href")
        if not href:
            continue
        if any(r in rels for r in ("preload", "prefetch", "preconnect", "dns-prefetch")):
            stream.emit("PRELOAD", ",".join(rels), href[:150])
            found_links.add(href)
        if "manifest" in rels:
            stream.emit("PWA-MANIFEST", url, href[:150])
            found_links.add(href)
        if "icon" in rels or "apple-touch-icon" in rels:
            stream.emit("ICON", href, el.get("sizes", ""))
        if "alternate" in rels:
            stream.emit("HREFLANG", el.get("hreflang", "?") or "?", href[:150])
            found_links.add(href)
        if "canonical" in rels:
            stream.emit("CANONICAL", url, href[:150])
        if "next" in rels or "prev" in rels:
            stream.emit("PAGINATION", ",".join(rels), href[:150])
            found_links.add(href)
        if "stylesheet" in rels:
            found_links.add(href)
        if "amphtml" in rels:
            stream.emit("AMP", url, href[:150])
            found_links.add(href)
        if "preconnect" in rels:
            stream.emit("PRECONNECT", url, href[:150])

    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if "#" in h and not h.startswith("#"):
            stream.emit("FRAGMENT", h.split("#")[0] or url, h.split("#", 1)[1][:80])
        if h.startswith("mailto:"):
            stream.emit("MAILTO", h[7:].split("?")[0], h[:200])
        elif h.startswith("tel:"):
            stream.emit("TEL", h[4:], url)
        elif h.startswith("sms:"):
            stream.emit("SMS", h[4:], url)
        elif h.startswith(("whatsapp://", "intent://", "fb://", "twitter://",
                            "instagram://", "tg://", "line://", "wechat://",
                            "viber://", "skype:", "market://")):
            stream.emit("DEEPLINK", h.split(":")[0], h[:200])
            for pk, pv in re.findall(r'[?&]([a-zA-Z_]+)=([^&]+)', h):
                stream.emit("DEEPLINK-PARAM", pk, unquote(pv)[:100])
        elif h.startswith(("javascript:", "data:", "blob:")):
            stream.emit("DANGEROUS-HREF", url, h[:120])

    for f in soup.find_all("form"):
        action = f.get("action", "") or url
        method = (f.get("method") or "GET").upper()
        enctype = f.get("enctype", "")
        target_attr = f.get("target", "")
        inputs = [i.get("name") for i in f.find_all(["input", "textarea", "select"]) if i.get("name")]
        stream.emit("FORM", f"{method} {urljoin(url, action)}",
                    f"inputs={inputs[:10]} enctype={enctype} target={target_attr}")
        if method == "POST":
            stream.emit("POST-FORM", urljoin(url, action), f"inputs={inputs[:6]}")
            if not any(RE_CSRF_HINT.search(n or "") for n in inputs):
                stream.emit("CSRF-MISSING", urljoin(url, action), "POST without CSRF token")
        if target_attr == "_blank":
            stream.emit("FORM-TARGET", urljoin(url, action), "_blank without noopener")
        for i in f.find_all("input"):
            itype = (i.get("type") or "text").lower()
            if itype == "hidden":
                stream.emit("HIDDEN-INPUT", i.get("name") or "?", (i.get("value") or "")[:150])
            if i.get("pattern"):
                stream.emit("INPUT-PATTERN", i.get("name") or "?", i.get("pattern")[:100])
            if itype == "file" and i.get("accept"):
                stream.emit("INPUT-FILE-ACCEPT", i.get("name") or "?", i.get("accept")[:100])
            if itype == "password":
                stream.emit("PASSWORD-FIELD", i.get("name") or "?", urljoin(url, action))
            if itype == "email":
                stream.emit("EMAIL-FIELD", i.get("name") or "?", urljoin(url, action))
            if i.get("autocomplete") == "off":
                stream.emit("AUTOCOMPLETE-OFF", i.get("name") or "?", urljoin(url, action))

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            found_links.add(src)
            stream.emit("IMG", src[:120], f"alt={img.get('alt', '')[:40]}")
        if img.get("srcset"):
            for part in img["srcset"].split(","):
                u = part.strip().split(" ")[0]
                if u:
                    found_links.add(u)
    for v in soup.find_all(["video", "audio"]):
        for s in v.find_all("source"):
            if s.get("src"):
                found_links.add(s["src"])
        if v.get("poster"):
            found_links.add(v["poster"])
        if v.get("src"):
            found_links.add(v["src"])
    for t in soup.find_all("track", src=True):
        found_links.add(t["src"])
        stream.emit("VTT", t["src"], t.get("kind", ""))

    for svg in soup.find_all("svg"):
        txt = str(svg)
        for m in re.findall(r'(?:data-[a-z\-]+|token|key)="([^"]{20,})"', txt):
            stream.emit("SVG-LEAK", url, m[:100])

    for m in RE_GA_UA.findall(html):
        stream.emit("ANALYTICS", "GA-UA", m)
    for m in RE_GA4.findall(html):
        stream.emit("ANALYTICS", "GA4", m)
    for m in RE_GTM.findall(html):
        stream.emit("ANALYTICS", "GTM", m)
    for m in RE_FB_PIXEL.findall(html):
        stream.emit("ANALYTICS", "FB-Pixel", m)
    for m in RE_HOTJAR.findall(html):
        stream.emit("ANALYTICS", "Hotjar", m)
    for m in RE_SEGMENT.findall(html):
        stream.emit("ANALYTICS", "Segment", m)
    for m in RE_SENTRY.findall(html):
        stream.emit("ERROR-TRACKING", "Sentry", f"{m[1]} p={m[2]}")
    for m in RE_INTERCOM.findall(html):
        stream.emit("CHAT", "Intercom", m)
    for m in RE_DRIFT.findall(html):
        stream.emit("CHAT", "Drift", m)
    for m in RE_CRISP.findall(html):
        stream.emit("CHAT", "Crisp", m)
    for m in RE_ZENDESK.findall(html):
        stream.emit("CHAT", "Zendesk", m)
    for m in RE_RECAPTCHA.findall(html):
        stream.emit("CAPTCHA", "reCAPTCHA", m)
    for m in RE_HCAPTCHA.findall(html):
        stream.emit("CAPTCHA", "hCaptcha", m)
    for m in RE_TURNSTILE.findall(html):
        stream.emit("CAPTCHA", "Turnstile", m)
    for m in RE_STRIPE_PK.findall(html):
        stream.emit("PAYMENTS", "Stripe-PK", m)
    for m in RE_STRIPE_SK.findall(html):
        stream.emit("SECRET", "STRIPE-SK", m[:60])
    for m in RE_PAYPAL.findall(html):
        stream.emit("PAYMENTS", "PayPal", m)
    for m in RE_SQUARE.findall(html):
        stream.emit("PAYMENTS", "Square", m)
    for m in RE_BRAINTREE.findall(html):
        stream.emit("PAYMENTS", "Braintree", m)
    for m in RE_ADYEN.findall(html):
        stream.emit("PAYMENTS", "Adyen", m)
    for m in RE_FIREBASE.findall(html):
        stream.emit("CLOUD", "Firebase", f"apiKey={m[0][:20]} project={m[1]}")
    for m in RE_FIREBASE_DB.findall(html):
        stream.emit("CLOUD", "Firebase-DB", m)
    for m in RE_SUPABASE.findall(html):
        stream.emit("CLOUD", "Supabase", f"{m}.supabase.co")
    for m in RE_SUPABASE_KEY.findall(html):
        stream.emit("CLOUD", "Supabase-Key", m[:40])
    for m in RE_AUTH0.findall(html):
        stream.emit("AUTH", "Auth0", m)
    for m in RE_OKTA.findall(html):
        stream.emit("AUTH", "Okta", m)
    for m in RE_COGNITO.findall(html):
        stream.emit("AUTH", "Cognito", m)
    for m in RE_CLERK.findall(html):
        stream.emit("AUTH", "Clerk", m)
    for m in RE_FIREBASE_AUTH.findall(html):
        stream.emit("AUTH", "FirebaseAuth", m)
    for m in RE_AUTH0_CLIENT.findall(html):
        stream.emit("AUTH", "Auth0-Client", f"{m[0]} @ {m[1]}")
    for m in RE_MAPBOX.findall(html):
        stream.emit("MAPS", "Mapbox", m[:40])
    for m in RE_MAPBOX_SK.findall(html):
        stream.emit("SECRET", "MAPBOX-SK", m[:40])
    for m in RE_GOOGLE_MAPS.findall(html):
        stream.emit("MAPS", "Google-Maps", m[:40])
    for m in RE_HERE_MAPS.findall(html):
        stream.emit("MAPS", "Here", m[:40])
    for m in RE_PUSHER.findall(html):
        stream.emit("REALTIME", "Pusher", m)
    for m in RE_PUBNUB.findall(html):
        stream.emit("REALTIME", "PubNub", m)
    for m in RE_ABLY.findall(html):
        stream.emit("REALTIME", "Ably", m[:40])
    for m in RE_ALGOLIA.findall(html):
        stream.emit("SEARCH", "Algolia", m)
    for m in RE_ALGOLIA_KEY.findall(html):
        stream.emit("SEARCH", "Algolia-Key", m)
    for m in RE_TYPESENSE.findall(html):
        stream.emit("SEARCH", "Typesense", m[:40])
    for m in RE_MEILISEARCH.findall(html):
        stream.emit("SEARCH", "MeiliSearch", m[:40])
    for m in RE_LAUNCHDARKLY.findall(html):
        stream.emit("FEATURE-FLAGS", "LaunchDarkly", m)
    for m in RE_OPTIMIZELY.findall(html):
        stream.emit("AB-TESTING", "Optimizely", m)
    for m in RE_DATADOG_RUM.findall(html):
        stream.emit("ERROR-TRACKING", "Datadog", m[:40])
    for m in RE_NEW_RELIC.findall(html):
        stream.emit("ERROR-TRACKING", "New-Relic", m[:20])
    for m in RE_ROLLBAR.findall(html):
        stream.emit("ERROR-TRACKING", "Rollbar", m[:20])
    for m in RE_HONEYBADGER.findall(html):
        stream.emit("ERROR-TRACKING", "Honeybadger", m)
    for m in RE_BUGSNAG.findall(html):
        stream.emit("ERROR-TRACKING", "Bugsnag", m)
    for m in RE_SENTRY_DSN.findall(html):
        stream.emit("ERROR-TRACKING", "Sentry-DSN", m[:80])
    for m in RE_RAYGUN.findall(html):
        stream.emit("ERROR-TRACKING", "Raygun", m)
    for m in RE_LOGRocket.findall(html):
        stream.emit("SESSION-RECORD", "LogRocket", m)
    for m in RE_FULLSTORY.findall(html):
        stream.emit("SESSION-RECORD", "FullStory", m)
    for m in RE_AMPLITUDE.findall(html):
        stream.emit("ANALYTICS", "Amplitude", m)
    for m in RE_MIXPANEL.findall(html):
        stream.emit("ANALYTICS", "Mixpanel", m)
    for m in RE_POSTHOG.findall(html):
        stream.emit("ANALYTICS", "PostHog", m)
    for m in RE_PLAUSIBLE.findall(html):
        stream.emit("ANALYTICS", "Plausible", m)
    for m in RE_MATOMO.findall(html):
        stream.emit("ANALYTICS", "Matomo", m)
    for m in RE_UMAMI.findall(html):
        stream.emit("ANALYTICS", "Umami", m)
    for m in RE_CLARITY.findall(html):
        stream.emit("ANALYTICS", "Clarity", m)
    for m in RE_HEAP.findall(html):
        stream.emit("ANALYTICS", "Heap", m)
    for m in RE_SEGMENT_WRITE.findall(html):
        stream.emit("ANALYTICS", "Segment-WriteKey", m)
    for m in RE_RUDDERSTACK.findall(html):
        stream.emit("ANALYTICS", "RudderStack", m)
    for m in RE_MPARTICLE.findall(html):
        stream.emit("ANALYTICS", "mParticle", m)
    for m in RE_TEALIUM.findall(html):
        stream.emit("TAG-MANAGER", "Tealium", m)
    for m in RE_ONETRUST.findall(html):
        stream.emit("CONSENT", "OneTrust", m)
    for m in RE_COOKIEBOT.findall(html):
        stream.emit("CONSENT", "Cookiebot", m)

    for lib, pat in LIB_VERSION_PATTERNS.items():
        for m in pat.findall(html)[:3]:
            stream.emit("LIB-VERSION", lib, m)

    for m in re.findall(r'\?ver=([0-9][0-9a-zA-Z.\-]+)', html):
        stream.emit("ASSET-VER", "?ver=", m[:20])

    for el in soup.find_all(["script", "link"]):
        src = el.get("src") or el.get("href") or ""
        if src.startswith("http") and not el.get("integrity"):
            ext = urlparse(src).netloc
            if ext and ext != urlparse(url).netloc:
                stream.emit("NO-SRI", src[:120], f"external={ext}")

    for m in RE_CLIENT_ID.findall(html):
        stream.emit("OAUTH-CLIENT-ID", url, m[:80])
    for m in RE_RESET_TOKEN.findall(html):
        stream.emit("RESET-TOKEN", url, m[:80])

    html_l = html.lower()
    for kw, label in [
        ("/oauth", "oauth-path"), ("signin-with-google", "google-oauth"),
        ("signin-with-facebook", "fb-oauth"), ("signin-with-github", "github-oauth"),
        ("/login", "login-link"), ("/signin", "signin-link"),
        ("/register", "register-link"), ("/signup", "signup-link"),
        ("/forgot", "forgot-link"), ("/reset-password", "reset-password"),
        ("/mfa", "mfa-link"), ("/2fa", "2fa-link"), ("/otp", "otp-link"),
        ("/verify", "verify-link"), ("/activate", "activate-link"),
        ("/callback", "callback-link"), ("/sso", "sso-link"),
    ]:
        if kw in html_l:
            stream.emit("AUTH-PATH", label, kw)

    for tag, attr in TARGET_TAGS:
        for el in soup.find_all(tag):
            v = el.get(attr)
            if not v:
                continue
            if isinstance(v, list):
                v = v[0] if v else None
            if v:
                found_links.add(v.strip())
    for attr in DATA_ATTRS:
        for el in soup.find_all(attrs={attr: True}):
            v = el.get(attr)
            if v:
                found_links.add(v.strip())
    for ns in soup.find_all("noscript"):
        try:
            ns_soup = BeautifulSoup(str(ns), "lxml")
            for tag, attr in TARGET_TAGS:
                for el in ns_soup.find_all(tag):
                    v = el.get(attr)
                    if v:
                        found_links.add(v.strip())
        except Exception:
            pass
    for style in soup.find_all(style=True):
        for m in re.findall(r'url\(([^)]+)\)', style["style"]):
            found_links.add(m.strip().strip("'\""))

    for e in set(RE_EMAIL.findall(html)):
        if not ext_of(e):
            stream.emit("EMAIL", e, url)

    for m in RE_SOURCEMAP.findall(html):
        stream.emit("SOURCEMAP", url, urljoin(url, m))

    analyze_sensitive_inline(html, url, stream)

    for u in list(found_links):
        try:
            n = normalize(u, effective_base)
            if n:
                host = urlparse(n).netloc
                if host and host != urlparse(url).netloc:
                    external_domains.add(host)
        except Exception:
            pass
    for host in external_domains:
        stream.emit("EXTERNAL-DOMAIN", host, url)

    resolved = set()
    for u in found_links:
        n = normalize(u, effective_base)
        if n:
            resolved.add(n)
    return resolved, page_css, page_js


def defensive_pass(resp, stream):
    h = resp.headers
    url = str(resp.url)
    for hdr, label in SEC_HEADERS.items():
        v = h.get(hdr)
        stream.emit("HDR+" if v else "HDR-", label, (v or "MISSING")[:150])

    hsts = h.get("strict-transport-security", "")
    if hsts:
        m = re.search(r'max-age=(\d+)', hsts)
        if m and int(m.group(1)) < 31536000:
            stream.emit("HSTS-WEAK", url, f"max-age={m.group(1)} <1yr")
        if "preload" in hsts.lower():
            stream.emit("HSTS-PRELOAD", url, "declared")
        if "includeSubDomains" in hsts:
            stream.emit("HSTS-SUBDOMAINS", url, "declared")

    csp = h.get("content-security-policy", "")
    if csp:
        if "unsafe-inline" in csp:
            stream.emit("CSP-WEAK", url, "unsafe-inline")
        if "unsafe-eval" in csp:
            stream.emit("CSP-WEAK", url, "unsafe-eval")
        if "*" in csp:
            stream.emit("CSP-WEAK", url, "wildcard")
        m = re.search(r'report-uri\s+([^;\s]+)', csp)
        if m:
            stream.emit("CSP-REPORT-URI", url, m.group(1))
        m = re.search(r'report-to\s+([^;\s]+)', csp)
        if m:
            stream.emit("CSP-REPORT-TO", url, m.group(1))

    for leak in ("Server", "X-Powered-By", "X-AspNet-Version", "X-Generator",
                 "Via", "X-Debug-Token", "X-Runtime", "X-Version",
                 "X-Backend-Server", "X-Served-By", "X-Cache", "CF-Ray",
                 "X-Cache-Status", "X-Request-ID", "X-Correlation-ID",
                 "Server-Timing", "X-Robots-Tag", "Age", "ETag", "Last-Modified",
                 "X-Git-Commit", "X-Git-Branch", "X-Git-SHA", "X-Env",
                 "X-Environment", "X-Stage", "X-Region", "X-AZ",
                 "X-Instance-Id", "X-Instance", "X-Node", "X-Pod",
                 "X-Namespace", "X-Service", "X-Cluster", "X-Datacenter",
                 "X-Proxy-Id", "X-Edge-Id", "X-Pop", "X-Origin-Id"):
        v = h.get(leak)
        if v:
            stream.emit("TECH", leak, v[:120])

    acao = h.get("access-control-allow-origin")
    if acao:
        if acao == "*":
            stream.emit("CORS", url, "wildcard ACAO")
        elif acao != urlparse(url).netloc:
            stream.emit("CORS", url, f"reflects {acao}")
        if h.get("access-control-allow-credentials", "").lower() == "true" and acao == "*":
            stream.emit("CORS", url, "CREDENTIALS+WILDCARD (critical)")
    acam = h.get("access-control-allow-methods")
    if acam:
        stream.emit("CORS-METHODS", url, acam[:150])
    acah = h.get("access-control-allow-headers")
    if acah:
        stream.emit("CORS-HEADERS", url, acah[:150])

    for c in cookie_items(resp):
        flags = []
        if c["secure"]:
            flags.append("Secure")
        if c["httponly"]:
            flags.append("HttpOnly")
        if c["samesite"]:
            flags.append("SameSite")
        prefix = ""
        if c["name"].startswith("__Host-"):
            prefix = "__Host-"
        elif c["name"].startswith("__Secure-"):
            prefix = "__Secure-"
        stream.emit("COOKIE", c["name"],
                    f"flags={'|'.join(flags) or 'NONE'} domain={c['domain'] or '?'} "
                    f"path={c['path']} prefix={prefix or '-'}")
        if c["value"] and c["value"].count(".") == 2:
            audit_jwt(c["value"], f"cookie:{c['name']}", stream)
        dec = safe_b64_decode(c["value"] or "")
        if dec and looks_like_json(dec):
            stream.emit("COOKIE-JSON", c["name"], dec[:120])

    if getattr(resp, "history", None):
        for i, hr in enumerate(resp.history):
            stream.emit("REDIRECT", f"{i}:{hr.status_code}", str(hr.url)[:120])


def idor_scan(urls, stream):
    by_path_num = defaultdict(list)
    by_path_uuid = defaultdict(list)
    for u in urls:
        p = urlparse(u)
        q = parse_qs(p.query)
        for k, v in q.items():
            if not v:
                continue
            val = v[0]
            if RE_IDOR_NUM.match(val):
                by_path_num[(p.path, k)].append(int(val))
            elif RE_IDOR_UUID.match(val):
                by_path_uuid[(p.path, k)].append(val.lower())
    for (path, k), ids in by_path_num.items():
        if len(ids) >= 2 and max(ids) - min(ids) < 1000:
            stream.emit("IDOR-CANDIDATE", f"{path}?{k}=",
                        f"numeric seq {min(ids)}..{max(ids)} ({len(ids)} samples)")
    for (path, k), ids in by_path_uuid.items():
        if len(ids) >= 2:
            stream.emit("IDOR-CANDIDATE", f"{path}?{k}=",
                        f"uuid set ({len(ids)} distinct)")


class ClientWrapper:
    def __init__(self, proxy=None):
        self._session = None
        self._httpx = None
        self.proxy = proxy

    async def __aenter__(self):
        if HAS_CURL_CFFI:
            kwargs = {"impersonate": "chrome120"}
            if self.proxy:
                kwargs["proxies"] = {"http": self.proxy, "https": self.proxy}
            self._session = AsyncSession(**kwargs)
            return self
        if httpx:
            kwargs = {"timeout": 15, "verify": False, "follow_redirects": True,
                      "http2": False, "cookies": httpx.Cookies()}
            if self.proxy:
                kwargs["proxy"] = self.proxy
            self._httpx = httpx.AsyncClient(**kwargs)
            return self
        raise RuntimeError("Neither curl_cffi nor httpx is available")

    async def __aexit__(self, *exc):
        if self._session:
            try:
                await self._session.close()
            except Exception:
                pass
        if self._httpx:
            try:
                await self._httpx.aclose()
            except Exception:
                pass

    async def get(self, url, headers=None, timeout=15, follow_redirects=True):
        if self._session:
            return await self._session.get(url, headers=headers, timeout=timeout,
                                           allow_redirects=follow_redirects)
        return await self._httpx.get(url, headers=headers, timeout=timeout,
                                     follow_redirects=follow_redirects)

    async def post(self, url, headers=None, json=None, data=None, timeout=15):
        if self._session:
            if json is not None:
                return await self._session.post(url, headers=headers, json=json, timeout=timeout)
            return await self._session.post(url, headers=headers, data=data, timeout=timeout)
        if json is not None:
            return await self._httpx.post(url, headers=headers, json=json, timeout=timeout)
        return await self._httpx.post(url, headers=headers, data=data, timeout=timeout)

    async def options(self, url, headers=None, timeout=15):
        if self._session:
            return await self._session.options(url, headers=headers, timeout=timeout)
        return await self._httpx.options(url, headers=headers, timeout=timeout)

    async def request(self, method, url, headers=None, timeout=15):
        if self._session:
            return await self._session.request(method, url, headers=headers, timeout=timeout)
        return await self._httpx.request(method, url, headers=headers, timeout=timeout)


async def probe_methods(client, stealth, url, stream):
    try:
        r = await client.options(url, headers=stealth.build_headers(url), timeout=10)
        allow = r.headers.get("allow", "")
        if allow:
            stream.emit("METHODS", url, ",".join(m.strip().upper() for m in allow.split(",")))
            for risky in ("TRACE", "PUT", "DELETE", "PATCH", "CONNECT", "PROPFIND",
                          "PROPPATCH", "MKCOL", "COPY", "MOVE", "LOCK", "UNLOCK"):
                if risky in allow.upper():
                    stream.emit("METHOD-RISK", url, risky)
    except Exception:
        pass
    try:
        r = await client.request("TRACE", url, headers=stealth.build_headers(url), timeout=10)
        if r.status_code == 200 and "TRACE" in (r.text or "").upper():
            stream.emit("METHOD-RISK", url, "TRACE enabled (XST)")
    except Exception:
        pass


async def probe_redirect(client, stealth, url, stream):
    for param in ("next", "url", "redirect", "return", "returnUrl", "continue",
                  "redirect_uri", "redirect_url", "callback", "callback_url",
                  "target", "dest", "destination", "goto", "to", "link",
                  "forward", "redir", "r", "u", "out", "view", "ref", "referrer"):
        sep = "&" if "?" in url else "?"
        test_url = f"{url}{sep}{param}=https://evil.example.com"
        try:
            r = await client.get(test_url, headers=stealth.build_headers(test_url),
                                 timeout=8, follow_redirects=False)
            if "evil.example.com" in r.headers.get("location", ""):
                stream.emit("OPEN-REDIRECT", test_url, f"param={param}")
        except Exception:
            pass


async def probe_cors_preflight(client, stealth, url, stream):
    try:
        hdrs = stealth.build_headers(url, is_ajax=True)
        hdrs["Origin"] = "https://evil.example.com"
        hdrs["Access-Control-Request-Method"] = "GET"
        r = await client.options(url, headers=hdrs, timeout=8)
        acao = r.headers.get("access-control-allow-origin", "")
        acac = r.headers.get("access-control-allow-credentials", "")
        if "evil.example.com" in acao:
            stream.emit("CORS-PREFLIGHT", url, f"reflects evil origin creds={acac}")
    except Exception:
        pass
    try:
        hdrs = stealth.build_headers(url)
        hdrs["Origin"] = "null"
        r = await client.get(url, headers=hdrs, timeout=8)
        acao = r.headers.get("access-control-allow-origin", "")
        if acao == "null":
            stream.emit("CORS-PREFLIGHT", url, "null origin reflected")
    except Exception:
        pass


async def probe_cache_poisoning(client, stealth, url, stream):
    canary = f"silkfang-{random.randint(1000, 9999)}"
    for hdr in ("X-Forwarded-Host", "X-Forwarded-For", "X-Original-URL",
                "X-Rewrite-URL", "X-Forwarded-Scheme", "X-Forwarded-Port",
                "X-Forwarded-Proto", "X-Host", "X-Backend", "X-Real-IP",
                "X-Proxy-Host", "Forwarded", "X-Original-Host", "X-HTTP-Host-Override"):
        try:
            hdrs = stealth.build_headers(url)
            hdrs[hdr] = canary
            r = await client.get(url, headers=hdrs, timeout=8)
            body = r.text[:20000] if hasattr(r, "text") else ""
            if canary in body:
                cacheable = "public" in r.headers.get("cache-control", "").lower()
                age = r.headers.get("age")
                if cacheable or (age is not None and age != ""):
                    stream.emit("CACHE-POISONING", url, f"unkeyed {hdr} reflected + cacheable")
        except Exception:
            pass


async def probe_cache_deception(client, stealth, url, stream):
    if url.endswith((".css", ".js", ".png", ".jpg", ".ico", ".gif", ".woff", ".woff2")):
        return
    try:
        ctrl = await client.get(url, headers=stealth.build_headers(url), timeout=8)
    except Exception:
        return
    ctrl_hash = hashlib.md5((ctrl.content or b"")).hexdigest() if ctrl.status_code == 200 else None
    for suffix in (".css", ".js", ".png", ".gif", ".ico", ".woff", ".woff2",
                   ".svg", ".jpg", ".jpeg", ".webp", ".txt"):
        t = url + suffix
        try:
            r = await client.get(t, headers=stealth.build_headers(t), timeout=8)
        except Exception:
            continue
        if r.status_code == 200 and len(r.content or b"") > 500:
            body_hash = hashlib.md5(r.content or b"").hexdigest()
            if body_hash != ctrl_hash:
                stream.emit("CACHE-DECEPTION", t, "static extension served non-trivial body")
                break


async def probe_method_override(client, stealth, url, stream):
    try:
        ctrl = await client.post(url, headers=stealth.build_headers(url), timeout=8)
    except Exception:
        return
    for hdr in ("X-HTTP-Method-Override", "X-HTTP-Method", "X-Method-Override"):
        for meth in ("PUT", "DELETE", "PATCH"):
            try:
                hdrs = stealth.build_headers(url)
                hdrs[hdr] = meth
                test = await client.post(url, headers=hdrs, timeout=8)
            except Exception:
                continue
            if test.status_code in (200, 204) and ctrl.status_code >= 400:
                stream.emit("METHOD-OVERRIDE", url,
                            f"{hdr}={meth} override={test.status_code} control={ctrl.status_code}")
                return


async def probe_fat_get(client, stealth, url, stream):
    try:
        ctrl = await client.get(url, headers=stealth.build_headers(url), timeout=8)
    except Exception:
        return
    hdrs = stealth.build_headers(url)
    hdrs["Content-Type"] = "application/x-www-form-urlencoded"
    try:
        test = await client.request("GET", url, headers=hdrs, timeout=8)
    except Exception:
        return
    if test.status_code == 400 and ctrl.status_code == 200:
        stream.emit("FAT-GET", url, "GET with body rejected, GET without accepted")


async def probe_robots(client, stealth, base, stream):
    paths = []
    try:
        url = urljoin(base, "/robots.txt")
        r = await client.get(url, headers=stealth.build_headers(url), timeout=8)
        if r.status_code == 200:
            body = r.text
            disallows = re.findall(r'Disallow:\s*(\S+)', body)
            allows = re.findall(r'Allow:\s*(\S+)', body)
            stream.emit("ROBOTS", base, f"disallow={len(disallows)} allow={len(allows)}")
            for d in disallows[:100]:
                if d and d != "/":
                    stream.emit("ROBOTS-DISALLOW", base, d)
                    paths.append(urljoin(base, d))
            for a in allows[:100]:
                if a and a != "/":
                    stream.emit("ROBOTS-ALLOW", base, a)
                    paths.append(urljoin(base, a))
            for s in re.findall(r'Sitemap:\s*(\S+)', body)[:20]:
                stream.emit("SITEMAP", base, s)
                paths.append(s)
            for s in re.findall(r'Host:\s*(\S+)', body)[:5]:
                stream.emit("ROBOTS-HOST", base, s)
    except Exception:
        pass
    return paths


async def probe_sitemap(client, stealth, base, stream, max_urls=100000):
    urls = []
    queue = [urljoin(base, "/sitemap.xml")]
    seen = set()
    while queue and len(urls) < max_urls:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            r = await client.get(sm, headers=stealth.build_headers(sm), timeout=15)
            if r.status_code != 200:
                continue
            for u in re.findall(r'<loc>([^<]+)</loc>', r.text):
                u = u.strip()
                if u.endswith(".xml") and "sitemap" in u.lower():
                    queue.append(u)
                else:
                    urls.append(u)
                    if len(urls) <= 200:
                        stream.emit("SITEMAP-URL", base, u[:120])
        except Exception:
            continue
    return urls


async def probe_security_txt(client, stealth, base, stream):
    for path in ("/.well-known/security.txt", "/security.txt"):
        try:
            url = urljoin(base, path)
            r = await client.get(url, headers=stealth.build_headers(url), timeout=8)
            if r.status_code == 200:
                for line in r.text.splitlines()[:30]:
                    if line.strip() and not line.startswith("#"):
                        stream.emit("SECURITY-TXT", base, line[:120])
                return
        except Exception:
            pass


async def probe_humans_ads(client, stealth, base, stream):
    for path, label in [("/humans.txt", "HUMANS"), ("/ads.txt", "ADS-TXT"),
                        ("/app-ads.txt", "APP-ADS-TXT"),
                        ("/manifest.json", "PWA-MANIFEST"),
                        ("/site.webmanifest", "PWA-MANIFEST"),
                        ("/feed.xml", "FEED"), ("/feed", "FEED"),
                        ("/rss.xml", "RSS"), ("/rss", "RSS"),
                        ("/atom.xml", "ATOM"),
                        ("/changelog", "CHANGELOG"),
                        ("/CHANGELOG.md", "CHANGELOG"),
                        ("/README.md", "README"),
                        ("/LICENSE", "LICENSE"),
                        ("/SECURITY.md", "SECURITY-POLICY")]:
        try:
            url = urljoin(base, path)
            r = await client.get(url, headers=stealth.build_headers(url), timeout=8)
            if r.status_code == 200 and len(r.text or "") > 10:
                stream.emit(label, url, r.text[:150].replace("\n", " "))
        except Exception:
            pass


async def probe_favicon(client, stealth, base, stream):
    for path in ("/favicon.ico", "/favicon.png", "/apple-touch-icon.png",
                 "/apple-touch-icon-precomposed.png", "/logo.png", "/logo.svg"):
        try:
            url = urljoin(base, path)
            r = await client.get(url, headers=stealth.build_headers(url), timeout=8)
            if r.status_code == 200 and r.content:
                stream.emit("FAVICON-HASH", base,
                            f"{path} md5={hashlib.md5(r.content).hexdigest()}")
                return
        except Exception:
            pass


async def probe_graphql(client, stealth, base, stream):
    paths = ("/graphql", "/api/graphql", "/v1/graphql", "/query", "/gql",
             "/api/query", "/api/gql", "/v2/graphql", "/graphql/v1",
             "/api/v1/graphql", "/graphql-api", "/graph")
    payloads = [
        ("application/json", {"query": "{__schema{types{name fields{name}}}}"}),
        ("application/graphql", "{__schema{types{name fields{name}}}}"),
    ]
    for path in paths:
        url = urljoin(base, path)
        for ct, payload in payloads:
            hdrs = stealth.build_headers(url, is_ajax=True)
            hdrs["Content-Type"] = ct
            try:
                if ct == "application/json":
                    r = await client.post(url, headers=hdrs, json=payload, timeout=10)
                else:
                    r = await client.post(url, headers=hdrs, data=payload, timeout=10)
                body = r.text or ""
                if r.status_code == 200 and "__schema" in body:
                    stream.emit("GRAPHQL", url, f"introspection enabled ({ct})")
                    if "mutation" in body.lower():
                        stream.emit("GRAPHQL", url, "mutations present")
                    return
            except Exception:
                pass


async def probe_path_fuzz(client, stealth, base, stream):
    sem = asyncio.Semaphore(8)
    hits = []

    async def check(p):
        async with sem:
            url = urljoin(base, f"/{p}")
            try:
                r = await client.get(url, headers=stealth.build_headers(url), timeout=8)
                if r.status_code in (200, 301, 302, 401, 403):
                    stream.emit("PATH", url, f"{r.status_code} len={len(r.content or b'')}")
                    if r.status_code == 200:
                        hits.append(url)
            except Exception:
                pass

    await asyncio.gather(*[check(p) for p in FUZZ_PATHS])
    return hits


def dns_deep(domain, stream):
    try:
        seen = set()
        for ip in socket.getaddrinfo(domain, None):
            addr = ip[4][0]
            if addr not in seen:
                stream.emit("DNS", domain, addr)
                seen.add(addr)
    except Exception as e:
        stream.emit("DNS-ERR", domain, str(e)[:80])
    if not HAS_DNS:
        return
    for rtype in ("A", "AAAA", "NS", "MX", "TXT", "SRV", "CAA", "DNSKEY",
                  "SOA", "PTR", "SPF", "TLSA", "SSHFP", "NAPTR"):
        try:
            for a in dns.resolver.resolve(domain, rtype):
                stream.emit(f"DNS-{rtype}", domain, str(a)[:150])
        except Exception:
            pass
    for name, label in [(f"_dmarc.{domain}", "DMARC"), (domain, "SPF"),
                        (f"default._domainkey.{domain}", "DKIM-DEFAULT"),
                        (f"google._domainkey.{domain}", "DKIM-GOOGLE"),
                        (f"selector1._domainkey.{domain}", "DKIM-SELECTOR1"),
                        (f"selector2._domainkey.{domain}", "DKIM-SELECTOR2"),
                        (f"k1._domainkey.{domain}", "DKIM-K1")]:
        try:
            for a in dns.resolver.resolve(name, "TXT"):
                txt = b"".join(a.strings).decode() if hasattr(a, "strings") else str(a)
                stream.emit("EMAIL-AUTH", label, txt[:200])
        except Exception:
            pass
    for name in (f"default._bimi.{domain}", f"_mta-sts.{domain}",
                 f"_smtp._tls.{domain}", f"_dmarc.{domain}"):
        try:
            for a in dns.resolver.resolve(name, "TXT"):
                stream.emit("EMAIL-POLICY", name, b"".join(a.strings).decode()[:200])
        except Exception:
            pass
    for ns_name in (f"_acme-challenge.{domain}", f"_dnslink.{domain}",
                    f"_github-pages-challenge.{domain}"):
        try:
            for a in dns.resolver.resolve(ns_name, "TXT"):
                stream.emit("WELL-KNOWN", ns_name, b"".join(a.strings).decode()[:200])
        except Exception:
            pass


def reverse_ip_lookup(ip, stream):
    if not HAS_DNS:
        return
    try:
        rev = ".".join(reversed(ip.split("."))) + ".in-addr.arpa"
        for a in dns.resolver.resolve(rev, "PTR"):
            stream.emit("RDNS", ip, str(a)[:120])
    except Exception:
        pass


def zone_transfer(domain, stream):
    if not HAS_DNS:
        return
    try:
        ns_records = dns.resolver.resolve(domain, "NS")
    except Exception:
        return
    for ns in ns_records:
        ns_host = str(ns).rstrip(".")
        try:
            ns_ip = dns.resolver.resolve(ns_host, "A")[0].to_text()
            z = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=5))
            if z:
                stream.emit("DNS-ZONE-TRANSFER", ns_host, "AXFR successful — zone dumped")
                for name in list(z.nodes.keys())[:100]:
                    stream.emit("ZONE-RECORD", ns_host, str(name))
        except dns.exception.DNSException:
            pass
        except Exception:
            pass


def whois_asn(ip, stream):
    try:
        from ipwhois import IPWhois
        rec = IPWhois(ip).lookup_rdap(depth=1)
        stream.emit("ASN", ip,
                    f"ASN={rec.get('asn','?')} {rec.get('asn_description','?')[:60]}")
        stream.emit("ORG", ip, (rec.get("network") or {}).get("name", "?")[:80])
    except Exception:
        pass


async def subdomain_takeover_check(client, stealth, sub, stream):
    if not HAS_DNS:
        return
    cnames = []
    try:
        for a in dns.resolver.resolve(sub, "CNAME"):
            cnames.append(str(a).rstrip(".").lower())
    except Exception:
        pass
    matched_providers = set()
    for cname in cnames:
        for provider, hints in TAKEOVER_CNAME_HINTS.items():
            for h in hints:
                if h in cname:
                    matched_providers.add((provider, cname))
                    break
    if not matched_providers:
        return
    try:
        r = await client.get(f"https://{sub}",
                             headers=stealth.build_headers(f"https://{sub}"),
                             timeout=8)
        body = r.text if hasattr(r, "text") else ""
    except Exception:
        for provider, cname in matched_providers:
            stream.emit("DANGLING-CNAME", sub, f"{provider} via {cname}")
        return
    for provider, cname in matched_providers:
        for fp in TAKEOVER_FINGERPRINTS.get(provider, []):
            if fp in body:
                stream.emit("SUBDOMAIN-TAKEOVER", sub, f"{provider} via {cname}")
                break


def tls_deep(url, stream):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((parsed.hostname, parsed.port or 443), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=parsed.hostname) as ssock:
                cert = ssock.getpeercert()
                stream.emit("TLS-PROTO", parsed.hostname, ssock.version() or "?")
                c = ssock.cipher()
                if c:
                    stream.emit("TLS-CIPHER", parsed.hostname, f"{c[0]} ({c[1]})")
        if cert:
            issuer = dict(x[0] for x in cert.get("issuer", []))
            subject = dict(x[0] for x in cert.get("subject", []))
            stream.emit("TLS", "issuer", issuer.get("organizationName", "?"))
            stream.emit("TLS", "subject", subject.get("commonName", "?"))
            stream.emit("TLS", "expires", cert.get("notAfter", "?"))
            sans = [v for k, v in cert.get("subjectAltName", []) if k == "DNS"]
            if sans:
                stream.emit("TLS", "SANs", ", ".join(sans[:50]))
    except Exception as e:
        stream.emit("TLS", "error", str(e)[:80])


async def crt_sh_subdomains(domain, stream):
    subs = set()
    sources = [
        f"https://crt.sh/?q=%25.{domain}&output=json",
        f"https://crt.sh/?q={domain}&output=json",
    ]
    for src in sources:
        try:
            if HAS_CURL_CFFI:
                async with AsyncSession(impersonate="chrome120") as c:
                    r = await c.get(src, timeout=25)
                    if r.status_code == 200:
                        for entry in r.json():
                            for name in entry.get("name_value", "").split("\n"):
                                name = name.strip().lstrip("*.")
                                if name.endswith("." + domain) or name == domain:
                                    subs.add(name)
            elif httpx:
                async with httpx.AsyncClient(timeout=25) as c:
                    r = await c.get(src)
                    if r.status_code == 200:
                        for entry in r.json():
                            for name in entry.get("name_value", "").split("\n"):
                                name = name.strip().lstrip("*.")
                                if name.endswith("." + domain) or name == domain:
                                    subs.add(name)
        except Exception:
            pass
    try:
        if HAS_CURL_CFFI:
            async with AsyncSession(impersonate="chrome120") as c:
                r = await c.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=20)
                if r.status_code == 200:
                    for line in (r.text or "").splitlines():
                        if "," in line:
                            name = line.split(",")[0].strip()
                            if name.endswith("." + domain) or name == domain:
                                subs.add(name)
    except Exception:
        pass
    try:
        if HAS_CURL_CFFI:
            async with AsyncSession(impersonate="chrome120") as c:
                r = await c.get(f"https://rapiddns.io/subdomain/{domain}?full=1", timeout=20)
                if r.status_code == 200:
                    for m in re.findall(r'<td>([a-z0-9.\-_]+\.[a-z]{2,})</td>', r.text or ""):
                        name = m.strip().lstrip("*.")
                        if name.endswith("." + domain) or name == domain:
                            subs.add(name)
    except Exception:
        pass
    try:
        if HAS_CURL_CFFI:
            async with AsyncSession(impersonate="chrome120") as c:
                r = await c.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", timeout=20)
                if r.status_code == 200:
                    data = r.json()
                    for entry in data.get("passive_dns", []):
                        name = entry.get("hostname", "").strip().lstrip("*.")
                        if name and (name.endswith("." + domain) or name == domain):
                            subs.add(name)
    except Exception:
        pass
    for s in sorted(subs)[:1000]:
        stream.emit("SUBDOMAIN", s, "aggregated")
    return subs


class Crawler:
    def __init__(self, start, mode, workers=10, max_pages=100,
                 rate_limit=0, passive=False, allow_subdomains=True,
                 timeout=15, stealth=None, deep_assets=False,
                 state_store=None, field_scope="rdn", crawl_scope=None,
                 cookie=None, bearer=None, jwt_wordlist=None, proxy=None,
                 stream=None, output_dir="output"):
        self.start = start
        self.mode = mode
        self.scope = registered_domain(start)
        self.workers = workers
        self.max_pages = max_pages
        self.rate_limit = rate_limit
        self.passive = passive
        self.allow_subdomains = allow_subdomains
        self.timeout = timeout
        self.stealth = stealth or Stealth()
        self.deep_assets = deep_assets
        self.state_store = state_store
        self.field_scope = field_scope
        self.crawl_scope = crawl_scope
        self.cookie = cookie
        self.bearer = bearer
        self.jwt_wordlist = jwt_wordlist
        self.proxy = proxy
        self.stream = stream or LiveStream()
        self.output_dir = output_dir

        self.visited = set()
        self.assets = set()
        self.queue = asyncio.Queue()
        self.pending = 0
        self.lock = asyncio.Lock()
        self.results = []
        self.all_urls = set()
        self.tech_stack = set()
        self.param_wordlist = set()
        self._last = 0.0
        self._rl = asyncio.Lock()
        self.start_time = time.time()
        self._last_checkpoint = 0.0
        self._finished = False
        self._interrupted = False
        self._active_tasks = []

        self.stream.set_listener(self._record)

    def _record(self, typ, key, val):
        self.results.append((typ, key, val))

    def _in_scope(self, url):
        if not in_scope(url, self.scope, self.field_scope):
            return False
        return path_in_scope(url, self.crawl_scope)

    def _extra_headers(self):
        h = {}
        if self.cookie:
            h["Cookie"] = self.cookie
        if self.bearer:
            h["Authorization"] = f"Bearer {self.bearer}"
        return h

    async def _throttle(self):
        if not self.rate_limit:
            return
        async with self._rl:
            wait = (1.0 / self.rate_limit) - (time.time() - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.time()

    async def enqueue(self, u):
        if not u or not self._in_scope(u):
            return
        async with self.lock:
            if u in self.visited or u in self.assets:
                return
            if is_binary(u) and not self.deep_assets:
                self.assets.add(u)
                self.stream.emit("ASSET", u, ext_of(u) or "binary")
                return
            if self.max_pages is not None and self.pending >= self.max_pages:
                return
            self.visited.add(u)
            self.pending += 1
            await self.queue.put(u)

    async def worker(self, client):
        while True:
            url = await self.queue.get()
            if url is None:
                self.queue.task_done()
                return
            if self._interrupted:
                self.queue.task_done()
                return
            try:
                await self._throttle()
                await self.stealth.wait(url)
                if self._interrupted:
                    self.queue.task_done()
                    return
                await self.handle(client, url)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.stream.emit("ERR", url, str(e)[:100])
            finally:
                async with self.lock:
                    self.pending -= 1
                self.queue.task_done()

    async def _fetch(self, client, url, method="GET", is_ajax=False):
        for attempt in range(3):
            if self._interrupted:
                return None
            hdrs = self.stealth.build_headers(url, is_ajax=is_ajax)
            hdrs.update(self._extra_headers())
            try:
                if method == "GET":
                    r = await client.get(url, headers=hdrs, timeout=self.timeout)
                else:
                    r = await client.request(method, url, headers=hdrs, timeout=self.timeout)
                if r.status_code in (429, 503):
                    vendor = detect_bot_challenge(r)
                    if vendor:
                        self.stream.emit("BOT-CHALLENGE", url, vendor)
                    await self.stealth.mark_failure(url, r.status_code)
                    if attempt < 2:
                        await asyncio.sleep(2 ** attempt)
                        continue
                else:
                    await self.stealth.mark_success(url)
                return r
            except Exception:
                await self.stealth.mark_failure(url)
                if attempt < 2:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return None
        return None

    async def handle(self, client, url):
        r = await self._fetch(client, url)
        if r is None:
            return
        ctype = r.headers.get("content-type", "").lower()

        self.stream.emit("FETCHED", url, f"{r.status_code} {ctype[:40]}")

        if r.status_code == 200:
            path = urlparse(url).path
            if path in HIGH_RISK_SENSITIVE:
                body_snip = ""
                try:
                    body_snip = (r.text or "")[:200].replace("\n", " ")
                except Exception:
                    pass
                self.stream.emit("SENSITIVE-200", url,
                                 f"len={len(r.content or b'')} snip={body_snip[:100]}")

        if self.deep_assets and ext_of(url) in DEEP_ASSET_EXT and r.status_code == 200:
            content = r.content if hasattr(r, "content") else b""
            self.stream.emit("ASSET-FETCHED", url, f"{len(content)} bytes")
            try:
                deep_analyze_asset(content, url, self.stream)
            except Exception as e:
                self.stream.emit("ASSET-ERR", url, str(e)[:100])

        body = ""
        if any(t in ctype for t in ("text", "json", "xml", "javascript", "yaml", "css")):
            try:
                body = r.text
            except Exception:
                body = ""

        if self.mode in ("defensive", "all"):
            defensive_pass(r, self.stream)
            waf_fingerprint(r, self.stream)
        if self.mode in ("offensive", "all"):
            fingerprint_tech(r, body, self.stream)

        if not body:
            return
        ext = ext_of(url)

        if "html" in ctype or "xml" in ctype or "svg" in ctype:
            page_css, page_js = set(), set()
            links, page_css, page_js = extract_all(body, url, self.stream,
                                                   page_css=page_css, page_js=page_js)
            for js in page_js:
                try:
                    for l in mine_js_deep(js, url, self.stream):
                        n = normalize(l, url)
                        if n:
                            links.add(n)
                except Exception:
                    pass
            for cs in page_css:
                try:
                    for l in parse_css(cs, url, self.stream):
                        n = normalize(l, url)
                        if n:
                            links.add(n)
                except Exception:
                    pass
            for l in links:
                self.all_urls.add(l)
                p = urlparse(l)
                for k in parse_qs(p.query).keys():
                    self.param_wordlist.add(k)
                await self.enqueue(l)
            if self.mode == "all":
                for n in self._discover_pagination(body, url):
                    await self.enqueue(n)

        elif "javascript" in ctype or ext in (".js", ".mjs"):
            if self.mode in ("offensive", "all"):
                for l in mine_js_deep(body, url, self.stream):
                    n = normalize(l, url)
                    if n:
                        self.all_urls.add(n)
                        await self.enqueue(n)
                for imp in extract_dynamic_imports(body, url):
                    if self._in_scope(imp):
                        await self.enqueue(imp)
        elif "json" in ctype or ext == ".json":
            if self.mode in ("offensive", "all"):
                for l in mine_json_deep(body, url, self.stream):
                    n = normalize(l, url)
                    if n:
                        self.all_urls.add(n)
                        await self.enqueue(n)
        elif "css" in ctype or ext == ".css":
            if self.mode in ("offensive", "all"):
                for l in parse_css(body, url, self.stream):
                    n = normalize(l, url)
                    if n:
                        self.all_urls.add(n)
                        await self.enqueue(n)
        else:
            for l in RE_URL.findall(body) + RE_PATH.findall(body):
                n = normalize(l, url)
                if n:
                    self.all_urls.add(n)
                    await self.enqueue(n)

    def _discover_pagination(self, html, url):
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        for k in q:
            if k.lower() in NON_PAGINATION_KEYS:
                return []
        out = []
        for key in PAGINATION_KEYS:
            if key in q:
                try:
                    cur = int(q[key][0])
                except Exception:
                    continue
                for nxt in (cur + 1, cur + 2, cur + 3, cur + 5, cur + 10):
                    q2 = {**q, key: [str(nxt)]}
                    out.append(parsed._replace(query=urlencode(q2, doseq=True)).geturl())
                break
        return out

    def _checkpoint(self, force=False):
        if not self.state_store:
            return
        now = time.time()
        if not force and (now - self._last_checkpoint < 30):
            return
        self._last_checkpoint = now
        self.state_store.save({
            "target": self.start, "mode": self.mode,
            "visited": list(self.visited), "assets": list(self.assets),
            "all_urls": list(self.all_urls), "results": self.results,
            "timestamp": now,
        })

    def save_results(self):
        try:
            fqdn = extract(self.start).fqdn or "target"
        except Exception:
            fqdn = "target"
        out = Path(self.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        try:
            fname = out / f"{fqdn}-{self.mode}.txt"
            seen = set()
            with open(fname, "w") as f:
                for typ, key, val in self.results:
                    t = (typ, str(key), str(val))
                    if t in seen:
                        continue
                    seen.add(t)
                    safe_val = str(val).replace("\t", " ").replace("\n", " ")
                    safe_key = str(key).replace("\t", " ").replace("\n", " ")
                    f.write(f"{typ}\t{safe_key}\t{safe_val}\n")
            with open(out / f"{fqdn}-visited.txt", "w") as f:
                for u in sorted(self.visited):
                    f.write(u + "\n")
            with open(out / f"{fqdn}-all-urls.txt", "w") as f:
                for u in sorted(self.all_urls):
                    f.write(u + "\n")
            if self.assets:
                with open(out / f"{fqdn}-assets.txt", "w") as f:
                    for a in sorted(self.assets):
                        f.write(a + "\n")
            if self.param_wordlist:
                with open(out / f"{fqdn}-params.txt", "w") as f:
                    for p in sorted(self.param_wordlist):
                        f.write(p + "\n")
            return fname
        except Exception:
            return None

    async def run_probes(self, client):
        base = base_url_of(self.start)

        async def _bundle():
            try:
                await asyncio.to_thread(dns_deep, self.scope, self.stream)
                await asyncio.to_thread(tls_deep, self.start, self.stream)
                try:
                    ip = await asyncio.to_thread(socket.gethostbyname, self.scope)
                    await asyncio.to_thread(reverse_ip_lookup, ip, self.stream)
                    await asyncio.to_thread(whois_asn, ip, self.stream)
                    await asyncio.to_thread(zone_transfer, self.scope, self.stream)
                except Exception:
                    pass

                if self.mode in ("defensive", "all"):
                    for p in await probe_robots(client, self.stealth, base, self.stream):
                        await self.enqueue(p)
                    for u in await probe_sitemap(client, self.stealth, base, self.stream,
                                                 max_urls=self.max_pages or 100000):
                        await self.enqueue(u)
                    await probe_security_txt(client, self.stealth, base, self.stream)
                    await probe_humans_ads(client, self.stealth, base, self.stream)

                if self.mode in ("offensive", "all") and not self.passive:
                    subs = await crt_sh_subdomains(self.scope, self.stream)
                    if self.allow_subdomains:
                        for s in subs:
                            if self.mode == "all":
                                await self.enqueue(f"https://{s}")
                            await subdomain_takeover_check(client, self.stealth, s, self.stream)
                    await probe_methods(client, self.stealth, self.start, self.stream)
                    await probe_redirect(client, self.stealth, self.start, self.stream)
                    await probe_cors_preflight(client, self.stealth, self.start, self.stream)
                    await probe_cache_poisoning(client, self.stealth, self.start, self.stream)
                    await probe_cache_deception(client, self.stealth, self.start, self.stream)
                    await probe_method_override(client, self.stealth, self.start, self.stream)
                    await probe_fat_get(client, self.stealth, self.start, self.stream)
                    await probe_graphql(client, self.stealth, base, self.stream)
                    await probe_favicon(client, self.stealth, base, self.stream)
                    for p in await probe_path_fuzz(client, self.stealth, base, self.stream):
                        if self.mode == "all":
                            await self.enqueue(p)

                if self.mode in ("offensive", "all"):
                    for p in SENSITIVE_PATHS:
                        await self.enqueue(urljoin(base, p))
            except Exception as e:
                self.stream.emit("PROBE-ERR", "bundle", str(e)[:120])

        task = asyncio.create_task(_bundle())
        self._active_tasks.append(task)

    async def run(self, resume_state=None):
        if resume_state:
            self.stream.emit("INFO", self.start,
                             f"resume visited={len(resume_state.get('visited', []))} "
                             f"findings={len(resume_state.get('results', []))}")
            self.visited = set(resume_state.get("visited", []))
            self.assets = set(resume_state.get("assets", []))
            self.all_urls = set(resume_state.get("all_urls", []))
            for r in resume_state.get("results", []):
                self.results.append(tuple(r))

        await self.enqueue(self.start)

        monitor_task = None
        try:
            async with ClientWrapper(proxy=self.proxy) as client:
                workers = [asyncio.create_task(self.worker(client))
                           for _ in range(self.workers)]

                if not resume_state:
                    await self.run_probes(client)

                async def monitor():
                    try:
                        while not self._interrupted:
                            if not (self.stream.silent or self.stream.jsonl):
                                elapsed = time.time() - self.start_time
                                rate = len(self.visited) / elapsed if elapsed > 0 else 0
                                hud_line(self.start, "RUNNING", self.stream.count,
                                         len(self.visited), len(self.assets),
                                         self.max_pages, elapsed, rate,
                                         self.stealth.get_host_backoff())
                            self._checkpoint()
                            await asyncio.sleep(2)
                    except asyncio.CancelledError:
                        return
                    except Exception:
                        return

                monitor_task = asyncio.create_task(monitor())
                try:
                    await self.queue.join()
                except asyncio.CancelledError:
                    pass

                for _ in range(self.workers):
                    try:
                        await self.queue.put(None)
                    except Exception:
                        pass
                try:
                    await asyncio.gather(*workers, return_exceptions=True)
                except Exception:
                    pass
        finally:
            if monitor_task is not None and not monitor_task.done():
                monitor_task.cancel()
                try:
                    await monitor_task
                except (asyncio.CancelledError, Exception):
                    pass
            for t in self._active_tasks:
                if not t.done():
                    t.cancel()
            for t in self._active_tasks:
                if not t.done():
                    try:
                        await t
                    except (asyncio.CancelledError, Exception):
                        pass
            if self.mode in ("offensive", "all"):
                try:
                    idor_scan(self.all_urls, self.stream)
                except Exception:
                    pass
            self._checkpoint(force=True)
            self.save_results()
            self._finished = True

    def interrupt(self):
        self._interrupted = True


def hud_line(target, status="IDLE", findings=0, pages=0, assets=0, cap=None,
             elapsed=0, rate=0, backoff=None):
    cap_str = f"/{cap}" if cap else "/∞"
    line = (
        f"[bold cyan]{status:<9}[/] [white]{target[:55]:<55}[/] "
        f"[dim]pages[/] {pages}{cap_str} "
        f"[dim]assets[/] {assets} "
        f"[dim]find[/] {findings} "
        f"[dim]t[/] {elapsed:.0f}s "
        f"[dim]r[/] {rate:.1f}/s"
    )
    console.print(line, highlight=False)
    if backoff:
        items = ", ".join(f"{h}:{s:.0f}s" for h, s in list(backoff.items())[:3])
        console.print(f"[dim red]⏸ backoff {items}[/]", highlight=False)


def parse_args(argv):
    p = argparse.ArgumentParser(
        description=f"{TOOL_NAME} — live streaming recon engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Author: {AUTHOR}")
    p.add_argument("target", nargs="?", default=None)
    p.add_argument("-l", "--list", default=None)
    p.add_argument("-m", "--max-pages", type=int, default=100)
    p.add_argument("--unlimited", action="store_true")
    p.add_argument("-w", "--workers", type=int, default=10)
    p.add_argument("-r", "--rate", type=float, default=0)
    p.add_argument("-t", "--timeout", type=float, default=15.0)
    p.add_argument("--passive", action="store_true")
    p.add_argument("--no-subdomains", action="store_true")
    p.add_argument("--deep-assets", action="store_true")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--reset", action="store_true")
    p.add_argument("-o", "--output", default="output")
    p.add_argument("-y", "--yes", action="store_true")
    p.add_argument("--min-delay", type=float, default=0.5)
    p.add_argument("--max-delay", type=float, default=2.5)
    p.add_argument("--fast", action="store_true")
    p.add_argument("-fs", "--field-scope", choices=["rdn", "fqdn", "dn"], default="rdn")
    p.add_argument("-cs", "--crawl-scope", default=None)
    p.add_argument("-j", "--jsonl", action="store_true")
    p.add_argument("--silent", dest="silent", action="store_true")
    p.add_argument("-silent", dest="silent", action="store_true")
    p.add_argument("-q", "--quiet", action="store_true")
    p.add_argument("-nc", "--no-color", action="store_true")
    p.add_argument("--sarif", action="store_true")
    p.add_argument("--baseline", default=None)
    p.add_argument("--cookie", default=None)
    p.add_argument("--bearer", default=None)
    p.add_argument("--jwt-wordlist", default=None)
    p.add_argument("--proxy", default=None)
    p.add_argument("--self-test", action="store_true")
    return p.parse_args(argv)


def emit_sarif(results, fqdn, out_path):
    rules = {}
    findings = []
    for typ, key, val in results:
        if typ not in rules:
            rules[typ] = {
                "id": typ, "name": typ,
                "shortDescription": {"text": typ},
                "defaultConfiguration": {"level": {
                    "critical": "error", "high": "error",
                    "medium": "warning", "low": "note", "info": "note",
                }.get(severity_of(typ), "note")},
            }
        findings.append({
            "ruleId": typ,
            "level": "error" if severity_of(typ) in ("critical", "high") else "warning",
            "message": {"text": f"{key} -> {val}"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": str(key)[:500]},
                "region": {"startLine": 1, "startColumn": 1},
            }}],
        })
    doc = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": TOOL_NAME, "rules": list(rules.values())}},
            "results": findings,
            "properties": {"target": fqdn},
        }],
    }
    with open(out_path, "w") as f:
        json.dump(doc, f, indent=2)


def diff_with_baseline(current, baseline_path):
    try:
        baseline = set()
        with open(baseline_path) as f:
            for line in f:
                parts = line.rstrip("\n").split("\t", 2)
                if len(parts) == 3:
                    baseline.add(tuple(parts))
    except Exception:
        return
    current_set = set((str(t), str(k), str(v)) for t, k, v in current)
    new = current_set - baseline
    if new:
        console.print(Panel.fit(
            f"[green]{len(new)} new findings since baseline[/]",
            border_style="green"))
        for typ, key, val in sorted(new)[:100]:
            console.print(f"[green]+[/] {typ}: {key} -> {val}")


def run_self_test():
    test_stream = LiveStream(silent=True)
    test_stream.set_target("https://example.com")
    test_stealth = Stealth(min_delay=0, max_delay=0)
    crawler = Crawler("https://example.com", "all", workers=3, max_pages=5,
                      rate_limit=0, passive=True, allow_subdomains=False,
                      timeout=10, stealth=test_stealth, deep_assets=False,
                      state_store=None, field_scope="rdn", crawl_scope=None,
                      stream=test_stream)

    async def go():
        await crawler.run()
    try:
        asyncio.run(go())
        print(json.dumps({"ok": True, "findings": test_stream.count}))
        return 0
    except Exception as e:
        print(json.dumps({"ok": False, "err": str(e)}))
        return 1


def run_scan(target, mode, args, stream, state_store, resume_state=None):
    max_pages = None if args.unlimited else args.max_pages
    stealth = Stealth(min_delay=0 if args.fast else args.min_delay,
                      max_delay=0 if args.fast else args.max_delay)

    crawler = Crawler(target, mode, workers=args.workers, max_pages=max_pages,
                      rate_limit=args.rate, passive=args.passive,
                      allow_subdomains=not args.no_subdomains,
                      timeout=args.timeout, stealth=stealth,
                      deep_assets=args.deep_assets,
                      state_store=state_store,
                      field_scope=args.field_scope,
                      crawl_scope=args.crawl_scope,
                      cookie=args.cookie, bearer=args.bearer,
                      jwt_wordlist=args.jwt_wordlist,
                      proxy=args.proxy,
                      stream=stream,
                      output_dir=args.output)

    def _sig_handler(signum, frame):
        try:
            console.print("\n[yellow]⏸ Interrupt — flushing results...[/]")
        except Exception:
            pass
        crawler.interrupt()

    old_int = None
    old_term = None
    try:
        old_int = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, _sig_handler)
    except Exception:
        pass
    try:
        old_term = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, _sig_handler)
    except Exception:
        pass
    interrupted = False
    t0 = time.time()
    try:
        asyncio.run(crawler.run(resume_state=resume_state))
    except KeyboardInterrupt:
        interrupted = True
        crawler.interrupt()
    except asyncio.CancelledError:
        pass
    finally:
        try:
            if old_int is not None:
                signal.signal(signal.SIGINT, old_int)
            if old_term is not None:
                signal.signal(signal.SIGTERM, old_term)
        except Exception:
            pass
        try:
            crawler._checkpoint(force=True)
            crawler.save_results()
        except Exception:
            pass
    elapsed = time.time() - t0
    return crawler, elapsed, interrupted


def normalize_target(raw):
    if not raw:
        return None
    t = raw.strip()
    if not t:
        return None
    if not t.startswith(("http://", "https://")):
        t = "https://" + t
    try:
        p = urlparse(t)
        if not p.hostname:
            return None
    except Exception:
        return None
    return t


def main():
    args = parse_args(sys.argv[1:])

    if args.self_test:
        sys.exit(run_self_test())

    interactive = not args.silent and not args.jsonl and not args.list

    if interactive and not args.target:
        banner()
        warning()
        if not args.yes:
            if not get_consent():
                console.print("\n[red]Aborted.[/]")
                sys.exit(1)

    targets = None
    if args.list:
        try:
            targets = [normalize_target(l.strip())
                       for l in Path(args.list).read_text().splitlines() if l.strip()]
            targets = [t for t in targets if t]
        except Exception as e:
            console.print(f"[red]Cannot read list: {e}[/]")
            sys.exit(1)
    elif args.target:
        n = normalize_target(args.target)
        if n:
            targets = [n]

    current_target = targets[0] if targets else None

    while True:
        if interactive:
            if current_target is None:
                try:
                    t = console.input("[bold cyan]Enter target URL (or '5' to quit): [/]").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                if not t or t.lower() in ("q", "quit", "exit", "5"):
                    break
                current_target = normalize_target(t)
                if not current_target:
                    console.print("[red]Invalid target.[/]")
                    continue

            show_menu(current_target)
            try:
                choice = console.input("[bold cyan]>> [/]").strip().lower()
            except (EOFError, KeyboardInterrupt):
                break
            if choice in ("q", "quit", "exit", "5"):
                break
            if choice in ("n", "4"):
                current_target = None
                continue
        else:
            choice = "3"

        if choice not in ("1", "2", "3"):
            console.print("[red]Invalid selection.[/]")
            continue

        mode = {"1": "offensive", "2": "defensive", "3": "all"}[choice]

        target = current_target
        if not target:
            continue

        stream = LiveStream(silent=args.silent, jsonl=args.jsonl, quiet=args.quiet)
        stream.set_target(target)

        try:
            fqdn = extract(target).fqdn or "target"
        except Exception:
            fqdn = "target"
        state_store = StateStore(fqdn, args.output)
        if args.reset:
            state_store.clear()
        resume_state = state_store.load() if args.resume else None

        if interactive:
            console.print()
            console.print(f"[bold cyan]── BEGIN LIVE STREAM ──[/]  "
                          f"[dim]target[/] [white]{target}[/]  "
                          f"[dim]mode[/] [cyan]{mode}[/]  "
                          f"[dim]cap[/] [cyan]{'∞' if args.unlimited else args.max_pages}[/]"
                          f"{'  [dim]quiet[/]' if args.quiet else ''}")
            console.print()

        try:
            crawler, elapsed, interrupted = run_scan(
                target, mode, args, stream, state_store, resume_state)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped.[/]")
            if not interactive:
                break
            continue
        except Exception as e:
            console.print(f"\n[red]Scan error: {e}[/]")
            if not interactive:
                break
            wait_enter("Press Enter to return to menu")
            continue

        if args.baseline:
            diff_with_baseline(crawler.results, args.baseline)

        out = Path(args.output)
        out.mkdir(parents=True, exist_ok=True)
        if args.sarif:
            try:
                emit_sarif(crawler.results, fqdn, out / f"{fqdn}-{mode}.sarif")
            except Exception:
                pass

        if args.silent or args.jsonl:
            if not interactive:
                break
            continue

        sev_counts = stream.sev_counts
        console.print()
        status_color = "yellow" if interrupted else "green"
        status_text = "INTERRUPTED (results saved)" if interrupted else "COMPLETE"

        summary = Table.grid(expand=False, padding=(0, 1))
        summary.add_column(justify="left")
        summary.add_row(
            f"[bold {status_color}]{status_text}[/]",
            f"pages=[cyan]{len(crawler.visited)}[/]",
            f"assets=[cyan]{len(crawler.assets)}[/]",
            f"findings=[cyan]{stream.count}[/]",
            f"crit=[bright_red]{sev_counts.get('critical', 0)}[/]",
            f"high=[red]{sev_counts.get('high', 0)}[/]",
            f"med=[yellow]{sev_counts.get('medium', 0)}[/]",
            f"low=[cyan]{sev_counts.get('low', 0)}[/]",
            f"info=[white]{sev_counts.get('info', 0)}[/]",
            f"elapsed=[cyan]{elapsed:.1f}s[/]",
        )
        console.print(Panel(summary, border_style=status_color, expand=False))

        cap = None if args.unlimited else args.max_pages
        visited_n = len(crawler.visited)
        site_name = fqdn

        if interrupted:
            console.print(Panel(
                f"[bold yellow]⏸ CRAWL INTERRUPTED[/]\n\n"
                f"[white]{site_name}[/] — stopped after [bold cyan]{visited_n}[/] "
                f"page{'s' if visited_n != 1 else ''}.\n"
                f"Run with [cyan]--resume[/] to continue from the checkpoint.",
                title="[bold yellow]PARTIAL CRAWL[/]",
                border_style="yellow", padding=(1, 2)))
        elif cap is not None and visited_n >= cap:
            console.print(Panel(
                f"[bold yellow]⚠ CRAWL CAP REACHED[/]\n\n"
                f"[white]{site_name}[/] — stopped at the configured "
                f"[bold]{cap}[/]-page limit after crawling [bold cyan]{visited_n}[/] pages.\n"
                f"The queue may still have links. Re-run with [cyan]--unlimited[/] "
                f"or raise [cyan]-m[/] to discover everything.",
                title="[bold yellow]PARTIAL CRAWL[/]",
                border_style="yellow", padding=(1, 2)))
        else:
            console.print(Panel(
                f"[bold green]✔ ENTIRE WEBSITE CRAWLED[/]\n\n"
                f"[white]{site_name}[/] has only [bold cyan]{visited_n}[/] "
                f"crawlable page{'s' if visited_n != 1 else ''} "
                f"within the current scope.\n"
                f"All in-scope links have been exhausted — nothing left to follow.",
                title="[bold green]CRAWL COMPLETE[/]",
                border_style="green", padding=(1, 2)))

        console.print(f"[dim]Findings   → [cyan]{out / (fqdn + '-' + mode + '.txt')}[/][/]")
        console.print(f"[dim]Visited    → [cyan]{out / (fqdn + '-visited.txt')}[/][/]")
        console.print(f"[dim]All URLs   → [cyan]{out / (fqdn + '-all-urls.txt')}[/][/]")
        console.print(f"[dim]Checkpoint → [cyan]{state_store.path}[/][/]")

        if not interactive:
            break

        wait_enter("Press Enter to return to menu")

    console.print(f"\n[dim italic]{TOOL_NAME} · {AUTHOR}[/]")


if __name__ == "__main__":
    main()

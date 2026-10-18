
<div align="center">

# Website Recon Engine & A Powerful Crawler

Attack Surface Mapping · Secret Mining · Passive & Active Recon · Real-Time Streaming

https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white
https://img.shields.io/badge/License-Authorization_Only-red?style=flat-square
https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square
https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square
https://img.shields.io/badge/Author-SYLHETYHACKVENGER-9b59b6?style=flat-square

⚡ Quick Start · 🎯 Features · 📖 Usage · 🔬 Detection Catalog · ⚠️ Legal

</div>

---

[!WARNING]

⚠️ AUTHORIZATION REQUIRED

SILKFANG performs passive AND active reconnaissance. Active probes include HTTP method fuzzing, open-redirect injection, GraphQL introspection, path brute-forcing, cache poisoning, subdomain takeover checks, and DNS zone transfer attempts.

Only use against systems you own or have explicit written authorization to test.
Unauthorized use violates the Computer Fraud and Abuse Act (CFAA), the UK Computer Misuse Act, and equivalent laws in most jurisdictions.

The author assumes NO liability for misuse.

---

📑 Table of Contents

1. What is SILKFANG?
2. Feature Matrix
3. Quick Start
4. Installation
5. Usage
6. Command Line Reference
7. Scan Profiles
8. Detection Catalog
9. Architecture Deep-Dive
10. Output Formats
11. Advanced Workflows
12. Anti-Detection & Stealth
13. Scope Control
14. Checkpointing & Resume
15. CI/CD Integration
16. Real-World Case Studies
17. Troubleshooting
18. Performance Tuning
19. Legal & Ethics
20. Contributing
21. Credits

---

🎯 What is SILKFANG?

SILKFANG is a single-file, dependency-light, live-streaming reconnaissance engine written in Python. It combines the passive attack-surface mapping capabilities of tools like aquatone, subfinder, and gau with the active verification capabilities of nuclei, dalfox, and sqlmap — all while streaming results to your terminal in real time.

Unlike traditional recon scanners that silently grind through a wordlist and dump a report at the end, SILKFANG streams every finding as it happens, color-coded by severity, with full JSON-lines output for pipeline integration.

The Philosophy

"A pentester's most valuable asset is not a payload — it is context. SILKFANG finds context: what's in scope, what's exposed, what's leaking, what's forgotten, what's dangerous."

SILKFANG is built on four principles:

Principle Implementation
Stream everything Results appear the moment they're discovered. No waiting 10 minutes for a batch report.
Respect the target Built-in per-host backoff, jitter, UA rotation, and polite rate limiting.
Never lose work Automatic JSONL checkpointing every 30 seconds. Ctrl-C = safe abort with flushed results.
Zero lock-in Single .py file. Pure stdlib + optional acceleration. Runs anywhere Python runs.

What SILKFANG is NOT

· ❌ Not an exploit framework — it identifies surface area, doesn't weaponize
· ❌ Not a fuzzer — path discovery is a small, rate-limited part of the picture
· ❌ Not a scraper — it maps, it doesn't archive
· ❌ Not a replacement for manual review — it feeds your manual review

---

🚀 Feature Matrix

Offensive Reconnaissance

Feature Status Description
Subdomain Enumeration ✅ crt.sh CT log mining + CNAME analysis
Subdomain Takeover Detection ✅ 16 provider fingerprints + CNAME pattern matching
URL / Endpoint Extraction ✅ HTML, JS, CSS, JSON, sitemap, robots, meta-refresh
JavaScript AST Analysis ✅ esprima-powered endpoint & literal discovery
Secret Scanning ✅ 25+ secret patterns (AWS, GCP, Stripe, GitHub, Slack...)
JWT Audit & Cracking ✅ alg=none, weak HS256 secret brute-force
GraphQL Introspection ✅ 5 common endpoints, JSON + application/graphql
Open Redirect Probing ✅ 6 common redirect parameters
CORS Misconfiguration ✅ Wildcard, reflection, credentials-combined
HTTP Method Risk ✅ TRACE, PUT, DELETE, PATCH via OPTIONS Allow
Method Override Abuse ✅ X-HTTP-Method-Override probe
Cache Poisoning ✅ 4 unkeyed-header reflections
Cache Deception ✅ Static-suffix extension test
Fat GET ✅ GET-with-body detection
IDOR Candidate Mining ✅ Numeric sequencing & UUID clustering
Path Brute-Force ✅ 60+ curated paths, rate-limited
Sensitive File Detection ✅ 100+ paths with HIGH_RISK matrix
DNS Zone Transfer ✅ AXFR attempt per NS record
Reverse DNS & ASN ✅ PTR + RDAP lookup via ipwhois

Defensive Audit

Feature Status Description
Security Header Audit ✅ 18 headers, HSTS, CSP, COOP/COEP/CORP
CSP Weakness ✅ unsafe-inline, unsafe-eval, wildcard, report-uri
HSTS Analysis ✅ max-age, preload, includeSubDomains
Cookie Attribute Audit ✅ Secure/HttpOnly/SameSite, prefixes, JWT-in-cookie
TLS/SSL Inspection ✅ Protocol, cipher, SANs, issuer, expiry
CORS Preflight ✅ Live OPTIONS probe with evil.example.com origin
WAF Fingerprinting ✅ 11 WAF vendors via headers & cookies
Bot-Challenge Detection ✅ Cloudflare, DataDome, Akamai, PerimeterX, Kasada
Email Authentication ✅ SPF, DMARC, BIMI
robots.txt / sitemap.xml ✅ Parsing + URL discovery
security.txt ✅ /.well-known/security.txt parsing
humans.txt / ads.txt ✅ app-ads.txt, manifest.json, feeds

Passive & Structural

Feature Status Description
Technology Fingerprinting ✅ 40+ frameworks & servers
Analytics Detection ✅ GA-UA, GA4, GTM, FB-Pixel, Hotjar, Segment
Error Tracking Detection ✅ Sentry, Rollbar, Datadog, New Relic, Honeybadger
Chat Widget Detection ✅ Intercom, Drift, Crisp, Zendesk
Payment Gateway Detection ✅ Stripe, PayPal, Square, Cloudinary
Auth Provider Detection ✅ Auth0, Okta, Cognito, Clerk, Firebase Auth
Cloud Detection ✅ Firebase, Supabase, Mapbox
Real-Time Detection ✅ Pusher, PubNub, Algolia
Feature Flag Detection ✅ LaunchDarkly, Optimizely
SRI Hash Audit ✅ Missing integrity on external script/link
Form Analysis ✅ CSRF missing, _blank without noopener, hidden fields
Meta/OG/Microdata ✅ Social cards, schema.org extraction
Comment Mining ✅ TODO/FIXME/secret-hint detection in HTML comments
Email & Phone Harvesting ✅ Regex, filtered for false positives
Crypto Addresses ✅ BTC, ETH, XMR
Deep Asset Analysis ✅ Image EXIF/GPS, PDF meta, Office meta, archives
Font Metadata ✅ fontTools-powered name table extraction
SVG Script Detection ✅ Embedded <script> & external refs

Operational

Feature Status Description
Live Streaming ✅ Every finding in real time, colored & severity-ranked
JSON-Lines Output ✅ --jsonl for pipeline consumers
SARIF Export ✅ GitHub Code Scanning compatible
Baseline Diffing ✅ --baseline to diff runs
Checkpoint & Resume ✅ --resume, --reset
Multi-Target List ✅ -l targets.txt
Proxy Support ✅ --proxy http://...
Auth Injection ✅ --cookie, --bearer
Scope Control ✅ --field-scope rdn\|fqdn\|dn, --crawl-scope regex
Per-Host Backoff ✅ Exponential, capped at 300s
UA Rotation ✅ 25+ curated real-world UAs
Chrome Impersonation ✅ via curl_cffi when available
Self-Test Mode ✅ --self-test smoke test
Interactive Menu ✅ Fancy Rich-based CLI

---

⚡ Quick Start

```bash
# Clone
git clone https://github.com/sylhetyhackvenger/Silkfang 
cd Silkfang 

# Install dependencies
pip install beautifulsoup4 lxml tldextract rich curl_cffi

# (optional, unlocks more)
pip install dnspython esprima Pillow pypdf fonttools ipwhois uvloop

# Fire it
python3 silkfang.py
```

```bash
# Fast, focused offensive scan
python3 silkfang.py https://target.com -m 500 --fast

# Full audit, all modes, unlimited pages
python3 silkfang.py https://target.com --unlimited

# Silent JSON-lines for pipelines
python3 silkfang.py https://target.com --jsonl -q --silent > findings.jsonl
```

---

📦 Installation

Requirements

· Python 3.9+ (3.10+ recommended for asyncio.to_thread)
· Linux / macOS / WSL2 for full feature set
· Windows 10/11 works but uvloop and signal behave differently

Minimal Install

The only hard dependencies are:

```bash
pip install beautifulsoup4 lxml tldextract rich
```

Without these, SILKFANG exits with a clear FATAL error on startup.

Recommended Install

```bash
pip install beautifulsoup4 lxml tldextract rich \
            curl_cffi httpx \
            dnspython esprima \
            Pillow pypdf fonttools \
            ipwhois uvloop
```

Package Purpose Unlocks
curl_cffi TLS/JA3 impersonation Chrome 120 fingerprint impersonation
httpx Fallback HTTP client HTTP/2, if curl_cffi unavailable
dnspython DNS queries Full DNS record dump, zone transfer, DMARC/SPF
esprima JS parsing AST-level endpoint discovery
Pillow Image processing EXIF/GPS extraction
pypdf PDF parsing PDF metadata
fonttools Font parsing name table extraction
ipwhois ASN lookup RDAP-enriched ASN/org info
uvloop Event loop 2-3× throughput on asyncio-heavy runs

Virtual Environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Docker

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY silkfang.py .
ENTRYPOINT ["python", "silkfang.py"]
```

```bash
docker build -t silkfang .
docker run --rm -it silkfang https://target.com -m 200
```

Verifying the Install

```bash
python3 silkfang.py --self-test
# {"ok": true, "findings": 42}
```

If ok: true, you're ready.

---

📖 Usage

Interactive Mode

Run with no target to enter the guided menu:

```bash
python3 silkfang.py
```

You'll see a legal warning, authorization prompt, then a menu:

```
╭──────────────────── SELECT SCAN PROFILE ────────────────────╮
│ [1] OFFENSIVE   //  attack surface · DNS · subdomains · ... │
│ [2] DEFENSIVE   //  headers · TLS · cookies · CORS · ...    │
│ [3] ALL + FULL  //  everything + full-site crawl            │
│ [q] QUIT                                                    │
╰─────────────────────────────────────────────────────────────╯
```

Non-Interactive Mode

Provide a target and it runs straight through:

```bash
python3 silkfang.py https://example.com -y
```

Scan Profiles

Profile Flag What runs
Offensive -m 1 or default --target Attack surface mapping, subdomains, secrets, active probes
Defensive -m 2 Headers, TLS, cookies, CORS, robots.txt, sitemap
All -m 3 Both, plus full-site crawl & pagination discovery

Sample Output

```
15:42:01  CRIT  SECRET                →  AKIAIOSFODNN7EXAMPLE
15:42:01  HIGH  SENSITIVE-200         https://api.target.com/.env  →  len=2048 snip=DB_HOST=...
15:42:02  HIGH  CORS                  https://api.target.com/  →  reflects https://evil.com
15:42:02  HIGH  GRAPHQL               https://api.target.com/graphql  →  introspection enabled
15:42:03  MED   HDR-                  HSTS  →  MISSING
15:42:03  MED   COOKIE                sessionid  →  flags=Secure|HttpOnly|SameSite domain=.target.com path=/ prefix=-
15:42:04  INFO  TECH-ID               https://target.com  →  Next.js
15:42:04  INFO  SUBDOMAIN             api.target.com  →  crt.sh
15:42:05  LOW   COMMENT               https://target.com  →  TODO: remove before prod - admin/key
```

Real-Time Dashboard

While running, SILKFANG updates a live HUD every 2 seconds:

```
RUNNING   https://target.com      pages 47/100  assets 12  find 156  t 34s  r 1.4/s
⏸ backoff api.target.com:120s
```

Interrupt with Ctrl-C at any time — the crawler flushes state and writes the final report.

---

⌨️ Command Line Reference

```
usage: silkfang.py [-h] [-l LIST] [-m MAX_PAGES] [--unlimited] [-w WORKERS]
                   [-r RATE] [-t TIMEOUT] [--passive] [--no-subdomains]
                   [--deep-assets] [--resume] [--reset] [-o OUTPUT] [-y]
                   [--min-delay MIN_DELAY] [--max-delay MAX_DELAY] [--fast]
                   [-fs {rdn,fqdn,dn}] [-cs CRAWL_SCOPE] [-j] [--silent]
                   [-silent] [-q] [-nc] [--sarif] [--baseline BASELINE]
                   [--cookie COOKIE] [--bearer BEARER]
                   [--jwt-wordlist JWT_WORDLIST] [--proxy PROXY]
                   [--self-test] [target]
```

Target Selection

Flag Argument Description
target URL Single target. Auto-prepends https:// if scheme missing.
-l, --list File Newline-separated list of targets.
--self-test — Smoke test against example.com (passive only). Exits 0/1.

Crawl Control

Flag Default Description
-m, --max-pages 100 Hard cap on pages fetched.
--unlimited off Disable page cap. Respect the target.
-w, --workers 10 Concurrent workers.
-r, --rate 0 Max requests/sec per host. 0 = unlimited.
-t, --timeout 15.0 Per-request timeout (seconds).
--passive off No active probes. Only passive recon.
--no-subdomains off Skip subdomain enumeration.
--deep-assets off Download & analyze binary assets (images, PDFs, archives).

Stealth

Flag Default Description
--min-delay 0.5 Min inter-request delay (seconds).
--max-delay 2.5 Max inter-request delay (seconds).
--fast off Disable all delays. Very noisy.

Scope Control

Flag Values Description
-fs, --field-scope rdn / fqdn / dn rdn = registered domain (all subdomains), fqdn = exact host only, dn = domain-name match (host == scope or host.endswith("." + scope)).
-cs, --crawl-scope regex Only crawl URLs matching this regex.

Output

Flag Description
-o, --output Output directory. Default: output/.
-j, --jsonl Emit each finding as a JSON line on stdout.
--silent Suppress all non-JSON output.
-q, --quiet Suppress FETCHED, INFO, TECH-ID, EXTERNAL-DOMAIN, etc.
-nc, --no-color Disable ANSI colors.
--sarif Emit SARIF file alongside text report.
--baseline Path to prior report; only show new findings.

Auth & Proxy

Flag Description
--cookie Raw Cookie: header string (e.g., session=abc123; csrftoken=xyz).
--bearer Bearer token (adds Authorization: Bearer <token>).
--jwt-wordlist Wordlist for HS256 JWT secret brute-force (first 10,000 entries).
--proxy HTTP/SOCKS proxy URL.

Checkpointing

Flag Description
--resume Resume from prior checkpoint.
--reset Clear prior checkpoint before run.

---

🔬 Detection Catalog

SILKFANG has 150+ individual detectors organized into 15 categories.

🔐 Secrets (SEVERITY: critical)

Structured secret patterns scanned in JS, HTML, JSON, and CSS:

Pattern Label Severity
AKIA[0-9A-Z]{16} AWS-KEY critical
ASIA[0-9A-Z]{16} AWS-STS critical
sk_live_* STRIPE-LIVE critical
sk_test_* STRIPE-TEST high
pk_live_* STRIPE-PK medium
AIza[0-9A-Za-z_-]{35} GOOGLE-API high
xox[baprs]-* SLACK-TOKEN critical
ghp_* / gho_* / github_pat_* GITHUB-* critical
glpat-* GITLAB-PAT critical
-----BEGIN * PRIVATE KEY----- PRIVATE-KEY critical
SG.*.* SENDGRID critical
dop_v1_* DIGITALOCEAN critical
LTAI* ALIBABA critical
cloudinary://* CLOUDINARY critical
SK[0-9a-f]{32} TWILIO critical
hf_* HUGGINGFACE critical
sk-ant-* ANTHROPIC critical
sk-* (48 chars) OPENAI critical
[MN]*.*.* DISCORD critical
\d+:[a-zA-Z0-9_-]{35} TELEGRAM critical
sq0*-* SQUARE high
High-entropy base64 HIGH-ENTROPY medium

Entropy threshold: Shannon entropy > 4.2, length 20-200, no scheme prefix, not pure digit/alpha, no whitespace.

🪙 JWT Vulnerabilities

Check Finding Severity
alg: none JWT-VULN critical
jwk header present JWT-VULN critical
Missing exp claim JWT-WEAK medium
Weak HS256 secret (wordlist) WEAK-JWT-SECRET critical

JWT cracking works offline via hmac.compare_digest on candidate secrets — no network round-trip.

🌐 DNS & Subdomains

Detector Output
A / AAAA / NS / MX / TXT / SRV / CAA / DNSKEY DNS-<TYPE>
SPF (v=spf1) EMAIL-AUTH
DMARC (v=DMARC1 @ _dmarc.) EMAIL-AUTH
BIMI (default._bimi.) BIMI
Reverse DNS (PTR) RDNS
ASN (RDAP) ASN, ORG
Zone Transfer (AXFR) DNS-ZONE-TRANSFER ⚠️
CT log mining SUBDOMAIN
CNAME dangling DANGLING-CNAME
Takeover fingerprint SUBDOMAIN-TAKEOVER ⚠️

Takeover providers detected: AWS S3, GitHub Pages, Heroku, Azure, Shopify, Tumblr, Fastly, Ghost, Pantheon, WordPress.com, Surge.sh, Bitbucket, Netlify, Vercel, Read the Docs, Cargo Collective.

🧬 JavaScript Analysis

Detector Description
JS-AST Endpoints found via esprima AST (string literals, template literals)
SOURCEMAP sourceMappingURL= references
WS WebSocket endpoints
FETCH fetch() / axios.*() call sites
DOM-SINK Sink locations (innerHTML, eval, document.write)
DOM-XSS Source→sink flow (naive taint tracking)
POSTMESSAGE-FLAW addEventListener('message') without .origin check
POSTMESSAGE-WILDCARD postMessage(..., '*')
PROTO-POLLUTION __proto__ / constructor.prototype in merge contexts
STORAGE-SENSITIVE localStorage.setItem('token', ...) style patterns
LIB-VERSION jQuery, Bootstrap, React, Vue, Angular, Lodash, Moment, D3

🍪 Cookies & Session

Detector Description
COOKIE Flags audit (Secure, HttpOnly, SameSite, prefixes)
COOKIE-JWT JWT-in-cookie
COOKIE-JSON Base64-decodes to JSON

🛡️ Headers & TLS

18 security headers audited: HSTS, CSP, CSP-RO, XFO, XCTO, Referrer-Policy, Permissions-Policy, Feature-Policy, COOP, COEP, CORP, XSS-Protection, X-Permitted-Cross-Domain-Policies, X-Download-Options, X-DNS-Prefetch-Control, Expect-CT, Clear-Site-Data, Cache-Control.

CSP weaknesses: unsafe-inline, unsafe-eval, wildcard *, report-uri, report-to.

HSTS: max-age < 1 year → HSTS-WEAK; preload / includeSubDomains → info.

TLS: protocol version, cipher suite, issuer, subject, SAN list, expiry.

🕸️ Active Probes (--passive disables)

Probe Severity Method
METHODS info OPTIONS → parse Allow
METHOD-RISK high TRACE/PUT/DELETE/PATCH present
OPEN-REDIRECT high Inject https://evil.example.com into next, url, redirect, return, returnUrl, continue
CORS high ACAO: * or origin reflection
CORS-PREFLIGHT high OPTIONS + Origin: evil.example.com
CACHE-POISONING high Reflect X-Forwarded-Host etc. in cacheable response
CACHE-DECEPTION high /path.css returns non-trivial body
METHOD-OVERRIDE high X-HTTP-Method-Override: PUT changes behavior
FAT-GET high GET-with-body rejected, GET-without accepted
GRAPHQL high Introspection enabled on 5 common endpoints
IDOR-CANDIDATE high Numeric sequence or UUID cluster across query params
SENSITIVE-200 high HTTP 200 on a high-risk path
ROBOTS-DISALLOW info Parsed Disallow: entries
SITEMAP-URL info Parsed <loc> entries

💰 Payments & Cloud

Detector Description
PAYMENTS Stripe PK, PayPal business=, Square, Cloudinary
SECRET STRIPE-SK Live/test secret key (critical)
CLOUD Firebase apiKey + projectId, Supabase
AUTH Auth0, Okta, Cognito, Clerk, Firebase Auth
MAPS Mapbox, Google Maps
REALTIME Pusher, PubNub
SEARCH Algolia app ID
FEATURE-FLAGS LaunchDarkly client-side-id
AB-TESTING Optimizely ID

📊 Analytics & Error Tracking

Detector Description
ANALYTICS GA-UA, GA4, GTM, FB-Pixel, Hotjar, Segment
ERROR-TRACKING Sentry, Rollbar, Datadog RUM, New Relic, Honeybadger
CHAT Intercom, Drift, Crisp, Zendesk

🖼️ Assets & Metadata (--deep-assets)

Asset Type Analyzer Output
Image PIL Dimensions, format, GPS coordinates, Make, Model, Software, DateTime
PDF pypdf + regex fallback Author, Creator, Producer, Title, Subject, Pages
Office zipfile docProps/core.xml → creator, company, manager
Archive zipfile / tarfile File listing (up to 40 entries)
SVG text Embedded <script>, xlink:href refs
Font fontTools Name table entries

📝 Comments & Content

Detector Description
COMMENT HTML comments containing TODO/FIXME/HACK/password/secret/token/admin/auth/bypass/...
DEV-BANNER "lorem ipsum", "coming soon", "staging", "under construction"
INTERNAL-ID data-id, data-user, data-session values
EMAIL Harvested emails (filtered: no image extensions)
PHONE International phone regex
CRYPTO BTC, ETH, XMR addresses
HASH MD5/SHA1/SHA256 hashes
UUID UUID v1-v5

🕵️ WAF & Bot-Challenge Detection

WAF vendors: Cloudflare, Akamai, Incapsula, Sucuri, AWS CloudFront, Fastly, F5 BIG-IP, Barracuda, ModSecurity, Imperva, DDoS-Guard.

Bot challenges: Cloudflare, DataDome, Akamai, PerimeterX, Kasada. Detected on 429/503 responses and triggers per-host exponential backoff.

---

🏗️ Architecture Deep-Dive

SILKFANG is architected as a pipeline of async workers fed by a single queue.

```
┌──────────────┐
│   Target URL │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│   run_probes()   │  ← DNS, TLS, subdomains, path fuzz, GraphQL, CORS...
│   (background)   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐     ┌─────────────────────┐
│   asyncio.Queue  │◄────│   Crawler.enqueue   │
│   (bounded)      │     │  scope check + norm │
└──────┬───────────┘     └─────────────────────┘
       │
       ▼ (N workers)
┌──────────────────┐
│    worker()      │
│  1. throttle     │
│  2. stealth.wait │
│  3. handle()     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   _fetch()       │  ← 3× retry, backoff on 429/503
│   headers built  │
│   UA rotated     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   handle()       │
│  ┌─────────────┐ │
│  │ content-type│ │
│  │ dispatcher  │ │
│  └──────┬──────┘ │
│         │        │
│  ┌──────▼──────┐ │
│  │ HTML parser │ │ → extract_all()
│  │ JS parser   │ │ → mine_js_deep()
│  │ CSS parser  │ │ → parse_css()
│  │ JSON parser │ │ → mine_json_deep()
│  └─────────────┘ │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   LiveStream     │───► Terminal (Rich)  ──► JSONL (file)
│   .emit()        │
└──────────────────┘
```

Key Components

Stealth — Per-host state machine. Tracks backoff, failure count, last request time. Rotates UA from a shuffled pool, cycles Chrome sec-ch-ua headers when UA is Chromium-based, adds Sec-Fetch-* for realism.

Crawler — The orchestrator. Runs N workers against a single asyncio.Queue. enqueue() runs scope checks, binary detection, and populates the queue. handle() is the per-response dispatcher.

LiveStream — Central event emitter. Dedupes (type, key, value) triples, counts severity, and routes to Rich console or JSONL or both.

ClientWrapper — Unified curl_cffi / httpx facade. When curl_cffi is available, uses impersonate="chrome120" for TLS fingerprint realism. Otherwise falls back to httpx.

StateStore — Append-only JSONL checkpoint file. Written every 30s and on Ctrl-C. Loaded with --resume.

extract_all() — The HTML extractor. Parses with lxml (fallback html.parser), handles <base> resolution, <noscript>, data-* attributes, srcset, meta refresh, JSON-LD, microdata, comments, style attributes, and every known link-bearing tag.

mine_js_deep() — The JS analyzer. Uses esprima AST when available, else regex fallback. Also runs secret scanning, JWT audit, DOM-sink analysis, proto-pollution, storage-write, and fetch-call detection.

Why Async?

A typical crawl visits 100-500 pages, each with 20-100 assets. A synchronous scanner doing 5 req/s takes 5-20 minutes. SILKFANG with 10 workers and rate-limited stealth does the same in 2-4 minutes without tripping WAFs (the rate limiting is applied per-host, not globally).

Why curl_cffi?

Modern WAFs (Cloudflare Bot Management, Akamai, PerimeterX) fingerprint TLS handshakes via JA3/JA4. Python's ssl module produces a very different TLS fingerprint from Chrome — trivially blocked. curl_cffi uses actual curl+boringssl with matching cipher suites and extensions, mimicking Chrome's JA3.

Fallback: If curl_cffi is missing, SILKFANG uses httpx — works but is more likely to trigger bot challenges.

---

📊 Output Formats

Standard Report (.txt)

Tab-separated: TYPE\tKEY\tVALUE

```
SECRET	https://cdn.target.com/app.js	AKIAIOSFODNN7EXAMPLE
CORS	https://api.target.com/	reflects https://evil.com
SENSITIVE-200	https://target.com/.env	len=2048 snip=DB_HOST=...
GRAPHQL	https://api.target.com/graphql	introspection enabled
```

Files written to output/:

File Contents
{fqdn}-{mode}.txt All findings, deduped
{fqdn}-visited.txt URLs fetched
{fqdn}-all-urls.txt All URLs discovered
{fqdn}-assets.txt Binary assets discovered
{fqdn}-params.txt Query param names harvested
{fqdn}-{mode}.sarif SARIF (with --sarif)

JSON-Lines (--jsonl)

Each finding is one JSON object:

```json
{
  "type": "SECRET",
  "url": "https://cdn.target.com/app.js",
  "value": "AKIAIOSFODNN7EXAMPLE",
  "target": "https://target.com",
  "severity": "critical",
  "ts": "2024-01-15T15:42:01"
}
```

Pipe-friendly:

```bash
python3 silkfang.py https://target.com --jsonl -q --silent \
  | jq 'select(.severity=="critical") | .value'
```

SARIF (--sarif)

GitHub Code Scanning compatible. Upload via:

```yaml
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: output/target.com-all.sarif
```

Baseline Diffing (--baseline)

Run periodically against the same target and diff findings:

```bash
python3 silkfang.py https://target.com --baseline output/target.com-all.txt
# + 3 new findings since baseline
# + SECRET  https://cdn.target.com/new.js  AKIA...
# + CORS    https://api.target.com/        wildcard ACAO
# + GRAPHQL https://api.target.com/graphql introspection enabled
```

---

🧪 Advanced Workflows

Workflow 1 — Daily Attack-Surface Delta

```bash
#!/bin/bash
# /etc/cron.daily/silkfang-delta
set -euo pipefail
TARGET="${1:-https://example.com}"
PREV="output/$(echo "$TARGET" | sed 's|https\?://||;s|/|_|g')-all.txt"

python3 silkfang.py "$TARGET" -m 2000 --fast -y \
  --baseline "$PREV" 2>&1 | mail -s "SILKFANG delta: $TARGET" soc@example.com
```

Workflow 2 — Authenticated SPA Crawl

```bash
python3 silkfang.py https://app.target.com -m 1000 \
  --cookie "$(cat .cookie)" \
  --bearer "$(cat .token)" \
  --crawl-scope '/app|/api|/dashboard' \
  --jwt-wordlist /usr/share/wordlists/jwt-secrets.txt
```

Workflow 3 — Bug Bounty Program (Respectful)

```bash
python3 silkfang.py https://bugbounty.target.com \
  -m 500 \
  --min-delay 1.5 --max-delay 4.0 \
  --cookie "$BB_COOKIE" \
  -fs rdn -cs '^https://bugbounty\.target\.com' \
  --sarif --baseline baseline.txt
```

Note the slow rate (--min-delay 1.5) — responsible scanning.

Workflow 4 — Passive-Only Fingerprinting

For hostile CDNs or strict WAFs:

```bash
python3 silkfang.py https://target.com \
  -m 20 --passive \
  --no-subdomains \
  --quiet
```

Only fetches the target page and follows same-origin links.

Workflow 5 — SIEM / Splunk Ingestion

```bash
python3 silkfang.py https://target.com --jsonl -q --silent \
  | tee -a /var/log/silkfang.jsonl
```

Then in Splunk:

```
index=security sourcetype=silkfang severity="critical"
| stats count by type, url
```

Workflow 6 — CI/CD Secret Gate

```yaml
# .github/workflows/secret-gate.yml
name: Secret Gate
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r silkfang/requirements.txt
      - run: |
          python3 silkfang/silkfang.py "https://${{ secrets.PREVIEW_HOST }}" \
            -m 50 --passive --jsonl --silent -q \
            > findings.jsonl || true
          if jq -e 'select(.type=="SECRET" and .severity=="critical")' \
               findings.jsonl > /dev/null; then
            echo "::error::Critical secret found in preview deployment"
            exit 1
          fi
```

---

🥷 Anti-Detection & Stealth

SILKFANG takes evasion seriously.

UA Rotation

25+ real-world user agents, shuffled at start and every full cycle:

· Chrome 120-122 (Windows, macOS, Linux, Android, iOS)
· Firefox 122-123
· Safari 17.2-17.3
· Edge 122, Opera 107, Brave 122
· Samsung Browser 23
· Googlebot, Bingbot, Facebook, Twitter
· curl/8.5.0, python-httpx/0.27.0, Wget/1.21.4

Header Fidelity

When UA is Chromium-family, SILKFANG generates consistent:

· sec-ch-ua (3 variants, matched to major version)
· sec-ch-ua-mobile, sec-ch-ua-platform (parsed from UA)
· sec-fetch-dest, sec-fetch-mode, sec-fetch-site
· Accept-Language (5 real-world locale variants)
· DNT on Firefox
· Upgrade-Insecure-Requests
· Contextual Referer (same origin root)

TLS fingerprinting: via curl_cffi impersonate="chrome120".

Rate Limiting

Two layers:

1. Per-host spacing — minimum 0.2 + rand(0.05, 0.35) between requests to the same host
2. Global jitter — rand(min_delay, max_delay) after each request, configurable via CLI

Exponential Backoff

On 429, 503, or fetch error:

```
backoff(n) = min(300s, base × 2^(failures - 1))
```

base defaults to 5s. After 6 failures, the host is paused for the full 300s. Successful requests reset the counter. The HUD shows active backoffs in red.

Bot-Challenge Detection

SILKFANG recognizes challenge pages from Cloudflare, DataDome, Akamai, PerimeterX, and Kasada, both via headers and body content. When detected, it emits BOT-CHALLENGE and backs off harder.

What You Cannot Evade

SILKFANG will not bypass:

· Hard authentication (you must supply --cookie/--bearer)
· CAPTCHAs (not solved)
· JS-rendered SPAs (no headless browser; see Limitations)
· mTLS (no client cert injection)
· Cloudflare Turnstile / hCaptcha / reCAPTCHA v3 challenges

It will handle:

· Soft UA blocks (via rotation)
· Header-based bot scoring (via header fidelity)
· TLS/JA3 blocks (via curl_cffi)
· Simple rate limits (via backoff)
· Basic WAF rules (path fuzz is gentle and rate-limited)

---

🎯 Scope Control

The most important feature for responsible scanning. Two independent controls:

--field-scope

Controls which hosts are fetched.

Value Match rule Example
rdn (default) Same registered domain a.target.com ✅ evil.com ❌
fqdn Exact hostname only a.target.com ✅ b.target.com ❌
dn Dot-boundary suffix a.target.com ✅ target.com ✅ nottarget.com ❌

⚠️ rdn uses tldextract — a.target.co.uk and b.target.co.uk are the same registered domain, but a.target.co.uk and a.other.co.uk are not.

--crawl-scope

Regex matched against the full URL. Only matches are crawled.

```bash
# Only crawl the /app and /api subtrees
--crawl-scope '^https://app\.target\.com/(app|api)/'

# Exclude logged-out paths
--crawl-scope '^https://target\.com/(?!logout|signout)'
```

Both must pass. This means you can safely run against https://bugbounty.target.com while allowing the crawler to follow CDN links to cdn.target.com only if -fs rdn is set (default), and block the payment processor stripe.target.com with -cs.

--passive

The nuclear option. Disables:

· DNS zone transfer
· Path brute-force
· HTTP method probe
· Open-redirect injection
· CORS preflight
· Cache poisoning/deception
· Method override
· Fat GET
· GraphQL introspection
· Subdomain takeover checks

Leaves only passive fetches and DNS queries. Perfect for pre-engagement recon where you need to see the target without touching it.

---

💾 Checkpointing & Resume

Long scans get interrupted. SILKFANG's checkpoint system is crash-safe and append-only.

How It Works

Every 30s (and on SIGINT/SIGTERM):

1. Serialize current state to .silkfang-state-{fqdn}.jsonl.tmp
2. os.replace() to .silkfang-state-{fqdn}.jsonl

os.replace is atomic on POSIX. A crash mid-write leaves the old file intact — no corruption.

The state file records:

· meta — target, mode, timestamp
· visited — every URL fetched
· assets — every binary asset discovered
· all_urls — every URL discovered
· result — every finding (type, key, value)

Resume Workflow

```bash
# Run #1 (interrupt with Ctrl-C)
$ python3 silkfang.py https://target.com -m 5000
^C
⏸ Interrupt — flushing results...
[results saved]

# Run #2 — continues from where Run #1 stopped
$ python3 silkfang.py https://target.com -m 5000 --resume
INFO  https://target.com  resume visited=1432 findings=87
```

Clean Slate

```bash
$ python3 silkfang.py https://target.com --reset
```

Deletes the checkpoint and starts fresh. Useful when you've changed -fs or --crawl-scope and don't want stale URLs.

Where the State Lives

output/.silkfang-state-{fqdn}.jsonl. It's not a .txt report — it's internal machinery. Deleting it is always safe.

---

🔄 CI/CD Integration

GitHub Actions (full example)

```yaml
name: SILKFANG Nightly Recon
on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  recon:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    permissions:
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install
        run: pip install beautifulsoup4 lxml tldextract rich \
                           curl_cffi dnspython esprima \
                           Pillow pypdf fonttools ipwhois

      - name: Download prior baseline
        run: |
          curl -fsSL -o baseline.txt \
            "https://artifacts.example.com/silkfang/${{ secrets.TARGET_SLUG }}-latest.txt" \
            || echo "" > baseline.txt

      - name: Scan
        env:
          TARGET: ${{ secrets.TARGET_URL }}
          COOKIE: ${{ secrets.SESSION_COOKIE }}
        run: |
          python3 silkfang.py "$TARGET" \
            -m 2000 -y \
            --cookie "$COOKIE" \
            --min-delay 1.0 --max-delay 3.0 \
            --baseline baseline.txt \
            --sarif \
            -o output

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: output/*.sarif

      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: silkfang-output
          path: output/
          retention-days: 30
```

GitLab CI

```yaml
silkfang:
  image: python:3.11-slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
  before_script:
    - apt-get update && apt-get install -y build-essential libssl-dev libffi-dev
    - pip install beautifulsoup4 lxml tldextract rich curl_cffi dnspython esprima
  script:
    - python3 silkfang.py "$TARGET_URL" -m 1000 -y --jsonl -q --silent -o output
  artifacts:
    when: always
    paths: [output/]
    expire_in: 1 month
  timeout: 1h
```

Jenkins (Declarative Pipeline)

```groovy
pipeline {
  agent any
  triggers { cron('H 2 * * *') }
  options { timeout(time: 60, unit: 'MINUTES') }
  stages {
    stage('Recon') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
          python3 silkfang.py "$TARGET" -m 2000 -y \
            --cookie "$COOKIE" \
            --sarif -o output
        '''
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'output/**', allowEmptyArchive: true
    }
  }
}
```

---

📚 Real-World Case Studies

Case Study 1 — The Forgotten .env

Target: Fintech SaaS, ~3M MAU
Profile: Offensive, -m 500
Duration: 4 minutes

SILKFANG's SENSITIVE_PATHS list included /.env. On a legacy marketing subdomain (legacy.target.com), an HTTP 200 response was returned for /.env. Contents:

```
DB_HOST=prod-db.target.internal
DB_PASSWORD=...
STRIPE_SECRET_KEY=sk_live_...
AWS_ACCESS_KEY_ID=AKIA...
```

SENSITIVE-200 emitted with a length of 4127 and a snippet. The full report was in output/legacy.target.com-offensive.txt within 30 seconds of the scan starting — before the main target's pages were even fully crawled.

Fix: Instant rotation of all exposed credentials, DNS removal of the legacy subdomain. The client was notified within 5 minutes of scan start.

Case Study 2 — GraphQL Introspection in Production

Target: E-commerce platform
Profile: Offensive, --fast -m 200
Duration: 90 seconds

/api/graphql responded to {__schema{types{name}}} with full type definitions — 340 types, including:

· AdminUser, AdminOrder, InternalTicket
· Mutation.updatePrice, Mutation.refundOrder
· CredentialRotationInput

GRAPHQL at severity high. This wasn't a bug in itself, but it was the entry point to a P1 privilege-escalation report.

Case Study 3 — Subdomain Takeover at Scale

Target: Media conglomerate with 1,200 subdomains
Profile: Offensive, --fast
Duration: 18 minutes (mostly waiting on crt.sh rate limits)

crt.sh mined 1,247 subdomains. Of those, 312 had CNAMEs pointing at *.herokuapp.com. 41 of those CNAMEs resolved to No such app — classic Heroku dangling CNAME.

SUBDOMAIN-TAKEOVER × 41. The client was notified to claim the CNAMEs within 24 hours. All 41 were claimed by the client without incident.

Case Study 4 — The Leaky PDF

Target: Legal firm
Profile: --deep-assets enabled
Duration: 12 minutes

A downloaded /downloads/annual-report.pdf had an Author field of j.smith@legalfirm.com and a Producer field of Microsoft® Word 2019. Not a vulnerability. But a downloaded /downloads/strategy-2024.pdf had Author: CEO_NAME, Keywords: confidential, M&A, acquisition target: AcmeCorp.

PDF-META × N. The client had no idea that internal strategy documents were being published with metadata intact.

Case Study 5 — IDOR by Clustering

Target: Booking platform
Profile: All, -m 3000
Duration: 40 minutes

Across 3,000 crawled URLs, SILKFANG extracted booking_id=10000 through booking_id=10047 from pagination and search results. IDOR-CANDIDATE on /api/bookings?booking_id= with numeric seq 10000..10047 (48 samples).

Manual testing (with permission) showed booking_id=10001 returned a stranger's booking. The client had rate-limited but not access-controlled this endpoint.

Case Study 6 — The CSP Bypass Heuristic

Target: Healthcare portal
Profile: Defensive
Duration: 3 minutes

CSP header included unsafe-inline and unsafe-eval and script-src *. CSP-WEAK × 3, severity medium. But combined with a reflected XSS observed on /search?q=, this CSP was effectively no protection at all.

The client had added the CSP to "pass the security audit" — it was documented as a compensating control. It wasn't.

---

🔧 Troubleshooting

"FATAL: beautifulsoup4 is required"

```bash
pip install beautifulsoup4 lxml tldextract rich
```

"FATAL: tldextract is required"

```bash
pip install tldextract
```

On first run, tldextract downloads the public suffix list from publicsuffix.org. On airgapped systems:

```bash
python3 -m tldextract --update
# or pre-download the cache and pass TLDEXTRACT_CACHE env var
```

Cloudflare turnstile loop / constant 503s

SILKFANG will detect and back off — but you'll get almost no results. Options:

1. Ensure curl_cffi is installed (pip install curl_cffi)
2. Slow down: --min-delay 3 --max-delay 8
3. Use a residential proxy: --proxy http://user:pass@host:port
4. Use --passive — Cloudflare rarely challenges passive reads
5. Accept that you need a real browser

uvloop.install() fails on Windows

Expected. uvloop isn't available on Windows. The try/except handles it — you'll just run slower.

"Address already in use" on repeated runs

Rare port leak from socket.getaddrinfo. Kill lingering Python processes:

```bash
pkill -f silkfang.py
```

UTF-8 / encoding errors from bodies

Add PYTHONIOENCODING=utf-8:

```bash
PYTHONIOENCODING=utf-8 python3 silkfang.py https://target.com
```

findings=0 on a live site

Likely causes:

1. Wrong scope — -fs rdn may match nothing if the target uses an unusual TLD. Try -fs dn.
2. Blocked — you're being silently rate-limited. Try --min-delay 3.
3. Cookies expired — refresh --cookie.
4. Real site has nothing to find — rare, but possible.

Debug with --jsonl --silent -q and inspect raw events.

SENSITIVE-200 for a soft-404

Some servers return 200 for every path (SPA catch-all). SILKFANG doesn't auto-detect this. If you see 30+ SENSITIVE-200 findings with len=<same>, the site is a soft-404. Ignore.

SENSITIVE-200 for a real page

Conversely, /admin returning 200 is normal. SENSITIVE-200 is only notable for paths in the HIGH_RISK_SENSITIVE set — .env, .git/config, backup.sql, phpinfo.php, etc.

"BOT-CHALLENGE" spam

Your requests are being challenged. This is information. It tells you the site has bot management. For results, you need a proxy or a slow rate.

GraphQL "introspection enabled" but body is empty

Some GraphQL servers return 200 with a JSON body of {"errors":[...]} when introspection is disabled. SILKFANG only reports GRAPHQL if the body contains __schema. If you get a false positive, let us know.

High CPU on large crawls

The bottleneck is BeautifulSoup + lxml parsing. Options:

1. Increase workers (-w 20)
2. Reduce page cap (-m 500)
3. Use --fast (removes await asyncio.sleep overhead)

--resume doesn't resume

Check output/.silkfang-state-{fqdn}.jsonl exists. The {fqdn} is computed via tldextract — verify it matches your target:

```bash
ls -la output/.silkfang-state-*
```

---

⚡ Performance Tuning

Concurrency

-w CPU Memory Network Use case
3 low low very gentle Prod-touching, polite
10 (default) medium medium polite General use
25 high high aggressive Own infra, fast result
50+ very high very high hostile Never — you'll be blocked

Rate Limiting

--rate Behavior
0 (default) Unlimited, but Stealth still spaces per-host
5 5 req/s per host
20 20 req/s per host
--fast All delays off, --rate 0

Recommended Profiles

Polite (prod):

```bash
-w 5 -r 3 --min-delay 2 --max-delay 5 -m 500
```

Balanced (default):

```bash
-w 10 -m 2000
```

Aggressive (own infra):

```bash
-w 25 --fast -m 50000
```

Passive (hostile target):

```bash
-w 3 -r 1 --passive --min-delay 5 --max-delay 10 -m 50
```

Where the Time Goes

On a 1,000-page crawl with 10 workers:

Phase % of wall time
Fetching HTML ~40%
HTML parsing + extraction ~25%
JS analysis ~15%
Probes (DNS, TLS, subdomains) ~10% (parallel)
Secret scanning ~10%

Memory

Roughly ~80MB per 1,000 pages, ~1KB per finding, ~100 bytes per URL. A 10,000-page crawl peaks at ~500MB.

--deep-assets Cost

--deep-assets downloads every binary asset. On media-heavy sites, this can be 10-100× slower and consume significant disk/network. Use with -m 100 and -w 3.

---

⚖️ Legal & Ethics

TL;DR

Only scan targets you own or have written permission to test.

What SILKFANG Does That Requires Authorization

· HTTP fetches (even to / — unauth'd GET is a computer access)
· DNS lookups (generally fine, but aggregates look like recon)
· Active probes — method fuzz, CORS preflight, GraphQL introspection, path brute-force, cache poisoning probes, open-redirect injection, DNS zone transfer attempts
· Subdomain takeover checks — sends requests to third-party providers

What SILKFANG Does That Does NOT Require Authorization

· Reading its own source code
· Scanning localhost, 127.0.0.1, or your own lab VMs
· Reading public data offline
· --self-test against example.com (passive only, well-known safe target)

Applicable Laws

Jurisdiction Statute Notes
🇺🇸 USA CFAA (18 U.S.C. § 1030) "Exceeds authorized access" — read Van Buren v. United States (2021)
🇺🇸 USA DMCA § 1201 Circumvention — mostly irrelevant here but active probes may touch it
🇬🇧 UK Computer Misuse Act 1990 § 1 Unauthorized access
🇪🇺 EU Directive 2013/40/EU Attacks against information systems
🇩🇪 Germany StGB § 202a-c Data espionage, interception
🇦🇺 Australia Criminal Code Act 1995, Part 10.7 Unauthorized access
🇮🇳 India IT Act 2000, § 66 Unauthorized access

Safe Harbor

If you're a security researcher, get written authorization in advance. A typical scope-of-work document includes:

1. Named targets (FQDNs, IP ranges)
2. Explicit exclusion list (e.g., production billing)
3. Time window
4. Rate limits
5. Test account credentials
6. Emergency contact for P1 findings

SILKFANG's --cookie, --bearer, -fs, and -cs flags exist precisely so you can stay inside the scope-of-work.

Bug Bounty Programs

Most programs allow scanning but forbid:

· DoS / heavy fuzzing
· Data exfiltration
· Lateral movement
· Automated exploitation
· Submitting findings on other programs' targets (e.g., their CDN provider)

SILKFANG respects these by default with per-host backoff. Still, always read the program rules.

Responsible Disclosure

If you find something:

1. Don't exploit further than proving the finding.
2. Document minimally — enough to reproduce, no PII.
3. Report privately — email or program portal.
4. Give reasonable time — 90 days is industry standard.
5. Don't publicize until fixed or agreed.

Ethical Use

SILKFANG is a tool. Its ethics are the operator's. Every feature exists because the defensive world needs to know how to see itself. Every active probe exists because passive scanning alone leaves blind spots.

Use it defensively. Use it with permission. Use it to make systems safer, not to cause harm.

---

🛠️ Contributing

SILKFANG is a single-file tool by design. Contributions should preserve that.

Adding a Detector

1. Pick a category (SECRET, CORS, DNS, etc.).
2. Add the regex or logic inside the relevant parser (extract_all, mine_js_deep, defensive_pass, analyze_postmessage, etc.).
3. Emit with a new TYPE if needed (add to SEVERITY dict).
4. Add a line to the Detection Catalog in this README.
5. Test against --self-test and a real target you control.

Example: adding a detector for AWS Secret Access Key (not just key ID):

```python
# In SECRET_PATTERNS
(r'\b[A-Za-z0-9/+=]{40}\b', "AWS-SECRET-CANDIDATE"),

# In mine_js_deep, after finding AWS-KEY, correlate:
for m in re.finditer(r'AKIA[0-9A-Z]{16}', text):
    # look for 40-char base64 nearby
    ...
```

Adding a Path

Add to SENSITIVE_PATHS. If it's a high-risk path (would-be critical if reachable), also add to HIGH_RISK_SENSITIVE.

Adding a Subdomain Takeover Provider

1. Add fingerprint to TAKEOVER_FINGERPRINTS[<provider>].
2. Add CNAME hints to TAKEOVER_CNAME_HINTS[<provider>].

Style Guidelines

· Async — any network I/O must be await
· No blocking in the loop — use asyncio.to_thread for sync libs (PIL, pypdf)
· Emit early, emit often — stream findings, don't batch
· One .py file — no modules, no packages
· All deps optional — every import must be guarded by try/except ImportError
· Preserve backwards compat — don't rename existing TYPE strings

Testing Checklist

☐ python3 silkfang.py --self-test returns {"ok": true, ...}
☐ Runs on a target you own in all 3 modes
☐ --passive skips active probes (verify with tcpdump)
☐ --resume after Ctrl-C continues correctly
☐ --jsonl --silent -q produces valid JSON-lines
☐ --sarif produces valid SARIF (validate via cat output/*.sarif | jq .version)
☐ No new required dependencies

Reporting Bugs

Include:

1. OS + Python version
2. pip freeze for the relevant packages
3. The exact command
4. The first 20 lines of output
5. (redacted) output/<target>-<mode>.txt if possible

Reporting Security Issues in SILKFANG Itself

Email security@<author domain> with subject SILKFANG: <one-line summary>. PGP key on request.

---

🙏 Credits

Author

SYLHETYHACKVENGER — THE-ERROR808
· GitHub: @sylhetyhackvenger

Built With

· Beautiful Soup — HTML parsing
· lxml — fast parser backend
· tldextract — public suffix list
· Rich — terminal rendering
· curl_cffi — TLS impersonation
· httpx — HTTP client fallback
· dnspython — DNS queries
· esprima — JS AST
· Pillow — image processing
· pypdf — PDF parsing
· fontTools — font parsing
· ipwhois — RDAP lookups
· uvloop — fast event loop

Inspired By

· ProjectDiscovery — subfinder, httpx, nuclei, katana
· TomNomNom — waybackurls, gau, assetfinder
· trufflesecurity — trufflehog
· The Bug Bounty Community — every person who shared a technique

Attribution

Algorithms and detection ideas are drawn from public research and CTF write-ups. Where a specific technique has a clear originator, it should be cited in the commit message.

---

<div align="center">

📜 License

This tool is provided for educational and authorized security testing purposes only.

Usage constitutes acceptance of the full disclaimer at the top of this README. The author is not responsible for misuse. This is not a product — it is a security research tool released to the community in the spirit of the hacker ethic.

---

⬆ Back to Top

Built with paranoia. Deployed with permission. Reported responsibly.

```
  ███████╗██╗██╗     ██╗  ██╗███████╗ █████╗ ███╗   ██╗ ██████╗
  ██╔════╝██║██║     ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝
  ███████╗██║██║     █████╔╝ █████╗  ███████║██╔██╗ ██║██║  ███╗
  ╚════██║██║██║     ██╔═██╗ ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║
  ███████║██║███████╗██║  ██╗██║     ██║  ██║██║ ╚████║╚██████╔╝
  ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝
```

SILKFANG · SYLHETYHACKVENGER (THE-ERROR808) · Live Streaming Recon Engine

</div>

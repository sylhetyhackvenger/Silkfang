
<div align="center">
  
# Website Recon Engine & A Powerful Crawler
attack-surface intelligence for gray-hat operators

https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/License-MIT-green?style=for-the-badge
https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge
https://img.shields.io/badge/Author-SYLHETYHACKVENGER-red?style=for-the-badge

</div>

---

⚠️ LEGAL WARNING — READ BEFORE YOU TOUCH ANYTHING

SILKFANG performs BOTH passive reconnaissance AND ACTIVE offensive probes.

Active probes include: HTTP method fuzzing, open-redirect injection, GraphQL introspection,
path brute-forcing, cache-poisoning attempts, subdomain-takeover validation, and DNS zone-transfer attempts.

Only run this tool against systems you own, or systems for which you carry explicit written authorization from the asset owner.

Unauthorized use may violate the Computer Fraud and Abuse Act (CFAA), the UK Computer Misuse Act, the EU NIS2 directive, GDPR Article 32, or any comparable local statute. The author (SYLHETYHACKVENGER / THE-ERROR808) assumes no liability for how this software is used.

If you cannot produce a signed scope-of-work, do not run this tool.

---

Table of Contents

1. What SILKFANG Is
2. The Philosophy
3. Feature Matrix — The Complete Breakdown
4. Architecture Diagram
5. Quick Start
6. Installation
7. The Three Scan Profiles
8. Command-Line Reference
9. Live Streaming Output Engine
10. Offensive Capabilities
11. Defensive Audit Capabilities
12. Technology Fingerprinting
13. JavaScript Deep Mining
14. Secret Detection Engine
15. Asset Intelligence — The Deep Analyzer
16. Subdomain Intelligence & Takeover Hunting
17. DNS Deep Dive
18. TLS Fingerprinting
19. WAF & Bot-Challenge Detection
20. Anti-Detection & Stealth Layer
21. Resume & Checkpoint System
22. Output Formats
23. SARIF Integration for CI/CD
24. Baseline Diffing
25. Scope Control
26. Operational Playbooks
27. Signature Library Reference
28. Sensitive Path Dictionary
29. Developer Reference
30. Performance & Tuning
31. Troubleshooting
32. FAQ
33. Roadmap
34. Credits & Contact
35. Final Word

---

What SILKFANG Is

SILKFANG is an asynchronous, live-streaming website reconnaissance engine written in Python. It is not a scanner in the traditional sense — it does not "find vulnerabilities" via a static rulebook. Instead, it behaves like a patient, methodical operator:

· It crawls a target and every asset it can reach.
· It mines JavaScript, JSON, CSS, HTML comments, JSON-LD blobs, meta tags, and inline scripts for secrets, endpoints, and structural clues.
· It fingerprints the entire technology stack — WAF, CDN, framework, language, server, auth provider, analytics, payment provider, cloud bucket, and more.
· It audits the security posture — headers, TLS, cookies, CORS, CSP, HSTS, robots, sitemap, security.txt.
· It probes for classes of bugs that are commonly missed by static checkers — open redirects, GraphQL introspection, cache poisoning, HTTP method overrides, subdomain takeovers.
· It streams every finding to your terminal the instant it is discovered.

The design goal is operator empathy: give a human researcher a fast, honest, uncluttered view of a target's attack surface, without drowning them in false positives or fabricated CVEs.

---

The Philosophy

Traditional vulnerability scanners are loud, slow, and frequently wrong. They fire every payload in the book and hope the target complains in a way that matches a regex. SILKFANG takes the opposite approach.

1. Evidence over inference.
If SILKFANG emits WEAK-JWT-SECRET, it means a wordlist candidate literally produced a valid HMAC signature. If it emits SUBDOMAIN-TAKEOVER, a CNAME literally resolves to a known provider and the HTTP body literally contains that provider's "not found" fingerprint. No speculation.

2. Context is everything.
A CREDIT-CARD hit is only emitted after a Luhn check. An INTERNAL-IP is only reported for private ranges. OPEN-S3, OPEN-AZURE, and OPEN-GCS findings include the concrete bucket name and a GET response. Nothing is reported "because a regex matched a comment."

3. Speed with manners.
Every request goes through a per-host scheduler that enforces jittered spacing, exponential backoff on failure, and hard caps on total pages. SILKFANG will never hammer a target into a 503.

4. Findings are streams, not files.
Every emit is timestamped, deduplicated, and severity-coloured. You watch the attack surface unfold in real time, not after the tool has already scrolled off-screen.

5. Everything is resumable.
If you Ctrl-C, a checkpoint is saved. --resume continues from exactly where you stopped — visited URLs, discovered assets, and prior findings all restored.

---

Feature Matrix — The Complete Breakdown

Domain Capability Category
HTTP Full crawl with custom User-Agent rotation Core
HTTP Per-host jittered rate limiting + exponential backoff Core
HTTP Redirect chain capture and analysis Core
HTTP Retry with staggered delay on 429/503 Core
HTTP Bot challenge detection (Cloudflare, DataDome, Akamai, Kasada, PerimeterX) Active
HTML Full link extraction from <a>, <form>, <link>, <script>, <iframe>, <img>, <video>, <audio>, <source>, <track>, <embed>, <object>, <use>, <image>, <base> Core
HTML data-* attribute mining (data-href, data-url, data-endpoint, …) Core
HTML JSON-LD schema.org extraction Core
HTML Microdata (itemprop) extraction Core
HTML OpenGraph and Twitter card extraction Core
HTML Generator meta, viewport, canonical, hreflang, pagination rels Core
HTML Meta refresh target discovery Core
HTML HTML comment mining for TODO, FIXME, password, secret, admin, api_key, xss, sqli, bypass, auth, credential, aws, gcp, azure, salt, hash, jwt, oauth, pem, keystore, htpasswd, shadow, sudo, root Passive
HTML Inline <script> and <style> harvesting Core
HTML Deep-link protocol extraction (whatsapp://, intent://, tg://, viber://, …) Passive
HTML Form method/action/enctype/CSRF audit Defensive
HTML Hidden input extraction Passive
HTML SVG embedded-script detection Passive
HTML <noscript> fallback extraction Core
CSS url() and @import extraction Core
CSS Font-file discovery Core
CSS CSS source-map detection Active
JS Full ESprima AST parse (falls back to regex on parse failure) Active
JS Template literal endpoint extraction Active
JS Dynamic import / require resolution Active
JS Source map discovery + fetch hint Active
JS WebSocket URL extraction Active
JS postMessage origin-check audit Active
JS Wildcard postMessage target audit Active
JS DOM-XSS source/sink correlation Active
JS Prototype-pollution detection in __proto__-merge patterns Active
JS Sensitive localStorage/sessionStorage key detection Active
JS fetch/axios endpoint extraction Active
JS JWT audit (alg=none, jku, jwk, kid injection, missing exp) Active
JS HS256 JWT offline cracking against wordlist Active
JSON Recursive key mining for token, api_key, secret, password, private_key, aws_access_key_id, client_secret, … Active
JSON Nested endpoint URL extraction Active
Secrets 40+ signature classes (AWS, GCP, Stripe, Slack, GitHub, GitLab, Twilio, SendGrid, Mailgun, HuggingFace, OpenAI, Anthropic, Cohere, Groq, Perplexity, Replicate, Cloudinary, DigitalOcean, Alibaba, Discord, Telegram, Clerk, Supabase, Vercel, Netlify, Fly, Railway, Render, Datadog, PagerDuty, Opsgenie, Linear, Notion, Airtable, Figma, Shopify, AssemblyAI, ElevenLabs, Deepgram, Mistral, XAI, OpenRouter, …) Active
Secrets Shannon-entropy high-entropy-string detection Active
Secrets Luhn-validated credit card detection Active
Secrets IBAN detection with length validation Active
Secrets SSN detection Active
Secrets Private key / certificate PEM detection Active
Cloud S3 bucket URL discovery Passive
Cloud Azure Blob URL discovery Passive
Cloud Google Cloud Storage bucket discovery Passive
Cloud Firebase Storage / Realtime-DB discovery Passive
Cloud Firebase apiKey+projectId correlation Passive
Cloud Supabase instance + key detection Passive
Cloud Cloudinary URL credential extraction Passive
Auth Auth0 tenant + client_id correlation Passive
Auth Okta tenant detection Passive
Auth AWS Cognito pool detection Passive
Auth Clerk instance detection Passive
Auth OAuth client_id extraction Passive
Auth Password reset token extraction Passive
Auth CSRF token field detection Passive
Payments Stripe publishable key extraction Passive
Payments Stripe secret key detection Active
Payments PayPal business email Passive
Payments Square application ID Passive
Payments Braintree tokenization key Passive
Payments Adyen client key Passive
Analytics GA-UA, GA4, GTM, FB Pixel, Hotjar, Segment, Amplitude, Mixpanel, PostHog, Plausible, Matomo, Umami, Clarity, Heap, RudderStack, mParticle, Tealium Passive
Analytics Segment write key detection Active
Error Tracking Sentry, Datadog RUM, New Relic, Rollbar, Honeybadger, Bugsnag, Raygun, LogRocket, FullStory Passive
Chat Intercom, Drift, Crisp, Zendesk Passive
Maps Mapbox (pk/sk), Google Maps, Here Passive
Realtime Pusher, PubNub, Ably Passive
Search Algolia appId+apiKey, Typesense, MeiliSearch Passive
Feature Flags LaunchDarkly client-side ID, Optimizely project ID Passive
Consent OneTrust, Cookiebot Passive
CAPTCHA reCAPTCHA, hCaptcha, Cloudflare Turnstile site keys Passive
Crypto BTC, ETH, XMR, LTC, DOGE, SOL address extraction Passive
Hashes MD5, SHA1, SHA256, UUID, JWT discovery Passive
Base64 Recursive base64 payload unwrapping Passive
Contact Email, phone, mailto:, tel:, sms: extraction Passive
Library 35+ JS library version extraction (jQuery, Bootstrap, React, Vue, Angular, Svelte, D3, Chart.js, GSAP, Lodash, Moment, Day.js, Three.js, Alpine, HTMX, Axios, Socket.io, Handlebars, Mustache, RequireJS, Modernizr, Popper, Ember, Backbone, Knockout, Underscore, Foundation, Bulma, Tailwind, jQuery-UI, jQuery-Mobile, Vuex, React-DOM, Redux) Passive
SRI Missing integrity= on external scripts/styles Passive
Headers 30+ security header audit (HSTS, CSP, XFO, XCTO, Referrer, Permissions-Policy, COOP, COEP, CORP, X-XSS, …) Defensive
Headers HSTS max-age weakness, preload, includeSubDomains Defensive
Headers CSP unsafe-inline, unsafe-eval, wildcard, report-uri extraction Defensive
Headers Server version leakage (Server, X-Powered-By, X-AspNet-Version, X-Generator, X-Git-Commit, X-Env, X-Pod, X-Namespace, …) Passive
Headers Trace headers (X-Request-ID, X-Correlation-ID, W3C Traceparent, B3) Passive
Headers Edge/CDN headers (CF-Ray, X-Cache, X-Served-By, X-Varnish, X-Akamai) Passive
CORS Wildcard ACAO detection Defensive
CORS Credentials + wildcard detection Active
CORS Origin reflection probe with evil.example.com Active
CORS Null-origin acceptance probe Active
CORS Preflight method/header disclosure Defensive
Cookies Secure, HttpOnly, SameSite, domain, path, __Host-/__Secure- prefix audit Defensive
Cookies JWT-in-cookie audit Active
Cookies Base64 JSON payload detection Active
TLS Protocol version, cipher suite, issuer, subject, expiry, SANs Passive
WAF 25+ WAF product fingerprints (Cloudflare, Akamai, Incapsula, Sucuri, CloudFront, AWS WAF, Fastly, F5 BIG-IP, Barracuda, ModSecurity, Imperva, DDoS-Guard, FortiWeb, Citrix NetScaler, Radware, Wallarm, Signal Sciences, Rapid7, StackPath, KeyCDN, BunnyCDN, Gcore, Qrator, Vercel, Netlify, Deno Deploy, Cloudflare Workers, Fastly Compute) Active
DNS A, AAAA, NS, MX, TXT, SRV, CAA, DNSKEY, SOA, PTR, TLSA, SSHFP, NAPTR Passive
DNS DMARC, SPF, DKIM (default/google/selector1/selector2/k1) Passive
DNS MTA-STS, SMTP TLS, BIMI Passive
DNS ACME challenge TXT, DNSLink, GitHub Pages challenge Passive
DNS AXFR zone-transfer attempt Active
DNS Reverse PTR, RDAP ASN + organization Passive
Subdomains crt.sh certificate transparency aggregation Passive
Subdomains HackerTarget host-search API Passive
Subdomains RapidDNS aggregation Passive
Subdomains AlienVault OTX passive DNS Passive
Subdomains CNAME-resolved takeover fingerprinting (60+ providers) Active
Subdomains Dangling CNAME detection Active
Probes OPTIONS method discovery + TRACE XST Active
Probes Risky method enumeration (PUT, DELETE, PATCH, PROPFIND, …) Active
Probes Open-redirect injection across 20+ common parameters Active
Probes Cache-poisoning via X-Forwarded-* / X-Original-URL / Forwarded Active
Probes Web cache deception via appended static extensions Active
Probes HTTP method override via X-HTTP-Method-Override Active
Probes FAT-GET (GET-with-body) behavior detection Active
Probes GraphQL introspection across 12 common endpoint paths Active
Probes Path brute-force across 200+ common paths Active
Probes Sensitive path enumeration (.env, .git, wp-config, Dockerfile, package.json, actuator/*, phpinfo, backups, …) Active
Discovery robots.txt parsing + Allow/Disallow + Sitemap Passive
Discovery Sitemap recursion (up to 100k URLs) Passive
Discovery security.txt parsing Passive
Discovery humans.txt, ads.txt, app-ads.txt Passive
Discovery PWA manifest discovery Passive
Discovery RSS, Atom, feed discovery Passive
Discovery Changelog, README, LICENSE, SECURITY.md discovery Passive
Discovery Favicon hash (Shodan-compatible MD5) Passive
Discovery Pagination detection (page, p, offset, cursor, after, before, …) Core
Assets EXIF GPS + Make/Model/Software/SerialNumber extraction Active
Assets PDF metadata (Author, Creator, Producer, Title, Subject, Keywords, CreationDate, ModDate, Trapped) + page count Active
Assets Office (docx/xlsx/pptx/odt/ods/odp/epub) core.xml metadata Active
Assets ZIP/TAR archive entry listing Active
Assets SVG embedded-script / xlink-href extraction Active
Assets Font metadata (name table IDs 1–20) Active
Analysis IDOR candidate detection from numeric/UUID param sequences Passive
Analysis Parameter wordlist building Core
Analysis Internal ID attribute extraction Passive
Analysis Internal IP address detection (RFC1918) Passive
Analysis Dev-banner detection (lorem ipsum, coming soon, staging, beta) Passive
Analysis GraphQL endpoint URL extraction Passive
Reporting Live coloured streaming to terminal Core
Reporting JSONL streaming for SIEM ingestion Core
Reporting Deduplication of every emit Core
Reporting Severity classification (critical/high/medium/low/info) Core
Reporting Per-run text file output Core
Reporting SARIF 2.1.0 export Core
Reporting Baseline diffing Core
Reporting Resume checkpoints (JSONL) Core
Stealth 60+ User-Agent rotation Core
Stealth Accept-header variant rotation Core
Stealth Accept-Language rotation Core
Stealth Sec-CH-UA variant rotation Core
Stealth Referer construction Core
Stealth curl_cffi TLS impersonation (Chrome 120) Core
Stealth Per-host exponential backoff Core
Stealth Per-host jittered spacing Core
Stealth Graceful SIGINT/SIGTERM shutdown Core

---

Architecture Diagram

```
                    ┌────────────────────────────────┐
                    │      CLI / Interactive Menu     │
                    │   (-m, --jsonl, -fs, --resume)  │
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │          Crawler Core           │
                    │  queue · workers · scope · cap  │
                    └──┬──────────┬──────────┬────────┘
                       │          │          │
        ┌──────────────▼──┐  ┌────▼─────┐  ┌─▼──────────────┐
        │   Stealth Layer │  │ Fetcher  │  │   LiveStream    │
        │   UA / Sec-CH   │  │ curl_cffi│  │   dedup + emit  │
        │   jitter/backoff│  │  or httpx│  │   severity/color│
        └─────────────────┘  └────┬─────┘  └────────┬────────┘
                                  │                 │
                       ┌──────────▼─────────────────▼────────┐
                       │           Handler Pipeline          │
                       │  ┌────────────┐  ┌──────────────┐   │
                       │  │  HTML      │  │  JS (ESprima) │   │
                       │  │  extractor │  │  AST + regex  │   │
                       │  └────────────┘  └──────────────┘   │
                       │  ┌────────────┐  ┌──────────────┐   │
                       │  │  JSON      │  │  CSS parser   │   │
                       │  └────────────┘  └──────────────┘   │
                       │  ┌────────────┐  ┌──────────────┐   │
                       │  │  Secrets   │  │  Headers      │   │
                       │  │  Entropy   │  │  Cookies/CORS │   │
                       │  └────────────┘  └──────────────┘   │
                       │  ┌────────────┐  ┌──────────────┐   │
                       │  │  Asset     │  │  WAF / bot    │   │
                       │  │  EXIF/PDF  │  │  fingerprint  │   │
                       │  └────────────┘  └──────────────┘   │
                       └────────────┬────────────────────────┘
                                    │
                       ┌────────────▼────────────────────────┐
                       │       Active Probe Bundle           │
                       │  subdomain → CNAME takeover         │
                       │  paths · graphql · cache · redirect │
                       │  methods · fat-get · IDOR correlate │
                       └────────────┬────────────────────────┘
                                    │
                       ┌────────────▼────────────────────────┐
                       │       Reporting & Persistence        │
                       │  .txt · .jsonl · .sarif · .visited   │
                       │  checkpoint resume · baseline diff   │
                       └─────────────────────────────────────┘
```

---

Quick Start

```bash
# 1. Clone
git clone https://github.com/Sylhetyhackvenger/Silkfang 
cd Silkfang

# 2. Install
pip install -r requirements.txt

# 3. (run the tool)
python silkfang.py 

# Full crawl, unlimited pages, JSONL output
python silkfang.py https://target.example --unlimited --jsonl -y

# Offensive profile only, resume if previously interrupted
python silkfang.py https://target.example -m 200 --resume -y
```

---

Installation

Requirements

· Python 3.9+
· curl-cffi or httpx for HTTP fetching (curl-cffi highly recommended — it impersonates Chrome TLS)
· beautifulsoup4 + lxml for HTML parsing
· tldextract for registered-domain detection
· rich for terminal UI

Optional (each unlocks additional capability)

Package Unlocks
uvloop 2–4× faster asyncio event loop on Linux/macOS
esprima Full JS AST parsing instead of regex fallback
dnspython All DNS types, DMARC/SPF/DKIM, AXFR
Pillow EXIF GPS + camera metadata extraction
pypdf Precise PDF metadata parsing
fonttools TrueType/OpenType name-table extraction
ipwhois RDAP ASN + organization lookups

One-liner install

```bash
pip install curl-cffi httpx beautifulsoup4 lxml tldextract rich uvloop esprima dnspython Pillow pypdf fonttools ipwhois
```

From requirements.txt

```bash
pip install -r requirements.txt
```

Verify

```bash
python silkfang.py --self-test
# → {"ok": true, "findings": <n>}
```

---

The Three Scan Profiles

SILKFANG exposes three deliberate profiles. Choose the one that matches your intent.

1 — OFFENSIVE

Focused on attack surface discovery. Runs:

· Full crawl with all extraction pipelines
· Technology fingerprinting (framework, server, WAF, CDN)
· JavaScript AST mining for endpoints and secrets
· Secret detection across the whole signature library
· Subdomain aggregation from 4 public sources
· Subdomain takeover validation (CNAME + HTTP fingerprint)
· Sensitive path enumeration (.env, .git, wp-config, Dockerfile, package.json, backups, actuator endpoints, …)
· Path brute-force (200+ common paths)
· GraphQL introspection across 12 common endpoints
· HTTP method discovery + risky-method reporting (PUT, DELETE, PATCH, TRACE, PROPFIND, …)
· Open-redirect injection across 20+ common parameters
· Cache poisoning via X-Forwarded-*, X-Original-URL, Forwarded
· Cache deception via appended static extensions
· HTTP method override probes
· FAT-GET behavior detection
· Favicon hash (Shodan-compatible)
· DNS zone transfer attempt (AXFR)

Use this when you are performing authorized attack-surface mapping, bug-bounty reconnaissance, or red-team staging.

2 — DEFENSIVE

Focused on configuration hardening. Runs:

· Full crawl with all extraction pipelines
· Security header audit (30+ headers)
· HSTS max-age / preload / includeSubDomains validation
· CSP unsafe-inline / unsafe-eval / wildcard detection
· Cookie flag audit (Secure, HttpOnly, SameSite, __Host-/__Secure- prefix)
· CORS policy audit (wildcard, credentials, null origin)
· Form method/action audit, CSRF-token presence
· TLS certificate and cipher inspection
· robots.txt + sitemap + security.txt parsing
· humans.txt, ads.txt, app-ads.txt, PWA manifest, feeds
· Server-version leakage
· Trace-header leakage (X-Request-ID, X-Correlation-ID, Traceparent, B3)
· WAF fingerprinting (informational)

Use this when you are auditing your own infrastructure, preparing for a SOC2 / ISO 27001 audit, or reviewing a client's hardening posture.

3 — ALL + FULL

Runs both profiles, plus:

· Full-site crawl with pagination discovery
· Deep asset analysis (EXIF, PDF, Office, ZIP, SVG, fonts)
· IDOR parameter-sequence correlation across every discovered URL
· Resume checkpoints every 30 seconds

Use this when you want the complete picture in a single pass.

---

Command-Line Reference

```
usage: silkfang.py [-h] [target] [-l LIST] [-m MAX_PAGES] [--unlimited]
                   [-w WORKERS] [-r RATE] [-t TIMEOUT] [--passive]
                   [--no-subdomains] [--deep-assets] [--resume] [--reset]
                   [-o OUTPUT] [-y] [--min-delay MIN_DELAY]
                   [--max-delay MAX_DELAY] [--fast] [-fs {rdn,fqdn,dn}]
                   [-cs CRAWL_SCOPE] [-j] [--silent] [-q] [-nc] [--sarif]
                   [--baseline BASELINE] [--cookie COOKIE] [--bearer BEARER]
                   [--jwt-wordlist JWT_WORDLIST] [--proxy PROXY] [--self-test]
```

Target selection

Flag Description
target Single target URL (positional). Prefix https:// added automatically if missing.
-l, --list FILE Read multiple targets from a file, one URL per line.
--self-test Run the internal self-test suite and exit.

Crawl scope

Flag Default Description
-m, --max-pages N 100 Hard cap on total URLs crawled per run.
--unlimited off Disable the page cap entirely.
-w, --workers N 10 Concurrent fetch workers.
-r, --rate N 0 Global requests/second cap (0 = unlimited).
-t, --timeout N 15.0 Per-request timeout (seconds).
--passive off Skip all active probes; passive crawl only.
--no-subdomains off Disable subdomain enumeration and enqueueing.
--deep-assets off Download and analyze binary assets (images, PDFs, Office docs, archives, fonts, SVG).
--resume off Resume the previous run from its checkpoint.
--reset off Delete the checkpoint before starting.

Scope control

Flag Default Description
-fs, --field-scope {rdn,fqdn,dn} rdn rdn = registered domain + all subdomains; fqdn = exact hostname only; dn = hostname and any subdomain of the given hostname.
-cs, --crawl-scope REGEX — Only crawl URLs whose full URL matches this regex.

Stealth & pacing

Flag Default Description
--min-delay S 0.5 Minimum jitter delay between requests (seconds).
--max-delay S 2.5 Maximum jitter delay between requests (seconds).
--fast off Set min/max delay to zero. Rude. Use only against your own property.

Authentication

Flag Description
--cookie "name=value; name2=value2" Send this cookie header on every request.
--bearer TOKEN Send Authorization: Bearer TOKEN on every request.
--jwt-wordlist PATH Wordlist to attempt HS256 JWT cracking.

Networking

Flag Description
--proxy URL Route all traffic through http:// or socks5:// proxy.
--sarif Also write a .sarif file alongside the .txt output.
--baseline PATH Diff current findings against a previously-generated .txt.

Output control

Flag Description
-j, --jsonl Emit findings as JSONL to stdout. No menu, no colour.
--silent Same as --jsonl but no human-readable output either.
-q, --quiet Suppress low-signal types (FETCHED, IMG, TECH-ID, EXTERNAL-DOMAIN, PRELOAD, META, OG, MICRODATA, ICON, HEARTBEAT, HUD, INFO).
-nc, --no-color Disable ANSI colour in the terminal.
-o, --output DIR Output directory (default output).
-y, --yes Skip the authorization confirmation prompt.

Interactive vs non-interactive

· No --silent / --jsonl → interactive menu.
· With --silent or --jsonl → non-interactive; runs the ALL profile and exits.

---

Live Streaming Output Engine

Every discovery flows through LiveStream.emit(typ, key, val). The engine:

1. Deduplicates — the triple (typ, key, val) is added to a per-run set. Duplicate emits are silently dropped. This means you can watch the same IMG line only once, no matter how many pages reference it.
2. Classifies — maps typ to critical, high, medium, low, or info via the SEVERITY prefix table.
3. Colours — critical → bright red, high → red, medium → yellow, low → cyan, info → white.
4. Streams — prints a single line per emit:
   ```
   12:34:56  CRIT SECRET                → AWS-KEY AKIAIOSFODNN7EXAMPLE
   12:34:57  HIGH DOM-XSS               → location.hash → innerHTML
   12:34:57  MED  HDR-                  → CSP MISSING
   12:34:58  INFO TECH-ID               → WordPress
   ```
5. Tallies — maintains running counts per severity and per type, exposed for the final summary.

Quiet mode

-q filters out types that are informational-but-noisy:

```
FETCHED · INFO · TECH-ID · EXTERNAL-DOMAIN · IMG · PRELOAD
META · OG · MICRODATA · ICON · HEARTBEAT · HUD
```

All findings that imply something concrete was found still stream.

JSONL mode

-j emits one JSON object per line to stdout:

```json
{"type":"SECRET","url":"https://t/static/app.js","value":"AWS-KEY AKIAIOSFODNN7EXAMPLE","target":"https://t","severity":"critical","ts":"2025-01-15T12:34:56"}
{"type":"HDR-","url":"https://t/","value":"CSP MISSING","target":"https://t","severity":"medium","ts":"2025-01-15T12:34:57"}
```

Pipe straight into jq, rg, or a SIEM:

```bash
python silkfang.py https://t -j -y | jq 'select(.severity=="critical")'
```

HUD line

While running, a HUD line refreshes every 2 seconds (suppressed in -j/--silent):

```
RUNNING   https://target.example                                pages 42/100 assets 118 find 231 t 12s r 3.5/s
```

When per-host backoff is active, a second line appears:

```
⏸ backoff api.target.example:30s, www.target.example:15s
```

---

Offensive Capabilities

HTTP method discovery

OPTIONS / is issued. If Allow: is returned, every method is logged. Any of TRACE, PUT, DELETE, PATCH, CONNECT, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK present triggers METHOD-RISK.

A separate TRACE / attempt is made. If the response echoes TRACE and returns 200, METHOD-RISK: TRACE enabled (XST) fires.

Open-redirect injection

For each of 20 parameters (next, url, redirect, return, returnUrl, continue, redirect_uri, redirect_url, callback, callback_url, target, dest, destination, goto, to, link, forward, redir, r, u, out, view, ref, referrer) a GET is issued with ?param=https://evil.example.com and follow_redirects=False. If Location contains evil.example.com, OPEN-REDIRECT fires with the exact URL.

CORS preflight probe

1. OPTIONS / with Origin: https://evil.example.com and Access-Control-Request-Method: GET.
2. If Access-Control-Allow-Origin reflects evil.example.com, CORS-PREFLIGHT fires.
3. GET / with Origin: null. If Access-Control-Allow-Origin: null is reflected, CORS-PREFLIGHT fires again.

Cache poisoning

A canary of the form silkfang-NNNN is injected into each of 15 headers: X-Forwarded-Host, X-Forwarded-For, X-Original-URL, X-Rewrite-URL, X-Forwarded-Scheme, X-Forwarded-Port, X-Forwarded-Proto, X-Host, X-Backend, X-Real-IP, X-Proxy-Host, Forwarded, X-Original-Host, X-HTTP-Host-Override.

If the canary appears in the response body and the response is Cache-Control: public (or has an Age: header), CACHE-POISONING fires with the specific header name.

Cache deception

The path is requested with each of .css, .js, .png, .gif, .ico, .woff, .woff2, .svg, .jpg, .jpeg, .webp, .txt appended. If any of those returns a 200 with a body > 500 bytes whose MD5 does not match the control body, CACHE-DECEPTION fires.

HTTP method override

POST / is issued as a control. Then POST / is issued with each of X-HTTP-Method-Override, X-HTTP-Method, X-Method-Override set to each of PUT, DELETE, PATCH.

If the overridden request returns 200/204 while the control returns ≥ 400, METHOD-OVERRIDE fires.

FAT-GET detection

GET / with Content-Type: application/x-www-form-urlencoded is issued. If it returns 400 while the plain GET / returns 200, FAT-GET fires.

GraphQL introspection

For each of /graphql, /api/graphql, /v1/graphql, /query, /gql, /api/query, /api/gql, /v2/graphql, /graphql/v1, /api/v1/graphql, /graphql-api, /graph:

1. POST with Content-Type: application/json, body {"query": "{__schema{types{name fields{name}}}}"}.
2. POST with Content-Type: application/graphql, body {__schema{types{name fields{name}}}}.

If the response body contains __schema, GRAPHQL fires. If the body also contains mutation, GRAPHQL fires again with mutations present.

Path brute-force

FUZZ_PATHS contains 200+ common strings. A semaphore caps concurrency at 8. Each path is requested as BASE/path. Any of 200, 301, 302, 401, 403 triggers PATH with the status and body length. 200 hits are also enqueued for deeper crawling.

Sensitive path enumeration

SENSITIVE_PATHS contains 200+ paths. Each is enqueued through the normal crawl pipeline, which means every fetched result goes through the same SENSITIVE-200 handler:

```python
if r.status_code == 200 and path in HIGH_RISK_SENSITIVE:
    stream.emit("SENSITIVE-200", url, f"len=... snip=...")
```

The HIGH_RISK_SENSITIVE set narrows to ~100 paths where a 200 is very interesting: .env*, .git/*, .svn/*, wp-config.php, config.php, backups (.zip, .sql, .tar.gz, .rar), Dockerfile, docker-compose.yml, package.json, composer.lock, requirements.txt, Gemfile, .github/workflows/, .vscode/, .idea/, actuator/env, actuator/heapdump, actuator/threaddump, server-status, phpinfo.php, settings.py, next.config.js, nuxt.config.js, webpack.config.js, etc.

IDOR correlation

Every crawled URL is scanned for query parameters. Numeric parameter values of the form ^\d{1,7}$ are grouped by (path, param). If two or more distinct values exist within a 1000-wide window, IDOR-CANDIDATE fires:

```
IDOR-CANDIDATE  → /user/profile?id= numeric seq 1..42 (7 samples)
```

UUID values ^[0-9a-f]{8}-[0-9a-f]{4}-…$ are grouped similarly. Two or more distinct UUIDs → IDOR-CANDIDATE.

---

Defensive Audit Capabilities

Security header audit

SEC_HEADERS maps 60+ header names to short labels. Every header is emitted either as HDR+ (present) or HDR- (missing). Presence does not guarantee correctness — but absence is always a signal.

HSTS deep-inspection

If Strict-Transport-Security is present:

· max-age below 31536000 → HSTS-WEAK
· preload present → HSTS-PRELOAD
· includeSubDomains present → HSTS-SUBDOMAINS

CSP deep-inspection

· unsafe-inline → CSP-WEAK
· unsafe-eval → CSP-WEAK
· * present → CSP-WEAK
· report-uri extracted → CSP-REPORT-URI
· report-to extracted → CSP-REPORT-TO

Cookie audit

For every Set-Cookie:

· flags=Secure|HttpOnly|SameSite or flags=NONE
· domain, path, __Host- / __Secure- prefix presence
· If the value looks like a JWT (value.count('.') == 2), it is audited via audit_jwt.
· If the value base64-decodes to JSON, COOKIE-JSON fires.

CORS audit

· Access-Control-Allow-Origin: * → CORS
· Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true → CORS CREDENTIALS+WILDCARD (critical)
· Access-Control-Allow-Origin: <something-else> → CORS reflects <something>
· Access-Control-Allow-Methods → CORS-METHODS
· Access-Control-Allow-Headers → CORS-HEADERS

Redirect chain audit

Every redirect in resp.history is emitted as REDIRECT <index>:<status> with the URL. Full chain visible.

---

Technology Fingerprinting

fingerprint_tech(resp, body, stream) walks four independent signals:

1. HTML markers

Marker Tech
wp-content, wp-includes, /wp-json/ WordPress
csrfmiddlewaretoken Django
__viewstate ASP.NET
ng-version, ng-app Angular
__next_data__ Next.js
_nuxt Nuxt
data-reactroot, react-dom React
vue.js, vue.runtime Vue
__svelte Svelte
data-turbo Hotwire/Turbo
astro-island Astro
remix Remix
gatsby Gatsby
swagger-ui Swagger UI
docusaurus Docusaurus
hugo Hugo
jekyll Jekyll
eleventy Eleventy
shopify Shopify
magento Magento
drupal Drupal
joomla Joomla
grav Grav
concrete5 Concrete5
modx MODX
typo3 TYPO3
craft Craft CMS
statamic Statamic
contentful Contentful
sanity Sanity
prismic Prismic

…and 40+ more.

2. X-Powered-By / Server markers

express, django, flask, php, asp.net, nginx, apache, iis, cloudflare, tomcat, jboss, gunicorn, uvicorn, kestrel, caddy, traefik, envoy, haproxy, varnish, lighttpd, openresty, litespeed, node, deno, bun, puma, unicorn, passenger, phusion, werkzeug, rails, laravel, symfony, codeigniter, cakephp, yii, zend, spring, quarkus, micronaut, vertx, netty — all matched.

3. Cookie names

wp-, phpsessid, jsessionid, laravel_session, csrftoken, _next, __cf, asp.net_sessionid, _shopify, _ga, _gid, _fbp, _hjid, __hs, _mkto, _intercom, __stripe — all matched.

4. Server header full-string

The literal Server: header is fingerprinted against the same list.

Every hit produces one TECH-ID emit. Deduplicated, so a page that mentions react twelve times still emits React once.

Library version extraction

LIB_VERSION_PATTERNS maps 35+ libraries to version-capturing regexes. Example hits:

```
LIB-VERSION  jQuery    3.6.0
LIB-VERSION  Bootstrap 5.2.3
LIB-VERSION  React     18.2.0
LIB-VERSION  Vue       3.4.21
LIB-VERSION  Angular   17.1.0
```

These versions drive manual CVE research. SILKFANG does not perform automatic CVE matching — that's a decision for the operator.

---

JavaScript Deep Mining

mine_js_deep(js_text, js_url, stream) is the workhorse. It runs eight independent analyses on every JavaScript blob:

1. AST parse (esprima)

If esprima is installed, the JS is parsed (script first, module fallback). A recursive walk collects every Literal string value and every TemplateLiteral raw string that begins with /, http://, https://, ws://, or wss://. Result: up to 300 JS-AST emits per blob, each of which is a candidate endpoint.

If esprima is not installed, a regex fallback runs (RE_URL + RE_PATH) so the tool still works — you just lose the template-literal extraction.

2. WebSocket URL extraction

RE_WS — every ws:// and wss:// URL.

3. Source-map discovery

sourceMappingURL=<path> — the referenced map is joined against the JS URL and emitted as SOURCEMAP, then re-emitted as SOURCE-MAP with the exact URL. Fetch it manually — it will give you the original source tree.

4. Secret scanning

For each (pattern, label) in SECRET_PATTERNS:

· Find up to 5 matches.
· If label == HIGH-ENTROPY, require is_high_entropy_string() — length 20–200, mixed characters, no spaces, no / prefix, entropy > 4.2 bits/char.
· If label is a credit-card class, require luhn_valid().
· Emit SECRET <label> <match>.

5. JWT audit

RE_JWT finds every eyJ... triple. audit_jwt() decodes the header and payload, then:

· alg=none → JWT-VULN
· jwk in header → JWT-VULN
· jku in header → JWT-VULN + URL
· kid containing ../, /, or \ → JWT-VULN (kid injection)
· exp missing → JWT-WEAK
· password, pwd, secret, token, api_key, apikey in payload → JWT-SENSITIVE

If --jwt-wordlist is passed and alg=HS256, HMAC-SHA256 is computed for each wordlist entry (first 10,000) against header.payload. Match → WEAK-JWT-SECRET with the offending word.

6. postMessage audit

· addEventListener('message') present but no event.origin check → POSTMESSAGE-FLAW
· postMessage(..., '*') → POSTMESSAGE-WILDCARD

7. DOM-XSS correlation

Sources scanned: location.hash, location.search, location.href, document.URL, document.referrer, window.name, document.cookie, location.pathname, window.location, history.state.

Sinks scanned: innerHTML, outerHTML, document.write, document.writeln, eval, setTimeout, setInterval, Function.

Each (source, sink) pair produces DOM-XSS <src> → <sink>.

8. Prototype pollution

If __proto__ or constructor.prototype appears and an Object.assign, merge, extend, $.extend, _.merge, or $.fn.extend call appears within 80 characters, PROTO-POLLUTION fires with the surrounding context.

9. Sensitive storage

Every localStorage.setItem('key', ...) / sessionStorage.setItem('key', ...) where key contains any of token, auth, session, jwt, key, secret, user, password, credential, api, bearer, oauth, csrf, xsrf → STORAGE-SENSITIVE.

10. Dynamic imports

require('...'), import ... from '...', import('...') — every relative or absolute path is resolved against the JS URL and enqueued for fetching.

11. Fetch/axios calls

fetch('...') and axios.get/post/put/delete/patch('...') — endpoint extraction into FETCH emits.

---

Secret Detection Engine

SECRET_PATTERNS is a list[tuple[regex, label]]. There are 44 distinct provider families and 60+ regexes. Every match is subject to two filters:

1. HIGH-ENTROPY — every 32-to-45-character mixed-character string. Requires Shannon entropy > 4.2 to fire. This is the "I don't know what this is, but it looks like a key" detector. High false-positive rate, but occasionally catches things nobody has written a rule for yet.
2. CREDIT-CARD — every 13-to-19-digit number. Requires luhn_valid().

Full provider list:

```
AWS-KEY · AWS-STS · AWS-IAM · AWS-USER · AWS-ROLE
STRIPE-LIVE · STRIPE-PK · STRIPE-TEST · STRIPE-RESTRICTED
GOOGLE-API · SLACK-TOKEN · SLACK-APP
GITHUB-PAT · GITHUB-OAUTH · GITHUB-USER · GITHUB-SERVER · GITHUB-REFRESH · GITHUB-FINE
GITLAB-PAT · GITLAB-RUNNER
PRIVATE-KEY · CERTIFICATE
SENDGRID · MAILGUN · MAILGUN-KEY
DIGITALOCEAN · DIGITALOCEAN-OAUTH
ALIBABA · CLOUDINARY
TWILIO · TWILIO-SID
HUGGINGFACE · ANTHROPIC · OPENAI · OPENAI-PROJECT
GCP-SA · DISCORD · TELEGRAM · SQUARE · JWT · HIGH-ENTROPY
LINEAR · NOTION · AIRTABLE · AIRTABLE-PAT · FIGMA
SHOPIFY · SHOPIFY-AT · SHOPIFY-SS · SHOPIFY-CA · SHOPIFY-PA
COHERE · REPLICATE · OPENROUTER · GROQ · XAI · PERPLEXITY
CLAUDE · MISTRAL · DEEPGRAM · ELEVENLABS · ASSEMBLYAI
CLERK · SUPABASE-SECRET · SUPABASE-KEY
VERCEL · NETLIFY · FLY · RAILWAY · RENDER · HEROKU
DATADOG · PAGERDUTY · OPSGENIE · SLACK
DISCORD-WEBHOOK · DISCORD-HOOK · SLACK-HOOK
MAPBOX-SK · STRIPE-SK · CREDIT-CARD · IBAN · SSN
```

Every hit includes only the first 80 characters of the matched value — enough to identify, not enough to accidentally leak in a screenshot.

---

Asset Intelligence — The Deep Analyzer

When --deep-assets is passed, every binary asset reached by the crawler is downloaded and passed to deep_analyze_asset(), which dispatches by extension.

Images (.png .jpg .jpeg .gif .bmp .webp .tif .tiff)

Requires Pillow. Emits:

· ASSET-DIM — width × height × format
· EXIF-MAKE, EXIF-MODEL, EXIF-SOFTWARE, EXIF-DATETIME, EXIF-ARTIST, EXIF-COPYRIGHT, EXIF-IMAGEDESCRIPTION, EXIF-USERCOMMENT, EXIF-HOSTCOMPUTER, EXIF-LENSMODEL, EXIF-LENSMAKE, EXIF-SERIALNUMBER, EXIF-CAMERAOWNERNAME, EXIF-BODYSERIALNUMBER, EXIF-IMAGEUNIQUEID, EXIF-OWNERNAME
· EXIF-GPS — full GPS IFD as string

GPS-bearing images are the single most useful asset finding for social-engineering engagements.

PDFs (.pdf)

Requires pypdf for full parsing; falls back to raw-header regex.

· PDF-META — Author, Creator, Producer, Title, Subject, Keywords, CreationDate, ModDate, Trapped
· PDF-PAGES — page count

Office (.docx .xlsx .pptx .odt .ods .odp .epub)

Unzips docProps/core.xml and extracts:

· creator, lastModifiedBy, title, subject, description, keywords, company, manager, category, revision, created, modified

Archives (.zip .tar .tgz .gz .doc .xls .ppt)

Lists up to 60 entries per archive as ARCHIVE-ENTRY. Internal file names frequently leak directory structure, developer names, and internal project names.

SVG (.svg)

· <script in body → SVG-SCRIPT
· Every xlink:href → SVG-REF

Fonts (.ttf .otf .woff .woff2)

Requires fonttools. Extracts name table records 1–20: family, subfamily, unique ID, full name, version, PostScript name, trademark, manufacturer, designer, description, vendor URL, designer URL, license, license URL, and more. Font metadata occasionally leaks vendor information.

---

Subdomain Intelligence & Takeover Hunting

Aggregation sources

1. crt.sh — certificate transparency. Two queries per domain (%.domain and domain). Every name_value is split on newlines and filtered for .domain or == domain.
2. HackerTarget host-search — one query. hostname,ip CSV split.
3. RapidDNS — HTML scrape. <td>hostname</td> extraction.
4. AlienVault OTX passive DNS — JSON parse of passive_dns[].hostname.

Up to 1,000 subdomains are emitted as SUBDOMAIN.

Takeover validation

For every discovered subdomain:

1. Resolve CNAME — follow every CNAME record. Collect all canonical names.
2. Match against TAKEOVER_CNAME_HINTS — 60+ providers, each with a list of substrings that identify their dangling infrastructure (e.g. s3.amazonaws.com, herokuapp.com, github.io, azurewebsites.net, myshopify.com, netlify.app, vercel.app, wordpress.com, ghost.io, pantheonsite.io, readthedocs.io, tilda.ws, webflow.io, wix.com, …).
3. Fetch the live host. https://<subdomain> is retrieved.
4. Match against TAKEOVER_FINGERPRINTS — per-provider "not found" strings.

If a fingerprint matches, SUBDOMAIN-TAKEOVER fires with the specific provider and the CNAME that resolved to it.

If the fetch fails entirely but a dangling CNAME exists, DANGLING-CNAME fires with the provider and CNAME — still exploitable, just not proven.

The takeover fingerprint table

The TAKEOVER_FINGERPRINTS dictionary contains 40+ providers, each with 1–3 fingerprints. Selected examples:

Provider Fingerprint
AWS S3 NoSuchBucket, The specified bucket does not exist, The specified key does not exist
GitHub Pages There isn't a GitHub Pages site here
Heroku No such app
Azure 404 Web Site not found, This site is stopped
Shopify Sorry, this shop is currently unavailable
Tumblr There's nothing here.
Fastly Fastly error: unknown domain
Ghost The thing you were looking for is no longer here
Pantheon The gods are wise
WordPress.com doesn't exist. Would you like to search for it?
Surge.sh project not found
Bitbucket Repository not found
Netlify Not found - Request ID
Vercel The deployment could not be found
Read the Docs The requested project was not found
Zendesk Help Center Closed, This help center no longer exists
Freshdesk There is no helpdesk here
Tilda Please renew your subscription
Webflow This site is not published
Strikingly Sorry, this page is not available
Wix Error ConnectYourDomain occurred
Ngrok Tunnel 

…and 20+ more.

---

DNS Deep Dive

dns_deep(domain, stream) runs a fixed sequence of resolvers.

Standard records

A, AAAA, NS, MX, TXT, SRV, CAA, DNSKEY, SOA, PTR, SPF, TLSA, SSHFP, NAPTR — each emits DNS-<TYPE> <domain> <value> on every record found.

Email authentication

Record Query Emits
DMARC _dmarc.domain TXT EMAIL-AUTH DMARC
SPF domain TXT EMAIL-AUTH SPF
DKIM (default) default._domainkey.domain TXT EMAIL-AUTH DKIM-DEFAULT
DKIM (google) google._domainkey.domain TXT EMAIL-AUTH DKIM-GOOGLE
DKIM (selector1) selector1._domainkey.domain TXT EMAIL-AUTH DKIM-SELECTOR1
DKIM (selector2) selector2._domainkey.domain TXT EMAIL-AUTH DKIM-SELECTOR2
DKIM (k1) k1._domainkey.domain TXT EMAIL-AUTH DKIM-K1

Email policy

· default._bimi.domain TXT → EMAIL-POLICY
· _mta-sts.domain TXT → EMAIL-POLICY
· _smtp._tls.domain TXT → EMAIL-POLICY
· _dmarc.domain TXT → EMAIL-POLICY

Well-known TXT

· _acme-challenge.domain — ACME challenge presence
· _dnslink.domain — IPFS / DNSLink presence
· _github-pages-challenge.domain — GitHub Pages verification

Reverse PTR + RDAP

1. socket.gethostbyname(scope) → IP
2. Reverse PTR (<reversed-ip>.in-addr.arpa) → RDNS
3. RDAP lookup via ipwhois → ASN + ORG

Zone transfer

For each NS record:

1. Resolve the NS hostname to an IP.
2. Attempt dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=5)).
3. If successful → DNS-ZONE-TRANSFER + up to 100 ZONE-RECORD emits.

AXFR is rare on modern DNS, but when it succeeds it is game-over. Worth the five seconds.

---

TLS Fingerprinting

tls_deep(url, stream) performs a raw socket TLS handshake with check_hostname=False and verify_mode=CERT_NONE — this means the tool captures the cert even when it is expired or self-signed.

Emits:

· TLS-PROTO <hostname> <version> — TLSv1.3, TLSv1.2, …
· TLS-CIPHER <hostname> <name> (<protocol>)
· TLS issuer <org> — issuer organization name
· TLS subject <cn> — subject common name
· TLS expires <date> — notAfter
· TLS SANs <comma-separated> — up to 50 SANs

SANs frequently reveal staging hosts, internal domains, and additional attack surface that never appears in public DNS.

---

WAF & Bot-Challenge Detection

WAF fingerprinting

WAF_SIGNATURES is a dictionary mapping provider names to lists of (header, needle) tuples. None needle means "any non-empty value of this header counts."

Provider list: Cloudflare, Akamai, Incapsula, Sucuri, AWS CloudFront, AWS WAF, Fastly, F5 BIG-IP, Barracuda, ModSecurity, Imperva, DDoS-Guard, FortiWeb, Citrix NetScaler, Radware, Wallarm, Signal Sciences, Rapid7, StackPath, KeyCDN, BunnyCDN, Gcore, Qrator, Vercel, Netlify, Deno Deploy, Cloudflare Workers, Fastly Compute.

Cookie-based WAFs are handled separately (incap_ses, visid_incap are checked against the cookie jar).

Any positive match emits WAF <provider> header=<header> and returns immediately — first match wins.

Bot challenge detection

detect_bot_challenge(resp) is called on every 429/503 response. BOT_CHALLENGE_SIGNATURES lists body and header markers for:

· Cloudflare (cf-mitigated, just a moment, checking your browser)
· DataDome (captcha-delivery)
· Akamai (reference #, _abck)
· PerimeterX (_px, px-captcha)
· Kasada (x-kpsdk-ct)
· hCaptcha
· reCAPTCHA
· Cloudflare Turnstile
· Arkose / FunCaptcha
· AWS WAF (aws-waf-token)
· Imperva (_incap_ses)
· F5 BIG-IP (bigip, ts_, mr_)
· Sucuri
· Wordfence
· Shield

Any hit → BOT-CHALLENGE <url> <vendor>. The stealth layer then backs off (exponential up to 300s) and retries.

---

Anti-Detection & Stealth Layer

User-Agent pool

USER_AGENTS contains 60+ distinct strings spanning:

· Chrome 117–122 on Windows, macOS, Linux
· Firefox 120–123 on Windows, macOS, Linux
· Safari 16.5–17.3 on macOS
· Edge 120–122
· Opera 106–107
· Brave 121–122
· Vivaldi 6.4–6.5
· Android Chrome 119–122, Samsung Internet 23
· iOS Safari 16.6–17.3, iPadOS
· Googlebot, Bingbot, YandexBot, Baiduspider, DuckDuckBot, Applebot
· cURL 8.0–8.5, python-httpx, python-requests, Wget
· Facebook, Twitter, LinkedIn, Slack, Telegram, WhatsApp preview bots

The pool is shuffled at start and reshuffled on cycle.

Header rotation

For every request, build_headers() picks:

· One User-Agent
· One Accept variant from 11 options
· One Accept-Language variant from 20 options
· One sec-ch-ua variant from 8 options (only for Chrome-family UAs)
· One sec-ch-ua-mobile, sec-ch-ua-platform, Sec-Fetch-* set matching the UA
· One Referer (origin URL of the target)

Accept-Encoding and Connection are fixed.

Per-host scheduling

Stealth.wait(url):

1. If the host is in backoff, sleep until backoff_until.
2. Acquire the global lock, enforce a per-host minimum spacing of 0.2 + uniform(0.05, 0.35) seconds.
3. Sleep uniform(min_delay, max_delay).

Stealth.mark_failure(url) increments failures and sets backoff_until = now + min(300, base * 2^(failures-1)) where base = 5.0.

Stealth.mark_success(url) resets failures to zero.

curl_cffi TLS impersonation

When curl_cffi is available, ClientWrapper opens an AsyncSession(impersonate="chrome120"). This makes the TLS ClientHello match Chrome 120 exactly — JA3/JA4 fingerprint-safe against most naive WAF TLS checks.

When curl_cffi is not available, httpx.AsyncClient is used with verify=False, http2=False. Less stealthy, but functional.

Graceful shutdown

SIGINT and SIGTERM are intercepted. On either, crawler.interrupt() sets _interrupted = True, workers drain the current fetch, and finally flushes the checkpoint. No findings are lost.

---

Resume & Checkpoint System

StateStore maintains a .jsonl file per target FQDN:

```
output/.silkfang-state-<fqdn>.jsonl
```

Content structure:

```
{"k": "meta",     "v": {"target": "...", "mode": "all", "timestamp": ...}}
{"k": "visited",  "v": "https://t/"}
{"k": "visited",  "v": "https://t/about"}
{"k": "assets",   "v": "https://t/logo.png"}
{"k": "all_urls", "v": "https://t/api/users"}
{"k": "result",   "v": ["SECRET", "AWS-KEY", "AKIA..."]}
```

Saving is atomic: it writes to .tmp then os.replaces. A crash mid-save cannot corrupt the checkpoint.

Checkpoints occur every 30 seconds and always on finally. --resume loads the checkpoint and skips re-fetching every visited URL. --reset deletes it.

The checkpoint survives Ctrl-C, SIGTERM, OOM-kill, and kill -9. (Only the 30-second window since the last write is lost.)

---

Output Formats

Terminal (default)

Live coloured, streamed. On completion, a summary panel:

```
COMPLETE  pages=142  assets=38  findings=1042  crit=3  high=47  med=82  low=201  info=709  elapsed=94.3s
```

Text file

output/<fqdn>-<mode>.txt — one line per finding:

```
SECRET            https://t/app.js       AWS-KEY AKIAIOSFODNN7EXAMPLE
HDR-              https://t/             CSP MISSING
DOM-XSS           https://t/app.js       location.hash → innerHTML
...
```

URL listings

· output/<fqdn>-visited.txt — every URL crawled
· output/<fqdn>-all-urls.txt — every URL discovered (visited + queued + asset)
· output/<fqdn>-assets.txt — every binary asset found
· output/<fqdn>-params.txt — every query parameter name discovered

JSONL

-j → stdout only, one JSON object per finding. Streamable directly into jq, rg, ELK, Splunk, or a custom indexer.

SARIF

--sarif → output/<fqdn>-<mode>.sarif, SARIF 2.1.0 compliant. Every finding becomes a SARIF result, every type becomes a rule. Severity mapping:

· critical → error
· high → error
· medium → warning
· low → note
· info → note

---

SARIF Integration for CI/CD

Upload the .sarif file to GitHub Advanced Security:

```yaml
# .github/workflows/silkfang.yml
name: silkfang
on: [push, workflow_dispatch]
jobs:
  recon:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt
      - run: python silkfang.py https://staging.mycorp.com -m 500 --sarif --silent -y
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: output/staging.mycorp.com-all.sarif
```

Now every new secret, every new sensitive path, every new WAF misconfiguration appears as an alert on the exact PR that introduced it.

---

Baseline Diffing

```bash
# First run — save baseline
python silkfang.py https://t -o baseline -y

# Later — diff against baseline
python silkfang.py https://t --baseline baseline/t-all.txt -y
```

diff_with_baseline() compares current findings against the baseline set and prints only the delta:

```
┌───────────────────────────────────────┐
│ 47 new findings since baseline         │
└───────────────────────────────────────┘
+ SECRET: https://t/v2/app.js → AWS-KEY AKIA...
+ SENSITIVE-200: https://t/.env.local → len=2048
+ SUBDOMAIN-TAKEOVER: staging.t → AWS S3 via s3.amazonaws.com
```

Perfect for weekly post-deploy audits.

---

Scope Control

SILKFANG enforces scope at two levels.

Field scope (-fs)

Controls which hostnames count as "in scope."

Value Behavior
rdn (default) Registered domain + all subdomains. example.com, api.example.com, foo.bar.example.com are all in scope.
fqdn Exact hostname only. example.com is in scope; api.example.com is not.
dn Hostname and any subdomain of that hostname. example.com and api.example.com are in scope; example.co.uk is not.

Implementation uses tldextract for rdn and dn. fqdn is a plain string compare.

Crawl scope (-cs)

An optional regex. If set, only URLs whose full string matches the regex are enqueued for crawling. Example:

```bash
# Only crawl /api and /v2 paths
python silkfang.py https://t -cs '^https://t/(api|v2)/' -y
```

Both checks run inside _in_scope(). Anything failing either check is dropped before it enters the queue.

---

Operational Playbooks

Playbook 1 — Quick external attack-surface map

```bash
python silkfang.py https://target.example -m 300 -w 15 --fast -y
```

· 300-page cap
· 15 concurrent workers
· Fast mode (no jitter)
· Interactive menu → pick 1 OFFENSIVE

Expected output: subdomain list, sensitive path hits, technology stack, JS endpoints, any leaked secrets.

Duration: 3–8 minutes for a medium-sized target.

Playbook 2 — Full-site defensive audit

```bash
python silkfang.py https://myapp.mycorp.com --unlimited -y
```

· No cap
· Menu → pick 2 DEFENSIVE

Expected output: header audit, cookie audit, CORS audit, TLS cert report.

Duration: depends on size; typically under 15 minutes.

Playbook 3 — Authenticated crawl

```bash
python silkfang.py https://myapp.mycorp.com \
  --cookie "session=$(cat session.txt)" \
  --unlimited -y
```

Or bearer:

```bash
python silkfang.py https://api.mycorp.com \
  --bearer "$(cat token.txt)" \
  --unlimited -y
```

All requests carry the credential. Crawl into authenticated areas of the app.

Playbook 4 — JWT offline crack

```bash
python silkfang.py https://myapp.mycorp.com \
  --jwt-wordlist rockyou.txt \
  -m 50 -y
```

Any HS256 JWT found in a cookie, JS blob, or HTML is tested against the first 10,000 words of the wordlist.

Playbook 5 — Full red-team recon (combined)

```bash
python silkfang.py https://target.example \
  --unlimited --deep-assets -w 20 --sarif --jsonl -y > findings.jsonl
```

· Unlimited crawl
· Deep asset analysis (EXIF, PDF, Office, ZIP)
· 20 workers
· SARIF + JSONL output

Then:

```bash
jq 'select(.severity=="critical")' findings.jsonl
```

Playbook 6 — Continuous recon with baseline diffing

```bash
# Day 1
python silkfang.py https://target.example -o baseline1 -y

# Day 2
python silkfang.py https://target.example -o day2 --baseline baseline1/target.example-all.txt -y
```

Only new findings are printed to the delta panel. Perfect for monitoring a bug-bounty target.

Playbook 7 — Resume an interrupted scan

```bash
# Interrupted
python silkfang.py https://target.example --unlimited -y
# ^C

# Continue
python silkfang.py https://target.example --unlimited --resume -y
```

The checkpoint in output/.silkfang-state-*.jsonl restores visited URLs, assets, and prior findings.

Playbook 8 — Batched multi-target

```bash
cat targets.txt
# https://target1.example
# https://target2.example
# https://target3.example

python silkfang.py -l targets.txt --silent --jsonl -y > all-findings.jsonl
```

Runs the ALL profile on each in sequence, streaming JSONL continuously.

Playbook 9 — Bug bounty scope lockdown

```bash
python silkfang.py https://target.example \
  -fs fqdn \
  -cs '^https://target\.example/' \
  --no-subdomains \
  --passive \
  -y
```

· Only the exact FQDN
· Only URLs starting with https://target.example/
· No subdomain lookup
· No active probes
· Zero out-of-scope traffic.

---

Signature Library Reference

Secret patterns

60+ regexes across 44 providers. See Secret Detection Engine.

Sensitive comments

sensitive_comment_hints regex — matches HTML comments containing:
todo, fixme, hack, bug, password, passwd, pwd, secret, token, api_key, api-key, apiKey, admin, internal, debug, staging, backup, private, hidden, vulnerable, xss, sqli, injection, bypass, auth, credential, apikey, aws, gcp, azure, client_secret, private_key, salt, hash, jwt, oauth, bearer, ssh, pem, cert, keystore, htpasswd, shadow, sudo, root.

Library version patterns

35+ JS libraries: jQuery, jQuery-UI, jQuery-Mobile, Bootstrap, Foundation, Bulma, Tailwind, React, React-DOM, Redux, Vue, Vuex, Angular, Svelte, Ember, Backbone, Knockout, Lodash, Underscore, Moment, Day.js, D3, Chart.js, Three.js, GSAP, Axios, Socket.io, Handlebars, Mustache, RequireJS, Modernizr, Popper, Alpine, HTMX.

WAF signatures

25+ providers: see WAF & Bot-Challenge Detection.

Bot challenge signatures

15+ vendors: Cloudflare, DataDome, Akamai, PerimeterX, Kasada, hCaptcha, reCAPTCHA, Turnstile, Arkose, AWS WAF, Imperva, F5, Sucuri, Wordfence, Shield.

Takeover fingerprints

60+ providers, 40+ "not found" strings: see Subdomain Intelligence & Takeover Hunting.

Analytics providers

GA-UA, GA4, GTM, Facebook Pixel, Hotjar, Segment, Amplitude, Mixpanel, PostHog, Plausible, Matomo, Umami, Clarity, Heap, RudderStack, mParticle, Tealium.

Error-tracking providers

Sentry, Datadog RUM, New Relic, Rollbar, Honeybadger, Bugsnag, Raygun, LogRocket, FullStory.

Chat providers

Intercom, Drift, Crisp, Zendesk.

CAPTCHA providers

reCAPTCHA, hCaptcha, Cloudflare Turnstile.

Map providers

Mapbox, Google Maps, Here.

Realtime providers

Pusher, PubNub, Ably.

Search providers

Algolia, Typesense, MeiliSearch.

---

Sensitive Path Dictionary

SENSITIVE_PATHS contains 200+ paths grouped by category. Selected highlights:

Configuration files

.env, .env.local, .env.production, .env.backup, .env.dev, .env.staging, .env.test, .env.old, .env.bak, .env.example, config.json, config.yaml, config.yml, settings.py, web.config, app.config, appsettings.json, .htaccess, .htpasswd.

Version-control metadata

.git/config, .git/HEAD, .git/logs/HEAD, .git/index, .gitignore, .git/refs/heads/master, .git/refs/heads/main, .git/packed-refs, .svn/entries, .svn/wc.db, .hg/, .bzr/, .DS_Store.

WordPress

wp-login.php, wp-admin/, wp-json/wp/v2/users, xmlrpc.php, wp-config.php, wp-config.php.bak, wp-config.php~, wp-content/debug.log, wp-content/uploads/, wp-includes/version.php.

Admin panels

administrator/, admin/, admin, admin.php, admin.html, login, login.php, login.html, signin, signin.php, dashboard, console, panel, cpanel, webadmin, manager.

API surface

api, api/, api/v1, api/v2, api/v3, api/v4, api/docs, api/swagger.json, api/openapi.json, api/swagger.yaml, api/graphql, api/users, api/admin, api/config, api/health, api/status, api/me, api/profile, api/token, api/auth.

API documentation

graphql, graphiql, altair, playground, voyager, apollo, swagger-ui/, swagger-ui.html, swagger.json, swagger.yaml, openapi.json, openapi.yaml, api-docs, docs, redoc, redoc.html.

Spring Boot Actuator

actuator, actuator/env, actuator/health, actuator/mappings, actuator/beans, actuator/heapdump, actuator/threaddump, actuator/metrics, actuator/loggers, actuator/info, actuator/auditevents.

Well-known

.well-known/security.txt, .well-known/openid-configuration, .well-known/change-password, .well-known/host-meta, .well-known/webfinger, .well-known/assetlinks.json, .well-known/apple-app-site-association, security.txt.

Server diagnostic

server-status, server-info, phpinfo.php, info.php, php.php, test.php, debug.php, config.php, config.php.bak.

Backups

backup.zip, backup.sql, backup.tar.gz, backup.rar, backup.7z, db.sql, dump.sql, site.tar.gz, www.zip, site.zip, db.sqlite.

Robots / sitemap / feed

robots.txt, sitemap.xml, sitemap_index.xml, sitemap-news.xml, sitemap-images.xml, sitemap-video.xml, feed, rss, atom.xml, blog/feed, news/feed.

Package manifests

package.json, package-lock.json, yarn.lock, pnpm-lock.yaml, composer.json, composer.lock, Gemfile, Gemfile.lock, requirements.txt, Pipfile, Pipfile.lock, pyproject.toml, go.mod, go.sum, Cargo.toml, Cargo.lock, pom.xml, build.gradle, build.gradle.kts, Makefile, CMakeLists.txt.

CI/CD

.github/workflows/, .github/, .circleci/config.yml, .gitlab-ci.yml, .travis.yml, azure-pipelines.yml.

Build configuration

.vscode/, .idea/, .editorconfig, .eslintrc, .eslintrc.json, .prettierrc, .babelrc, .browserslistrc, tsconfig.json, gulpfile.js, Gruntfile.js, webpack.config.js, vite.config.js, next.config.js, nuxt.config.js, svelte.config.js, astro.config.mjs.

Container

Dockerfile, docker-compose.yml, docker-compose.yaml, .dockerignore, kubernetes/, k8s/, helm/.

A 200 response on any member of HIGH_RISK_SENSITIVE (the top ~100 of the above) triggers SENSITIVE-200 with a body snippet — these are the highest-value findings in the entire tool.

---

Developer Reference

Extending the signature library

All signature tables are module-level constants. To add a new secret pattern:

```python
# In SECRET_PATTERNS
(r'NEWPROVIDER_[A-Za-z0-9]{40}', "NEWPROVIDER-KEY"),
```

To add a new sensitive path:

```python
# In SENSITIVE_PATHS
"/.newpath", "/new/config.json",
# And optionally in HIGH_RISK_SENSITIVE
"/.newpath",
```

To add a new takeover fingerprint:

```python
# In TAKEOVER_FINGERPRINTS
"NewProvider": ["fingerprint string 1", "fingerprint string 2"],
# In TAKEOVER_CNAME_HINTS
"NewProvider": ["newprovider.com", "newprovider.io"],
```

To add a new WAF signature:

```python
# In WAF_SIGNATURES
"NewWAF": [("server", "newwaf"), ("x-newwaf", None)],
```

To add a new JS library version pattern:

```python
# In LIB_VERSION_PATTERNS
"newlib": re.compile(r'newlib[.\-/]?v?(\d+\.\d+(?:\.\d+)?)', re.I),
```

Adding a new analysis pass

Every analysis function has signature f(input_text, source_url, stream) and emits via stream.emit(typ, key, val). To add a new one:

1. Write the function.
2. Call it from mine_js_deep (for JS), extract_all (for HTML), mine_json_deep (for JSON), or parse_css (for CSS).
3. Add a severity mapping to SEVERITY if you introduce a new typ.
4. Add a documentation entry.

Adding a new active probe

probe_* functions are async and receive (client, stealth, url, stream). Register them in Crawler.run_probes under the appropriate mode guard:

```python
if self.mode in ("offensive", "all") and not self.passive:
    await probe_my_new_probe(client, self.stealth, self.start, self.stream)
```

Adding a new output format

1. Subclass or extend Crawler.save_results.
2. Walk self.results (a list of (typ, key, val) triples).
3. Emit to your format.
4. Hook into run_scan after crawler.run() completes.

Adding a new stealth header

In Stealth.build_headers, append to the dict:

```python
headers["X-Custom"] = my_random_value(),
```

The current implementation already produces a coherent Chrome/Firefox/Safari header set. Diverging carelessly will make the fingerprint more suspicious, not less.

---

Performance & Tuning

Workers

Workers Context
5 Small site, polite crawl
10 Default — balanced
20–30 Larger sites, higher concurrency, still respectful of jitter
50+ Only against your own property; jitter + backoff will still apply

Workers are asyncio.Tasks running Crawler.worker. Each one loops on queue.get(). Queue depth is capped by max_pages minus pending.

Rate limiting

· -r 10 — global cap of 10 requests/second across all workers.
· The per-host spacing enforced by Stealth.wait is independent of -r — it enforces a minimum per-host spacing regardless of global rate.

Memory

Each finding is a (str, str, str) tuple. At 10,000 findings, memory footprint is a few megabytes. visited, all_urls, assets are Python sets of strings — negligible.

The LiveStream._seen set grows linearly with unique findings. On a very large target, if memory becomes an issue, patch _seen to a Bloom filter or a bounded LRU.

Disk

Checkpoint .jsonl grows linearly with visited URLs + findings. A 100,000-page crawl produces roughly 10 MB of checkpoint. Results file similar.

uvloop

Installing uvloop (auto-detected at import time) typically produces a 2–4× throughput improvement on Linux and macOS. On Windows, it is silently skipped.

Large sites

For sites with more than 100,000 pages, use:

```bash
python silkfang.py https://huge.site --unlimited -w 30 --fast -y \
  -cs '^https://huge\.site/(docs|api|blog)/'
```

And run in --jsonl mode so terminal rendering does not become the bottleneck:

```bash
python silkfang.py https://huge.site --unlimited -w 30 -j -y > huge.jsonl
```

---

Troubleshooting

"FATAL: beautifulsoup4 is required"

```bash
pip install beautifulsoup4 lxml
```

"FATAL: tldextract is required"

```bash
pip install tldextract
```

"FATAL: rich is required"

```bash
pip install rich
```

curl_cffi import fails

Install the binary wheel:

```bash
pip install curl-cffi
# or, on some systems:
pip install curl-cffi --no-cache-dir
```

If the wheel is unavailable for your platform, httpx is used as fallback — stealth drops but functionality is preserved.

esprima not installed

SILKFANG works without esprima — the JS parser falls back to regex extraction. You lose template-literal endpoint detection, but everything else still works. Install with:

```bash
pip install esprima
```

"Neither curl_cffi nor httpx is available"

```bash
pip install curl-cffi
# or
pip install httpx
```

DNS queries fail silently

Check that dnspython is installed:

```bash
pip install dnspython
```

Without it, dns_deep, zone_transfer, subdomain_takeover_check, and crt_sh_subdomains's DNS portion are silently skipped. HTTP-based subdomain sources still work.

Every request returns 403

You are behind a WAF that does not like your headers. Options:

1. Confirm curl_cffi is installed — Chrome TLS impersonation is the most effective counter.
2. Slow down: --min-delay 2 --max-delay 5.
3. Use a proxy: --proxy http://user:pass@proxy:port.
4. Switch User-Agent pool (edit USER_AGENTS).
5. Accept the 403s and move to another target.

Cache poisoning findings are false positives

SILKFANG reports cache poisoning only when both conditions are true:

1. The canary reflects in the response body.
2. The response is either Cache-Control: public or has an Age: header.

If both are true, you almost certainly have a real issue. If you suspect a false positive, verify manually with cURL.

Subdomain takeover findings are false positives

The takeover check requires:

1. A real CNAME to a known provider.
2. A live HTTP fetch returning the provider's specific "not found" fingerprint.

If you get a hit, the response body literally contains the provider's "site does not exist" message. Verify manually — this is nearly always genuine.

Scan hangs

· Check output/.silkfang-state-*.jsonl for the last visited URL.
· Ctrl-C once — the checkpoint will flush.
· Rerun with --resume.
· If it hangs again on the same URL, exclude that path with -cs.

Memory grows unbounded

· Cap with -m instead of --unlimited.
· Use --passive to skip active probes.
· Narrow scope with -cs.

--self-test fails

```bash
pip install -r requirements.txt
python silkfang.py --self-test
```

If the failure is "ok": false with an err, install the missing core dependency named in the error.

---

FAQ

Q: Is SILKFANG safe to run against my own site?
A: Yes. Use --fast only against your own property, since it disables the jitter delays.

Q: Does SILKFANG find actual vulnerabilities?
A: It finds classes of issues — secrets, misconfigurations, exposed paths, open redirects, IDOR candidates, takeover-able subdomains, weak JWT secrets, prototype-pollution patterns. It does not perform automated exploitation. Every finding requires a human to triage.

Q: Will it get me blocked?
A: Almost certainly on a well-defended target. The stealth layer is sophisticated but not omniscient — Cloudflare Bot Management, DataDome, and Kasada will still detect a bot at scale. Reduce -w, increase --min-delay, and use curl_cffi.

Q: How does it compare to Amass, Subfinder, httpx, nuclei?
A: SILKFANG is a single tool that does the surface-scanning work of those tools together, streaming results live. For deep subdomain enumeration use Amass. For deep vulnerability scanning use nuclei. SILKFANG is the reconnaissance engine that feeds them.

Q: Does it support proxies?
A: Yes, --proxy http://user:pass@host:port or --proxy socks5://host:port (socks5 requires curl_cffi).

Q: Does it handle authenticated targets?
A: Yes, --cookie "name=value" or --bearer TOKEN. All requests carry the credential.

Q: What is the difference between --passive and --no-subdomains?
A: --passive skips all active probes (path fuzz, method discovery, GraphQL, cache poisoning, takeover validation, redirect injection). --no-subdomains only skips subdomain aggregation and enqueueing — active probes still run against the main target.

Q: What does -fs fqdn do vs -fs rdn?
A: rdn scopes to the registered domain — example.com and all its subdomains. fqdn scopes to the exact host — api.example.com only, nothing else.

Q: Why does --jsonl skip the menu?
A: Because the menu requires a TTY. JSONL is meant for piping into other tools.

Q: Can I run this in CI/CD?
A: Yes. --silent --sarif -y is designed exactly for that. See SARIF Integration.

Q: How do I resume after Ctrl-C?
A: python silkfang.py <target> --resume -y. The checkpoint is auto-loaded.

Q: What is the difference between -j, --silent, and -q?
A: -j/--jsonl outputs JSON lines to stdout, no menu. --silent is -j plus no coloured terminal output. -q still uses the interactive menu and coloured output but suppresses low-value types.

Q: Can I add my own secret regex?
A: Yes, append a (pattern, label) tuple to SECRET_PATTERNS. See Developer Reference.

Q: Does it work on Windows?
A: Yes. uvloop is skipped; all other functionality is identical.

Q: What is --self-test?
A: A minimal end-to-end check against https://example.com. If it succeeds and reports findings > 0, the tool is operational.

Q: Is the .silkfang-state-*.jsonl file sensitive?
A: It contains every URL crawled and every finding — that is, it may contain secrets, session IDs, and internal URLs. Treat it with the same care as the target itself.

Q: Does SILKFANG respect robots.txt?
A: No. It parses robots.txt (to find disallowed paths, which are usually the most interesting), but it does not honour Disallow. This is deliberate — the tool is for authorized research, and robots directives are not a security control.

Q: What about security.txt?
A: It does fetch and parse security.txt, because it identifies the correct disclosure contact for the target.

---

Roadmap

☐ v1.1 — Headless-browser fallback via Playwright for JS-rendered SPAs
☐ v1.2 — Built-in OpenAPI / Swagger parser → auto-endpoint discovery
☐ v1.3 — S3 / GCS / Azure bucket anonymous-access validation (opt-in --probe-cloud)
☐ v1.4 — HTTP/2-only target support (curl_cffi already does it; exposing the flag)
☐ v1.5 — Response-time-based blind-SQLi timing heuristic (very opt-in)
☐ v1.6 — Interactive shell — drop into help, add <url>, skip <url>, show <type> mid-crawl
☐ v1.7 — Plugin API for third-party extractors
☐ v1.8 — Distributed crawling (Redis queue backend)
☐ v2.0 — Web UI

---

Credits & Contact

Author: SYLHETYHACKVENGER (THE-ERROR808)
Project name: SILKFANG
License: MIT
Language: Python 3.9+

Built with

· curl_cffi — TLS fingerprint impersonation, the single most important dependency for effective web reconnaissance against modern WAFs.
· httpx — HTTP fallback
· BeautifulSoup + lxml — HTML parsing
· tldextract — registered-domain extraction
· rich — terminal UI
· esprima-python — JavaScript AST
· dnspython — DNS
· Pillow — image EXIF
· pypdf — PDF parsing
· fonttools — font metadata
· ipwhois — RDAP lookups
· uvloop — event loop

Signature data derived from

· crt.sh certificate transparency
· HackerTarget hostsearch
· RapidDNS
· AlienVault OTX passive DNS
· ProjectDiscovery's nuclei-template conventions
· Common community knowledge on subdomain takeover fingerprints

Special thanks

The gray-hat community that quietly maintains the fingerprint tables, the WAF signatures, and the takeover-proof strings that make tools like this possible. Without you, everything here would be Server: nginx and hope.

---

Final Word

"The best reconnaissance is the kind that discovers what nobody else bothered to look at."

SILKFANG exists because the gap between "I know how to read HTML" and "I can enumerate an entire attack surface" is wider than most people realize. The tool is fast, honest, and — most importantly — it tells you exactly what it found, exactly where it found it, and exactly why it thinks it matters.

If it saves you one hour on one engagement, it was worth building.

Use it well. Use it lawfully. And when you find something interesting, disclose it responsibly.

---

<div align="center">

SILKFANG · Website Recon Engine & A Powerful Crawler

Made by SYLHETYHACKVENGER (THE-ERROR808)

If this tool helped you, star the repo. If it found something critical, buy me a coffee.

</div>

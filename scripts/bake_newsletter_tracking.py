#!/usr/bin/env python3
"""Bake Coop newsletter / dealer-email tracking into HTML.

Email (CRM paste):
  - UTMs on store + magazine CTAs only
  - utm_medium MUST be exactly "email" (GA4 Default Channel Group)
  - NEVER inject gtag.js into email HTML
  - Optional 1x1 open pixel if --open-pixel-url is set

Site magazine (Motive paste):
  - UTMs on store CTAs: source=<pub>, medium=site, campaign=<issue>
  - Lightweight engagement hook that uses existing window.gtag if Motive already loaded it
  - NEVER double-load gtag / GTM / CoopTag (site shell owns those)

Usage:
  python3 bake_newsletter_tracking.py email --file path.html --campaign sline-news-01 --source newsletter
  python3 bake_newsletter_tracking.py site  --file path.html --campaign sline-news-01 --source sline-news --store-hosts audibatonrouge.com
  python3 bake_newsletter_tracking.py batch-sept-2026
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit, unquote

ROOT_EMAIL = Path(__file__).resolve().parents[1]
ROOT_SEO = Path("/Users/lucfaucheux/.openclaw/workspace/seo-pages")

SKIP_HOST_BITS = (
    "facebook.com",
    "fb.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "linkedin.com",
    "youtube.com",
    "maps.google",
    "google.com/maps",
    "fonts.googleapis",
    "fonts.gstatic",
    "wikimedia",
    "hodinkee",
    "carscoops",
    "espn.com",
    "resy.com",
    "ticketbud",
    "salesforce",
    "manshiptheatre",
    "lasm.org",
    "ardenland",
    "msmuseumart",
    "msbookfestival",
    "visitjackson",
    "jacksonbroadway",
    "newstagetheatre",
    "elsiespies",
    "motor1",
    "commons.wikimedia",
    "tigerdroppings",
    "gojsutigers",
    "hailstate",
    "olemisssports",
    "qtego.us",
    "cdn.ui.porsche",
    "thecooperativeagency.github.io/fonts",
    "thecooperativeagency.github.io/seo-pages/style-specs",
)

HREF_RE = re.compile(r'href=(["\'])(https?://[^"\']+)\1', re.I)
CTA_TEXT_RE = re.compile(
    r'href=(["\'])(https?://[^"\']+)\1[^>]*>(.*?)</a>',
    re.I | re.S,
)

SITE_HOOK = """
<!-- Coop magazine tracking: uses Motive/site gtag if present; does not load GA -->
<script>
(function () {
  var meta = document.querySelector('meta[name="coop-magazine"]');
  if (!meta) return;
  var pub = meta.getAttribute('data-publication') || 'magazine';
  var issue = meta.getAttribute('data-issue') || '';
  var store = meta.getAttribute('data-store') || '';
  function fire(name, params) {
    params = params || {};
    params.publication = pub;
    params.issue = issue;
    params.store = store;
    params.page_path = location.pathname;
    try {
      if (typeof gtag === 'function') {
        gtag('event', name, params);
        return;
      }
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: name }, params));
    } catch (e) {}
  }
  fire('magazine_issue_view', { engagement_type: 'view' });
  if ('IntersectionObserver' in window) {
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id || entry.target.getAttribute('data-section') || '';
        if (!id || seen[id]) return;
        seen[id] = 1;
        fire('magazine_section_view', { section_id: id });
      });
    }, { threshold: 0.35 });
    document.querySelectorAll('section[id], article[id], [data-section]').forEach(function (el) {
      io.observe(el);
    });
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (!/^https?:/i.test(href)) return;
    fire('magazine_cta_click', {
      link_url: href.split('#')[0],
      link_text: (a.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 80)
    });
  }, true);
})();
</script>
""".strip()


def slugify(text: str) -> str:
    t = re.sub(r"<[^>]+>", "", text or "")
    t = unquote(t)
    t = t.lower().strip()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    t = t.strip("-")
    return (t or "cta")[:48]


def content_from_url(url: str) -> str:
    path = urlsplit(url).path.rstrip("/").split("/")[-1] or "home"
    path = unquote(path)
    path = re.sub(r"\.[a-z0-9]+$", "", path, flags=re.I)
    return slugify(path)[:40]


def should_skip(url: str, store_hosts: list[str] | None, mode: str) -> bool:
    u = url.lower()
    if u.startswith(("mailto:", "tel:", "sms:", "#", "javascript:")):
        return True
    host = urlsplit(url).netloc.lower()
    path = urlsplit(url).path.lower()
    full = f"{host}{path}"
    for bit in SKIP_HOST_BITS:
        if bit in full:
            return True
    if mode == "email":
        # Track store domains + our github.io magazine previews
        if store_hosts:
            if any(h in host for h in store_hosts):
                return False
            if "thecooperativeagency.github.io" in host and "seo-pages" in path:
                return False
            return True
        return False
    # site mode: only store hosts (internal magazine CTAs to lot/service)
    if store_hosts:
        return not any(h in host for h in store_hosts)
    return True


def add_utms(url: str, source: str, medium: str, campaign: str, content: str) -> str:
    parts = urlsplit(url)
    q = dict(parse_qsl(parts.query, keep_blank_values=True))
    # Do not stomp existing Coop UTMs if already complete
    if q.get("utm_source") and q.get("utm_medium") and q.get("utm_campaign"):
        # still fill missing content
        if content and not q.get("utm_content"):
            q["utm_content"] = content
            return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q, doseq=True), parts.fragment))
        return url
    q["utm_source"] = source
    q["utm_medium"] = medium
    q["utm_campaign"] = campaign
    if content:
        q["utm_content"] = content
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q, doseq=True), parts.fragment))


def build_content_map(html: str) -> dict[str, str]:
    """Map bare URL -> preferred utm_content from anchor text when useful."""
    m: dict[str, str] = {}
    for _q, url, inner in CTA_TEXT_RE.findall(html):
        text = re.sub(r"<[^>]+>", "", inner)
        text = re.sub(r"\s+", " ", text).strip()
        if not text or len(text) > 60:
            continue
        # Prefer action-y labels
        if re.search(r"\b(shop|read|book|service|specials|inventory|new|used|pre-owned|offer|q[0-9]|x[0-9]|macan|cayenne|taycan)\b", text, re.I):
            m[url] = slugify(text)
    return m


def bake_html(
    html: str,
    *,
    mode: str,
    source: str,
    medium: str,
    campaign: str,
    store_hosts: list[str],
    publication: str = "",
    issue: str = "",
    store: str = "",
    open_pixel_url: str = "",
) -> tuple[str, int]:
    content_map = build_content_map(html)
    changed = 0

    def repl(match: re.Match) -> str:
        nonlocal changed
        quote, url = match.group(1), match.group(2)
        if should_skip(url, store_hosts, mode):
            return match.group(0)
        content = content_map.get(url) or content_from_url(url)
        new = add_utms(url, source, medium, campaign, content)
        if new != url:
            changed += 1
            return f"href={quote}{new}{quote}"
        return match.group(0)

    out = HREF_RE.sub(repl, html)

    if mode == "site":
        meta = (
            f'<meta name="coop-magazine" data-publication="{publication or source}" '
            f'data-issue="{issue or campaign}" data-store="{store}" />'
        )
        if 'name="coop-magazine"' not in out:
            m_head = re.search(r"</head>", out, re.I)
            if m_head:
                i = m_head.start()
                out = out[:i] + f"  {meta}\n" + out[i:]
            else:
                out = meta + "\n" + out
        if "magazine_issue_view" not in out:
            m_body = re.search(r"</body>", out, re.I)
            if m_body:
                i = m_body.start()
                out = out[:i] + SITE_HOOK + "\n" + out[i:]
            else:
                out += "\n" + SITE_HOOK

    if mode == "email" and open_pixel_url:
        # Ensure UTMs not required on pixel; append cache-bust friendly src once
        pixel = (
            f'<img data-coop="open-pixel" src="{open_pixel_url}" width="1" height="1" alt="" '
            f'style="display:block;width:1px;height:1px;border:0;" />'
        )
        if 'data-coop="open-pixel"' not in out and open_pixel_url not in out:
            m_body = re.search(r"</body>", out, re.I)
            if m_body:
                i = m_body.start()
                out = out[:i] + pixel + "\n" + out[i:]
            else:
                out += "\n" + pixel

    return out, changed


SEPT_BATCH = [
    # Emails
    {
        "mode": "email",
        "file": ROOT_EMAIL / "Audi Baton Rouge/Sales/abr-september-2026-sales-email-sline-teaser.html",
        "source": "newsletter",
        "medium": "email",
        "campaign": "sline-news-01",
        "store_hosts": ["audibatonrouge.com", "thecooperativeagency.github.io"],
    },
    {
        "mode": "email",
        "file": ROOT_EMAIL / "Audi Baton Rouge/Sales/abr-september-2026-sales-email.html",
        "source": "newsletter",
        "medium": "email",
        "campaign": "sep-2026-sales",
        "store_hosts": ["audibatonrouge.com", "thecooperativeagency.github.io"],
    },
    {
        "mode": "email",
        "file": ROOT_EMAIL / "Brian Harris BMW/Sales/bh-bmw-september-2026-email.html",
        "source": "newsletter",
        "medium": "email",
        "campaign": "ultimate-driver-issue-01",
        "store_hosts": ["brianharrisbmw.com", "thecooperativeagency.github.io"],
    },
    {
        "mode": "email",
        "file": ROOT_EMAIL / "BMW of Jackson/Sales/bmw-jackson-september-2026-email.html",
        "source": "newsletter",
        "medium": "email",
        "campaign": "ultimate-driver-issue-01",
        "store_hosts": ["bmwofjackson.net", "thecooperativeagency.github.io"],
    },
    {
        "mode": "email",
        "file": ROOT_EMAIL / "Harris Porsche/Sales/harris-porsche-september-2026-email.html",
        "source": "newsletter",
        "medium": "email",
        "campaign": "sep-2026-sales",
        "store_hosts": ["harris.porsche.com", "thecooperativeagency.github.io"],
    },
    # Site magazines
    {
        "mode": "site",
        "file": ROOT_SEO / "Audi Baton Rouge/s-line-news-issue-01-september-2026.html",
        "source": "sline-news",
        "medium": "site",
        "campaign": "sline-news-01",
        "store_hosts": ["audibatonrouge.com"],
        "publication": "sline-news",
        "issue": "issue-01-sep-2026",
        "store": "abr",
    },
    {
        "mode": "site",
        "file": ROOT_SEO / "Brian Harris BMW/bhbmw-news-issue-01-september-2026.html",
        "source": "ultimate-driver",
        "medium": "site",
        "campaign": "ultimate-driver-issue-01",
        "store_hosts": ["brianharrisbmw.com"],
        "publication": "ultimate-driver",
        "issue": "issue-01-sep-2026",
        "store": "bhbmw",
    },
    {
        "mode": "site",
        "file": ROOT_SEO / "BMW of Jackson/bmwj-news-issue-01-september-2026.html",
        "source": "ultimate-driver",
        "medium": "site",
        "campaign": "ultimate-driver-issue-01",
        "store_hosts": ["bmwofjackson.net"],
        "publication": "ultimate-driver",
        "issue": "issue-01-sep-2026",
        "store": "bmwj",
    },
    {
        "mode": "site",
        "file": ROOT_SEO / "Harris Porsche/drivers-cut-issue-01-september-2026.html",
        "source": "drivers-cut",
        "medium": "site",
        "campaign": "drivers-cut-issue-01",
        "store_hosts": ["harris.porsche.com", "service-booking.porsche.com"],
        "publication": "drivers-cut",
        "issue": "issue-01-sep-2026",
        "store": "hp",
    },
]


def process_one(cfg: dict) -> None:
    path: Path = cfg["file"]
    if not path.exists():
        print(f"SKIP missing {path}")
        return
    html = path.read_text(encoding="utf-8")
    out, n = bake_html(
        html,
        mode=cfg["mode"],
        source=cfg["source"],
        medium=cfg["medium"],
        campaign=cfg["campaign"],
        store_hosts=cfg.get("store_hosts") or [],
        publication=cfg.get("publication", ""),
        issue=cfg.get("issue", ""),
        store=cfg.get("store", ""),
        open_pixel_url=cfg.get("open_pixel_url", ""),
    )
    if out != html:
        path.write_text(out, encoding="utf-8")
        print(f"OK {cfg['mode']:5} +{n:3} utms  {path.relative_to(path.parents[2] if 'email-creative' in str(path) else path.parents[1])}")
    else:
        print(f"NOOP {path}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_email = sub.add_parser("email")
    p_email.add_argument("--file", required=True)
    p_email.add_argument("--campaign", required=True)
    p_email.add_argument("--source", default="newsletter")
    p_email.add_argument("--medium", default="email")
    p_email.add_argument("--store-hosts", default="")
    p_email.add_argument("--open-pixel-url", default="")

    p_site = sub.add_parser("site")
    p_site.add_argument("--file", required=True)
    p_site.add_argument("--campaign", required=True)
    p_site.add_argument("--source", required=True)
    p_site.add_argument("--medium", default="site")
    p_site.add_argument("--store-hosts", required=True)
    p_site.add_argument("--publication", default="")
    p_site.add_argument("--issue", default="")
    p_site.add_argument("--store", default="")

    sub.add_parser("batch-sept-2026")

    args = ap.parse_args(argv)
    if args.cmd == "batch-sept-2026":
        for cfg in SEPT_BATCH:
            process_one(cfg)
        return 0

    hosts = [h.strip() for h in args.store_hosts.split(",") if h.strip()]
    cfg = {
        "mode": args.cmd,
        "file": Path(args.file),
        "source": args.source,
        "medium": args.medium,
        "campaign": args.campaign,
        "store_hosts": hosts,
        "publication": getattr(args, "publication", ""),
        "issue": getattr(args, "issue", ""),
        "store": getattr(args, "store", ""),
        "open_pixel_url": getattr(args, "open_pixel_url", ""),
    }
    process_one(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

"""Resilient job description extraction."""
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(dict.fromkeys(line for line in lines if len(line) > 1))


def scrape_job_url(url: str, timeout: int = 20) -> str:
    if not url or not urlparse(url).scheme:
        return ""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Gerador-de-Curriculo-Especifico/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        html = response.text
        try:
            import trafilatura
            extracted = trafilatura.extract(html, include_links=False,
                                             include_comments=False,
                                             favor_recall=True)
            if extracted and len(extracted) > 300:
                return clean_text(extracted)
        except Exception:
            pass
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()
        return clean_text(soup.get_text("\n"))
    except Exception:
        return scrape_with_playwright(url, timeout)


def scrape_with_playwright(url: str, timeout: int = 20) -> str:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0")
            page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            page.wait_for_timeout(1500)
            text = page.locator("body").inner_text()
            browser.close()
            return clean_text(text)
    except Exception as exc:
        return f"[Não foi possível extrair automaticamente: {exc}]"

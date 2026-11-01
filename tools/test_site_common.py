import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import site_common as sc

def test_store_link_has_campaign_and_mt():
    assert sc.store_link("web_home_nl") == "https://apps.apple.com/app/apple-store/id6784261188?ct=web_home_nl&mt=8"

def test_asset_prefix_root_vs_subdir():
    assert sc.asset("nl", "styles.css") == "styles.css"
    assert sc.asset("en", "styles.css") == "/styles.css"

def test_nav_marks_current_language():
    html = sc.nav("fr", current="index.html")
    assert 'hreflang="fr" aria-current="page"' in html
    assert html.count("<li>") == 5

def test_qr_svg_is_inline_svg():
    svg = sc.qr_svg("https://example.com")
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")

def test_head_contains_hreflang_for_all_languages():
    h = sc.head("nl", title="T", desc="D", path="index.html", alt={"nl": "index.html", "en": "en/index.html", "fr": "fr/index.html", "de": "de/index.html", "es": "es/index.html"})
    assert h.count('rel="alternate" hreflang=') == 6  # 5 talen + x-default
    assert '<link rel="canonical" href="https://rightsetfret.studioplanb.be/index.html">' in h

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)

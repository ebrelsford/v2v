

HTML_CODES = (
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    ("'", '&#39;'),
)

def html_unescape(html):
    """
    Apparently this doesn't exist anywhere else. Translate common HTML entities
    in an html string.

    """
    for code in HTML_CODES:
        html = html.replace(code[1], code[0])
    return html

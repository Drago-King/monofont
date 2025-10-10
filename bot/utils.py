def escape_markdown(text: str) -> str:
    """Escape special characters for MarkdownV2."""
    if not text:
        return ""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    for ch in special_chars:
        text = text.replace(ch, f'\\{ch}')
    return text


def to_monospace(text: str) -> str:
    """Convert plain text to monospace MarkdownV2 format."""
    escaped = escape_markdown(text)
    # Use triple backticks safely by escaping them
    return "```\n" + escaped + "\n```"

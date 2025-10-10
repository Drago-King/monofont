def escape_markdown(text: str) -> str:
    """Escape special characters for MarkdownV2 inline contexts.

    Note: Not used for code blocks since escaping is not required inside
    triple backtick blocks in Telegram MarkdownV2.
    """
    if not text:
        return ""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    for ch in special_chars:
        text = text.replace(ch, f'\\{ch}')
    return text


def to_monospace(text: str) -> str:
    """Wrap text in a MarkdownV2 code block.

    No escaping is needed inside triple backticks. We only guard against
    accidental occurrences of "```" in the content by breaking the sequence
    with a zero-width space.
    """
    if text is None:
        text = ""
    safe_text = text.replace("```", "`\u200b``")
    return f"```\n{safe_text}\n```"

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split('\n\n'):
        stripped = line.strip()
        if stripped:
            blocks.append(stripped)
    return blocks
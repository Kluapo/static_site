from enum import Enum

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split('\n\n'):
        stripped = line.strip()
        if stripped:
            blocks.append(stripped)
    return blocks

class Blocktype(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST ='unordered_list'
    ORDERED_LIST = 'ordered_list' 

def is_ordered_list(block):
    lines = block.split('\n')
    for i, line in enumerate(lines, start=1):
        expected = f"{i}. "
        if not line.startswith(expected):
            return False
    return True

def is_quote(block):
    lines = block.split('\n')
    for line in lines:
        if not line.startswith('>'):
            return False
    return True
        
def block_to_block_type(block):
    match block:
        case block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return Blocktype.HEADING
        case block.startswith("```"): 
            if block.endswith('```'):
                return Blocktype.CODE
        case _ if is_quote(block):
            return Blocktype.QUOTE
        case block.startswith(('* ','- ')):
            return Blocktype.UNORDERED_LIST
        case _ if is_ordered_list(block):
            return Blocktype.ORDERED_LIST
        case _:
            return Blocktype.PARAGRAPH
            
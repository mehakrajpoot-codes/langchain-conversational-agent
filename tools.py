from langchain_core.tools import tool
from datetime import datetime
import ast
import operator
import requests


# ==========================================
# TOOL 1: CALCULATOR
# ==========================================

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_calculate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](
            _safe_calculate(node.operand)
        )

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_calculate(node.left)
        right = _safe_calculate(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    raise ValueError("Invalid mathematical expression.")


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression such as 25 * 48 or (100 + 50) / 5."""

    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_calculate(tree.body)
        return f"Result: {result}"

    except Exception as e:
        return f"Calculation error: {e}"


# ==========================================
# TOOL 2: WEB RESEARCH
# ==========================================

@tool
def web_research(query: str) -> str:
    """Research a topic from Wikipedia and return useful information."""

    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(
            " ", "_"
        )

        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "LangChainResearchAgent/1.0"}
        )

        if response.status_code != 200:
            return "Could not find reliable information for this topic."

        data = response.json()

        title = data.get("title", query)
        extract = data.get("extract", "No information found.")

        return f"Research result for {title}:\n\n{extract}"

    except Exception as e:
        return f"Research error: {e}"


# ==========================================
# TOOL 3: TEXT SUMMARIZER
# ==========================================

@tool
def text_summarizer(text: str) -> str:
    """Summarize a long piece of text into a short and clear summary."""

    if not text.strip():
        return "No text was provided."

    sentences = text.replace("\n", " ").split(". ")

    if len(sentences) <= 3:
        return text.strip()

    summary = ". ".join(sentences[:3])

    if not summary.endswith("."):
        summary += "."

    return summary


# ==========================================
# TOOL 4: WORD COUNTER
# ==========================================

@tool
def word_counter(text: str) -> str:
    """Count the number of words in the provided text."""

    words = text.split()

    return f"The text contains {len(words)} words."


# ==========================================
# TOOL 5: CURRENT DATE AND TIME
# ==========================================

@tool
def current_datetime() -> str:
    """Return the current local date and time."""

    now = datetime.now()

    return now.strftime(
        "Current date: %Y-%m-%d\nCurrent time: %H:%M:%S"
    )


# ==========================================
# ALL TOOLS
# ==========================================

tools = [
    calculator,
    web_research,
    text_summarizer,
    word_counter,
    current_datetime,
]
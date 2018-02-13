import duckduckgo as ddg
import asks
from answer import Answer

client = asks.Session(connections=20)


def ddg_ia(query: str) -> Answer:
    """Searches ddg."""

    result = ddg.query(query)

    answer = Answer(body=None)

    if result.redirect.url != "":
        answer.body = result.redirect.url
    elif result.answer.text != "":
        answer.body = f"_{result.answer.text}_"
    elif result.abstract.text != "":
        answer.body = str(result.abstract.text)
        answer.url = result.abstract.url
        answer.icon = result.image.url
        answer.related = result.related
    elif len(result.related) is not 0:
        answer.title = "Did you mean..."
        answer.related = result.related
    else:
        # XXX Find where it gets its data from
        answer.body = ddg.get_zci(query)

    return answer

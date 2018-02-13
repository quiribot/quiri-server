import duckduckgo as ddg
import asks
from response import Response

client = asks.Session(connections=20)


def ddg_ia(query):
    """Searches ddg."""

    result = ddg.query(query)

    response = Response(body=None)

    if result.redirect.url != "":
        response.body = result.redirect.url
    elif result.answer.text != "":
        response.body = f"_{result.answer.text}_"
    elif result.abstract.text != "":
        response.body = str(result.abstract.text)
        response.url = result.abstract.url
        response.icon = result.image.url
        response.related = result.related
    elif len(result.related) is not 0:
        response.title = "Did you mean..."
        response.related = result.related
    else:
        # XXX Find where it gets its data from
        response.body = ddg.get_zci(query)

    return response

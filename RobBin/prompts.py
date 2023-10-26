def format_zone(z):
    return f"{z['name']} ({z['temperature']} grader)"


def introduction(name: str) -> str:
    return f"""
        Du har blitt tilkalt av {name} for å hjelpe dem kvitte seg med søppel.
        {name} har aldri møtt deg før, så du må introdusere deg selv og forklare hva din funksjon er.
        Bruk maks 50 ord.
    """


def hello(name: str) -> str:
    return f"""
        Du har blitt tilkalt av {name}. {name} har møtt deg før,
        så du trenger ikke å introdusere deg selv på nytt.
        Fortell {name} at du er glad for å se dem igjen.
        Bruk maks 50 ord.
    """


def feedback(name: str) -> str:
    return f"""
        Brukeren {name} har kildesortert søppel.
        Gi dem tilbakemelding med ett personalisert dikt eller haiku.
        Bruk maks 50 ord.
    """


def goodbye_and_suggestion(name: str, zone: dict[str, str], available_zones: list[dict[str, str]]) -> str:
    return f"""
        Brukeren {name} er i sone {format_zone(zone)}.
        Tilgjengelige soner er {', '.join([format_zone(z) for z in available_zones])}. 
        Fortell {name} om temperaturen i sonen de er i,
        og nevn noen av de andre tilgjengelige sonene (maks 2) og temperaturene deres.
        Påminn {name} om at de kan flytte seg til de andre sonene hvis det høres mer behaglig ut.
        Fortell {name} at du må videre og at du håper de får en fin dag.
    """

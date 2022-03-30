import re


SINGER_COLLABORATION_TERMS = ["featuring", "with", "&"]


class SongMetadataCurator:

    def __init__(self) -> None:
        pass

    def remove_apostrophes(self, text: str) -> str:
        processed_text = text.replace("'", "")
        return processed_text

    def normalise_singer_collaboration(self, text: str) -> str:
        pattern = "\s" + "|\s".join(SINGER_COLLABORATION_TERMS)
        replacement = ", "
        processed_text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE)
        return processed_text

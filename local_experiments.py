from typing import Union
from urllib.request import urlopen

import spacy
from spacy.tokens import Span


def load_txt_from_url(url="https://sherlock-holm.es/stories/plain-text/houn.txt"):
    data = urlopen(url)
    text = ""
    for line in data:
        text += line.decode("utf-8")
    return text


if __name__ == '__main__':
    text = load_txt_from_url()
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("entityLinker", last=True)
    doc = nlp(text)
    print(doc._.linkedEntities[:5])

    # Create a lookup table based on extracted entities to allow Span access
    entity_lookup = {(ent.start, ent.end): ent for ent in doc.ents}

    def get_entity(span: Span) -> Union[Span, int]:
        if (span.start, span.end) in entity_lookup.keys():
            return entity_lookup[(span.start, span.end)]
        else:
            return -1

    Span.set_extension("ent", getter=get_entity)

    # Reduce linkedEntities to only mentions that are likely actual "entities"
    # Basically combine the start/end positions.

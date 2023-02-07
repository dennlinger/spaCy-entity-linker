from typing import Union
from urllib.request import urlopen

import spacy
import spacy_entity_linker
from spacy_entity_linker.TermCandidate import TermCandidate
from spacy_entity_linker.EntityClassifier import EntityClassifier
from spacy.tokens import Span, Doc


def load_txt_from_url(url="https://sherlock-holm.es/stories/plain-text/houn.txt"):
    data = urlopen(url)
    text = ""
    for line in data:
        text += line.decode("utf-8")
    return text


def associate_entities_with_span(text: str):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("entityLinker", last=True)
    doc = nlp(text)

    # Create a lookup table based on extracted entities to allow Span access
    entity_lookup = {(ent.start, ent.end): ent for ent in doc.ents}

    def get_entity(span: Span) -> Union[Span, int]:
        if (span.start, span.end) in entity_lookup.keys():
            return entity_lookup[(span.start, span.end)]
        else:
            return -1

    Span.set_extension("ent", getter=get_entity)
    # Doc.set_extension("filtered_links", getter=)

    # Reduce linkedEntities to only mentions that are likely actual "entities"
    # Basically combine the start/end positions.

    return doc


def match_entities_to_spacy(text: str):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    external_entities = {}
    # classifier
    classifier = EntityClassifier()
    for ent in doc.ents:
        # build a term candidate (a simple span)
        termCandidate = TermCandidate(ent)
        # get all the candidates for the term
        entityCandidates = termCandidate.get_entity_candidates()
        if len(entityCandidates) > 0:
            # select the best candidate
            entity = classifier(entityCandidates)
            # entity.span.sent._.linkedEntities.append(entity) # --> cannot if the attribute is not registered
            # entities[ent.entity)
        else:
            entity = None
        print(f'SpaCy: {(ent.text + " " + ent.label_).ljust(40)}spaCy-entity-linker: {entity}')


if __name__ == '__main__':
    baskervilles = load_txt_from_url()

    doc = associate_entities_with_span(baskervilles)




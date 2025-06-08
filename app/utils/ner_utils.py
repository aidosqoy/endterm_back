from transformers import pipeline

ner_pipeline = pipeline(
    task="ner",
    model="Davlan/distilbert-base-multilingual-cased-ner-hrl",
    aggregation_strategy="simple"
)

def extract_person_names(text):
    results = ner_pipeline(text)
    persons = set()

    for res in results:
        if res["entity_group"] == "PER":
            persons.add(res["word"])

    return list(persons)

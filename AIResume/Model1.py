import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
import pandas as pd
import re
import random
import os
import json

def remove_overlapping_entities(entities):
    if not entities:
        return entities
    # Sort entities by their start position and length (longest first)
    sorted_entities = sorted(entities, key=lambda x: (x[0], x[1] - x[0]), reverse=True)
    non_overlapping_entities = []
    covered_positions = set()

    for start, end, label in sorted_entities:
        # Check if this entity overlaps with any positions already covered
        if any(pos in covered_positions for pos in range(start, end)):
            continue  # Skip this entity because it overlaps
        # Add this entity to the list and mark its positions as covered
        non_overlapping_entities.append((start, end, label))
        covered_positions.update(range(start, end))

    # Return the list sorted by the start position
    return sorted(non_overlapping_entities, key=lambda x: x[0])

def generate_training_data(job_descriptions, keywords):
    training_data = []

    for job_desc in job_descriptions:
        entities = []
        for keyword, label in keywords.items():
            # Find all non-overlapping matches of the keyword in the job description
            for match in re.finditer(re.escape(keyword), job_desc, re.IGNORECASE):
                start, end = match.span()
                entities.append((start, end, label))
        
        # Only add the job description to the training data if at least one entity was found
        if entities:
            training_data.append((job_desc, {"entities": entities}))
    
    return training_data

nlp = spacy.load('en_core_web_sm') #load the small english model
spacy.require_gpu()  # Force the use of GPU
print(spacy.prefer_gpu()) 
if "ner" not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner)
else:
    ner = nlp.get_pipe("ner")

# Labels from text file
with open('C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\labels.txt') as f:
    labels = f.read().splitlines()

# Add the labels to the NER
for label in labels:
    ner.add_label(label)


keywords = {}

with open('C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\keywords.txt', 'r') as file:
    #i = 0
    for line in file:
        #i += 1
        #print(i)
        keyword, label = line.strip().split('$')
        keywords[keyword] = label

df = pd.read_excel("C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\JDSheet.xlsx", usecols=[0],header=None)

df.columns = ['JD']
if(os.path.exists("C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\trainingData.json")):
        with open("C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\trainingData.json") as f:
            trainingData = json.load(f)
else:
    trainingData = generate_training_data(df['JD'], keywords)
    with open("C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\trainingData.json",'w') as f:
        json.dump(trainingData, f, indent=4)
#print(trainingData)

# Disable other pipeline components during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.resume_training()
    for i in range(1000):  # Number of training iterations, you can adjust this
        random.shuffle(trainingData)
        losses = {}
        batches = minibatch(trainingData, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
        print(f"Losses at iteration {i}: {losses}")

nlp.to_disk("C:\\Users\\TheKilogram\\OneDrive\\Documents\\programs\\AIResume\\Model")

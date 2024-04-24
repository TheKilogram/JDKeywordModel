def generate_training_data(job_descriptions, keywords):
    training_data = []

    for job_desc in job_descriptions:
        entities = []
        for keyword, label in keywords.items():
            for match in re.finditer(re.escape(keyword), job_desc, re.IGNORECASE):
                start, end = match.span()
                entities.append((start, end, label))
        
        # Clean and remove overlapping entities
        entities = remove_overlapping_entities(entities)
        entities = check_entity_alignment(job_desc, entities)  # Check and clean alignment
        
        if entities:
            training_data.append((job_desc, {"entities": entities}))
    return training_data
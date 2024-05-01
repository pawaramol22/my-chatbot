import random
from app.chat.redis import client


def random_component_by_score(component_type, component_map):
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError("Not valid component type")
    
    values = client.hgetall(f"{component_type}_score_values")
    counts = client.hgetall(f"{component_type}_score_count")

    avg_scores = {}
    names = component_map.keys()
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg = score/count

        # To give components some chance of selection if never being used
        avg_scores[name] = max(avg, 0.1)

    # Weighted randon selection
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative_score = 0
    for name, score in avg_scores.items():
        cumulative_score += score
        if random_val <= cumulative_score:
            return name


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:

    score = min(max(score, 0), 1)
    print(score, llm, retriever, memory)
    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_count", llm, 1)

    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_count", retriever, 1)

    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_count", memory, 1)


def get_scores():
    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [score1, score2],
                'chatopenai-4': [score3, score4]
            },
            'retriever': { 'pinecone_store': [score5, score6] },
            'memory': { 'persist_memory': [score7, score8] }
        }
    """

    aggregate = {"llm": {}, "retriever": {}, "memory": {}}

    for component_type, _ in aggregate.items():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_count")

        names = values.keys()

        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg = score/count

            aggregate[component_type][name] = [avg]

    return aggregate

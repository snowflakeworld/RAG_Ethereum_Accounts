from pinecone import Pinecone, ServerlessSpec
import json

# Define the name and dimension of your vector index
index_name = "my-ethereum-index"
dimension = 1024  # Replace with the dimension size of your embeddings

# Initialize Pinecone with your API key
pc = Pinecone(
    api_key="pcsk_718FQp_J3iprBXXEFRNzGiSMLuB9JNMji6VUDDDhmTh9zw7Ak3JyeF8XP3BNTh5VJek9Z"
)

# Create the index
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=dimension,
        vector_type="dense",
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Connect to the created index
index = pc.Index(index_name)


def upsert_records(id, text, cypher, type):
    index.upsert_records(
        "__default__",
        [{"_id": id, "text": text, "cypher": cypher, "type": type}],
    )


def search_records(prompt):
    results = index.search(
        namespace="__default__",
        query={"inputs": {"text": prompt}, "top_k": 1},
        fields=["text", "cypher", "type"],
    )

    hits = results["result"]["hits"]

    if len(hits) == 0:
        return None

    relevant_record = hits[0]
    id = relevant_record["_id"]
    score = relevant_record["_score"]
    text = relevant_record["fields"]["text"]
    cypher = relevant_record["fields"]["cypher"]
    type = relevant_record["fields"]["type"]

    print(id, score, text, cypher, type)

    return (id, score, text, cypher, type)


def clear_db():
    index.delete(delete_all=True, namespace="__default__")


def construct_db():
    try:
        with open("testcases.json", "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")

    for i in range(len(data)):
        text = data[i]["text"]
        cypher = data[i]["cypher"]
        type = data[i]["type"]

        upsert_records(f"sql#{i + 1}", text, cypher, type)


# construct_db()
# clear_db()
search_records(
    "What's the total count of transactions sent from account 0x121212121212121"
)

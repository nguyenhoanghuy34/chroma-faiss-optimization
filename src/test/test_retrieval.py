from src.retrieval.retriever import retrieve


def test_retrieval():

    query = """
    Người sử dụng lao động có được giữ giấy tờ tùy thân của người lao động không?
    """


    results = retrieve(query)


    for i, doc in enumerate(results["documents"][0]):

        print("=" * 50)

        print(f"Result {i + 1}")

        print(doc)

        print("\nMetadata:")

        print(
            results["metadatas"][0][i]
        )


if __name__ == "__main__":

    test_retrieval()
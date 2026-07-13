from src.retrieval.retriever import retrieve



def test_retrieval():


    query = """
    Người lao động có quyền đơn phương chấm dứt hợp đồng lao động mà không cần báo trước trong những trường hợp nào?
    """



    results = retrieve(
        query
    )



    for i, result in enumerate(results):


        print(
            "=" * 70
        )


        print(
            f"RESULT {i+1}"
        )


        print(
            "ID:",
            result["id"]
        )


        print(
            "Distance:",
            result["distance"]
        )


        print(
            "\nMetadata:"
        )


        print(
            result["metadata"]
        )


        print(
            "\nContent:"
        )


        print(
            result["content"]
        )



        print()
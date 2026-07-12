import os
import json
import re

from config import LABOR_LAW_CLEAN_TXT_PATH


OUTPUT_DIR = os.path.join(
    os.getcwd(),
    "Dataset",
    "data",
    "processed"
)

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "labor_law_chunks.json"
)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_structure(text):
    """
    Tách theo Điều
    """

    articles = re.split(
        r"(?=Điều\s+\d+\.)",
        text
    )

    return [
        x.strip()
        for x in articles
        if x.strip()
    ]


def extract_chapter(text):
    """
    Lấy chương gần nhất phía trước Điều
    """

    chapter_pattern = re.search(
        r"(Chương\s+[IVXLCDM]+.*?)(?=Điều\s+\d+\.)",
        text,
        re.DOTALL
    )

    if chapter_pattern:
        return chapter_pattern.group(1).strip()

    return None


def extract_article(article_text):

    match = re.search(
        r"(Điều\s+\d+\..*?)(?=\n\d+\.\s|$)",
        article_text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return article_text.strip()


def split_paragraph(article_text):

    paragraphs = re.split(
        r"(?=\n\d+\.\s)",
        article_text
    )

    return [
        p.strip()
        for p in paragraphs
        if p.strip()
    ]


def split_points(paragraph):

    points = re.split(
        r"(?=\n[a-zđ]\))",
        paragraph
    )

    return [
        p.strip()
        for p in points
        if re.match(r"[a-zđ]\)", p.strip())
    ]


def group_points(points):

    """
    Chia điểm:
    - không ít hơn 2
    - không quá 3 điểm/chunk
    """

    result = []

    size = len(points)


    if size <= 3:
        return [points]


    index = 0


    while index < size:

        remain = size - index


        if remain <= 3:
            group_size = remain

        elif remain % 3 == 1:
            group_size = 2

        else:
            group_size = 3


        result.append(
            points[index:index+group_size]
        )

        index += group_size


    return result



def create_chunk(
        chapter,
        article,
        paragraph,
        points
):

    content = []


    if chapter:
        content.append(chapter)


    content.append(article)


    if paragraph:
        content.append(paragraph)


    if points:

        content.extend(points)


    return "\n".join(content)



def chunker():

    """
    Main function gọi từ main.py
    """


    text = read_file(
        LABOR_LAW_CLEAN_TXT_PATH
    )


    articles = split_structure(text)


    chunks = []


    chunk_id = 0


    current_chapter = None


    for article_text in articles:


        chapter = extract_chapter(
            article_text
        )


        if chapter:
            current_chapter = chapter


        article = extract_article(
            article_text
        )


        paragraphs = split_paragraph(
            article
        )


        for paragraph_index, paragraph in enumerate(paragraphs):


            points = split_points(
                paragraph
            )


            # Không có điểm
            if not points:


                chunk_id += 1


                chunks.append({

                    "id":
                        f"labor_law_{chunk_id}",


                    "content":
                        create_chunk(
                            current_chapter,
                            article,
                            paragraph,
                            None
                        ),


                    "metadata": {

                        "law":
                            "Bộ luật Lao động 2019",

                        "chapter":
                            current_chapter,

                        "article":
                            article.split("\n")[0],

                        "paragraph":
                            paragraph_index + 1,

                        "has_points":
                            False
                    }
                })


            else:


                groups = group_points(
                    points
                )


                for group in groups:


                    chunk_id += 1


                    chunks.append({

                        "id":
                            f"labor_law_{chunk_id}",


                        "content":
                            create_chunk(
                                current_chapter,
                                article,
                                paragraph,
                                group
                            ),


                        "metadata": {


                            "law":
                                "Bộ luật Lao động 2019",


                            "chapter":
                                current_chapter,


                            "article":
                                article.split("\n")[0],


                            "paragraph":
                                paragraph_index + 1,


                            "points":
                                [
                                    p[:5]
                                    for p in group
                                ],


                            "has_points":
                                True

                        }
                    })



    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=4
        )


    print(
        f"Created {len(chunks)} chunks"
    )


    print(
        f"Saved: {OUTPUT_PATH}"
    )


    return chunks
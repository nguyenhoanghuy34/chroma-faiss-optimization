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


def split_articles(text):
    """
    Tách từng Điều
    """

    articles = re.split(
        r"(?=Điều\s+\d+\.)",
        text
    )

    return [
        a.strip()
        for a in articles
        if re.search(r"Điều\s+\d+\.", a)
    ]


def extract_chapter(article_text):
    """
    Lấy Chương phía trước Điều
    """

    match = re.search(
        r"(Chương\s+[IVXLCDM]+.*?)(?=\nĐiều\s+\d+\.)",
        article_text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return None



def clean_article(article_text):

    """
    Bỏ phần Chương ra khỏi Điều
    """

    article = re.sub(
        r"^Chương\s+[IVXLCDM]+.*?\n(?=Điều)",
        "",
        article_text,
        flags=re.DOTALL
    )

    return article.strip()



def split_paragraph(article_text):

    """
    Tách khoản:

    1.
    2.
    """

    parts = re.split(
        r"(?=\n\d+\.\s)",
        article_text
    )

    return [
        p.strip()
        for p in parts
        if p.strip()
    ]



def split_points(paragraph):

    """
    Tách điểm:

    a)
    b)
    c)
    """

    points = re.split(
        r"(?=\n[a-zđ]\))",
        paragraph
    )


    return [
        p.strip()
        for p in points
        if re.match(
            r"^[a-zđ]\)",
            p.strip()
        )
    ]



def group_points(points):

    """
    Mỗi chunk:
    - 2 đến 3 điểm
    """

    if len(points) <= 3:
        return [points]


    result = []

    index = 0


    while index < len(points):

        remain = len(points) - index


        if remain == 4:
            size = 2

        elif remain > 3:
            size = 3

        else:
            size = remain


        result.append(
            points[index:index+size]
        )

        index += size


    return result



def build_content(
        chapter,
        article,
        paragraph,
        points=None
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



def create_chunk(
        chunks,
        counter,
        content,
        chapter,
        article,
        paragraph,
        points
):

    chunks.append({

        "id":
            f"labor_law_{counter}",


        "content":
            content,


        "metadata": {

            "law":
                "Bộ luật Lao động 2019",

            "chapter":
                chapter,

            "article":
                article.split("\n")[0],

            "paragraph":
                paragraph.split("\n")[0]
                if paragraph and re.match(r"^\d+\.", paragraph)
                else None,

            "points":
                [
                    p[:2]
                    for p in points
                ]
                if points
                else None,

            "has_points":
                bool(points)
        }
    })



def chunker():

    text = read_file(
        LABOR_LAW_CLEAN_TXT_PATH
    )


    articles = split_articles(text)


    chunks = []

    chunk_id = 0

    current_chapter = None


    for raw_article in articles:


        chapter = extract_chapter(
            raw_article
        )


        if chapter:
            current_chapter = chapter



        article = clean_article(
            raw_article
        )


        paragraphs = split_paragraph(
            article
        )


        for paragraph in paragraphs:


            points = split_points(
                paragraph
            )


            # =====================
            # Không có điểm
            # =====================

            if not points:


                chunk_id += 1


                create_chunk(
                    chunks,
                    chunk_id,
                    build_content(
                        current_chapter,
                        article,
                        paragraph
                    ),
                    current_chapter,
                    article,
                    paragraph,
                    None
                )



            # =====================
            # Có điểm
            # =====================

            else:


                groups = group_points(
                    points
                )


                for group in groups:


                    chunk_id += 1


                    create_chunk(
                        chunks,
                        chunk_id,
                        build_content(
                            current_chapter,
                            article,
                            paragraph,
                            group
                        ),
                        current_chapter,
                        article,
                        paragraph,
                        group
                    )



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
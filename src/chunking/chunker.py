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


TEMP_TREE_PATH = os.path.join(
    OUTPUT_DIR,
    "labor_law_tree.json"
)


OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "labor_law_chunks.json"
)



LAW_NAME = "Bộ luật Lao động 2019"



# ===============================
# READ
# ===============================


def read_file(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()



# ===============================
# CLEAN
# ===============================


def clean_lines(text):

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:

            lines.append(line)


    return lines



# ===============================
# PARSE TREE
# ===============================


def parse_structure(lines):

    tree = []


    chapter = None
    article = None


    for line in lines:


        # Chương

        if re.match(
            r"^Chương\s+[IVXLCDM]+",
            line
        ):

            chapter = {

                "title": line,

                "articles": []

            }


            tree.append(
                chapter
            )


            article = None



        # Điều

        elif re.match(
            r"^Điều\s+\d+\.",
            line
        ):


            if chapter is None:

                chapter = {

                    "title": "",

                    "articles": []

                }


                tree.append(
                    chapter
                )



            article = {

                "title": line,

                "paragraphs": [],

                "content": []

            }


            chapter["articles"].append(
                article
            )



        # Khoản

        elif re.match(
            r"^\d+\.",
            line
        ):


            if article:


                paragraph = {

                    "title": line,

                    "points": []

                }


                article["paragraphs"].append(
                    paragraph
                )



        # Điểm

        elif re.match(
            r"^[a-zđ]\)",
            line
        ):


            if article and article["paragraphs"]:


                article["paragraphs"][-1]["points"].append(
                    line
                )



        # Nội dung tiếp theo

        else:


            if article:


                if article["paragraphs"]:


                    last = article["paragraphs"][-1]


                    if last["points"]:

                        last["points"][-1] += " " + line


                    else:

                        last["title"] += " " + line



                else:

                    article["content"].append(
                        line
                    )


    return tree



# ===============================
# SAVE TREE
# ===============================


def save_tree(tree):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    with open(
        TEMP_TREE_PATH,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            tree,
            f,
            ensure_ascii=False,
            indent=4
        )



# ===============================
# METADATA STANDARD
# ===============================


def create_metadata(
        chapter="",
        article="",
        paragraph="",
        points=None,
        level=""
):


    if points is None:

        points = []



    return {


        "chapter":
            chapter,


        "article":
            article,


        "paragraph":
            paragraph,


        "points":
            " | ".join(points),


        "level":
            level

    }



# ===============================
# CHUNK UTIL
# ===============================


def split_children(items):


    result = []


    for i in range(
        0,
        len(items),
        3
    ):

        result.append(
            items[i:i+3]
        )


    return result



def build_content(
        chapter,
        article,
        children
):


    content = []


    if chapter:

        content.append(
            chapter
        )


    content.append(
        article
    )


    content.extend(
        children
    )


    return "\n".join(content)



# ===============================
# CHUNK ARTICLE
# ===============================


def chunk_article(
        chunks,
        counter,
        chapter,
        article
):


    title = article["title"]



    # Điều không có khoản

    if not article["paragraphs"]:


        counter += 1


        chunks.append({

            "id":
                f"labor_law_{counter}",


            "content":
                build_content(
                    chapter,
                    title,
                    article["content"]
                ),


            "metadata":
                create_metadata(
                    chapter=chapter,
                    article=title,
                    level="article"
                )

        })


        return counter



    paragraphs = article["paragraphs"]



    has_points = any(

        len(x["points"]) > 0

        for x in paragraphs

    )



    # Có khoản nhưng không có điểm

    if not has_points:


        groups = split_children(

            [
                x["title"]

                for x in paragraphs

            ]

        )


        for group in groups:


            counter += 1


            chunks.append({

                "id":
                    f"labor_law_{counter}",


                "content":
                    build_content(
                        chapter,
                        title,
                        group
                    ),


                "metadata":
                    create_metadata(
                        chapter=chapter,
                        article=title,
                        paragraph=" | ".join(group),
                        level="paragraph"
                    )

            })



    # Có điểm

    else:


        for paragraph in paragraphs:


            points = paragraph["points"]



            if not points:


                counter += 1


                chunks.append({

                    "id":
                        f"labor_law_{counter}",


                    "content":
                        build_content(
                            chapter,
                            title,
                            [
                                paragraph["title"]
                            ]
                        ),


                    "metadata":
                        create_metadata(
                            chapter=chapter,
                            article=title,
                            paragraph=paragraph["title"],
                            level="paragraph"
                        )

                })


                continue



            groups = split_children(
                points
            )



            for group in groups:


                counter += 1


                chunks.append({

                    "id":
                        f"labor_law_{counter}",


                    "content":
                        build_content(
                            chapter,
                            title,
                            [
                                paragraph["title"],
                                *group
                            ]
                        ),


                    "metadata":
                        create_metadata(
                            chapter=chapter,
                            article=title,
                            paragraph=paragraph["title"],
                            points=group,
                            level="point"
                        )

                })



    return counter



# ===============================
# MAIN
# ===============================


def chunker():


    text = read_file(
        LABOR_LAW_CLEAN_TXT_PATH
    )


    lines = clean_lines(
        text
    )


    tree = parse_structure(
        lines
    )


    save_tree(
        tree
    )



    chunks = []


    counter = 0



    for chapter in tree:


        for article in chapter["articles"]:


            counter = chunk_article(

                chunks,

                counter,

                chapter["title"],

                article

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
        "Total chunks:",
        len(chunks)
    )


    print(
        "Saved:",
        OUTPUT_PATH
    )


    return chunks
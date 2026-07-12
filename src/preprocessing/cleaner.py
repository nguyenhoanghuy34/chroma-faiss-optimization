import re


def remove_header(text):
    """
    Xóa phần thông tin đầu văn bản:
    QUỐC HỘI
    CỘNG HÒA...
    Bộ luật số...
    """

    match = re.search(
        r"Chương I",
        text
    )

    if match:
        text = text[match.start():]

    return text



def normalize_space(text):

    # bỏ khoảng trắng giữa các dòng
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # gom nhiều dòng trống thành 1 dòng
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text



def clean_lines(text):

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)



def add_article_marker(text):

    """
    Thêm marker trước Điều
    để chunk sau này dễ hơn

    Điều 1.
    Điều 2.
    """

    text = re.sub(
        r"(Điều\s+\d+\.)",
        r"\n---ARTICLE---\n\1",
        text
    )

    return text


def add_structure_marker(text):

    # Điều
    text = re.sub(
        r"(Điều\s+\d+\.)",
        r"\n---ARTICLE---\n\1",
        text
    )


    # Khoản: 1. 2. 3. ở đầu dòng
    text = re.sub(
        r"(?m)^(\d+\.)\s",
        r"\n---CLAUSE---\n\1 ",
        text
    )


    # Điểm: a) b) c) đ)
    text = re.sub(
        r"(?m)^([a-zđ])\)\s",
        r"\n---POINT---\n\1) ",
        text
    )


    return text


def clean_text(text):

    # 1. Xóa header
    text = remove_header(text)

    # 2. Chuẩn hóa khoảng trắng
    text = normalize_space(text)

    # 3. Xóa dòng rác
    text = clean_lines(text)

    # 4. Thêm marker cấu trúc
    # text = add_structure_marker(text)

    return text.strip()
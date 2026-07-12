import re


def clean_text(text):

    # bỏ khoảng trắng thừa
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # gom các dòng trống liên tiếp
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    # bỏ khoảng trắng đầu cuối mỗi dòng
    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            lines.append(line)

    text = "\n".join(lines)

    return text.strip()
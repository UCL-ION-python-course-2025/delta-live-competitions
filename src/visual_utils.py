def wrap_text(text, font, max_width):
    texts = text.replace("\t", "    ").split("\n")
    lines = []

    for text in texts:
        text = text.rstrip(" ")

        if not text:
            lines.append("")
            continue

        # Preserve leading spaces in all cases.
        a = len(text) - len(text.lstrip(" "))

        # At any time, a is the rightmost known index you can legally split a line. I.e. it's legal
        # to add text[:a] to lines, and line is what will be added to lines if
        # text is split at a.
        a = text.index(" ", a) if " " in text else len(text)
        line = text[:a]

        while a + 1 < len(text):
            # b is the next legal place to break the line, with `bline`` the
            # corresponding line to add.
            if " " not in text[a + 1 :]:
                b = len(text)
                bline = text

            else:
                # Lines may be split at any space character that immediately follows a non-space
                # character.
                b = text.index(" ", a + 1)
                while text[b - 1] == " ":
                    if " " in text[b + 1 :]:
                        b = text.index(" ", b + 1)
                    else:
                        b = len(text)
                        break
                bline = text[:b]

            bline = text[:b]

            if font.size(bline)[0] <= max_width:
                a, line = b, bline

            else:
                lines.append(line)
                text = text[a:].lstrip(" ")
                a = text.index(" ", 1) if " " in text[1:] else len(text)
                line = text[:a]

        if text:
            lines.append(line)

    return lines

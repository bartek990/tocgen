SOURCE_PATH = "./doc/03_media.md"                                # Plik źródłowy
OUTPUT_PATH = "./doc/toc_03_media.md"                      # Plik wyjściowy
TOC_LINK = "↑[Table of Contents](#table-of-contents)↑"  # Link do spisu treści
TOC_TITLE = "## Table of Contents"                      # Nagłówek spisu treści

def clean_toc_links(lines: list[str]) -> list[str]:
    """
    Returns a list of strings without toc links
    :param lines:
    :return:
    """
    return [line if TOC_LINK not in line else '' for line in lines]

def insert_toc_links(lines: list[str]) -> list[str]:
    """
    Returns a list of strings with toc links at the end of chapters
    :param lines:
    :return:
    """
    return [TOC_LINK + '\n' + line if line.startswith('# ') or line.startswith('## ') else line for line in lines]

def make_list_of_chapters(lines: list[str]) -> list[str]:
    """
    Returns a list of chapters
    :param lines:
    :return:
    """
    return [line for line in lines if line.startswith('# ') or line.startswith('## ')]

def main():
    # Open file
    with open(SOURCE_PATH, "r") as f:
        lines = f.readlines()

    # Remove existing TOC_LINKs, add new ones and make a list of chapters
    # new_lines = []
    # chapters = []

    chapters = make_list_of_chapters(lines)
    lines = clean_toc_links(lines)
    lines = insert_toc_links(lines)

    # for line in lines:
    #     # Remove TOC_LINK if present
    #     # if TOC_LINK in line or TOC_TITLE in line:
    #     #     line = ''
    #     #     continue
    #     # Adding TOC before every chapter
    #     if line.startswith('# ') or line.startswith('## '):
    #         # Append line to chapters list
    #         chapters.append(line)
    #         line = TOC_LINK + "\n" + line
    #
    #     new_lines.append(line)

    table_of_contents = []
    table_of_contents.append(TOC_TITLE + '\n\n')

    # Make table of contents
    for chapter in chapters:
        chapter = chapter.replace('\n', '')
        chapter = chapter.replace('# ', '')
        chapter = chapter.replace('#', '\t')

        link = chapter.lower()
        link = link.replace('.', '')
        link = link.replace('\t', '')
        link = link.replace(' ', '-')
        link = '#' + link

        chapter = chapter.replace('. ', '. [')
        chapter = chapter + f"]({link})\n"
        if not chapter.startswith('\t'):
            chapter = chapter + '\n'
        table_of_contents.append(chapter)

    table_of_contents.append('\n')

    new_file = table_of_contents + lines

    # Write a new file
    with open(OUTPUT_PATH, 'w') as f:
        f.writelines(new_file)

if __name__ == '__main__':
    main()

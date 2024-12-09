SOURCE_PATH = "./doc/03_media.md"                                # Plik źródłowy
OUTPUT_PATH = "./doc/toc_03_media.md"                      # Plik wyjściowy
TOC_LINK = "↑[Table of Contents](#table-of-contents)↑"  # Link do spisu treści
TOC_TITLE = "## Table of Contents"                      # Nagłówek spisu treści

def main():
    # Open file
    with open(SOURCE_PATH, "r") as f:
        lines = f.readlines()

    # Remove existing TOC_LINKs, add new ones and make a list of chapters
    new_lines = []
    chapters = []

    for line in lines:
        # Remove TOC_LINK if present
        if TOC_LINK in line or TOC_TITLE in line:
            line = ''
            continue
        # Adding TOC before every chapter
        if line.startswith('# ') or line.startswith('## '):
            # Append line to chapters list
            chapters.append(line)
            line = TOC_LINK + "\n" + line

        new_lines.append(line)

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

    new_file = table_of_contents + new_lines

    # Write a new file
    with open(OUTPUT_PATH, 'w') as f:
        f.writelines(new_file)

if __name__ == '__main__':
    main()

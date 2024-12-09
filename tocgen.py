import sys
from dataclasses import dataclass, field

TOC_LINK = "↑[Table of Contents](#table-of-contents)↑"  # Link do spisu treści
TOC_TITLE = "## Table of Contents"                      # Nagłówek spisu treści

@dataclass(order=True, frozen=True)
class Chapter:
    line: str = field(repr=False)
    tag: str = field(init=False)
    number: str = field(init=False)
    title: str = field(init=False)

    def __post_init__(self):
        rest, title = self.line.split('. ', 1)
        tag, number = rest.split(' ')

        object.__setattr__(self, 'tag', tag)
        object.__setattr__(self, 'number', number)
        object.__setattr__(self, 'title', title.replace('\n', ''))

    def get_link(self) -> str:
        """
        Returns a link to header - a chapter line
        :return:
        """
        # todo: find better solution for replacing special chars with '-'
        return (f'\n{(self.tag.count('#') - 1) * "\t"}{self.number}. '
                f'[{self.title}](#{self.number}-{self.title.lower().replace(' ', '-')})\n'.replace(':', ''))


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
    lines = [TOC_LINK + '\n' + line if line.startswith('# ') or line.startswith('## ') else line for line in lines]
    lines.append(TOC_LINK)
    return lines


def make_list_of_chapters(lines: list[str]) -> list[str]:
    """
    Returns a list of chapters
    :param lines:
    :return:
    """
    return [line for line in lines if line.startswith('# ') or line.startswith('## ')]


def make_table_of_contents(chapters: list[str]):
    """
    Returns a table of content from chapters list
    :param chapters:
    :return:
    """
    table_of_contents = [TOC_TITLE + '\n\n',]

    # Make table of contents
    for chapter in chapters:
        chapter = Chapter(chapter)
        table_of_contents.append(chapter.get_link())

    table_of_contents.append('\n')
    return table_of_contents


def parse_toc(source_path: str, output_path: str) -> None:
    """
    Loads file from source_path, adds table of contents and saves new file on output_path
    :param source_path:
    :param output_path:
    """
    # Open file
    with open(source_path, "r") as f:
        lines = f.readlines()

    chapters = make_list_of_chapters(lines)

    lines = clean_toc_links(lines)
    lines = insert_toc_links(lines)

    table_of_contents = make_table_of_contents(chapters)

    new_file = table_of_contents + lines

    # Write a new file
    with open(output_path, 'w') as f:
        f.writelines(new_file)


def main():
    match sys.argv[1]:
        case 'parse':
            source_path = sys.argv[2]
            output_path = sys.argv[3]

            print(f'Plik źródłowy: {source_path}\nPlik wyjściowy: {output_path}')
            parse_toc(source_path, output_path)
            print(f'Pomyślnie zapisano')

        case '--help':
            print('Aby dodać spis treści do pliku MarkDown użyj:\ntocgen.py parse plik_źródłowy plik_wynikowy')

        case '--test':
            chapter = Chapter('## 046. Defining Enums\n')

            print(chapter)
            print(chapter.get_link())

        case _:
            print(f'Brak komendy "{sys.argv[1]}".\nAby uzyskać pomoc wpisz "tocgen.py --help"')


if __name__ == '__main__':
    main()

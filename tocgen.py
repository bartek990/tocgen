import sys
from dataclasses import dataclass, field

TOC_LINK = "↑[Table of Contents](#table-of-contents)↑"  # Link do spisu treści
TOC_TITLE = "## Table of Contents"                      # Nagłówek spisu treści
eg_lines = [
                '# 05. Enums Unleashed: Pattern Matching and Options\n',
                '\n', '↑[Table of Contents](#table-of-contents)↑\n',
                '## 046. Defining Enums\n',
                '\n',
                '```rust\n',
                '#[derive(Debug)]\n',
                'enum Media {\n',
                '    Book {title: String, author: String},\n',
                '    Movie {title: String, director: String},\n',
                '    Audiobook {title: String}\n',
                '}\n',
                '\n',
                'fn print_media(media: Media) {\n',
                '    println!("{:#?}", media);\n',
                '}\n',
                '\n',
                'fn main() {\n',
                '    let audiobook = Media::Audiobook {\n',
                '        title: String::from("An Audiobook"),\n',
                '    };\n',
                '\n',
                '    print_media(audiobook);\n',
                '}\n',
                '```\n',
                '\n',
                '↑[Table of Contents](#table-of-contents)↑\n',]

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
                f'[{self.title}](#{self.number}-{self.title.lower().replace(' ', '-')})\n'
                .replace(':', ''))


class TableOfContents:
    def __init__(self, lines: list[str]):
        self._title: str = TOC_TITLE + '\n\n'
        self._content: list[Chapter] = []
        self._list_of_chapters: list[str] = [line for line in lines if line.startswith('# ') or line.startswith('## ')]
        self._make_table_of_contents()

    def __repr__(self) -> str:
        return f'<TableOfContent: len={len(self)}>'

    def __len__(self) -> int:
        return len(self._content)

    def add_chapter(self, chapter: Chapter) -> None:
        """
        Adds a chapter to table of content.
        :param chapter: *Chapter*
        """
        self._content.append(chapter)

    def get_toc(self) -> list[str]:
        """
        Returns table of content as list of strings or empty list
        :return: *list[str]* | *[]*
        """
        if len(self) > 0:
            return [self._title] + [con.get_link() for con in self._content]
        return []

    def _make_table_of_contents(self) -> None:
        """
        Generates table of contents based on *self._list_of_chapters* and saves it in *self._content.
        """
        # Make table of contents
        for chapter in self._list_of_chapters:
            self.add_chapter(Chapter(chapter))


class Document:
    def __init__(self, lines: list[str]):
        self._lines: list[str] = lines
        self.toc_link = TOC_LINK

    def __len__(self) -> int:
        return len(self._lines)

    def __repr__(self) -> str:
        return f'<Document: len={len(self)}>'

    def print_document(self) -> None:
        for line in self._lines:
            print(line, end='')


def clean_toc_links(lines: list[str]) -> list[str]:
    """
    Returns a list of strings without toc links
    :param lines:
    :return:
    """
    return [line if TOC_LINK not in line else '' for line in lines]


def remove_lines(lines: list[str], line_to_remove: str):
    return [line for line in lines if line_to_remove not in line]


def insert_toc_links(lines: list[str]) -> list[str]:
    """
    Returns a list of strings with toc links at the end of chapters
    :param lines:
    :return:
    """
    lines = [TOC_LINK + '\n' + line if line.startswith('# ') or line.startswith('## ') else line for line in lines]
    lines.append(TOC_LINK)
    return lines


def parse_toc(source_path: str, output_path: str) -> None:
    """
    Loads file from source_path, adds table of contents and saves new file on output_path
    :param source_path:
    :param output_path:
    """
    # Open file
    with open(source_path, "r") as f:
        lines = f.readlines()

    toc = TableOfContents(lines)

    # todo: toclink chapter line join error
    lines = clean_toc_links(lines)
    lines = insert_toc_links(lines)

    new_file = toc.get_toc() + lines

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
            document = Document(remove_lines(eg_lines, TOC_LINK))
            document.print_document()
            print(len(eg_lines))
            print(document)

        case _:
            print(f'Brak komendy "{sys.argv[1]}".\nAby uzyskać pomoc wpisz "tocgen.py --help"')


if __name__ == '__main__':
    main()

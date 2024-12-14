from .toc import TableOfContents

# todo: move TOC_LINK to config file
TOC_LINK = "↑[Table of Contents](#table-of-contents)↑"  # Link do spisu treści
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
                '↑[Table of Contents](#table-of-contents)↑\n',
]

# todo: remove
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

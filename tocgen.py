import sys

from docparts import Chapter, Document, parse_toc, TOC_LINK


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
            document = Document.load_from_file('./doc/03_media.md')
            document.remove_lines(TOC_LINK)
            # document.print_document()
            # # print(len(eg_lines))
            # print(document)

            header = '## 046. Defining Enums\n'
            # header = 12
            chapter = Chapter()
            chapter.header = header
            # del chapter.header
            print(chapter.get_link())

        case _:
            print(f'Brak komendy "{sys.argv[1]}".\nAby uzyskać pomoc wpisz "tocgen.py --help"')


if __name__ == '__main__':
    main()

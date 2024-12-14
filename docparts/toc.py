from .chapter import Chapter

TOC_TITLE = "## Table of Contents"

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
            self.add_chapter(Chapter.from_header(chapter))

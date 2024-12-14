class Chapter:
    def __init__(self):
        self._header: str | None = None
        self._body: str | None = None
        self._footer: str | None = None
        self._tag: str | None = None
        self._number: str | None = None
        self._title: str | None = None

    def __repr__(self):
        return (f'<Chapter: header="{self.header}", '
                f'body_len={None if self.body is None else len(self.body)}, '
                f'footer={False if self._footer is None else True}>')

    @property
    def header(self) -> str | None:
        return self._header

    @header.setter
    def header(self, text: str) -> None:
        if not self._validate_header(text):
            raise AttributeError

        text = text.replace('\n', '')
        text, self._title = text.split('. ', 1)
        self._tag, self._number = text.split(' ')
        self._header = f'{self.tag} {self.number}. {self.title}'

    @header.deleter
    def header(self) -> None:
        self._header = None
        self._body = None
        self._tag = None
        self._number = None
        self._title = None

    @property
    def body(self) -> str | None:
        return self._body

    @property
    def footer(self) -> str | None:
        return self._footer

    @property
    def tag(self) -> str | None:
        return self._tag

    @property
    def number(self) -> str | None:
        return self._number

    @property
    def title(self) -> str | None:
        return self._title

    @classmethod
    def from_header(cls, header: str):
        chapter = cls.__new__(cls)
        chapter.__init__()
        chapter.header = header
        return chapter

    @classmethod
    def _validate_header(cls, header) -> bool:
        if not isinstance(header, str):
            return False

        if '#' not in header:
            return False

        if '. ' not in header:
            return False

        return True

    def get_link(self) -> str:
        """
        Returns a link to header - a chapter line
        :return:
        """
        # todo: find better solution for replacing special chars with '-'
        return (f'\n{(self.tag.count('#') - 1) * "\t"}{self.number}. '
                f'[{self.title}](#{self.number}-{self.title.lower().replace(' ', '-')})\n'
                .replace(':', ''))

class Document:
    def __init__(self):
        self._lines: list[str] = []

    def __len__(self) -> int:
        return len(self._lines)

    def __repr__(self) -> str:
        return f'<Document: len={len(self)}>'

    def add_lines(self, lines: list[str]) -> None:
        self._lines.extend(lines)

    def print_document(self) -> None:
        for line in self._lines:
            print(line, end='')

    def remove_lines(self, line_to_remove: str):
        self._lines = [line for line in self._lines if line_to_remove not in line]

    @classmethod
    def load_from_file(cls, source_path: str):
        with open(source_path, 'r') as file:
            lines = file.readlines()

        doc = cls.__new__(cls)
        cls.__init__(doc)
        doc.add_lines(lines)
        return doc

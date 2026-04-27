import ast


def detect_missing_docstring(
    node: ast.AsyncFunctionDef
    | ast.ClassDef
    | ast.FunctionDef
    | ast.Module,
) -> None:
    if ast.get_docstring(node) is None:
        entity = getattr(node, 'name', 'module')
        print(f'{entity} is missing a docstring')


class DocstringVisitor(ast.NodeVisitor):
    def _visit_helper(
        self,
        node: ast.AsyncFunctionDef
        | ast.ClassDef
        | ast.FunctionDef
        | ast.Module,
    ) -> None:
        detect_missing_docstring(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> None:
        self._visit_helper(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_helper(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_helper(node)

    def visit_Module(self, node: ast.Module) -> None:
        self._visit_helper(node)


if __name__ == '__main__':
    from pathlib import Path

    file = Path(__file__).parent / 'greet.py'
    source_code = file.read_text()
    tree = ast.parse(source_code)

    visitor = DocstringVisitor()
    tree = visitor.visit(tree)

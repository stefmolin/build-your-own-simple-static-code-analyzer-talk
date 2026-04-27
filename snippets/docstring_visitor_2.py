import ast


class DocstringVisitor(ast.NodeVisitor):
    def __init__(self, module_name: str) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.module_name: str = module_name

    def _detect_missing_docstring(
        self,
        node: ast.AsyncFunctionDef
        | ast.ClassDef
        | ast.FunctionDef
        | ast.Module,
    ) -> None:
        if ast.get_docstring(node) is None:
            entity = '.'.join(self.stack)
            print(f'{entity} is missing a docstring')

    def _visit_helper(
        self,
        node: ast.AsyncFunctionDef
        | ast.ClassDef
        | ast.FunctionDef
        | ast.Module,
    ) -> None:
        self.stack.append(
            getattr(node, 'name', self.module_name)
        )
        self._detect_missing_docstring(node)
        self.generic_visit(node)
        self.stack.pop()

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

    visitor = DocstringVisitor(file.stem)
    tree = visitor.visit(tree)

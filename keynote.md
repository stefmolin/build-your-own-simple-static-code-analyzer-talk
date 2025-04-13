---
title: Build Your Own (Simple) Static Code Analyzer
author: Stefanie Molin
description: In this keynote, Stefanie Molin walks you through the process of creating a simple static code analyzer in Python using a data structure called an abstract syntax tree, which represents your code's structure and allows you to access its components in order to perform checks.
published: TODO
last_modified: TODO
g_tag: G-25389D1SR4
keywords: [ast docstring abstract-syntax-tree docstring-generator numpydoc]
og:
  image:
    url: TODO
    width: 1200
    height: 800
    alt:
  locale: en_US
  site_name: Stefanie Molin
  title: "{title} | {author}"
  type: website
  url: https://stefaniemolin.com/TODO/
twitter:
  card: summary
  site: "@StefanieMolin"
  creator: "@StefanieMolin"
page_title: "{title} slides | {author}"
rel_me:
  - https://github.com/stefmolin
  - https://linkedin.com/in/stefanie-molin/
  - https://x.com/StefanieMolin
  - https://bsky.app/profile/stefaniemolin.com
license:
  name: CC BY-NC-SA 4.0
  link: https://creativecommons.org/licenses/by-nc-sa/4.0/
website: stefaniemolin.com
favicon: /favicon
intro_slide:
  title: Build Your Own (Simple) Static Code Analyzer
reveal:
  version: 5.1.0
  theme: simple
  config:
    controls: false
    hash: true
    history: true
    pdfSeparateFragments: false
highlightjs:
  version: 11.9.0
  theme: stackoverflow-light
fontawesome:
  version: 6.7.2
---

[id=bio]
## Bio

- 👩🏻‍💻 Software engineer at Bloomberg in NYC
- ✨ Core developer of [numpydoc](https://github.com/numpy/numpydoc) and creator of [numpydoc's pre-commit hook](https://numpydoc.readthedocs.io/en/latest/validation.html)
- ✍ Author of "[Hands-On Data Analysis with Pandas](https://stefaniemolin.com/books/Hands-On-Data-Analysis-with-Pandas-2nd-edition/)"
- 🎓 Bachelor's in operations research from Columbia University
- 🎓 Master's in computer science (ML specialization) from Georgia Tech

---

## (1) Section 1

TODO: intro to the keynote and topic

Mention that the goal is to find missing docstrings and suggest templates for them based on the code

---

### (2) Example input file

`greet.py`

```python
class Greeter:
    def __init__(self, enthusiasm: int = 1) -> None:
        self.enthusiasm = enthusiasm

    def greet(self, name: str = 'World') -> str:
        return f'Hello, {name}{"!" * self.enthusiasm}'
```

---

### (3) Possible ways to do this

<ol>
  <li class="fragment fade-in" data-fragment-index="1">
    <span class="fragment strike" data-fragment-index="2">Manually (open each file and edit)</span>
    <span class="fragment fade-in" data-fragment-index="2">&ndash; tedious and error prone</span>
  </li>
  <li class="fragment fade-in" data-fragment-index="3">
    <span class="fragment strike" data-fragment-index="4">Regular expressions</span>
    <span class="fragment fade-in" data-fragment-index="4">&ndash; messy and hard to get right (edge cases, context, <i>etc.</i>)</span>
  </li>
  <li class="fragment fade-in" data-fragment-index="5">
    <span class="fragment strike" data-fragment-index="6">Script to import everything and check docstrings</span>
    <span class="fragment fade-in" data-fragment-index="6">&ndash; must be able to install codebase and its dependencies; slow</span>
  </li>
  <li class="fragment fade-in" data-fragment-index="7">
    <span>Static code analysis</span>
  </li>
</ol>

---

## Static code analysis

Analyze code **without** executing it

---

### Main benefits of static code analysis

<ul>
  <li class="fragment fade-in">
    Speed &ndash; can be <em>much</em> faster than dynamic code analysis
  </li>
  <li class="fragment fade-in">
    Portable &ndash; no need to install the codebase being analyzed or its dependencies
  </li>
</ul>

---

### Some open source examples may be familiar with

<ul>
  <li class="fragment fade-in">
    Linters and formatters like <code>ruff</code> (Rust) and <code>black</code> (Python)
  </li>
  <li class="fragment fade-in">
    Documentation tools like <code>sphinx</code> and the <code>numpydoc-validation</code> pre-commit hook
  </li>
  <li class="fragment fade-in">
    Automatic Python syntax upgrade tools like <code>pyupgrade</code>
  </li>
  <li class="fragment fade-in">
    Type checkers like <code>mypy</code>
  </li>
  <li class="fragment fade-in">
    Code security tools like <code>bandit</code>
  </li>
  <li class="fragment fade-in">
    Code and testing coverage tools like <code>vulture</code> and <code>coverage.py</code>
  </li>
  <li class="fragment fade-in">
    Testing frameworks that instrument your code or generate tests based on it like <code>hypothesis</code> and <code>pytest</code>
  </li>
</ul>

---

### How do you build a static code analyzer?

<p class="fragment fade-in-then-semi-out">It depends...</p>

<p class="fragment fade-in"><strong>Abstract Syntax Trees (ASTs)</strong> are a good place to start.</p>

---

## Abstract Syntax Tree (AST)

<ul>
  <li class="fragment fade-in">
    Represents of the structure of source code as a tree
  </li>
  <li class="fragment fade-in">
    Nodes in the tree are language constructs (<em>e.g.</em>, module, class, function)
  </li>
  <li class="fragment fade-in">
    Each node has a single parent (<em>e.g.</em>, a class is a child of a single module)
  </li>
  <li class="fragment fade-in">
    Parent nodes can have multiple children (<em>e.g.</em>, a class can have several methods)
  </li>
</ul>

---

[data-transition=slide-in fade-out]

Remember `greet.py`?

```python
class Greeter:
    def __init__(self, enthusiasm: int = 1) -> None:
        self.enthusiasm = enthusiasm

    def greet(self, name: str = 'World') -> str:
        return f'Hello, {name}{"!" * self.enthusiasm}'
```

---

[data-transition=slide-out fade-in]
<div class="center">
  <img width="650" src="media/full-ast.svg" alt="The AST for greet.py visualized with Graphviz">
  <br/>
  <small>The AST for <code>greet.py</code> visualized with Graphviz.</small>
</div>

---

## ASTs in Python

<ul>
  <li class="fragment fade-in">
    Created when compiling source code into byte code (necessary to run it)
  </li>
  <li class="fragment fade-in">
    Only syntactically-correct Python code can be parsed into an AST
  </li>
  <li class="fragment fade-in">
    Available in the standard library via the <code>ast</code> module
  </li>
</ul>

---

### Parsing Python source code into an AST

---

#### 1. Read in the source code

```pycon
>>> from pathlib import Path
>>> source_code = Path('greet.py').read_text()
```

---

#### 2. Parse it with the `ast` module

If the code is syntactically-correct, we get an AST back:

```
>>> import ast
>>> tree = ast.parse(source_code)
>>> print(type(tree))
&lt;class 'ast.Module'>
```

---

### Inspecting the AST

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    Use <code>ast.dump()</code> to display the AST:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    The root node is an <code>ast.Module</code> node:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    It contains everything else in its <code>body</code> attribute:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    The <code>greet.py</code> file first defines a class, named <code>Greeter</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    The <code>ast.ClassDef</code> node also contains the <code>body</code> of the <code>Greeter</code> class:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    The first entry is the <code>Greeter.__init__()</code> method:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="5">
    The <code>ast.FunctionDef</code> node includes information about the arguments:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="6">
    The <code>body</code> contains the AST representation of the function's code:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="7">
    The return annotation is stored in the <code>returns</code> attribute:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="8">
    The final entry is the <code>Greeter.greet()</code> method:
  </p>
</div>

<pre>
    <code data-trim class="language-pycon hide-line-numbers" data-line-numbers="1|2|3-51|4-5|6-53|7-8|9-16|17-24|25|26-53" data-fragment-index="0">
>>> print(ast.dump(tree, indent=2))
Module(
  body=[
    ClassDef(
      name='Greeter',
      body=[
        FunctionDef(
          name='__init__',
          args=arguments(
            args=[
              arg(arg='self'),
              arg(
                arg='enthusiasm',
                annotation=Name(id='int', ctx=Load()))],
            defaults=[
              Constant(value=1)]),
          body=[
            Assign(
              targets=[
                Attribute(
                  value=Name(id='self', ctx=Load()),
                  attr='enthusiasm',
                  ctx=Store())],
              value=Name(id='enthusiasm', ctx=Load()))],
          returns=Constant(value=None)),
        FunctionDef(
          name='greet',
          args=arguments(
            args=[
              arg(arg='self'),
              arg(
                arg='name',
                annotation=Name(id='str', ctx=Load()))],
            defaults=[
              Constant(value='World')]),
          body=[
            Return(
              value=JoinedStr(
                values=[
                  Constant(value='Hello, '),
                  FormattedValue(
                    value=Name(id='name', ctx=Load()),
                    conversion=-1),
                  FormattedValue(
                    value=BinOp(
                      left=Constant(value='!'),
                      op=Mult(),
                      right=Attribute(
                        value=Name(id='self', ctx=Load()),
                        attr='enthusiasm',
                        ctx=Load())),
                    conversion=-1)]))],
          returns=Name(id='str', ctx=Load()))])])
</code>
</pre>

---

## Detecting missing docstrings using the Python AST

<div class="r-stack r-stack-left">
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    We need to traverse the full AST (to account for nested functions and classes) and inspect each node's docstring with something like this:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    Only <code>ast.Module</code>, <code>ast.ClassDef</code>, <code>ast.FunctionDef</code>, and <code>ast.AsyncFunctionDef</code> nodes can have docstrings:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    <code>ast.get_docstring(node)</code> returns the docstring of <code>node</code> or <code>None</code>, if there isn't one:
  </p>
</div>

<div class="fragment" data-fragment-index="0">
<pre>
    <code data-trim class="language-python hide-line-numbers" data-line-numbers="1-9|2-5|7" data-fragment-index="1">
def detect_missing_docstring(
    node: ast.AsyncFunctionDef
    | ast.ClassDef
    | ast.FunctionDef
    | ast.Module
) -> None:
    if ast.get_docstring(node) is None:
        entity = getattr(node, 'name', 'module')
        print(f'{entity} is missing a docstring')
    </code>
</pre>
</div>

---

In `greet.py`, we want to call this function on these nodes only:

<div class="center">
  <img width="250" src="media/docstrings.svg" alt="The AST the nodes in greet.py that can have docstrings visualized with Graphviz">
</div>

---

## Traversing the AST

File structures vary, so we will create a `NodeVisitor` to ensure we find all missing docstrings:

<ol>
  <li class="fragment">Subclass <code>ast.NodeVisitor</code></li>
  <li class="fragment">Create <code>visit_&lt;NodeType&gt;()</code> methods for nodes we are interested in</li>
  <li class="fragment">Instantiate the visitor and call <code>visit(tree)</code></li>
</ol>

---

### 1. Subclass `ast.NodeVisitor`

```python
class DocstringVisitor(ast.NodeVisitor): ...
```

---

### 2. Create `visit_<NodeType>()` methods for nodes we are interested in

```python
class DocstringVisitor(ast.NodeVisitor):

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> None:
        detect_missing_docstring(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        detect_missing_docstring(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        detect_missing_docstring(node)

    def visit_Module(self, node: ast.Module) -> None:
        detect_missing_docstring(node)
```

---

### 3. Instantiate the visitor and call `visit(tree)`

```pycon
>>> visitor = DocstringVisitor()
>>> visitor.visit(tree)
module is missing a docstring
```

<p class="fragment">What about the missing docstrings for the <code>Greeter</code> class and its methods?</p>

---

### Complete traversal means visiting all fields

We aren't visiting the list of AST nodes in the `ast.Module` node's `body` field, so traversal starts and stops there:

<div class="center">
  <img width="275" src="media/docstring-nodes-with-attributes.svg" alt="The AST the nodes in greet.py that can have docstrings with attributes and types visualized with Graphviz">
</div>

---

### The `general_visit()` method

<ul>
  <li class="fragment">Defined on base class <code>ast.NodeVisitor</code></li>
  <li class="fragment">Visits child nodes by calling <code>visit()</code> on any nodes returned from <code>ast.iter_fields()</code></li>
  <li class="fragment">Called automatically for node types we didn't create methods for</li>
</ul>


---

### Modifying the `DocstringVisitor`

<div class="r-stack r-stack-left">
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    Add the <code>_visit_helper()</code> method, which checks the docstring and then continues the traversal:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    Calling <code>generic_visit()</code> on each node we check docstrings for ensures we continue the traversal:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    Now, we switch to calling <code>_visit_helper()</code> whenever we visit module, class, or function nodes:
  </p>
</div>

<div class="fragment" data-fragment-index="0">
<pre>
    <code data-trim class="language-python hide-line-numbers" data-line-numbers="3-11|11|13-25" data-fragment-index="1">
class DocstringVisitor(ast.NodeVisitor):

    def _visit_helper(
        self,
        node: ast.AsyncFunctionDef
        | ast.ClassDef
        | ast.FunctionDef
        | ast.Module
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
</code>
</pre>
</div>


---

### Complete traversal achieved 🎉

```pycon
>>> visitor = DocstringVisitor()
>>> visitor.visit(tree)
module is missing a docstring
Greeter is missing a docstring
__init__ is missing a docstring
greet is missing a docstring
```

---

<div class="center">
  <img width="85%" src="./media/traversal-animation.gif" alt="Complete traversal of the AST for greet.py visualized with Graphviz"/>
</div>

---

## Disambiguating docstring paths

`greet` could be the `greet()` method or the `greet` module, but `greet.Greeter.greet` can only be one:

```
greet is missing a docstring
```

---

### Tracking node ancestry with a stack

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    From a node, we can access its children, but not its parent.
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    We can track lineage with a stack:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    We internalize the missing docstring check as <code>_detect_missing_docstring()</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    It uses the stack to print the unambiguous path to the missing docstring:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    The <code>_visit_helper()</code> takes care of pushing onto and popping off of the stack:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    We push (append) a node onto the stack before we actually visit it:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="5">
    We pop the node off the stack after we have visited it and all of its descendants:
  </p>
</div>

<div class="fragment" data-fragment-index="0">
<pre>
    <code data-trim class="language-python hide-line-numbers" data-line-numbers="3-6|8-17|16|19-31|26-28|31" data-fragment-index="1">
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
        | ast.Module
    ) -> None:
        if ast.get_docstring(node) is None:
            entity = '.'.join(self.stack)
            print(f'{entity} is missing a docstring')

    def _visit_helper(
        self,
        node: ast.AsyncFunctionDef
        | ast.ClassDef
        | ast.FunctionDef
        | ast.Module
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
</code></pre></div>

[notes]
### Other uses for stacks

- determine whether a `ast.FunctionDef` node is a standalone function or method of a class
- detect when a function or class is nested
- check whether a function definition has a `return` statement (and therefore should be documented), despite not having a return type annotation


---

Now, we know exactly where the docstrings are missing:

```pycon [highlight-lines="3-6"][class="hide-line-numbers"]
>>> visitor = DocstringVisitor('greet')
>>> visitor.visit(tree)
greet is missing a docstring
greet.Greeter is missing a docstring
greet.Greeter.__init__ is missing a docstring
greet.Greeter.greet is missing a docstring
```

---

## Suggesting docstring templates

`ast.FunctionDef` and `ast.AsyncFunctionDef` nodes have information that often ends up in the docstring:

<ul>
  <li class="fragment"><code>args</code>: Argument names, types, and defaults</li>
  <li class="fragment"><code>returns</code>: Return type annotation (if present)</li>
  <li class="fragment"><code>body</code>: AST of function body to infer return types/yields/raises (out of scope)</li>
</ul>

<p class="fragment">We will focus on fully-typed code for this keynote.</p>

---

### An example using the `Greeter.greet()` method

```python [highlight-lines="5-6"][class="hide-line-numbers"]
class Greeter:
    def __init__(self, enthusiasm: int = 1) -> None:
        self.enthusiasm = enthusiasm

    def greet(self, name: str = 'World') -> str:
        return f'Hello, {name}{"!" * self.enthusiasm}'
```

---

<div class="center">
    <img width="450" src="./media/greet-method-full-attributes.svg" alt="The AST the Greeter.greet() method visualized with Graphviz with fields">
    <br/>
    <small>The arguments are on the left branch, the function body is in the middle, and the return annotation is on the right branch.</small>
</div>

---

### `ast.arguments`

|field|type|description|
|---|---|---|
|<code>posonlyargs</code>|<code>list[ast.arg]</code>|positional-only arguments|
|<code>args</code>|<code>list[ast.arg]</code>|arguments that can be passed positionally or by keyword|
|<code>vararg</code>|<code>Optional[ast.arg]</code>|<code>*args</code>|
|<code>kwonlyargs</code>|<code>list[ast.arg]</code>|keyword-only arguments|
|<code>kw_defaults</code>|<code>list[ast.arg]</code>|default values for keyword-only arguments, where <code>None</code> means the argument is required|
|<code>kwarg</code>|<code>Optional[ast.arg]</code>|<code>**kwargs</code>|
|<code>defaults</code>|<code>list[ast.arg]</code>|default values for last <code>n</code> positional arguments|


---

The `Greeter.greet()` method has two positional arguments, `self` and `name`, with the latter having a type of `str` and a default value of `'World'`:

```python [highlight-lines="2-6|7-8"][class="hide-line-numbers"]
arguments(
  args=[
    arg(arg='self'),
    arg(
      arg='name',
      annotation=Name(id='str', ctx=Load()))],
  defaults=[
    Constant(value='World')])
```
---

#### Extracting argument information in a docstring-friendly format

We need argument names, types, and default values for three groups of arguments:

<ul>
  <li class="fragment">positional</li>
  <li class="fragment">starred</li>
  <li class="fragment">keyword-only</li>
</ul>

---

##### Positional arguments

```python
from itertools import zip_longest


NO_DEFAULT = object()

def _extract_positional_args(
    arguments: ast.arguments
) -> list[dict]:
    return [
        {
            'name': arg.arg,
            'type': getattr(arg.annotation, 'id', '__type__'),
            'default': (
                default.value
                if default is not NO_DEFAULT
                else default
            ),
        }
        for arg, default in zip_longest(
            reversed([*arguments.posonlyargs, *arguments.args]),
            reversed(arguments.defaults),
            fillvalue=NO_DEFAULT
        )
        if arg.arg not in ['self', 'cls']
    ][::-1]
```

---

###### Example

Given a function with positional arguments:

```python
def func(a: str, /, b: int = 3): pass
```

We get the following result:

```pycon
>>> _extract_positional_args(
...     ast.parse(
...         'def func(a: str, /, b: int = 3): pass'
...     ).body[0].args
... )
[{'name': 'a', 'type': 'str',
  'default': &lt;object at 0x107c5e620&gt;},
 {'name': 'b', 'type': 'int', 'default': 3}]
```

---

##### Starred arguments

```python
def _extract_star_args(arguments: ast.arguments) -> list[dict]:
    return [
        {
            'name': (
                f'*{arg.arg}'
                if arg_type == 'vararg'
                else f'**{arg.arg}'
            ),
            'type': getattr(arg.annotation, 'id', '__type__'),
            'default': NO_DEFAULT,
        }
        if arg
        else None
        for arg_type in ['vararg', 'kwarg']
        for arg in [getattr(arguments, arg_type)]
    ]
```

---

###### Example

Given a function with starred arguments:

```python
def func(*args, **kwargs): pass
```

We get the following result:

```pycon
>>> _extract_star_args(
...     ast.parse(
...         'def func(*args, **kwargs): pass'
...     ).body[0].args
... )
[{'name': '*args', 'type': '__type__',
  'default': &lt;object at 0x107c5e630&gt;},
 {'name': '**kwargs', 'type': '__type__',
  'default': &lt;object at 0x107c5e630&gt;}]
```

---

##### Keyword-only arguments

```python
def _extract_keyword_args(
    arguments: ast.arguments
) -> list[dict]:
    return [
        {
            'name': arg.arg,
            'type': getattr(arg.annotation, 'id', '__type__'),
            'default': (
                NO_DEFAULT if default is None
                else default.value
            ),
        }
        for arg, default in zip(
            arguments.kwonlyargs, arguments.kw_defaults
        )
    ]
```

---

###### Example

Given a function with keyword-only arguments:

```python
def func(*, a: str, b: int = 3): pass
```

We get the following result:

```pycon
>>> _extract_keyword_args(
...     ast.parse(
...         'def func(*, a: str, b: int = 3): pass'
...     ).body[0].args
... )
[{'name': 'a', 'type': 'str',
  'default': &lt;object at 0x107c5e620&gt;},
 {'name': 'b', 'type': 'int', 'default': 3}]
```

---

##### Putting all the arguments together

```python
def extract_arguments(arguments: ast.arguments) -> tuple[dict]:
    params = _extract_positional_args(arguments)

    varargs, kwargs = _extract_star_args(arguments)
    if varargs:
        params.append(varargs)

    params.extend(_extract_keyword_args(arguments))

    if kwargs:
        params.append(kwargs)

    return tuple(params)
```

---

Running this on the `Greeter.greet()` method extracts the `name` argument (ignoring `self`):

```
[{'name': 'name', 'type': 'str', 'default': 'World'}]
```

---

### `returns`

The return annotation for `Greeter.greet()` is `str`:

```
returns=Name(id='str', ctx=Load())
```

---

#### Extracting returns information in a docstring-friendly format

Here, we simplify by assuming that the return notation is provided and only handling the cases of `Constant` and `Name` nodes:

```python
def _extract_return_annotation(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.Name):
        return str(node.id)
    return '__return_type__'
```

---

### Combining arguments and return type into a docstring

We will suggest Numpydoc-style docstrings:

```python
def suggest_docstring(
    node: ast.AsyncFunctionDef | ast.FunctionDef
) -> str:
    if args := extract_arguments(node.args):
        args = [
            f'{arg["name"]} : {arg["type"]}'
            + f', default {arg["default"].value}'
            if arg["default"] is not NO_DEFAULT else ''
            for arg in args
        ]
        args = ['', 'Parameters', '----------', *args]
    else:
        args = []

    returns = _extract_return_annotation(node.returns)

    return '\\n'.join(
        [
            '"""',
            '___description___',
            *args,
            '',
            'Returns',
            '-------',
            returns,
            '"""',
        ]
    )
```

---

#### Updating the `DocstringVisitor`

```python [highlight-lines="8-26|18-26"][class="hide-line-numbers"]
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
        | ast.Module
    ) -> None:
        if ast.get_docstring(node) is None:
            entity = '.'.join(self.stack)
            print(f'{entity} is missing a docstring')
        if isinstance(
            node, ast.AsyncFunctionDef | ast.FunctionDef
        ):
            print(
                'Hint:',
                suggest_docstring(node),
                '',
                sep='\\n',
            )

    def _visit_helper(
        self,
        node: ast.AsyncFunctionDef
        | ast.ClassDef
        | ast.FunctionDef
        | ast.Module
    ) -> None:
        self.stack.append(getattr(node, 'name', self.module_name))
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
```

---


```pycon [highlight-lines="1-2|5-17|19-31"][class="hide-line-numbers"]
>>> visitor = DocstringVisitor('greet')
>>> visitor.visit(tree)
greet is missing a docstring
greet.Greeter is missing a docstring
greet.Greeter.__init__ is missing a docstring
Hint:
"""
___description___

Parameters
----------
enthusiasm : int, default 1

Returns
-------
None
"""

greet.Greeter.greet is missing a docstring
Hint:
"""
___description___

Parameters
----------
name : str, default World

Returns
-------
str
"""
```

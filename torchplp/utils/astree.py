# -*- coding: utf-8 -*-
"""
astree.py - Abstract Syntax Tree Structure

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from collections import deque
from graphviz import Digraph


class ASTKind:
    """Abstract Syntax Tree Kind Class

    This class normalizes the node types generated by different parsers.
    
    Args:
        kind (str): The raw kind
        lang (str): The tpye of parser
            - 'cc': Kind generated by libclang
    """

    def __init__(self, kind, lang):
        if lang == 'cc':
            self._name = kind.name

    def __repr__(self):
        return self._name

    @property
    def name(self):
        return self._name


class ASTNode:
    """Abstract Syntax Tree Node Class"""

    def __init__(self):
        self._parent = None
        self._children = []
        self._id = None
        self._data = None
        self._kind = None
        self._source = None
        self._label = None
        self._is_definition = None

    def __repr__(self):
        return '<covec.utils.ast.ASTNode>'

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if isinstance(node, ASTNode):
            self._parent = node
        else:
            raise ValueError(f'{node} is not a ASTNode')

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, nodes):
        if hasattr(nodes, "__iter__"):
            for n in nodes:
                if isinstance(n, ASTNode):
                    self._children.append(n)
                else:
                    raise ValueError(f'{n} is not a ASTNode')
        else:
            raise ValueError(f'{nodes} is not Iterable')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = str(value)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = str(value)

    @property
    def kind(self):
        return self._kind.name

    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def is_definition(self):
        return self._is_definition

    @is_definition.setter
    def is_definition(self, value):
        self._is_definition = value

    def walk(self, method='DFS'):
        queue = deque()
        assert method.lower() in ['dfs', 'bfs']
        queue.append(self)
        while queue:
            node = queue.popleft()
            for child in node.children:
                if method.lower() == 'dfs':
                    queue.appendleft(child)
                else:
                    queue.append(self)
            yield node

    def graph(self):
        dot = Digraph()
        queue = deque()
        queue.append(self)
        while queue:
            node = queue.popleft()
            dot.node(node.id, f'{node.data}\n{node.kind}')
            for child in node.children:
                dot.node(child.id, f'{child.data}\n{child.kind}')
                dot.edge(node.id, child.id)
                queue.appendleft(child)
        return dot
ANTLR generated parser
======================

See general information about auto-generated parsers at the
`ANTLR home page <https://www.antlr.org/>`_ and for python at
`antlr4 github docs (python-target) <https://github.com/antlr/antlr4/blob/master/doc/python-target.md>`_


fcsql.FCSLexer
--------------

.. py:module:: fcsql.FCSLexer

    .. py:class:: FCSLexer


fcsql.FCSParser
---------------

.. py:module:: fcsql.FCSParser

    .. py:class:: FCSParser

        .. py:method:: __init__(self, input:TokenStream, output:TextIO = sys.stdout)

            
            Used like this::

                query: str = "some query"
                input_stream = antlr4.InputStream(query)
                lexer = fcsql.FCSLexer(input_stream)
                stream = antlr4.CommonTokenStream(lexer)
                parser = fcsql.FCSParser(stream)

            :param TokenStream input: The person sending the message

        .. py:method:: query(self) -> FCSParser.QueryContext

            Start the parsing process for the `query` rule (see BNF)


fcsql.FCSParserListener
-----------------------

.. py:module:: fcsql.FCSParserListener

    .. py:class:: FCSParserListener

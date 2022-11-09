from ipkiss3 import all as i3
from os.path import abspath, join, dirname, pardir, normpath

from ipkiss3.pcell.gdscell import GDSCell
import inspect


def compile_doc(cls, ignore_properties=[]):
    # Custom version of compile_doc, that doesn't add properties

    from ipcore.patterns.indent import indent
    indent4 = lambda s: indent(s, 4)
    linebreak = '\n'

    if not hasattr(cls, '__doc_src'):
        #first time __doc__ is generated
        #Strip trailing white spaces.
        doc = inspect.getdoc(cls)
        doc = '' if doc is None else doc
        cls.__doc_src = doc.strip()
        doc = cls.__doc_src  + linebreak

    lines = [cls.__doc_src, ""]
    doc = linebreak.join(lines)

    from ipkiss.plugins.documentation.example_handler import examples_to_doc
    doc += linebreak * 2
    doc += examples_to_doc(cls)
    #doc += linebreak.join(map(indent4, examples_to_doc(cls).split(linebreak)))

    cls.__doc__ = doc




class AIMCell(GDSCell):
    """Standard cell to use for aim-generated gray-box cells.

    It loads a GDS file.
    """
    compile_doc = classmethod(lambda cls: None)


    class Layout(GDSCell.Layout):

        compile_doc = classmethod(compile_doc)


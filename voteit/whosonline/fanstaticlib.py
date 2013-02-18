""" Fanstatic lib"""
from fanstatic import Library
from fanstatic import Resource


voteit_whosonline = Library('whosonline_static', 'static')

voteit_whosonline_css = Resource(voteit_whosonline, 'styles.css', bottom=True)

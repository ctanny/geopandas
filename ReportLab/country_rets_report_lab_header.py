# -*- coding: utf-8 -*-
"""
cdn_breadth_report_lab_header.py
Code to generate the header for the report lab file for Canadian breadth
"""

from reportlab.platypus import Table, Image
from reportlab.lib import colors
from ReportLab import country_rets_report_lab_control as control
import importlib
from ReportLab.country_rets_report_lab_control import line_color, background_color

importlib.reload(control)

strategy = control.strategy
calc_date = control.calc_date


def gen_header_table(width, height):
    """
    Generates the header for the page

    Parameters
    ----------
    width : TYPE
        DESCRIPTION.
    height : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    title = f'Global YTD Market Performance - As of {calc_date}'

    width_list = [
        width * 0.05,  # column 1 padding
        width * 0.9,  # column 2 title bar
        width * 0.05,  # colunn 3 padding
    ]

    height_list = [
        height * 0.3,  # top padding
        height * 0.5,  # title bar
        height * 0.2,  # bottom padding
    ]

    res = Table([
        ['', '', ''],
        ['', title, ''],
        ['', '', '']
    ], width_list, height_list)

    res.setStyle([
        # ('GRID', (0,0), (-1,-1), 1, 'red'),

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (1, 1), (1, 1), 'CENTER'),  # horizontal
        ('VALIGN', (1, 1), (1, 1), 'MIDDLE'),  # vertical
        ('BACKGROUND', (1, 1), (1, 1),
         colors.HexColor(background_color)),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
        ('LINEBELOW', (1, 1), (1, 1), 1, colors.HexColor(line_color)),
        # ('FONTSIZE', (2,0), (2,0), 20),
    ])

    return res

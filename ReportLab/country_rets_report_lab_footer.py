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


def gen_footer_table(width, height):
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
        width * 0.33,  # column 1
        width * 0.34,  # column 2
        width * 0.33,  # colunn 3
    ]

    height_list = [
        height * 1
    ]

    res = Table([
        [
            '* Weight in Vanguard Total World ETF (VT)',
            '** Weight in iShares MSCI World ETF',
            '^ Weight in iShares MSCI Emerging Markets ETF']
    ], width_list, height_list)

    res.setStyle([
        # ('GRID', (0,0), (-1,-1), 1, 'red'),

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # horizontal
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # vertical
        # ('BACKGROUND', (1, 1), (1, 1),
        #  colors.HexColor(background_color)),
        # ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
        # ('LINEBELOW', (1, 1), (1, 1), 1, colors.HexColor(line_color)),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ])

    return res

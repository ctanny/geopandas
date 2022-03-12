# -*- coding: utf-8 -*-
"""
body.py
Python code to generate the body of the reportlab performance report for Canadian market breadth report

Body has three rows and three columns.
Columns 0, 2 are padding.
Column 1 is main content.

Row 0 is the main table with the data
Row 1 will contain the two graphs, and will have 3 columns (middle column is spacing

"""
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, Image, Paragraph
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
import sys
import os
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from imp import reload
from ReportLab.country_rets_report_lab_control import background_color, line_color
import global_market_performance
from global_market_performance import top_5, bottom_5, dev_top_5, em_top_5, dev_bottom_5, em_bottom_5
from ReportLab import country_rets_report_lab_control as control
import importlib
importlib.reload(control)


strategy = control.strategy
calc_date = control.calc_date
image_file = control.image_file


def gen_body_table(width, height):
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
    # Change the width and height
    width_list = [
        width * 0.05,  # column 1 padding
        width * 0.9,  # column 2 main section will be divided into more tables
        width * 0.05,  # column 3 padding
    ]

    height_list = [
        height * 0.6,  # 1st row for components
        height * 0.2,  # 2nd row for other components
        height * 0.2,  # 3rd row for components
    ]

    res = Table([
        ['', gen_1st_component_row(width_list[1], height_list[0]), ''],
        ['', gen_2nd_component_row(width_list[1], height_list[1]), ''],
        ['', gen_3rd_component_row(width_list[1], height_list[2]), ''],
    ],
        width_list, height_list)

    res.setStyle([
        # ('GRID', (0, 0), (-1, -1), 1, 'red'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # ('ALIGN', (1,1), (1,1), 'CENTER'), # horizontal
        # ('VALIGN', (1,1), (1,1), 'MIDDLE'), # vertical
        # ('BACKGROUND', (1, 1), (1, 1),
        #  colors.HexColor('#4a73b0')),
        # ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
        # ('LINEBELOW', (1, 1), (1, 1), 1, colors.orange),
        # ('FONTSIZE', (2,0), (2,0), 20),
    ])
    return res


def gen_1st_component_row(width, height):
    """
    Function to produce the content on the 1st component row of the body
    - performance table
    - performance graph

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

    width_list = [
        width * 1
    ]

    height_list = [
        height * 1
    ]

    graph = Image(image_file,
                  width_list[0],
                  height_list[0],
                  kind='proportional'
                  )

    res = Table([
        [graph],
    ],
        width_list, height_list)

    res.setStyle([
        # ('GRID', (0, 0), (-1, -1), 1, 'red'),
        # ('LEFTPADDING', (0, 0), (-1, -1), 0),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # format positioning on canvas
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),   # horizontal
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # vertical
        # ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
        # ('LINEBELOW', (0, 0), (0, 0), 1, colors.HexColor(line_color)),
        # ('BACKGROUND', (0, 0), (0, 0),
        #  colors.HexColor(background_color)),
        # format right header bar
        # ('ALIGN', (2, 0), (2, 0), 'CENTER'),  # horizontal
        # ('VALIGN', (2, 0), (2, 0), 'MIDDLE'),  # vertical
        # ('BACKGROUND', (2, 0), (2, 0),
        #  colors.HexColor(background_color)),
        # ('TEXTCOLOR', (2, 0), (2, 0), colors.white),
        # ('LINEBELOW', (2, 0), (2, 0), 1, colors.HexColor(line_color)),
        # ('TEXTCOLOR', (2, 0), (2, 0), colors.white),
        # ('LINEBELOW', (2, 0), (2, 0), 1, colors.orange),
        # ('TEXTCOLOR', (4, 0), (4, 0), colors.white),
        # ('LINEBELOW', (4, 0), (4, 0), 1, colors.orange),
        # ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # alignment of title bars
        # ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # alignment of title bars
        # # # format returns table positioning
        # ('ALIGN', (0, 1), (0, 0), 'LEFT'),  # horizontal
        # ('VALIGN', (0, 1), (0, 1), 'TOP'),
        # ('TOPPADDING', (0, 1), (0, 1), 10),
        # # ('FONTSIZE', (2,0), (2,0), 20),
    ])

    return res


def gen_2nd_component_row(width, height):
    """
    Function to produce the content on the 1st component row of the body
    - performance table
    - performance graph

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

    width_list = [
        width * 0.49,
        width * 0.02,
        width * 0.49,
        # width * 0.395,
    ]

    height_list = [
        height * 0.15,  # title bar
        height * 0.85,  # component height
    ]

    res = Table([
        ['Top 5 Performing Countries', '', 'Bottom 5 Performing Countries'],
        [generate_table(top_5), '', generate_table(bottom_5)],
    ],
        width_list, height_list)

    res.setStyle([
        # ('GRID', (0, 0), (-1, -1), 1, 'red'),
        # overall formatting
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # Left header bar formatting
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # horizontal
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # vertical
        ('BACKGROUND', (0, 0), (0, 0),
         colors.HexColor(background_color)),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.HexColor(line_color)),
        # Right header bar formatting
        ('ALIGN', (2, 0), (2, 0), 'CENTER'),  # horizontal
        ('VALIGN', (2, 0), (2, 0), 'MIDDLE'),  # vertical
        ('BACKGROUND', (2, 0), (2, 0),
         colors.HexColor(background_color)),
        ('TEXTCOLOR', (2, 0), (2, 0), colors.white),
        ('LINEBELOW', (2, 0), (2, 0), 1, colors.HexColor(line_color)),
        # format table
        ('ALIGN', (0, 1), (0, 1), 'LEFT'),  # horizontal
        ('VALIGN', (0, 1), (0, 1), 'MIDDLE'),
        ('ALIGN', (2, 1), (2, 1), 'LEFT'),  # horizontal
        ('VALIGN', (2, 1), (2, 1), 'MIDDLE'),
        # ('TEXTCOLOR', (2, 0), (2, 0), colors.white),
        # ('LINEBELOW', (2, 0), (2, 0), 1, colors.orange),
        # ('FONTSIZE', (2,0), (2,0), 20),
    ])

    return res


def gen_3rd_component_row(width, height):
    """
    Function to produce the content on the 1st component row of the body
    - performance table
    - performance graph

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

    width_list = [
        width * 0.24,
        width * 0.01,
        width * 0.24,
        width * 0.02,
        width * 0.24,
        width * 0.01,
        width * 0.24,

    ]

    height_list = [
        height * 0.15,  # title bar
        height * 0.85,  # component height
    ]

    res = Table([
        # row 0, 7 columns
        ['Top 5 Developed Countries', '', 'Bottom 5 Developed Countries',
         '', 'Top 5 Emerging Countries', '', 'Bottom 5 Emerging Countries'],
        # row 1, 7 columns
        [generate_table(dev_top_5), '', generate_table(dev_bottom_5),
         '', generate_table(em_top_5), '', generate_table(em_bottom_5)],
    ],
        width_list, height_list)

    res.setStyle([
        # ('GRID', (0, 0), (-1, -1), 1, 'red'),
        # overall formatting
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # header bar formatting
        ('ALIGN', (0, 0), (6, 0), 'CENTER'),  # horizontal
        ('VALIGN', (0, 0), (6, 0), 'MIDDLE'),  # vertical
        ('TEXTCOLOR', (0, 0), (6, 0), colors.white),
        ('BACKGROUND', (0, 0), (0, 0),
         colors.HexColor(background_color)),
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.HexColor(line_color)),
        ('BACKGROUND', (2, 0), (2, 0),
         colors.HexColor(background_color)),
        ('LINEBELOW', (2, 0), (2, 0), 1, colors.HexColor(line_color)),
        ('BACKGROUND', (4, 0), (4, 0),
         colors.HexColor(background_color)),
        ('LINEBELOW', (4, 0), (4, 0), 1, colors.HexColor(line_color)),
        ('BACKGROUND', (6, 0), (6, 0),
         colors.HexColor(background_color)),
        ('LINEBELOW', (6, 0), (6, 0), 1, colors.HexColor(line_color)),
        # Right header bar formating
        # ('ALIGN', (2, 0), (2, 0), 'CENTER'),  # horizontal
        # ('VALIGN', (2, 0), (2, 0), 'MIDDLE'),  # vertical
        # ('TEXTCOLOR', (2, 0), (2, 0), colors.white),
        # ('LINEBELOW', (0, 0), (0, 0), 1, colors.HexColor(line_color)),
        # format table
        ('ALIGN', (0, 1), (0, 1), 'LEFT'),  # horizontal
        ('VALIGN', (0, 1), (0, 1), 'MIDDLE'),
        ('ALIGN', (2, 1), (2, 1), 'LEFT'),  # horizontal
        ('VALIGN', (2, 1), (2, 1), 'MIDDLE'),
        # ('TEXTCOLOR', (2, 0), (2, 0), colors.white),
        # ('LINEBELOW', (2, 0), (2, 0), 1, colors.orange),
        # ('FONTSIZE', (2,0), (2,0), 20),
    ])

    return res


def generate_table(table_name):

    '''
    https://stackoverflow.com/questions/57706068/how-to-align-text-to-center-in-reportlab-python
    Returns
    -------

    '''

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='Header_Right_Align',
        parent=styles['Normal'],
        textColor=colors.white,
        alignment=TA_RIGHT,
        wordWrap='LTR',
    ))

    headers = table_name.columns.values.tolist()
    # headers = [Paragraph(header, styles['Header_Right_Align']) for header in headers]

    final_table = [headers] + table_name.values.tolist()

    res = Table(final_table)

    res.setStyle([
        # ('GRID', (0, 0), (-1, -1), 1, 'red'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),   # right align table
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),    # Left align index
        ('BACKGROUND', (0, 0), (-1, 0),
         colors.HexColor(background_color)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor(line_color)),
        ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])

    return res

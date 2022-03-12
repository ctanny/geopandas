'''
cdn_breadth_report_lab_main.py
report lab file for market breadth reports

Test out, this should import the cdn_market_breadth.py file which will run it,
and then we can access the tables and graphs.
All maintenance functions should be moved to a new py file.

'''

import os

import seaborn as sns
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

# set working directory

path = (r'C:\Users\ctann\OneDrive\Quantitative_Finance\Spreadsheets\Geopandas')
os.chdir(path)

# imports for the other report lab components
from ReportLab import country_rets_report_lab_control as control
from ReportLab.country_rets_report_lab_body import gen_body_table
from ReportLab.country_rets_report_lab_header import gen_header_table
from ReportLab.country_rets_report_lab_footer import gen_footer_table
import importlib
import global_market_performance
importlib.reload(control)

sns.set()
# get_ipython().run_line_magic('matplotlib', 'auto')

# %% PDF Generation
# create the canvas
report_title = control.title

pdf = canvas.Canvas(report_title, pagesize=landscape(letter))
pdf.setTitle('Global Market Performance')

width, height = landscape(letter)

# heights of the rows in the pdf
main_table_heights = [
    height * 0.05,  # header
    height * 0.9,  # main content
    height * 0.05  # footer
    ]

global strategy, calc_date

main_table = Table([
    [gen_header_table(width, main_table_heights[0])],
    [gen_body_table(width, main_table_heights[1])],
    [gen_footer_table(width, main_table_heights[2])],
],
    colWidths=width,
    rowHeights=main_table_heights
)

main_table.setStyle([
    # ('GRID', (0, 0), (-1, -1), 1, 'red'),

    ('LEFTPADDING', (0, 0), (0, 1), 0),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
])

main_table.wrapOn(pdf, 0, 0)
main_table.drawOn(pdf, 0, 0)

# Close the PDF and save
pdf.showPage()
pdf.save()


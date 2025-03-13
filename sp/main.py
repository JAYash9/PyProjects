import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
filepath=glob.glob("*.txt")
pdf = FPDF(orientation='P', unit='mm', format='A4')

for i in filepath:
    filename = Path(i).stem
    name=filename.title()
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"{name}", ln=1)
  
pdf.output("Multiple_pdf.pdf")


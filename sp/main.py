import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
filepath=glob.glob("*.txt")
pdf = FPDF(orientation='P', unit='mm', format='A4')

for i in filepath:
    filename = Path(i).stem
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(w=50, h=10, txt=f"{filename}", ln=1)
    with open(i, "r") as file:
        content = file.read()
        sentences = content.split('. ')
        for sentence in sentences:
            pdf.cell(w=0, h=10, txt=sentence.strip() + '.', ln=1)

pdf.output("Multiple_pdf.pdf")


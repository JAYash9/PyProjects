import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
filepath=glob.glob("*.xlsx")
for i in filepath:
    print(i)
    read=pd.read_excel(i)
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    filename=Path(i).stem  
    invoice_nr=filename.split("-")[0]
    pdf.add_page()
    pdf.set_font("Arial", size=16,style="B")
    pdf.cell(w=50,h=10,txt=f"invoice_nr.{invoice_nr}",ln=1) 
    pdf.output(f"{filename}.pdf") 
from fpdf import FPDF
import pandas as pd

# Correct the file name to match the provided context
df = pd.read_csv('topic.csv')   

# Correct the column name from 'variiables' to 'Variables'
for index, row in df.iterrows():
    print(f"{row['Topic']} {row['Pages']}")
   

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font(family='Arial', style='B', size=12)

# Remove duplicate lines and correct the text
pdf.cell(w=10, h=12, txt='Hello world!', align="L", ln=1, border=1)

pdf.output("output.pdf")

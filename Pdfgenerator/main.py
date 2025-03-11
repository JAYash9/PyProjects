from fpdf import FPDF
pdf=FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font(family='Arial', style='B', size=12)
pdf.cell(w=10,h=12,txt='Hello world!',align="L",ln=1,border=1)
pdf.set_font(family='Arial', style='B', size=12)
pdf.cell(w=10,h=12,txt='Hello world!',align="L",ln=1,border=1)
pdf.set_font(family='Arial', style='B', size=12)
pdf.cell(w=10,h=12,txt='Hello world!',align="L",ln=1,border=1)
pdf.output("output.pdf")


from fpdf import FPDF
import pandas as pd

# Read the CSV file
df = pd.read_csv("topic.csv")

# Initialize the PDF
pdf = FPDF(orientation='P', unit='mm', format='A4')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Add a new page for each topic
    pdf.add_page()
    
    # Set the header font and color
    pdf.set_font(family='Arial', style='B', size=20)
    pdf.set_text_color(100, 100, 100)
    
    # Add the topic title
    pdf.cell(w=0, h=12, txt=row['Topic'], align="L", ln=1)
    
    # Draw a line under the header
    pdf.line(10, 21, 200, 21)
    
    # Add some space after the header
    pdf.ln(10)
    
    # Set the footer font and color
    pdf.set_font(family='Arial', style='I', size=12)
    pdf.set_text_color(180, 180, 180)
    
    # Add the footer with page number
    pdf.cell(w=0, h=12, txt=f"Page {index + 1} of {row['Pages']}", align="R", ln=1)
    
    # Add additional pages if the topic spans multiple pages
    for i in range(row['Pages'] - 1):
        pdf.add_page()
        pdf.set_font(family='Arial', style='B', size=12)
        pdf.cell(w=0, h=12, txt=f"Page {i + 2}", align="L", ln=1)
        pdf.line(10, 21, 200, 21)

# Output the PDF to a file
pdf.output("output.pdf")

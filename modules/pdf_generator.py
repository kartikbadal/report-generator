from fpdf import FPDF
import logging
import os

logger = logging.getLogger(__name__)

class ReportPDF(FPDF):
    """
    Custom PDF class that extends FPDF.
    Adds a consistent header and footer to every page.
    """
    def header(self):
        # Bold title at the top of every page
        self.set_font("Helvetica", style= "B", size = 12)
        self.cell(0,10,"Automated Business Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", style = "I", size = 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(summary: dict, chart_paths: list, output_path:str) -> str:
        """
        Generates a complete PDF report.
        
        Args:
            summary: Dictionary from get_summary()
            chart_paths: list of file paths from chart PNGs
            output_path : Where to save the final PDF

        Returns:
            output_path : Path where pdf was saved.
        """
        try:
            pdf = ReportPDF()
            pdf.set_auto_page_break(auto = True, margin=15)
            pdf.add_page()

            # Section 1 : Data Overview
            pdf.set_font("Helvetica", style="B", size= 13)
            pdf.cell(0, 10 , "1. Data Overview",new_x= "LMARGIN", new_y= "NEXT")
            pdf.ln(2)
            pdf.set_font("Helvetica", size= 11)
            pdf.cell(0, 8, f"Total Rows:{summary['rows']}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 8, f"Total Columns: {summary['columns']}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)


            # Section 2 : Data Types

            pdf.set_font("Helvetica", style="B", size = 13)
            pdf.cell(0, 10, "2. Column Data Types", new_x= "LMARGIN", new_y="NEXT")
            pdf.ln(2)

            pdf.set_font("Helvetica", size = 11)
            for col, dtype in summary["dtypes"].items():
                pdf.cell(0, 8, f"{col}: {dtype}", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)

            # Section 3 : Null Counts
            pdf.set_font("Helvetica", style = "B", size = 13)
            pdf.cell(0, 10 , "3. Missing Values", new_x= "LMARGIN", new_y="NEXT")
            pdf.ln(2)

            pdf.set_font("Helvetica", size = 11)
            for col, count in summary["null_counts"].items():
                pdf.cell(0, 8, f"{col}: {count} missing", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)

            # Section 4: Numeric Summary
            pdf.set_font("Helvetica", style= "B", size = 13)
            pdf.cell(0, 10, "4. Numeric Summary", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

            pdf.set_font("Helvetica", size = 11)
            for col, stats in summary["numeric_summary"].items():
                pdf.cell(0, 8, f"{col}:", new_x="LMARGIN", new_y="NEXT")
                for stat, value in stats.items():
                    pdf.cell(0, 8, f"  {stat}: {round(value, 2)}", new_x= "LMARGIN", new_y="NEXT")
            pdf.ln(4)

            # Section 5 - Charts
            if chart_paths:
                pdf.set_font("Helvetica", style="B", size=13)
                pdf.cell(0, 10, "5. Charts", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

                for chart_path in chart_paths:
                    if os.path.exists(chart_path):
                        pdf.add_page()
                        pdf.image(chart_path, x= 10, w=190)
                        pdf.ln(4)
                    else:
                        logger.warning(f"Chart not found, skipping: {chart_path}")
            # Save pdf
            pdf.output(output_path)
            logger.info(f"PDF report saved : {output_path}")
            return output_path
                    
        
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            raise




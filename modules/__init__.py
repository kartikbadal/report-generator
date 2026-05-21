# modules/__init__.py
try:
    from .data_processor import load_file, clean_data, get_summary
    from .chart_generator import save_bar_chart, save_line_chart, save_correlation_heatmap
    from .pdf_generator import generate_pdf
    from .email_sender import send_report
    from .scraper import get_usd_to_inr, get_page_text
except ImportError:
    from modules.data_processor import load_file, clean_data, get_summary
    from modules.chart_generator import save_bar_chart, save_line_chart, save_correlation_heatmap
    from modules.pdf_generator import generate_pdf
    from modules.email_sender import send_report
    from modules.scraper import get_usd_to_inr, get_page_text
"""
HTML to PDF Service
------------------
A lightweight microservice that converts HTML content to PDF using WeasyPrint.
"""

from .service import app, render_pdf, health_check

__version__ = "0.1.0"
__all__ = ["app", "render_pdf", "health_check"]

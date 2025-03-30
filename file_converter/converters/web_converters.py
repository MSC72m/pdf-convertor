import asyncio
import os

import weasyprint

from file_converter.converters.base import BaseConverter


class HTMLToPDFConverter(BaseConverter):
    """Convert HTML files to PDF"""
    
    def __init__(self, input_files_path: str, output_files_path: str):
        super().__init__(input_files_path, output_files_path)
        self.input_extension = ".html"
        self.output_extension = ".pdf"
    
    async def _convert_single_file(self, html_path: str, output_path: str) -> None:
        """Convert a single HTML file to PDF"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._convert_sync, html_path, output_path)
        print(f"Converted {html_path} to {output_path}")
        return None
    
    def _convert_sync(self, html_path: str, output_path: str) -> None:
        """Convert HTML to PDF using WeasyPrint"""
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert to PDF
        html = weasyprint.HTML(string=html_content, base_url=os.path.dirname(html_path))
        html.write_pdf(output_path) 
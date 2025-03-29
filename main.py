from convertor import (
    PDFToDOCXConverter,
    PDFToJPGConverter,
    PDFToPowerPointConverter,
    PDFToExcelConverter,
    PDFToPDFAConverter,
    JPGToPDFConverter,
    WordToPDFConverter,
    PowerPointToPDFConverter,
    ExcelToPDFConverter,
    HTMLToPDFConverter
)
import argparse
import asyncio


async def main():
    parser = argparse.ArgumentParser(description="Convert files between different formats")
    parser.add_argument("--input_files_path", type=str, required=True, help="Path to the input files")
    parser.add_argument("--output_files_path", "--out_files_path", type=str, required=True, 
                        help="Path to the output files")
    parser.add_argument("--conversion_type", type=str, required=True, 
                        choices=[
                            "pdf_to_docx", "pdf_to_jpg", "pdf_to_pptx", "pdf_to_xlsx", "pdf_to_pdfa",
                            "jpg_to_pdf", "docx_to_pdf", "pptx_to_pdf", "xlsx_to_pdf", "html_to_pdf"
                        ],
                        help="Type of conversion to perform")
    args = parser.parse_args()
    
    # Get the output path from either argument name
    output_path = args.output_files_path
    
    # Create the appropriate converter based on the conversion type
    converter_map = {
        "pdf_to_docx": PDFToDOCXConverter,
        "pdf_to_jpg": PDFToJPGConverter,
        "pdf_to_pptx": PDFToPowerPointConverter,
        "pdf_to_xlsx": PDFToExcelConverter,
        "pdf_to_pdfa": PDFToPDFAConverter,
        "jpg_to_pdf": JPGToPDFConverter,
        "docx_to_pdf": WordToPDFConverter,
        "pptx_to_pdf": PowerPointToPDFConverter,
        "xlsx_to_pdf": ExcelToPDFConverter,
        "html_to_pdf": HTMLToPDFConverter
    }
    
    converter_class = converter_map.get(args.conversion_type)
    if not converter_class:
        print(f"Unsupported conversion type: {args.conversion_type}")
        return
    
    converter = converter_class(args.input_files_path, output_path)
    await converter.convert_all_files()

if __name__ == "__main__":
    asyncio.run(main())

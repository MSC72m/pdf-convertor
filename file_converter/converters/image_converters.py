import asyncio
import os
from pathlib import Path
from typing import List

import img2pdf

from file_converter.converters.base import BaseConverter


class JPGToPDFConverter(BaseConverter):
    """Convert JPG images to PDF"""
    
    def __init__(self, input_files_path: str, output_files_path: str):
        super().__init__(input_files_path, output_files_path)
        self.input_extension = ".jpg"
        self.output_extension = ".pdf"
    
    async def convert_all_files(self) -> None:
        """Override to handle multiple images to one PDF or one image per PDF"""
        await self._get_all_files()
        if not self._input_files:
            print(f"No JPG files found in {self.input_files_path}")
            return None
        
        print(f"Found {len(self._input_files)} JPG files to convert")
        await self.ensure_output_directory()
        
        # Group files by base name (without numbers at the end)
        file_groups = {}
        for file_path in self._input_files:
            filename = os.path.basename(file_path)
            # Try to extract a base name by removing trailing numbers
            base_name = Path(filename).stem
            base_name = ''.join(c for c in base_name if not c.isdigit()).rstrip('_-. ')
            
            if not base_name:  # If we removed everything, use the original name
                base_name = Path(filename).stem
            
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(file_path)
        
        # Convert each group to a PDF
        conversion_tasks = []
        for base_name, files in file_groups.items():
            output_path = os.path.join(self.output_files_path, f"{base_name}.pdf")
            conversion_tasks.append(self._convert_file_group(files, output_path))
        
        await asyncio.gather(*conversion_tasks)
        print("All files converted successfully")
    
    async def _convert_file_group(self, image_paths: List[str], output_path: str) -> None:
        """Convert a group of JPG images to a single PDF"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._convert_sync, image_paths, output_path)
        print(f"Converted {len(image_paths)} images to {output_path}")
    
    def _convert_sync(self, image_paths: List[str], output_path: str) -> None:
        """Convert JPG images to PDF"""
        # Sort images by name to maintain order
        image_paths.sort()
        
        # Convert images to PDF
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
    
    async def _convert_single_file(self, jpg_path: str, output_path: str) -> None:
        """Convert a single JPG file to PDF"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._convert_single_sync, jpg_path, output_path)
        print(f"Converted {jpg_path} to {output_path}")
        return None
    
    def _convert_single_sync(self, jpg_path: str, output_path: str) -> None:
        """Convert a single JPG to PDF"""
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(jpg_path)) 
from typing import List
import os
import asyncio
from file_converter.utils.file_manager import FileManager


class BaseConverter(FileManager):
    """Base class for all converters"""
    
    def __init__(self, input_files_path: str, output_files_path: str):
        """
        Initialize the converter.
        
        Args:
            input_files_path: Directory path containing input files
            output_files_path: Directory path for output files
        """
        super().__init__(input_files_path, output_files_path)
        self._input_files = []
        self.input_extension = ""
        self.output_extension = ""
    
    async def _get_all_files(self) -> None:
        """Get all files with the specified input extension"""
        self._input_files = await super().load_multiple_files(self.input_extension)
        return None
    
    async def convert_all_files(self) -> None:
        """
        Convert all files in the input directory with the specified extension.
        
        This method:
        1. Finds all files with the input extension
        2. Creates the output directory if it doesn't exist
        3. Converts each file concurrently
        """
        await self._get_all_files()
        if not self._input_files:
            print(f"No {self.input_extension} files found in {self.input_files_path}")
            return None
        
        print(f"Found {len(self._input_files)} {self.input_extension} files to convert")
        await self.ensure_output_directory()
        
        conversion_tasks = []
        for input_path in self._input_files:
            filename = os.path.basename(input_path)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(self.output_files_path, f"{base_name}{self.output_extension}")
            
            # Create a task for each conversion
            conversion_tasks.append(self._convert_single_file(input_path, output_path))
        
        # Run conversions concurrently
        await asyncio.gather(*conversion_tasks)
        print("All files converted successfully")
        return None
    
    async def _convert_single_file(self, input_path: str, output_path: str) -> None:
        """
        Convert a single file - to be implemented by subclasses
        
        Args:
            input_path: Path to the input file
            output_path: Path where the converted file should be saved
        """
        raise NotImplementedError("Subclasses must implement this method") 
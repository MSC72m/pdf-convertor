from typing import List
from aiopath import AsyncPath
import os
import asyncio


class FileManager:
    """
    Handles file operations for converters, including validation and file discovery.
    """
    def __init__(self, input_files_path: str, output_files_path: str):
        """
        Initialize the file manager.
        
        Args:
            input_files_path: Directory path containing input files
            output_files_path: Directory path for output files
        """
        self.input_files_path = input_files_path
        self.output_files_path = output_files_path
        self.path = AsyncPath(input_files_path)
    
    async def __validate_file_path(self):
        """Validate that the input path exists and is a directory"""
        if not await self.path.exists():
            raise FileNotFoundError(f"Path {self.input_files_path} not found")
        if not await self.path.is_dir():
            raise ValueError(f"Path {self.input_files_path} is not a directory")

    async def __validate_file_type(self, file_path: str, file_type: str):
        """Validate that a file has the expected extension"""
        if not file_path.lower().endswith(file_type.lower()):
            raise ValueError(f"File {file_path} is not a {file_type} file")
        
    async def load_single_file(self, file_path: str, file_type: str) -> str:
        """
        Validate a single file
        
        Args:
            file_path: Path to the file
            file_type: Expected file extension (e.g., ".pdf")
            
        Returns:
            The validated file path
        """
        await self.__validate_file_type(file_path, file_type)
        return file_path
    
    async def load_multiple_files(self, file_type: str) -> List[str]:
        """
        Load multiple files paths
        
        Args:
            file_type: File extension to search for (e.g., ".pdf")
            
        Returns:
            List of file paths matching the extension
        """
        await self.__validate_file_path()
        files = []
        async for file in self.path.glob(f"*{file_type}"):
            files.append(str(file))
        return files

    async def ensure_output_directory(self):
        """Ensure the output directory exists"""
        output_path = AsyncPath(self.output_files_path)
        if not await output_path.exists():
            os.makedirs(self.output_files_path, exist_ok=True) 
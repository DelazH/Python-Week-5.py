import os

class FileProcessor:
    """
    A class to handle file processing operations including reading, modifying, and writing files.
    Implements proper exception handling and file validation.
    """
    
    def __init__(self, input_file_path=None, output_file_path=None):
        """
        Initialize the FileProcessor with optional file paths
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.content = None
    
    def validate_file_path(self, file_path, check_exists=True):
        """
        Validate a file path
        :param file_path: Path to validate
        :param check_exists: Whether to check if file exists
        :return: True if valid, False otherwise
        """
        if not file_path:
            raise ValueError("File path cannot be empty")
        
        if check_exists and not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not file_path.endswith('.txt'):
            print(f"Warning: {file_path} is not a .txt file")
            
        return True
    
    def read_file(self, file_path=None):
        """
        Read content from a file
        :param file_path: Path to file (uses instance path if None)
        :return: File content as string
        """
        path = file_path or self.input_file_path
        self.validate_file_path(path)
        
        try:
            with open(path, 'r') as file:
                self.content = file.read()
            return self.content
        except PermissionError:
            raise PermissionError(f"Permission denied when reading: {path}")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"Could not decode file: {path}")
        except Exception as e:
            raise Exception(f"Error reading file {path}: {str(e)}")
    
    def modify_content(self, modification_function=None):
        """
        Modify the file content
        :param modification_function: Function to apply to content (defaults to uppercase)
        """
        if self.content is None:
            raise ValueError("No content loaded. Read a file first.")
            
        if modification_function:
            self.content = modification_function(self.content)
        else:
            # Default modification: convert to uppercase
            self.content = self.content.upper()
    
    def write_file(self, content=None, file_path=None):
        """
        Write content to a file
        :param content: Content to write (uses instance content if None)
        :param file_path: Path to file (uses instance path if None)
        """
        path = file_path or self.output_file_path
        content = content or self.content
        
        if not path:
            raise ValueError("Output file path not specified")
            
        try:
            with open(path, 'w') as file:
                file.write(content)
            print(f"Successfully wrote to {path}")
        except PermissionError:
            raise PermissionError(f"Permission denied when writing to: {path}")
        except Exception as e:
            raise Exception(f"Error writing to file {path}: {str(e)}")
    
    def process_file(self, input_path=None, output_path=None, modification_function=None):
        """
        Complete file processing pipeline
        """
        try:
            self.input_file_path = input_path or self.input_file_path
            self.output_file_path = output_path or self.output_file_path
            
            # Validate paths
            self.validate_file_path(self.input_file_path)
            if not self.output_file_path:
                self.output_file_path = self._generate_output_path()
            
            # Process file
            self.read_file()
            self.modify_content(modification_function)
            self.write_file()
            
            return True
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return False
    
    def _generate_output_path(self):
        """Generate default output path based on input path"""
        if not self.input_file_path:
            raise ValueError("No input file path available")
        dirname = os.path.dirname(self.input_file_path)
        basename = os.path.basename(self.input_file_path)
        return os.path.join(dirname, f"modified_{basename}")


def example_modification(content):
    """Example custom modification function"""
    return content.replace("secret", "*****").upper()


def main():
    """Main function to demonstrate usage"""
    print("File Processing Program")
    print("----------------------")
    
    # Get user input
    input_path = input("Enter input file path (or press Enter for default 'input.txt'): ") or "input.txt"
    output_path = input("Enter output file path (or press Enter for automatic naming): ") or None
    
    # Create processor instance
    processor = FileProcessor(input_path, output_path)
    
    # Process with default modification (uppercase)
    print("\nProcessing with default modification (uppercase)...")
    if processor.process_file():
        print("File processed successfully!")
    else:
        print("File processing failed.")
    
    # Process with custom modification
    print("\nProcessing with custom modification (replace 'secret' and uppercase)...")
    if processor.process_file(modification_function=example_modification):
        print("File processed successfully!")
    else:
        print("File processing failed.")


if __name__ == "__main__":
    main()

from .base import Tool


class FileSystemTool(Tool):
    """
    A tool for interacting with an in-memory file system.
    The filesystem is a simple dictionary.
    """

    def __init__(self):
        self.files = {}

    def write_file(self, filename: str, content: str):
        """Writes or overwrites a file with the given content."""
        self.files[filename] = content
        return {
            "status": "success",
            "message": f"File '{filename}' written successfully.",
        }

    def read_file(self, filename: str):
        """Reads the content of a file."""
        if filename not in self.files:
            return {"status": "error", "message": f"File '{filename}' not found."}
        return {
            "status": "success",
            "filename": filename,
            "content": self.files[filename],
        }

    def list_files(self):
        """Lists all the files in the file system."""
        return {"status": "success", "files": list(self.files.keys())}

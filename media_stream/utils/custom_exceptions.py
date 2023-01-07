class VideoProcessFailed(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, file_name, message="Failed to process file"):
        self.file_name = file_name
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.file_name} -> {self.message}'
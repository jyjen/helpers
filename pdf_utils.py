from tika import parser

class PdfReader:

    """Reads PDF from a specified filepath.

    Arguments:
        pdf_fp {str} -- Path to pdf file to read
    """

    def __init__(self,
                pdf_fp: str):

        self.parsed_pdf = parser.from_file(pdf_fp)

    def get_content(self):

        """Returns parsed PDF contents."""

        content = self.parsed_pdf['content']

        return content

    def get_metadata(self):

        """Returns parsed PDF metadata."""

        metadata = self.parsed_pdf['metadata']

        return metadata

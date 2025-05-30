import unittest
import os
from src.word_review_parser import WordProcessor, LatexParser, WordBuilder # Import necessary classes

# Define paths relative to the test file location (assuming test_package.py is in the root)
# Adjust paths if test_package.py is moved
TEST_DOCX_PATH = "example_with_comments_and_revisions.docx"
TEST_LATEX_PATH = "tex.txt"
TEST_TEMPLATE_PATH = "word_template_base"
TEST_OUTPUT_DIR = "test_output"
TEST_OUTPUT_DOCX_PATH = os.path.join(TEST_OUTPUT_DIR, "test_converted_from_latex.docx")

class TestWordReviewParser(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
        # Ensure test files exist (these should be part of the project structure)
        if not os.path.exists(TEST_DOCX_PATH):
            self.skipTest(f"Test file not found: {TEST_DOCX_PATH}")
        if not os.path.exists(TEST_LATEX_PATH):
             self.skipTest(f"Test file not found: {TEST_LATEX_PATH}")
        if not os.path.exists(TEST_TEMPLATE_PATH):
             self.skipTest(f"Test template directory not found: {TEST_TEMPLATE_PATH}")


    def tearDown(self):
        """Clean up test environment."""
        # Clean up generated files/directories if needed
        # For now, we'll leave the output for inspection, but in a real test suite, you might clean up.
        # if os.path.exists(TEST_OUTPUT_DIR):
        #     shutil.rmtree(TEST_OUTPUT_DIR)
        pass

    def test_word_processor_load_and_format(self):
        """Test loading a docx and formatting with WordProcessor."""
        print(f"\nTesting WordProcessor with {TEST_DOCX_PATH}")
        processor = WordProcessor(filepath=TEST_DOCX_PATH, merge_revisions=True)
        self.assertTrue(processor.load_document(), "Failed to load document with WordProcessor")

        # Basic check for formatted output
        formatted_doc = processor.get_document_with_revisions_and_comments_formatted(include_comments=False)
        self.assertIsInstance(formatted_doc, str)
        self.assertGreater(len(formatted_doc), 0, "Formatted document is empty")
        print("WordProcessor load and format test passed.")

    def test_latex_parser(self):
        """Test parsing LaTeX text with LatexParser."""
        print(f"\nTesting LatexParser with {TEST_LATEX_PATH}")
        with open(TEST_LATEX_PATH, "r", encoding="utf-8") as f:
            latex_text = f.read()

        parser = LatexParser()
        parsed_data = list(parser.parse_text(latex_text))

        self.assertIsInstance(parsed_data, list)
        self.assertGreater(len(parsed_data), 0, "LatexParser returned no parsed data")

        # Add more specific assertions based on expected content in tex.txt
        # Example: Check for specific tag types
        tag_types = [tag['type'] for tag in parsed_data]
        self.assertIn('added', tag_types)
        self.assertIn('deleted', tag_types)
        self.assertIn('replaced', tag_types)
        self.assertIn('highlight', tag_types)
        self.assertIn('comment', tag_types)

        print("LatexParser test passed.")

    def test_latex_to_word_conversion(self):
        """Test the full LaTeX to Word conversion pipeline."""
        print(f"\nTesting LaTeX to Word conversion with {TEST_LATEX_PATH} and {TEST_TEMPLATE_PATH}")
        with open(TEST_LATEX_PATH, "r", encoding="utf-8") as f:
            latex_text = f.read()

        parser = LatexParser()
        parsed_data = list(parser.parse_text(latex_text))

        builder = WordBuilder(TEST_TEMPLATE_PATH, TEST_OUTPUT_DOCX_PATH)
        success = builder.build_document(latex_text, parsed_data)

        self.assertTrue(success, "Word document building failed")
        self.assertTrue(os.path.exists(TEST_OUTPUT_DOCX_PATH), "Output docx file was not created")
        self.assertGreater(os.path.getsize(TEST_OUTPUT_DOCX_PATH), 1000, "Output docx file is too small") # Basic size check

        print(f"LaTeX to Word conversion test passed. Output at: {TEST_OUTPUT_DOCX_PATH}")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

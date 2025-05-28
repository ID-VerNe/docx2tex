# --- ADD: Module docstring ---
"""Command-line interface for processing Word documents."""
# --- END ADD ---
import logging
import os
import sys

# Add the project root to the Python path
# This is necessary for the script to find modules like 'domain' and 'utils'
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, project_root)

from src.word_review_parser import WordProcessor

# --- ADD: Configure logging ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s.%(funcName)s] - %(message)s')
logger = logging.getLogger(__name__)
# --- END ADD ---

def main():
    """
    Main function to demonstrate the WordProcessor capabilities.
    """
    logger.info("Word document processing script started.")

    # Example DOCX file path (replace with your actual file)
    # For demonstration, we'll use the example_with_comments_and_revisions.docx
    # Make sure this file exists in your project root or provide a full path.
    docx_filepath = os.path.join(project_root, "example_with_comments_and_revisions.docx")

    if not os.path.exists(docx_filepath):
        logger.error(f"Example DOCX file not found at: {docx_filepath}. Please ensure it exists.")
        return

    logger.info(f"Attempting to process file: {docx_filepath}")

    # --- Demonstrate custom tags and different output types ---

    # 1. Default formatting (LaTeX-like tags)
    logger.info("\n--- 1. Formatted Document (Default Tags) ---")
    processor_default = WordProcessor(docx_filepath)
    if processor_default.load_document():
        print(processor_default.get_document_with_revisions_and_comments_formatted())
    else:
        logger.error("Failed to load document for default formatting.")

    # 2. Custom tags example (e.g., Markdown-like)
    logger.info("\n--- 2. Formatted Document (Custom Markdown-like Tags) ---")
    processor_markdown = WordProcessor(
        docx_filepath,
        added_tag_start="**++", added_tag_end="++**",
        deleted_tag_start="~~--", deleted_tag_end="--~~",
        comment_tag_start="[COMMENT: ", comment_tag_end="]"
    )
    if processor_markdown.load_document():
        print(processor_markdown.get_document_with_revisions_and_comments_formatted())
    else:
        logger.error("Failed to load document for custom markdown formatting.")

    # 3. Only Added Text
    logger.info("\n--- 3. Only Added Text ---")
    processor_added = WordProcessor(docx_filepath)
    if processor_added.load_document():
        print(processor_added.get_added_text_formatted())
    else:
        logger.error("Failed to load document for added text extraction.")

    # 4. Only Deleted Text
    logger.info("\n--- 4. Only Deleted Text ---")
    processor_deleted = WordProcessor(docx_filepath)
    if processor_deleted.load_document():
        print(processor_deleted.get_deleted_text_formatted())
    else:
        logger.error("Failed to load document for deleted text extraction.")

    # 5. Only Comments
    logger.info("\n--- 5. Only Comments ---")
    processor_comments = WordProcessor(docx_filepath)
    if processor_comments.load_document():
        print(processor_comments.get_comments_formatted())
    else:
        logger.error("Failed to load document for comments extraction.")

    # 6. Final Draft (all additions accepted, all deletions ignored, no comments)
    logger.info("\n--- 6. Final Draft ---")
    processor_final = WordProcessor(docx_filepath)
    if processor_final.load_document():
        print(processor_final.get_final_draft())
    else:
        logger.error("Failed to load document for final draft.")

    # 7. Original Draft (all additions ignored, all deletions included, no comments)
    logger.info("\n--- 7. Original Draft ---")
    processor_original = WordProcessor(docx_filepath)
    if processor_original.load_document():
        print(processor_original.get_original_draft())
    else:
        logger.error("Failed to load document for original draft.")

    logger.info("\nWord document processing script finished.")

if __name__ == "__main__":
    main()

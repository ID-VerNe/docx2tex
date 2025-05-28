from word_review_parser.core import WordProcessor
import os

# 假设您的测试文件在当前目录
filepath = "example_with_comments_and_revisions.docx"

if not os.path.exists(filepath):
    print(f"错误：文件 '{filepath}' 不存在。请确保文件在当前目录。")
else:
    processor = WordProcessor(filepath)
    if processor.load_document():
        print("\n--- 文档段落 ---")
        for paragraph in processor.read_paragraphs():
            print(paragraph)

        print("\n--- 文档修订 ---")
        for revision in processor.read_revisions():
            print(revision)

        print("\n--- 文档评论 ---")
        for comment in processor.read_comments():
            print(comment)

        print("\n--- 格式化后的文档 ---")
        formatted_doc = processor.get_document_with_revisions_and_comments_formatted()
        print(formatted_doc)
    else:
        print(f"无法加载文档：{filepath}")

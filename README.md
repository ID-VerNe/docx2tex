# word-review-parser

`word-review-parser` 是一个Python库，旨在帮助您解析Microsoft Word文档（.docx）中的审阅标记，包括修订（插入和删除的文本）和批注，**以及将带有特定标记的LaTeX文本转换为带有Word审阅标记的.docx文件**。它提供了一种以结构化方式访问这些信息的方法，并能将文档内容与审阅标记一起格式化输出为易于阅读的文本格式，例如类似LaTeX的 `\added{}` 和 `\deleted{}` 语法。

## 核心功能

*   **文档加载**：加载 `.docx` 文件。
*   **段落读取**：提取文档中的所有段落文本。
*   **批注提取**：获取批注的ID、作者、日期和文本内容。
*   **修订提取**：识别并提取插入（`\added{}`）和删除（`\deleted{}`）的文本，包括作者和日期。
*   **格式化输出**：将整个文档内容（包括段落、修订和批注）格式化为纯文本字符串，支持自定义标记。
*   **多种输出模式**：允许单独输出增加的文本、删除的文本、批注、最终稿（接受所有修订，忽略批注）和原始稿（拒绝所有修订，忽略批注）。
*   **LaTeX到Word转换**：将带有特定标记的LaTeX文本转换为带有Word审阅标记的.docx文件。

## 安装

您可以通过 `pip` 从 PyPI 安装此库：

```bash
pip install word-review-parser
```

## GitHub 仓库

您可以在 GitHub 上找到此项目的源代码：

[https://github.com/ID-VerNe/docx2tex](https://github.com/ID-VerNe/docx2tex)

## 许可证

本项目采用 MIT 许可证。详情请参阅仓库中的 `LICENSE` 文件。

## 项目结构

```
word_review_2_tex/
├── src/
│   ├── word_review_parser/
│   │   ├── __init__.py             # 库的入口，暴露主要API
│   │   ├── core.py                 # 核心逻辑：Word文档XML解析、文本提取、格式化
│   │   ├── latex_parser.py         # LaTeX文本解析器
│   │   ├── models.py               # 数据模型定义（如 Comment, Revision 类）
│   │   └── word_builder.py         # Word文档构建器
├── interface/                      # 命令行接口示例
│   └── cli.py
└── README.md                       
```

## 使用方法

库的核心功能封装在 `src/word_review_parser/core.py` 中的 `WordProcessor` 类里。

### 1. `WordProcessor` 类初始化

`WordProcessor` 类现在直接在初始化时接收 `.docx` 文件路径。您还可以自定义用于标记插入、删除和批注的字符串。

```python
from word_review_parser import WordProcessor
import os

# 假设您的文档在项目根目录
docx_filepath = "example_with_comments_and_revisions.docx" 
# 或者提供完整路径，例如：docx_filepath = "/path/to/your/document.docx"

# 默认初始化 (使用 LaTeX 风格标记)
processor_default = WordProcessor(docx_filepath)

# 自定义标记初始化 (例如，Markdown 风格)
processor_custom_tags = WordProcessor(
    docx_filepath,
    added_tag_start="**++", added_tag_end="++**",
    deleted_tag_start="~~--", deleted_tag_end="--~~",
    comment_tag_start="[COMMENT: ", comment_tag_end="]"
)

# 加载文档
if not processor_default.load_document():
    print("文档加载失败。")
    exit()

# --- 示例用法 ---

# a. 读取所有段落
print("\n--- 文档段落 ---")
for i, paragraph_text in enumerate(processor_default.read_paragraphs()):
    print(f"段落 {i+1}: {paragraph_text}")

# b. 读取所有批注
print("\n--- 文档批注 ---")
comments_list = list(processor_default.read_comments())
if comments_list:
    for i, comment in enumerate(comments_list):
        print(f"批注 {i+1}:")
        print(f"  作者: {comment['author']}")
        print(f"  日期: {comment['date']}")
        print(f"  文本: {comment['text']}")
else:
    print("未找到批注。")

# c. 读取所有修订（插入/删除）
print("\n--- 文档修订 ---")
revisions_list = list(processor_default.read_revisions())
if revisions_list:
    for i, revision in enumerate(revisions_list):
        print(f"修订 {i+1}:")
        print(f"  类型: {revision['type']}")
        print(f"  作者: {revision['author']}")
        print(f"  日期: {revision['date']}")
        print(f"  文本: {revision['text']}")
else:
    print("未找到修订。")

# d. 获取包含修订和批注的格式化文档文本 (使用默认标记)
print("\n--- 格式化文档（含修订和批注，默认标记）---")
formatted_doc_text = processor_default.get_document_with_revisions_and_comments_formatted()
print(formatted_doc_text)

# e. 获取包含修订和批注的格式化文档文本 (使用自定义标记)
print("\n--- 格式化文档（含修订和批注，自定义标记）---")
if processor_custom_tags.load_document(): # 重新加载文档以使用自定义处理器
    formatted_doc_text_custom = processor_custom_tags.get_document_with_revisions_and_comments_formatted()
    print(formatted_doc_text_custom)
else:
    print("文档加载失败，无法使用自定义标记进行格式化。")

# f. 单独输出各种类型的内容
print("\n--- 仅输出增加的文本 ---")
print(processor_default.get_added_text_formatted())

print("\n--- 仅输出删除的文本 ---")
print(processor_default.get_deleted_text_formatted())

print("\n--- 仅输出批注 ---")
print(processor_default.get_comments_formatted())

print("\n--- 输出最终稿（接受所有修订，忽略批注）---")
print(processor_default.get_final_draft())

print("\n--- 输出原始稿（忽略所有修订，包含删除的文本，忽略批注）---")
print(processor_default.get_original_draft())

# g. 文本替换（注意：此功能在处理带修订/批注的文档时有局限性，不推荐直接使用）
# old_text = "示例文本" # Change this to text present in your file
# new_text = "替换后的示例文本"
# output_filepath = "./modified_" + os.path.basename(docx_filepath)
# processor_default.replace_text(old_text, new_text)
# processor_default.save_document(output_filepath)
# print(f"\n已尝试文本替换并保存到: {output_filepath}")
# print("警告：直接文本替换在带修订/批注的文档上不推荐。")
```

### 2. 命令行接口示例 (`interface/cli.py`)

`interface/cli.py` 文件提供了一个全面的命令行接口，演示了 `WordProcessor` 类的所有新功能。您可以直接运行它来测试：

```bash
python interface/cli.py
```

### 3. `LatexParser` 类使用方法

`LatexParser` 类用于解析包含特定标记（如 `\added{}`, `\deleted{}`, `\replaced{}{}`, `\highlight{}`, `\comment{}`）的LaTeX文本。

```python
from word_review_parser import LatexParser

latex_text = r"""
这是一个示例文本。
\added{这是新增的内容。}
\deleted{这是被删除的内容。}
\replaced{这是新的内容}{这是被替换的旧内容}。
\highlight{这是需要高亮的内容}。
这是一个\comment{这是一个批注}示例。
"""

parser = LatexParser()
parsed_data = list(parser.parse_text(latex_text))

print("\n--- 解析后的LaTeX标记 ---")
for tag in parsed_data:
    print(tag)
```

### 4. `WordBuilder` 类使用方法

`WordBuilder` 类用于将解析后的LaTeX数据构建成一个带有Word审阅标记（修订和批注）的.docx文件。您需要提供一个Word模板文件和输出文件路径。Word文件模板可以在[https://github.com/ID-VerNe/docx2tex/blob/master/word_template_base.7z](https://github.com/ID-VerNe/docx2tex/blob/master/word_template_base.7z)下载，请解压后放到某个目录，然后用template_path向WordBuilder该参数。

```python
from word_review_parser import WordBuilder
import os

# 假设您有一个名为 'word_template_base' 的解压后的Word模板目录，
template_path = "word_template_base" 
output_path = "output_docs/converted_from_latex.docx"

# 确保输出目录存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 假设 parsed_data 是您从 LatexParser 获得的解析结果列表
# parsed_data = [...] 

builder = WordBuilder(template_path, output_path)
success = builder.build_document(latex_text, parsed_data) # 需要原始latex_text和解析数据

if success:
    print(f"\n成功生成Word文档: {output_path}")
else:
    print("\n生成Word文档失败。")
```

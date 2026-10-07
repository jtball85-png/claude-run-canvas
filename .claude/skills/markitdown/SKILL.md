---
name: markitdown
description: Convert files (Word, PowerPoint, Excel, images, audio, HTML, CSV/JSON/XML, ZIP, EPub, YouTube URLs) to Markdown for easier reading, summarizing, or editing. Use when asked to read or summarize a file type Claude Code's Read tool doesn't handle directly, or when a working Markdown copy of a document is needed.
---

# markitdown

Thin wrapper around Microsoft's `markitdown` CLI, which converts documents to Markdown.

Source: https://github.com/microsoft/markitdown

## When to use

- The file type isn't one Claude Code's Read tool already handles directly — Word, PowerPoint, Excel, audio (transcription), a YouTube URL, or a ZIP of mixed documents.
- A working `.md` copy of a document is needed so it can be edited further.

Not needed for PDFs (Read handles those directly) or files that are already plain text/Markdown — just read those normally.

## Setup (check before first use)

```bash
markitdown --version
```

If not found, install it — this is a normal pip install, confirm with the user first if there's any doubt it's wanted:

```bash
pip install 'markitdown[all]'
```

(`[all]` pulls in the optional converters — OCR, audio transcription, etc.)

## Usage

```bash
markitdown path-to-file.docx > output.md
# or explicitly:
markitdown path-to-file.pptx -o output.md
```

Same pattern for `.xlsx`, images (OCR), audio (transcription), `.html`, `.csv`/`.json`/`.xml`, `.zip`, `.epub`, and YouTube URLs (pass the URL directly in place of a path). Read the resulting `.md` file normally once converted.

## Notes

- No API keys required for the core converters.
- For interactive, repeated use within a long session, markitdown also ships an MCP server (`markitdown-mcp` on PyPI) exposing a `convert_to_markdown` tool. Not needed for one-off conversions — the CLI handles those fine.


import bibtexparser
import os

# Paths
INPUT_BIB = "_data/publications.bib"
OUTPUT_MD = "_pages/publications.md"

# Load BibTeX
with open(INPUT_BIB, "r", encoding="utf-8") as bibfile:
    bib_database = bibtexparser.load(bibfile)

# Sort entries by year (descending)
entries = sorted(bib_database.entries, key=lambda x: x.get("year", "0000"), reverse=True)

# Start writing the markdown content
lines = [
    "---",
    "layout: single",
    "title: \"Publications\"",
    "permalink: /publications/",
    "---",
    ""
]

current_year = None

for entry in entries:
    year = entry.get("year", "n.d.")
    if year != current_year:
        lines.append(
            f'<div style="display: flex; align-items: center; margin: 2em 0;">\n'
            f'<hr style="flex: 1; border: none; border-top: 1px solid #888;">\n'
            f'<span style="padding: 0 1em; white-space: nowrap; font-weight: bold;">{year}</span>\n'
            f'<hr style="flex: 1; border: none; border-top: 1px solid #888;">\n'
            f'</div>\n'
        )
        lines.append("")
        current_year = year

    authors = entry.get("author", "").replace("{", "").replace("}", "")
    title = entry.get("title", "").replace("{", "").replace("}", "").strip()
    venue = entry.get("booktitle") or entry.get("journal") or ""
    pdf = entry.get("pdf", "")
    code = entry.get("code", "")
    project = entry.get("project", "")
    url = entry.get("url", "")

    # Construct the entry
    entry_lines = [f"**{authors}** ({year}).  \n“{title}”  \n*{venue}*."]
    links = []
    if pdf:
        links.append(f"[PDF]({pdf})")
    if code:
        links.append(f"[Code]({code})")
    if project:
        links.append(f"[Project Page]({project})")
    if url and not pdf and not project and not code:
        links.append(f"[Link]({url})")

    if links:
        entry_lines.append(" " + " ".join(links))

    entry_lines.append("")  # Blank line between entries
    lines.extend(entry_lines)

# Write output
os.makedirs("_pages", exist_ok=True)
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

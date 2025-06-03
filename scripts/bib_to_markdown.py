
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
    "sidebar:",
    "  nav: main",
    "---",
    ""
]

for entry in entries:
    authors = entry.get("author", "").replace("{", "").replace("}", "")
    year = entry.get("year", "n.d.")
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

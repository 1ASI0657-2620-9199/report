"""Insert the three requested Sprint 3 sections and original screenshots in Word.

Uses the existing document as the package so its earlier content, relationships
and images survive. Run once per input document; refuses duplicate insertion.
"""

from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import quote
from zipfile import ZipFile

from lxml import etree

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.opc.constants import RELATIONSHIP_TYPE as RT


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "capitulos/05-implementacion.md"
OUTPUT = ROOT / "entrega/FinanZen-Reporte-Actualizado.docx"
EVIDENCE = ROOT / "evidencias/sprint-3/docker"
GITHUB = "https://github.com/1ASI0657-2620-9199/report/blob/main/"
START = "### 5.3.3. Sprint 3"
END = "## Pendientes que requieren evidencia externa"


def digest(data):
    return sha256(data).hexdigest()


def media(path):
    with ZipFile(path) as archive:
        return {name: digest(archive.read(name)) for name in archive.namelist()
                if name.startswith("word/media/")}


def target_url(target):
    if re.match(r"https?://", target):
        return target
    resolved = (CHAPTER.parent / target).resolve()
    assert resolved.exists(), target
    return GITHUB + quote(resolved.relative_to(ROOT).as_posix())


def inline(paragraph, text, small=False):
    pattern = r"(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|`[^`]+`)"
    for token in re.split(pattern, text):
        if not token:
            continue
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token)
        if link:
            hyperlink = OxmlElement("w:hyperlink")
            rid = paragraph.part.relate_to(target_url(link[2]), RT.HYPERLINK, is_external=True)
            hyperlink.set(qn("r:id"), rid)
            run = OxmlElement("w:r")
            props = OxmlElement("w:rPr")
            style = OxmlElement("w:rStyle")
            style.set(qn("w:val"), "Hyperlink")
            props.append(style)
            run.append(props)
            node = OxmlElement("w:t")
            node.text = link[1]
            run.append(node)
            hyperlink.append(run)
            paragraph._p.append(hyperlink)
        else:
            run = paragraph.add_run(token[2:-2] if token.startswith("**") else
                                    token[1:-1] if token.startswith("`") else token)
            if token.startswith("**"):
                run.bold = True
            if token.startswith("`"):
                run.font.name = "Consolas"
            if small:
                run.font.size = Pt(9)


def main():
    document = Document(OUTPUT)
    assert not any(p.style.name == "Heading 3" and p.text.startswith("5.3.3.")
                   for p in document.paragraphs), "Sprint 3 already inserted; restore the input before rerunning."
    anchor = next(p for p in document.paragraphs
                  if p.text == "Pendientes que requieren evidencia externa")
    original_body = [etree.tostring(element) for element in document._element.body
                     if element.tag != qn("w:sectPr")]
    original_media = media(OUTPUT)
    before_hash = digest(OUTPUT.read_bytes())
    backup = Path(tempfile.gettempdir()) / ("FinanZen-before-sprint3-" + before_hash[:12] + ".docx")
    if not backup.exists():
        shutil.copy2(OUTPUT, backup)

    def place(element):
        anchor._p.addprevious(element)

    def paragraph(text="", style=None, small=False):
        p = document.add_paragraph(style=style)
        inline(p, text, small)
        p.paragraph_format.space_after = Pt(7)
        place(p._p)
        return p

    source = CHAPTER.read_text(encoding="utf-8")
    start = source.index(START)
    end = source.find(END, start)
    block = source[start:end if end >= 0 else len(source)]
    lines = block.splitlines()
    pictures = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = re.match(r"^(#{3,4}) (.+)$", line)
        picture = re.fullmatch(r"!\[([^\]]+)\]\(([^)]+)\)", line)
        if heading:
            p = paragraph(heading[2], "Heading " + str(len(heading[1])))
            p.paragraph_format.keep_with_next = True
            if len(heading[1]) == 3:
                p.paragraph_format.page_break_before = True
        elif picture:
            path = (CHAPTER.parent / picture[2]).resolve()
            p = document.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            p.add_run().add_picture(str(path), width=Inches(6.45))
            place(p._p)
            caption = paragraph(picture[1], small=True)
            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pictures.append({"path": path.relative_to(ROOT).as_posix(),
                             "sha256": digest(path.read_bytes()), "caption": picture[1]})
        elif line.startswith("~~~"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("~~~"):
                code.append(lines[i])
                i += 1
            p = document.add_paragraph()
            run = p.add_run("\n".join(code))
            run.font.name = "Consolas"
            run.font.size = Pt(9)
            p.paragraph_format.left_indent = Inches(0.12)
            place(p._p)
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    rows.append(cells)
                i += 1
            i -= 1
            table = document.add_table(rows=len(rows), cols=len(rows[0]))
            table.style = "Table Grid"
            for row_index, cells in enumerate(rows):
                for cell, value in zip(table.rows[row_index].cells, cells):
                    p = cell.paragraphs[0]
                    inline(p, value, small=True)
                    p.paragraph_format.space_after = Pt(3)
                    if row_index == 0:
                        for run in p.runs:
                            run.bold = True
                # A table row stays on a single page; repeat the header.
                props = table.rows[row_index]._tr.get_or_add_trPr()
                props.append(OxmlElement("w:cantSplit"))
                if row_index == 0:
                    props.append(OxmlElement("w:tblHeader"))
            place(table._tbl)
            paragraph()
        else:
            paragraph(line)
        i += 1

    assert len(pictures) == 9, len(pictures)
    # Earlier body elements remain byte-identical; new elements are only inserted.
    remaining = iter(document._element.body)
    for old in original_body:
        assert any(etree.tostring(element) == old for element in remaining), "Earlier content changed."
    candidate = OUTPUT.with_name(OUTPUT.stem + ".candidate.docx")
    document.save(candidate)
    after_media = media(candidate)
    assert all(after_media.get(name) == value for name, value in original_media.items())
    assert len(after_media) == len(original_media) + 9
    assert all(item["sha256"] in after_media.values() for item in pictures)
    reopened = Document(candidate)
    headings = [p.text for p in reopened.paragraphs
                if p.style.name.startswith("Heading") and p.text.startswith("5.3.3.")]
    assert len(headings) == 4
    candidate.replace(OUTPUT)
    result = {
        "source_document_sha256": before_hash,
        "updated_document_sha256": digest(OUTPUT.read_bytes()),
        "original_media_count": len(original_media),
        "updated_media_count": len(after_media),
        "earlier_body_elements_preserved": True,
        "original_media_preserved_byte_for_byte": True,
        "headings_inserted": headings,
        "pictures_inserted": pictures,
        "original_media_sha256": original_media,
    }
    (EVIDENCE / "validacion-word.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"document": OUTPUT.name, "original_media": len(original_media),
                      "updated_media": len(after_media), "new_screenshots": len(pictures),
                      "earlier_content_preserved": True}, ensure_ascii=True))


if __name__ == "__main__":
    main()

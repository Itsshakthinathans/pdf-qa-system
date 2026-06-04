import fitz


def list_to_markdown_table(rows):
    if not rows:
        return ""
    cleaned_rows = []
    for row in rows:
        cleaned_row = []
        for cell in row:
            if cell is None or not cell.strip():
                cleaned_row.append("-")
            else:
                cleaned_row.append(cell.replace("\n", " ").strip())
        cleaned_rows.append(cleaned_row)
    header = cleaned_rows[0]
    body = cleaned_rows[1:]
    markdown = "| " + " | ".join(header) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
    for row in body:
        if len(row) < len(header):
            row += ["-"] * (len(header) - len(row))
        markdown += "| " + " | ".join(row[:len(header)]) + " |\n"
    return markdown


def parse_page_hybrid(page):
    tables = page.find_tables()
    table_list = []
    
    for tab in tables.tables:
        extracted = tab.extract()
        if not extracted:
            continue
            
        valid_rows = []
        spillover_text = ""
        
        for r_idx, row in enumerate(extracted):
            non_empty = [c for c in row if c is not None and c.strip()]
            
            # Heuristic for spillover: if a row contains only 1 non-empty cell and it is long
            if r_idx > 1 and len(non_empty) == 1:
                val = non_empty[0]
                if len(val) > 150 or val.count("\n") > 2:
                    # Gather this row and all subsequent rows as spillover plain text
                    spillover_parts = []
                    for remaining_row in extracted[r_idx:]:
                        rem_vals = [c for c in remaining_row if c is not None and c.strip()]
                        if rem_vals:
                            spillover_parts.extend(rem_vals)
                    spillover_text = "\n".join(spillover_parts)
                    break
            
            valid_rows.append(row)
            
        if valid_rows:
            md_table = list_to_markdown_table(valid_rows)
            table_list.append({
                "bbox": tab.bbox,
                "markdown": md_table,
                "spillover": spillover_text,
                "inserted": False
            })
            
    blocks = page.get_text("blocks")
    page_parts = []
    
    def get_overlap_ratio(bbox1, bbox2):
        x0 = max(bbox1[0], bbox2[0])
        y0 = max(bbox1[1], bbox2[1])
        x1 = min(bbox1[2], bbox2[2])
        y1 = min(bbox1[3], bbox2[3])
        if x1 > x0 and y1 > y0:
            overlap_area = (x1 - x0) * (y1 - y0)
            block_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
            if block_area <= 0:
                return 0.0
            return overlap_area / block_area
        return 0.0

    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        block_bbox = (x0, y0, x1, y1)
        
        overlap_table = None
        for tab in table_list:
            if get_overlap_ratio(block_bbox, tab["bbox"]) > 0.5:
                overlap_table = tab
                break
                
        if overlap_table:
            if not overlap_table["inserted"]:
                page_parts.append(overlap_table["markdown"])
                if overlap_table["spillover"]:
                    page_parts.append(overlap_table["spillover"])
                overlap_table["inserted"] = True
            continue
            
        page_parts.append(text)
        
    return "\n\n".join(page_parts)


def extract_text(pdf_path):
    pages = []

    pdf_document = fitz.open(pdf_path)

    for page in pdf_document:
        text = parse_page_hybrid(page)
        if text.strip():
            pages.append({
                "text": text,
                "page_number": page.number + 1
            })

    pdf_document.close()

    return pages
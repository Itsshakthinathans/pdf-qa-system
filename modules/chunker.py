def create_chunks(pages, chunk_size=1000, overlap=200):
    """
    Split page-annotated text into overlapping chunks using hierarchical separators.

    Parameters:
        pages (list[dict] or str): Page dicts with text and page_number, or raw string.
        chunk_size (int): Max size of each chunk.
        overlap (int): Overlap size.

    Returns:
        list[dict]: List of chunks with 'text' and 'page_numbers'.
    """
    if isinstance(pages, str):
        pages = [{"text": pages, "page_number": 1}]

    separators = ["\n\n", "\n", ". ", " ", ""]

    def get_joined_len(doc_list, sep):
        if not doc_list:
            return 0
        return sum(len(p[0]) for p in doc_list) + len(sep) * (len(doc_list) - 1)

    def _split_text(text: str, separators: list[str]) -> list[tuple[str, int]]:
        if len(text) <= chunk_size or not separators:
            return [(text, 0)]

        separator = separators[0]
        next_separators = separators[1:]

        splits = []
        if separator == "":
            splits = [(c, i) for i, c in enumerate(text)]
        else:
            parts = text.split(separator)
            curr = 0
            for part in parts:
                splits.append((part, curr))
                curr += len(part) + len(separator)

        good_splits = []
        for part, part_offset in splits:
            if len(part) > chunk_size:
                sub_splits = _split_text(part, next_separators)
                for sub_part, sub_offset in sub_splits:
                    good_splits.append((sub_part, part_offset + sub_offset))
            else:
                good_splits.append((part, part_offset))

        chunks = []
        current_doc = []

        for part, part_offset in good_splits:
            if not part.strip():
                continue

            sep_to_use = separator

            test_doc = current_doc + [(part, part_offset)]
            test_len = get_joined_len(test_doc, sep_to_use)

            if current_doc and test_len > chunk_size:
                chunk_text = sep_to_use.join([p[0] for p in current_doc])
                chunk_start = current_doc[0][1]
                chunks.append((chunk_text, chunk_start))

                while current_doc:
                    current_doc.pop(0)
                    temp_doc = current_doc + [(part, part_offset)]
                    if get_joined_len(temp_doc, sep_to_use) <= chunk_size and get_joined_len(current_doc, sep_to_use) <= overlap:
                        break

            current_doc.append((part, part_offset))

        if current_doc:
            chunk_text = sep_to_use.join([p[0] for p in current_doc])
            chunk_start = current_doc[0][1]
            chunks.append((chunk_text, chunk_start))

        return chunks

    result_chunks = []
    
    for p in pages:
        page_text = p.get("text", "")
        page_num = p.get("page_number", 1)
        
        raw_chunks = _split_text(page_text, separators)
        
        for chunk_text, _ in raw_chunks:
            if chunk_text.strip():
                result_chunks.append({
                    "text": chunk_text,
                    "page_numbers": [page_num]
                })

    return result_chunks
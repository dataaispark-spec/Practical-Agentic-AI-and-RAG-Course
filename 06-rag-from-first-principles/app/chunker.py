from .models import Chunk, Document


def chunk_document(document: Document, max_chars: int = 500, overlap: int = 50) -> list[Chunk]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap must satisfy 0 <= overlap < max_chars")

    text = " ".join(document.text.split())
    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        piece = text[start:end].strip()
        if piece:
            metadata = dict(document.metadata)
            metadata["chunk_index"] = index
            chunks.append(Chunk(f"{document.document_id}-c{index:04d}", document.document_id, piece, metadata))
            index += 1
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks

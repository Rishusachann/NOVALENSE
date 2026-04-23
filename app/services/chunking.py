def chunk_sentences(sentences: list[str], chunk_size: int = 5) -> list[str]:
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks

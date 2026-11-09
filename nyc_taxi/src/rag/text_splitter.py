
import re


def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Découpe le texte en chunks en respectant les titres Markdown."""

    if chunk_size <= 0:
        raise ValueError("chunk_size doit être positif.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap doit être positif ou nul et inférieur à chunk_size."
        )

    # Repérer les titres Markdown : #, ##, ###, etc.
    heading_pattern = re.compile(r"(?m)^#{1,6}\s+.+$")

    # Trouver les positions de tous les titres.
    headings = list(heading_pattern.finditer(text))

    if not headings:
        return _split_paragraphs(text, chunk_size, overlap)

    # Découper le document en sections commençant par un titre.
    sections = []
    start = 0

    for heading in headings:
        if heading.start() > start:
            content = text[start:heading.start()].strip()
            if content:
                sections.append(content)

        start = heading.start()

    # Ajouter la dernière section.
    content = text[start:].strip()
    if content:
        sections.append(content)

    # Découper chaque section sans mélanger les sections voisines.
    chunks = []

    for section in sections:
        if len(section) <= chunk_size:
            chunks.append(section)
        else:
            chunks.extend(
                _split_paragraphs(section, chunk_size, overlap)
            )

    return chunks


def _split_paragraphs(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    """Découpe un texte long en privilégiant les paragraphes."""

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    chunks = []
    current_paragraphs = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)
        separator_length = 2 if current_paragraphs else 0

        proposed_length = (
            current_length + separator_length + paragraph_length
        )

        if current_paragraphs and proposed_length > chunk_size:
            chunks.append("\n\n".join(current_paragraphs))

            # Garder les derniers paragraphes si leur taille le permet.
            overlap_paragraphs = []
            overlap_length = 0

            for previous in reversed(current_paragraphs):
                added_length = len(previous) + (
                    2 if overlap_paragraphs else 0
                )

                if overlap_length + added_length > overlap:
                    break

                overlap_paragraphs.insert(0, previous)
                overlap_length += added_length

            current_paragraphs = overlap_paragraphs
            current_length = overlap_length

        separator_length = 2 if current_paragraphs else 0
        current_paragraphs.append(paragraph)
        current_length += separator_length + paragraph_length

    if current_paragraphs:
        chunks.append("\n\n".join(current_paragraphs))

    return chunks


#
# def split_text2(
#     text: str,
#     chunk_size: int = 1000,
#     overlap: int = 150,
# ) -> list[str]:
#     """Découpe le texte en chunks en privilégiant les paragraphes."""
#
#     if chunk_size <= 0:
#         raise ValueError("chunk_size doit être positif.")
#
#     if overlap < 0 or overlap >= chunk_size:
#         raise ValueError(
#             "overlap doit être positif ou nul et inférieur à chunk_size."
#         )
#
#     # Séparer le texte en paragraphes non vides.
#     paragraphs = [
#         paragraph.strip()
#         for paragraph in text.split("\n\n")
#         if paragraph.strip()
#     ]
#
#     chunks = []
#     current_paragraphs = []
#     current_length = 0
#
#     for paragraph in paragraphs:
#         paragraph_length = len(paragraph)
#
#         # Taille du chunk si on ajoute ce paragraphe.
#         separator_length = 2 if current_paragraphs else 0
#         proposed_length = (
#             current_length + separator_length + paragraph_length
#         )
#
#         # Si le chunk devient trop grand, on le termine.
#         if current_paragraphs and proposed_length > chunk_size:
#             chunks.append("\n\n".join(current_paragraphs))
#
#             # Conserver des paragraphes entiers en chevauchement,
#             # tant que leur taille reste dans la limite demandée.
#             overlap_paragraphs = []
#             overlap_length = 0
#
#             for previous in reversed(current_paragraphs):
#                 added_length = len(previous) + (
#                     2 if overlap_paragraphs else 0
#                 )
#
#                 if overlap_length + added_length > overlap:
#                     break
#
#                 overlap_paragraphs.insert(0, previous)
#                 overlap_length += added_length
#
#             current_paragraphs = overlap_paragraphs
#             current_length = overlap_length
#
#         # Ajouter le paragraphe, même s'il dépasse seul la cible.
#         separator_length = 2 if current_paragraphs else 0
#         current_paragraphs.append(paragraph)
#         current_length += separator_length + paragraph_length
#
#     if current_paragraphs:
#         chunks.append("\n\n".join(current_paragraphs))
#
#     return chunks

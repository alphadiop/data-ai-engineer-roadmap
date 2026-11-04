

from nyc_taxi.src.rag.document_loader import load_markdown_documents
from nyc_taxi.src.rag.text_splitter import split_text


documents = load_markdown_documents("nyc_taxi/docs")

for document in documents:
    for chunk in split_text(document["content"]):
        content = chunk.lower()

        if any(
            term in content
            for term in ["bronze", "silver", "gold"]
        ):
            print(f"\nSource : {document['source']}")
            print(f"Longueur : {len(chunk)} caractères")
            print("-" * 70)
            print(chunk)
            print("=" * 70)



# from pathlib import Path
#
# from nyc_taxi.src.rag.document_loader import load_markdown_documents
# from nyc_taxi.src.rag.text_splitter import split_text
#
#
# path = Path("nyc_taxi/docs/data_model.md")
# lines = path.read_text(encoding="utf-8").splitlines()
#
# print("--- Documentation enregistrée ---")
# print("\n".join(lines[330:350]))
#
# print("\n--- Chunks contenant les termes recherchés ---")
#
# documents = load_markdown_documents("nyc_taxi/docs")
#
# for document in documents:
#     for chunk in split_text(document["content"]):
#         content = chunk.lower()
#
#         if "total_amount" in content or "chiffre d'affaires" in content:
#             print(f"\nSource : {document['source']}")
#             print(chunk[:700])

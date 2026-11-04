
from pathlib import Path


def load_markdown_documents(docs_dir: str) -> list[dict]:
    """
    Charge les fichiers Markdown d'un dossier.

    Retourne une liste de documents contenant :
    - source : nom du fichier ;
    - content : contenu textuel.
    """

    documents_exclus = {
        "rag_learning_recap.md",
        "rag_learning_recap3.md"
        "rag_assistant_roadmap.md",
        "generation_reponse_llm.md"
    }

    directory = Path(docs_dir)

    if not directory.exists():
        raise FileNotFoundError(
            f"Le dossier documentaire n'existe pas : {directory}"
        )

    documents = []

    for file_path in sorted(directory.glob("*.md")):
        if file_path.name in documents_exclus:
            continue

        content = file_path.read_text(encoding="utf-8")

        if content.strip():
            documents.append({
                    "source": file_path.name,
                    "content": content,
            })

    return documents


import requests

from nyc_taxi.src.rag.embedding_index import search_documents


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_answer(question: str, context: str) -> str:
    # prompt = f"""
    #             Tu es un assistant spécialisé dans le projet de données NYC Taxi.
    #
    #             Réponds en français à la question en utilisant uniquement le contexte fourni.
    #             Si le contexte ne contient pas suffisamment d'informations, indique-le clairement.
    #             N'invente ni formule SQL, ni indicateur, ni résultat.
    #
    #             CONTEXTE DOCUMENTAIRE :
    #             {context}
    #
    #             QUESTION :
    #             {question}
    #
    #             RÉPONSE :
    #         """

    prompt = f"""
            Tu es un assistant technique spécialisé dans le projet de données NYC Taxi.

            RÈGLES :
            - Réponds en français, de façon claire et concise.
            - Utilise uniquement les informations présentes dans le contexte.
            - Pour une question SQL, donne une requête SQL complète si le contexte le permet.
            - Pour une question Power BI, utilise la syntaxe DAX exacte si elle est documentée.
            - Explique précisément ce que fait chaque formule.
            - Distingue SQL et DAX : COUNT(*) est une fonction SQL,
              COUNTROWS est une fonction DAX.
            - Si la question porte sur une période, explique le rôle des filtres
              uniquement si le contexte le confirme.
            - Si une information manque, indique-le au lieu de l'inventer.
            - Ne répète pas la question.

            CONTEXTE DOCUMENTAIRE :
            {context}

            QUESTION :
            {question}

            RÉPONSE :
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,
    )

    response.raise_for_status()
    return response.json()["response"].strip()


def answer_question(question: str) -> None:
    print(f"\nQUESTION : {question}")
    print("=" * 70)

    results = search_documents(
        question=question,
        docs_dir="nyc_taxi/docs",
        top_k=5,
    )

    if not results:
        print("Aucun document pertinent trouvé.")
        return

    context_parts = []

    for rank, result in enumerate(results, start=1):
        print(
            f"\nSource {rank} : {result['source']} "
            f"(score : {result['score']:.3f})"
        )
        context_parts.append(
            f"Source : {result['source']}\n"
            f"Contenu : {result['content']}"
        )

    context = "\n\n".join(context_parts)

    print("\nGÉNÉRATION DE LA RÉPONSE...")
    answer = generate_answer(question, context)

    print("\nRÉPONSE DE QWEN")
    print("-" * 70)
    print(answer)



if __name__ == "__main__":
    questions = [
        "Quelle formule SQL utilise COUNT(*) pour compter les trajets ?",
        "Comment compter les lignes de gold_fact_trips en SQL ?",
        "Comment connaître le nombre de courses dans le tableau de bord Power BI ?",
        "Quel est le volume d'activité sur la période sélectionnée ?",
    ]

    for question in questions:
        answer_question(question)

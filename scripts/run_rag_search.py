
from nyc_taxi.src.rag.embedding_index import search_documents

#
# questions = [
#     "Comment calculer le nombre de courses ?",
#     "Comment calculer la distance moyenne des trajets ?",
#     "Quel est le rôle des couches Bronze, Silver et Gold ?",
#     "Quelle est la formule DAX de Nombre_Trajets avec COUNTROWS ?",
#     "Comment compter le nombre total de lignes dans gold_fact_trips ?",
# ]

questions = [
    "Quelle formule SQL utilise COUNT(*) pour compter les trajets ?",
    "Comment compter les lignes de gold_fact_trips en SQL ?",
    "Comment connaître le nombre de courses dans le tableau de bord ?",
    "Quel est le volume d'activité sur la période sélectionnée ?",

]

for question in questions:
    print(f"\nQUESTION : {question}")
    print("=" * 70)

    results = search_documents(
        question=question,
        docs_dir="nyc_taxi/docs",
        top_k=5,
    )

    for rank, result in enumerate(results, start=1):
        print(f"\nRang : {rank}")
        print("Source :", result["source"])
        print("Score :", round(result["score"], 3))
        print(result["content"][:500])
        print("-" * 70)



# from nyc_taxi.src.rag.embedding_index import search_documents
#
# results = search_documents(
#     question="Quelle formule SQL permet de calculer les revenus des courses ?",
#     docs_dir="nyc_taxi/docs",
#     top_k=3,
# )
#
# for result in results:
#     print("Source :", result["source"])
#     print("Score :", round(result["score"], 3))
#     print("---")
#     print(result["content"])

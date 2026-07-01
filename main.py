from pathlib import Path
from services.qa import answer_question 
from data_cache import load_data
from services.retrieval import build_index

docs = load_data()

build_index(docs)


def main():
    try:
        question = input("Ask your question: ")

        answer = answer_question(question)

        print(answer)

    except Exception as error:
        print(f"Application failed: {error}")
        raise


    



if __name__ == "__main__":
    main()
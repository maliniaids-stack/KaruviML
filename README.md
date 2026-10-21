# KaruviML

## Problem

Students often understand Machine Learning concepts better when explained in Tamil, but scikit-learn's source code and documentation are primarily in English. Students may copy code without fully understanding functions such as `fit()`, `transform()`, and `Pipeline`. This makes it difficult for them to understand how ML algorithms work internally and avoid common implementation mistakes. KaruviML bridges this language gap by allowing students to ask questions in Tamil, Tanglish, or English and receive clear explanations grounded in the original source code with citations.

## Who it is for

- Assistant professors managing Machine Learning laboratories for third-year AI and Data Science students at engineering colleges in Madurai.
- AI and Data Science students who want to understand scikit-learn code in Tamil, Tanglish, or English.

## Signature feature

Cross-language code search that matches Tamil or Tanglish questions with relevant English scikit-learn source code and returns explanations in the same language alongside cited English code lines.

## Hardest problem (my interview story)

The hardest problem is accurately matching Tamil and Tanglish questions to the correct English source code. Different language expressions and variations in Tanglish spelling make retrieval challenging. KaruviML uses multilingual embeddings to connect questions with relevant code and documentation, ensuring that generated answers are grounded in retrieved sources. I will evaluate the system by comparing Tamil-question retrieval accuracy with English-question retrieval accuracy on a bilingual test set of 60 questions, targeting a difference of no more than 10 percentage points.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---|---|---|
| scikit-learn source code and documentation | https://github.com/scikit-learn/scikit-learn | Target: 1,000+ Python and Cython source files | To be measured after ingestion | BSD-3-Clause; verify individual file and dependency licences |

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md).

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements-dev.txt

copy .env.example .env

uvicorn app.main:app --reload

curl http://localhost:8000/health
```

## Live link

To be added in Week 2, after deployment.

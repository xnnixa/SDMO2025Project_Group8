# 🧩 Project 1: Developer De-duplication

This project is part of **811372A-3007 Software Development, Maintenance and Operations**, showcasing data collection and processing for developer identity resolution in large open-source repositories.

---

## 📁 Repository Used

For this project, we used the **Servo** open-source repository, which has over 1000 contributors and 1000+ commits.

- `project1devs/`: Directory with data for Project 1
  - `devs.csv`: List of developers mined from eShopOnContainersProject
  - `devs_similarity.csv`: Similarity tests for each pair of developers
  - `devs_similarity_t=0.7.csv`: Similarity tests for each pair of developers with similarity threshold 0.7
- `project1developers.py`: Script demonstrating mining developer information and Bird heuristic to determine duplicate developers
- `project2&3traces/`: Directory with data for Projects 2 & 3
  - `train-ticket-traces.csv`: CSV file with traces for train-ticket system from an open dataset
  - `project2edgeflow.csv`: CSV file providing a list of real-time service calls for Project 2
  - `project3snapshots.csv`: CSV file providing snapshot networks for service calls grouped by intervals for Project 3
  - `project2_katz_exponential.csv`: CSV file with Temporal Katz Centrality with exponential decay
  - `project2_katz_constant.csv`: CSV file with Temporal Katz Centrality with constant decay
  - `project2_katz_truncated.csv`: CSV file with Temporal Katz Centrality with truncated exponential decay
- `project2&3data.py`: Script processing raw traces into formats required by Projects 2&3
- `project2centrality.py`: Script demonstrating temporal katz centrality on temporal edge flow network of microservice calls for Project 2
- `project3anomaly.py`: Script demonstrating temporal state detection on temporal networks of microservice calls for Project 3
- `requirements.txt`: List of used libraries with specified versions

---

## 🎯 Objective

The goal was to identify and merge duplicate developer identities that arise due to:
- Different emails used on various devices
- Misspellings, casing, or formatting differences
- Git misconfigurations (usernames instead of names)

We began with the **Bird heuristic**, implemented its logic, and then designed improved solutions using:
1. **Jaro–Winkler + Domain Weighted Matching**
2. **Semantic Similarity using Sentence Transformers + FAISS**

---

## ⚙️ Approaches and Results

| Method | Precision | Recall | F1 Score | Description |
|--------|------------|---------|-----------|--------------|
| **Bird Heuristic (t = 0.7)** | 0.066 | 0.695 | 0.121 | Baseline heuristic using Levenshtein similarity and name-prefix checks. High recall, poor precision. |
| **Improved Heuristic (Jaro–Winkler, t = 0.75)** | 0.301 | 0.375 | 0.334 | Added Jaro–Winkler similarity, domain check, and weighted scoring. Better balance between recall and precision. |
| **FAISS Semantic (t = 0.8)** | **0.411** | **0.606** | **0.490** | Used SentenceTransformer embeddings + FAISS similarity search. Achieved best trade-off between recall and accuracy. |

---

## 📊 Visual Comparison

The following chart shows how each method performs in terms of **Precision**, **Recall**, and **F1 Score**:

![Performance Comparison](week2/faiss/metrics/all%20comparisons.png)

> The semantic FAISS model achieved the **highest overall accuracy (F1 = 0.49)** while maintaining good recall and significantly reducing false positives compared to the Bird baseline.

---

## 🧠 Insights

- **Bird heuristic** → detects many duplicates but produces too many false positives.  
- **Improved heuristic** → balances precision and recall by filtering weak matches.  
- **FAISS semantic model** → semantically understands name variations and nicknames, providing the most robust solution.

---

## 📦 Tools & Libraries

- **PyDriller** → commit mining  
- **pandas** → data handling  
- **python-Levenshtein** → similarity scoring (Bird)  
- **jellyfish** → Jaro–Winkler similarity  
- **SentenceTransformers** → text embeddings  
- **FAISS** → scalable vector similarity search  
- **matplotlib** → visualization  

---

## 📁 Folder Structure

```text
SDMO2025Project_Group8/
│
├── week1/
│   ├── devs/                     # Bird heuristic outputs
│   ├── metrics/bird/             # Bird metrics and charts
│   └── project1developers.py     # Bird heuristic implementation
│
├── week2/
│   ├── jaro-winkler/             # Improved heuristic (Jaro–Winkler)
│   ├── faiss/                    # Semantic + FAISS implementation
│   └── metrics/                  # Visual and CSV performance reports
│
└── README.md

```

---

## 🧾 Conclusion

The **semantic FAISS-based model** demonstrates the best trade-off between accuracy and scalability for real-world developer identity deduplication tasks.  
It efficiently handles complex name variations and minimizes manual validation, outperforming traditional heuristics like Bird’s method.

---

📈 *Group 8 SDMO2025 – University of Oulu*

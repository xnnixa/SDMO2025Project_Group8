# 🧩 Project 1: Developer De-duplication

This project is part of **811372A-3007 Software Development, Maintenance and Operations**, showcasing data collection and processing for developer identity resolution in large open-source repositories.

---

## 📁 Repository Used

For this project, we used the **Servo** open-source repository, which has over 1000 contributors and 1000+ commits.

> **Repo:** [Servo GitHub Repository](https://github.com/servo/servo.git)

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

SDMO2025Project_Group8/
│
├── week1/
│ ├── devs/ # Bird heuristic outputs
│ ├── metrics/bird/ # Bird metrics and charts
│ └── project1developers.py # Bird heuristic implementation
│
├── week2/
│ ├── jaro-winkler/ # Improved heuristic (Jaro–Winkler)
│ ├── faiss/ # Semantic + FAISS implementation
│ └── metrics/ # Visual and CSV performance reports
│
└── README.md

---

## 🧾 Conclusion

The **semantic FAISS-based model** demonstrates the best trade-off between accuracy and scalability for real-world developer identity deduplication tasks.  
It efficiently handles complex name variations and minimizes manual validation, outperforming traditional heuristics like Bird’s method.

---

📈 *Group 8 SDMO2025 – University of Oulu*

import os
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer


# ---------------------------
# Configuration
# ---------------------------
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_THRESHOLD = 0.8
DEFAULT_TOP_K = 10


# ---------------------------
# Function 1: Load Developers
# ---------------------------
def load_developers(data_path: str) -> pd.DataFrame:
    """Load and preprocess developer data from a CSV file."""
    df = pd.read_csv(data_path)
    df["name"] = df["name"].fillna("").str.lower().str.strip()
    df["email"] = df["email"].fillna("").str.lower().str.strip()
    df["prefix"] = df["email"].apply(lambda e: e.split("@")[0] if "@" in e else "")
    df["text"] = "Name: " + df["name"] + ", Email prefix: " + df["prefix"]
    return df


# ---------------------------
# Function 2: Create Embeddings
# ---------------------------
def create_embeddings(df: pd.DataFrame, model_name: str = DEFAULT_MODEL) -> np.ndarray:
    """Generate normalized embeddings for developer identities."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(df["text"].tolist(), convert_to_numpy=True, show_progress_bar=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings


# ---------------------------
# Function 3: Build FAISS Index
# ---------------------------
def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Build a FAISS index using cosine similarity."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


# ---------------------------
# Function 4: Find Similar Pairs
# ---------------------------
def find_similar_pairs(
    df: pd.DataFrame,
    index: faiss.IndexFlatIP,
    embeddings: np.ndarray,
    threshold: float = DEFAULT_THRESHOLD,
    top_k: int = DEFAULT_TOP_K
) -> pd.DataFrame:
    """Find all pairs of developers with similarity >= threshold."""
    similarities, indices = index.search(embeddings, top_k)
    pairs = []
    for i in range(len(df)):
        for j, sim in zip(indices[i], similarities[i]):
            if i >= j:  # avoid self or duplicate pairs
                continue
            if sim >= threshold:
                pairs.append([
                    df.loc[i, "name"], df.loc[i, "email"],
                    df.loc[j, "name"], df.loc[j, "email"],
                    float(sim)
                ])
    return pd.DataFrame(pairs, columns=["name_1", "email_1", "name_2", "email_2", "semantic_similarity"])


# ---------------------------
# Function 5: Save Results
# ---------------------------
def save_results(df_pairs: pd.DataFrame, output_path: str) -> None:
    """Save the resulting pairs to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_pairs.to_csv(output_path, index=False)


# ---------------------------
# Main Pipeline Function
# ---------------------------
def main(data_folder: str, threshold: float = DEFAULT_THRESHOLD, model_name: str = DEFAULT_MODEL, top_k: int = DEFAULT_TOP_K):
    """Run the FAISS semantic similarity pipeline."""
    devs_path = os.path.join(data_folder, "devs.csv")
    df = load_developers(devs_path)

    print(f"Loaded {len(df)} developer identities.")
    embeddings = create_embeddings(df, model_name)

    index = build_faiss_index(embeddings)
    df_pairs = find_similar_pairs(df, index, embeddings, threshold, top_k)

    out_path = os.path.join(data_folder, f"devs_similarity_semantic_faiss_t={threshold}.csv")
    save_results(df_pairs, out_path)

    print(f"✅ Found {len(df_pairs)} pairs with similarity >= {threshold}")
    print(f"Results saved to {out_path}")
    return df_pairs


# ---------------------------
# Script Entry Point
# ---------------------------
if __name__ == "__main__":
    data_folder = "SDMO2025Project_Group8/week2/faiss/devs"
    main(data_folder)

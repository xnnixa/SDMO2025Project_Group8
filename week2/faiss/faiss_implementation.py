import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# ---------------------------
# Configuration
# ---------------------------
data_folder = "SDMO2025Project_Group8/week2/faiss/devs"
t = 0.8   # similarity threshold
model_name = "sentence-transformers/all-MiniLM-L6-v2"
top_k = 10  # how many nearest neighbors to check per vector (can tweak)

# ---------------------------
# Step 1: Load developers
# ---------------------------
df = pd.read_csv(os.path.join(data_folder, "devs.csv"))
df["name"] = df["name"].fillna("").str.lower().str.strip()
df["email"] = df["email"].fillna("").str.lower().str.strip()
df["prefix"] = df["email"].apply(lambda e: e.split("@")[0] if "@" in e else "")

# Create a text field for embedding
df["text"] = "Name: " + df["name"] + ", Email prefix: " + df["prefix"]

print(f"Loaded {len(df)} developer identities")

# ---------------------------
# Step 2: Create embeddings
# ---------------------------
print("Encoding developer identities with SentenceTransformer...")
model = SentenceTransformer(model_name)
embeddings = model.encode(df["text"].tolist(), convert_to_numpy=True, show_progress_bar=True)

# Normalize embeddings for cosine similarity
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# ---------------------------
# Step 3: Build FAISS index
# ---------------------------
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)  # inner product = cosine similarity since vectors are normalized
index.add(embeddings)

# ---------------------------
# Step 4: Query nearest neighbors
# ---------------------------
print("Performing FAISS similarity search...")
similarities, indices = index.search(embeddings, top_k)

pairs = []
for i in range(len(df)):
    for j, sim in zip(indices[i], similarities[i]):
        if i >= j:  # avoid duplicates and self-comparison
            continue
        if sim >= t:
            pairs.append([
                df.loc[i, "name"], df.loc[i, "email"],
                df.loc[j, "name"], df.loc[j, "email"],
                float(sim)
            ])

print(f"Found {len(pairs)} pairs with similarity >= {t}")

# ---------------------------
# Step 5: Save results
# ---------------------------
out_path = os.path.join(data_folder, f"devs_similarity_semantic_faiss_t={t}.csv")
pd.DataFrame(pairs, columns=["name_1", "email_1", "name_2", "email_2", "semantic_similarity"]).to_csv(out_path, index=False)

print(f"✅ Done! Saved results to {out_path}")

import os
import numpy as np
import pandas as pd
import pytest
import faiss

# ✅ Replace this with your actual filename if different
import faiss_implementation as pipeline

# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture
def sample_data(tmp_path):
    """Create a small temporary CSV for testing."""
    df = pd.DataFrame({
        "name": ["Alice", "Alicia", "Bob"],
        "email": ["alice@example.com", "alicia@company.com", "bob@other.com"]
    })
    csv_path = tmp_path / "devs.csv"
    df.to_csv(csv_path, index=False)
    return csv_path, df


@pytest.fixture
def mock_embeddings():
    """Provide deterministic mock embeddings (3 x 4)."""
    embeddings = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.9, 0.1, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0]
    ], dtype="float32")
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings


# ---------------------------
# Unit Tests
# ---------------------------

def test_load_developers(sample_data):
    csv_path, df_original = sample_data
    df = pipeline.load_developers(csv_path)

    assert "text" in df.columns
    assert all(df["name"].str.islower())
    assert all(df["email"].str.islower())
    assert df["prefix"].iloc[0] == "alice"
    assert df["text"].iloc[0].startswith("Name: alice")


def test_create_embeddings(monkeypatch, sample_data):
    """Mock SentenceTransformer.encode to avoid model download."""
    csv_path, _ = sample_data
    df = pipeline.load_developers(csv_path)

    class MockModel:
        def encode(self, texts, convert_to_numpy=True, show_progress_bar=True):
            return np.ones((len(texts), 3))

    monkeypatch.setattr(pipeline, "SentenceTransformer", lambda _: MockModel())

    embeddings = pipeline.create_embeddings(df, "mock-model")

    assert embeddings.shape == (3, 3)
    assert np.allclose(np.linalg.norm(embeddings, axis=1), 1.0, atol=1e-6)


def test_build_faiss_index(mock_embeddings):
    index = pipeline.build_faiss_index(mock_embeddings)
    assert isinstance(index, faiss.IndexFlatIP)
    assert index.ntotal == len(mock_embeddings)


def test_find_similar_pairs(sample_data, mock_embeddings):
    csv_path, df = sample_data
    index = pipeline.build_faiss_index(mock_embeddings)

    df = pipeline.load_developers(csv_path)
    df_pairs = pipeline.find_similar_pairs(df, index, mock_embeddings, threshold=0.5, top_k=3)

    expected_cols = ["name_1", "email_1", "name_2", "email_2", "semantic_similarity"]
    assert list(df_pairs.columns) == expected_cols
    assert not df_pairs.empty
    assert any("alice" in x or "alicia" in x for x in df_pairs["name_1"].tolist() + df_pairs["name_2"].tolist())


def test_save_results(tmp_path):
    df_pairs = pd.DataFrame({
        "name_1": ["Alice"], "email_1": ["alice@example.com"],
        "name_2": ["Alicia"], "email_2": ["alicia@company.com"],
        "semantic_similarity": [0.95]
    })
    out_path = tmp_path / "results" / "pairs.csv"
    pipeline.save_results(df_pairs, str(out_path))

    assert out_path.exists()
    df_loaded = pd.read_csv(out_path)
    assert "semantic_similarity" in df_loaded.columns
    assert len(df_loaded) == 1


# ---------------------------
# Optional Integration Test
# ---------------------------
def test_main_pipeline(monkeypatch, tmp_path):
    """End-to-end test (mock embeddings + index + saving)."""
    csv_path = tmp_path / "devs.csv"
    df = pd.DataFrame({
        "name": ["Alice", "Alicia"],
        "email": ["alice@example.com", "alicia@company.com"]
    })
    df.to_csv(csv_path, index=False)

    # Mock embeddings and FAISS index
    mock_embs = np.array([[1.0, 0.0], [0.9, 0.1]], dtype="float32")
    mock_embs = mock_embs / np.linalg.norm(mock_embs, axis=1, keepdims=True)
    monkeypatch.setattr(pipeline, "create_embeddings", lambda df, model_name: mock_embs)

    def mock_build_index(embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        return index

    monkeypatch.setattr(pipeline, "build_faiss_index", mock_build_index)

    # Run pipeline
    df_pairs = pipeline.main(str(tmp_path), threshold=0.5, top_k=2)

    assert not df_pairs.empty
    assert (tmp_path / "devs_similarity_semantic_faiss_t=0.5.csv").exists()

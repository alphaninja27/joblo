import json
import os
import numpy as np

def test_vector_file():
    assert os.path.exists("public/job_vectors.json")
    with open("public/job_vectors.json") as f:
        vectors = json.load(f)
    for vec in vectors:
        arr = np.array(vec["embedding"], dtype=np.float32)
        assert arr.shape[0] == 384, "❌ Incorrect embedding dimension"
import csv
import pandas as pd
import unicodedata
import string
from itertools import combinations
from jellyfish import jaro_winkler_similarity as sim
from pydriller import Repository
import os

repo_folder = "servo"
data_folder = "new_algorithm"
t = 0.75  # new threshold for weighted score

# ---------------------------
# Step 1: Extract (name, email) pairs
# ---------------------------
DEVS = set()
for commit in Repository(repo_folder).traverse_commits():
    DEVS.add((commit.author.name, commit.author.email))
    DEVS.add((commit.committer.name, commit.committer.email))

DEVS = sorted(DEVS)

# Save to CSV
os.makedirs(data_folder, exist_ok=True)
with open(os.path.join(data_folder, "devs.csv"), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(["name", "email"])
    writer.writerows(DEVS)

# ---------------------------
# Step 2: Load developers back from CSV
# ---------------------------
DEVS = []
with open(os.path.join(data_folder, "devs.csv"), 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        DEVS.append(row)
DEVS = DEVS[1:]  # skip header

# ---------------------------
# Step 3: Helper functions
# ---------------------------
def process(dev):
    name: str = dev[0]

    # Remove punctuation
    trans = name.maketrans("", "", string.punctuation)
    name = name.translate(trans)

    # Remove accents and normalize
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])

    # Lowercase and strip
    name = name.casefold()
    name = " ".join(name.split())

    # Split into parts
    parts = name.split(" ")
    if len(parts) == 2:
        first, last = parts
    elif len(parts) == 1:
        first, last = name, ""
    else:
        first, last = parts[0], " ".join(parts[1:])

    i_first = first[0] if len(first) > 1 else ""
    i_last = last[0] if len(last) > 1 else ""

    email: str = dev[1]
    prefix = email.split("@")[0]
    domain = email.split("@")[1] if "@" in email else ""

    return name, first, last, i_first, i_last, email, prefix, domain


# ---------------------------
# Step 4: Compare pairs using weighted heuristic
# ---------------------------
SIMILARITY = []
for dev_a, dev_b in combinations(DEVS, 2):
    # Preprocess both
    name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a, domain_a = process(dev_a)
    name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b, domain_b = process(dev_b)

    # Compute similarities
    name_sim = sim(name_a, name_b)
    prefix_sim = sim(prefix_a, prefix_b)
    same_domain = (domain_a == domain_b)

    # Weighted score
    score = (0.4 * name_sim) + (0.4 * prefix_sim) + (0.2 * (1 if same_domain else 0))

    SIMILARITY.append([
        dev_a[0], email_a,
        dev_b[0], email_b,
        name_sim, prefix_sim, same_domain, score
    ])

# ---------------------------
# Step 5: Save results
# ---------------------------
cols = ["name_1", "email_1", "name_2", "email_2", "name_sim", "prefix_sim", "same_domain", "score"]
df = pd.DataFrame(SIMILARITY, columns=cols)
df.to_csv(os.path.join(data_folder, "devs_similarity_improved.csv"), index=False, header=True)

# ---------------------------
# Step 6: Apply threshold filter
# ---------------------------
df_filtered = df[df["score"] >= t]
df_filtered.to_csv(os.path.join(data_folder, f"devs_similarity_improved_t={t}.csv"), index=False, header=True)

print(f"Threshold: {t}")
print(f"Total pairs after filtering: {len(df_filtered)}")
print("Saved improved results successfully!")

import pandas as pd
import random

# Task: implement a method, that will take a query string as input and produce N misspelling variants of the query.
# These variants with typos will be used to test a search engine quality.
# Example
# Query: machine learning applications
# Possible Misspellings:
# "machin learning applications" (missing "e" in "machine")
# "mashine learning applications" (phonetically similar spelling of "machine")
# "machine lerning aplications" (missing "a" in "learning" and "p" in "applications")
# "machin lerning aplications" (combining multiple typos)
# "mahcine learing aplication" (transposed letters in "machine" and typos in "learning" and "applications")
#
# Questions:
# 1. Does the search engine produce the same results for all the variants?
# 2. Do all variants make sense?
# 3. How to improve robustness of the method, for example, skip known abbreviations, like JFK or NBC.
# 4. Can you test multiple LLMs and figure out which one is the best?
# 5. Do the misspellings capture a variety of error types (phonetic, omission, transposition, repetition)?

# Task 2. a) Find the queries in web_search_queries.csv, containing example queries from different topics and use cases, like map search, job search, travel and tourism, general knowledge and learning

df = pd.read_csv("web_search_queries.csv")
print(df.head(2))

# Task 2. b) Implement code, that will load one query at a time and generate up to N misspellings.

queries = df["Query"].tolist()

# Task 2. c) Improve robustness of the method, for example, skip known abbreviations, like JFK.

DONT_TOUCH = {"JFK"}

def do_not_touch(word):
    if word in DONT_TOUCH:
        return True
    if word.isupper() and len(word) <= 5:
        return True
    return False

# removes a letter
def typo_omission(word):
    if len(word) <= 2: return word
    i = random.randrange(len(word))
    return word[:i] + word[i+1:]

# letter changes places with nearest one
def typo_transpose(word):
    if len(word) < 2: return word
    i = random.randrange(len(word) - 1)
    return word[:i] + word[i+1] + word[i] + word[i+2:]

def typo_repetition(word):
    if len(word) == 0:
        return word
    i = random.randrange(len(word))
    return word[:i+1] + word[i] + word[i+1:]

# very small phonetic substitutions e.g. s -> z
def typo_phonetic(word):
    replacements = {"ph": "f", "f": "ph", "c": "k", "k": "c", "s": "z", "z": "s"}
    for k, v in replacements.items():
        if k in word:
            return word.replace(k, v, 1)
    return word

# typo functions
TYPO_FUNCS = [typo_omission, typo_transpose, typo_phonetic, typo_repetition]

def generate_misspelling(query):
    words = query.split()
    if not words:
        return query

    # 2. choose only words that are NOT protected
    candidate_indices = [i for i, w in enumerate(words) if not do_not_touch(w)]

    if not candidate_indices:
        # nothing we can safely change
        return query

    idx = random.choice(candidate_indices)
    typo_func = random.choice(TYPO_FUNCS)
    print("Using:", typo_func.__name__)  # check which is used
    words[idx] = typo_func(words[idx])
    return " ".join(words)

if __name__ == "__main__":
    N = 5
    synthetic = []
    for q in queries:
        for _ in range(N):
            synthetic.append([q, generate_misspelling(q)])

    original_and_misspellings = pd.DataFrame(synthetic, columns=["original", "misspelling"])
    print(original_and_misspellings.head(40))

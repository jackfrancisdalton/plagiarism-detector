import hashlib
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Dict, Set, Generator

N_GRAM_SIZE = 5 # number of words per ngram
FILE_DIR = "texts"

def hash_words(words: List[str]) -> str:
    return hashlib.sha1(" ".join(words).encode("utf-8")).hexdigest()

def generate_ngrams(words: List[str], n: int = N_GRAM_SIZE) -> Generator[Tuple[str, str], None, None]:
    for i in range(len(words) - n + 1):
        ngram_words = words[i:i+n]
        ngram_text = " ".join(ngram_words)

        # TECH DEBT: memory usage would be huge storing all the phrases with a sliding window of +1
        # Consider changing the approach to be more efficient, perhaps don't include the phrase
        yield hash_words(ngram_words), ngram_text

def read_words_from_file(file_path: Path) -> List[str]:
    word_list: List[str] = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            normalised_words = line.strip().lower().split()
            word_list.extend(normalised_words)

    return word_list

def generate_ngrams_from_file(file_path: Path) -> List[Tuple[str, str]]:
    word_list = read_words_from_file(file_path)
    ngram_hash_and_ngram_text = list(generate_ngrams(word_list))
    return ngram_hash_and_ngram_text

def scan_for_plagiarism() -> None:
    ngram_hash_to_files_dict: Dict[str, Set[str]] = defaultdict(set)
    ngram_hash_to_text_dict: Dict[str, str] = {}

    file_paths = list(Path(FILE_DIR).glob("*.txt"))

    for file_path in file_paths:
        file_name = file_path.stem
        ngram_and_ngram_hash_tuple = generate_ngrams_from_file(file_path)

        # Assign the hash and ngram to dicts
        for ngram_hash, ngram_text in ngram_and_ngram_hash_tuple:
            ngram_hash_to_files_dict[ngram_hash].add(file_name)
            ngram_hash_to_text_dict[ngram_hash] = ngram_text

    print_suspects(ngram_hash_to_files_dict, ngram_hash_to_text_dict)

def print_suspects(
    ngram_hash_to_files: Dict[str, Set[str]],
    ngram_hash_to_text: Dict[str, str]
) -> None:
    # Dict of cases where more one than 1 file shares the same ngram hash
    duplicates = {
        ngram_hash: files 
        for ngram_hash, files in ngram_hash_to_files.items() 
        if len(files) > 1
    }

    print(f"\nFound {len(duplicates)} shared n-grams across scanned files.\n")

    for ngram_hash, files in list(duplicates.items())[:10]:
        words = ngram_hash_to_text[ngram_hash]
        files = sorted(files)

        print(f"'{words}' found in files: {files}")

if __name__ == "__main__":
    scan_for_plagiarism()

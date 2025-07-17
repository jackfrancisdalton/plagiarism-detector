from pathlib import Path

N_GRAM_SIZE = 3
TEXTS_DIR = "texts"

def run_assessment():
    
    text_files = list(Path(TEXTS_DIR).glob("*.txt"))

    for text_file in text_files:
        text_id = text_file.stem

        with open(text_file, 'r') as file:
            content = file.read().strip()
            print(f"Text ID: {text_id}, Content: {content}")

    print("Running assessment...")

if __name__ == "__main__":
    run_assessment()
import pickle
import random
import csv
import os


data_file = '/Users/anastassiashaitarova/Downloads/par3.pkl'

with open(data_file, "rb") as f:
    data = pickle.load(f)

# Dictionary to store books grouped by language
books_by_language = {}

# Iterate through each book in the data
for book_key in data.keys():
    # Extract language code from the book key (last two characters)
    source_lang = book_key[-2:]

    # Create a subfolder for the language if it doesn't exist
    language_folder = f"par3/{source_lang}"
    os.makedirs(language_folder, exist_ok=True)

    # Add the book key to the corresponding language group in the dictionary
    if source_lang not in books_by_language:
        books_by_language[source_lang] = []
    books_by_language[source_lang].append(book_key)

# Iterate over books grouped by language
for source_lang, books in books_by_language.items():
    print(f"Processing books for language: {source_lang}")
    language_folder = f"par3/{source_lang}"

    # Process each book in the current language group
    for book_key in books:
        if book_key.endswith(f"_{source_lang}"):
            # Extract source, Google Translate, and translator data for the current book
            source_paras = data[book_key]["source_paras"]
            gt_paras = data[book_key]["gt_paras"]
            translator_data = data[book_key]["translator_data"]
            num_trans = len(translator_data)  # Number of human translations

            # Prepare data for CSV
            csv_data = []
            for para_idx in range(len(source_paras)):
                source_text = source_paras[para_idx]
                gt_text = gt_paras[para_idx]
                translator_texts = [translator_data[f"translator_{i+1}"]["translator_paras"][para_idx] for i in range(num_trans)]
                csv_data.append([source_text, gt_text] + translator_texts)

            # Define CSV file path for the current book
            book_title = "_".join(book_key.split("_")[:-1])
            csv_file = os.path.join(language_folder, f"{book_title}.csv")

            # Write data to CSV file
            with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["Source", "GoogleTranslate"] + [f"human{i+1}" for i in range(num_trans)])
                csvwriter.writerows(csv_data)

            print(f"CSV file '{csv_file}' has been created successfully.")

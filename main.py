import json, sys, os, time
from decimal import Decimal
from scripts import get_names, get_urls, get_script, get_genres

ADDED_COUNT = 1
DATA_PATH = "data.json"
IGNORED_WORDS = ["the", "to", "and", "you", "in", "of", "at", "as", "it"]

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
    else:
        data ={}
    return data

def save_data():
    with open(DATA_PATH, 'w') as f:    
        json.dump(data, f, indent=4)

def reset_data():
    data = {}
    with open(DATA_PATH, 'w') as f:    
        json.dump(data, f, indent=4)

def get_text(path):
    with open(path, 'r') as f:
        text = f.read()
    return text

def get_word_counts(text):
    for char in text:
        if not char.isalpha():
            text = text.replace(char, " ")
    text = text.replace("  ", " ")
    words = text.lower().split(" ")
    word_counts = {}
    for word in words:
        if len(word) < 2 or word in IGNORED_WORDS:
            continue
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    return word_counts

def train_data(text, category):
    text = text.lower()
    word_counts = get_word_counts(text)
    for word in word_counts:
        if word in data[category]:
            data[category][word] += word_counts[word]
        else:
            data[category][word] = word_counts[word]

def get_probability(text, category):
    total_words = Decimal(sum(sum(data[category][word] + ADDED_COUNT for word in data[category]) for category in data))
    total_category_words = Decimal(sum(data[category][word] + ADDED_COUNT for word in data[category]))
    probability = Decimal(total_category_words / total_words)
    word_counts = get_word_counts(text)
    for word in word_counts:
        if word in data[category]:
            probability = probability * (((data[category][word] + ADDED_COUNT) / total_category_words) ** word_counts[word])
        else:
            probability = probability * ((ADDED_COUNT / total_category_words) ** (word_counts[word]))
    return probability

def get_categories(text):
    text = text.lower()
    probabilities = []
    for category in data:
        probability = get_probability(text, category)
        probabilities.append((probability, category))
    probabilities.sort(reverse=True, key=lambda probability: probability[0])
    return probabilities


def train_genre(genre):
    successful = 0
    failed = 0
    data[genre] = {}
    names = get_names(genre)
    urls = get_urls(names)
    for i, name in enumerate(names):
        print(f"\nRetrieving script for {name}...")
        script = get_script(urls[i])
        if script == "":
            print("Failed to retrieve script!")
            failed += 1
        else:
            print(f"Training script with genre: {genre}")
            train_data(script, genre)
            successful += 1
        
    print(f"\nSuccessfully retrieved {successful} scripts\nFailed to retrieve {failed} scripts\nTotal scripts attempted: {failed + successful}\n")

def incorrect_usage():
    print("Incorrect usage!")
    print("Usage:  train_auto  (Retrieves all genres and their scripts from imsdb and trains all available scripts)\n  train_genre [genre]  (Retrieves scripts from an imsdb genre)\n  train [filepath] [genre]  (Retreives a script from a file)\n  test [filepath]  (Tests what genre a script from a file belongs to)\n  delete [genre]  (Deletes all data for a specific genre)\n  reset  (resets all data)\n  list  (Lists all genres)")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["train_genre", "train", "test", "reset", "delete", "list", "train_auto"]:
        incorrect_usage()
        sys.exit()
        
    if sys.argv[1].lower() == "reset":
        reset_data()
        print("All data has been reset!")

    if sys.argv[1].lower() == "delete":
        if len(sys.argv) > 2:
            if sys.argv[2] in data:
                del data[sys.argv[2]]
                print(f"All data for {sys.argv[2]} has been deleted!")
            else:
                print("There is no data for this category!")
        else:
            incorrect_usage()

    if sys.argv[1].lower() == "train_auto":
        print("Retrieving Genres...")
        genres = get_genres()
        print(f"{len(genres)} genres found")
        for genre in genres:
            print(f"Training genre {genre}...")
            train_genre(genre)
            print(f"Successfully trained genre {genre}")
        save_data()
        print(f"Trained a total of {len(genres)} genres")
        
    if sys.argv[1].lower() == "train_genre":
        if len(sys.argv) > 2:
            train_genre(sys.argv[2])
            save_data()
        else:
            incorrect_usage()
            
    if sys.argv[1].lower() == "train":
        if len(sys.argv) > 3:
            if os.path.exists(sys.argv[2]):
                print("Training data...")
                train(get_text(sys.argv[2]), sys.argv[3])
                save_data()
                print(f"Successfully trained data with genre {sys.argv[3]}")
            else:
                incorrect_usage()
        else:
            incorrect_usage()

    if sys.argv[1].lower() == "test":
        if len(sys.argv) > 2:
            if os.path.exists(sys.argv[2]):
                print("Retreiving script...")
                script = get_text(sys.argv[2])
                print("Testing against data...")
                categories = get_categories(script)
                for i, category in enumerate(categories):
                    print(f"{i + 1}) {category[1]}  -  {category[0]}")
                print(f"Most probable category: {categories[0][1]}")
            else:
                incorrect_usage()
        else:
            incorrect_usage()

    if sys.argv[1].lower() == "list":
        print("Listing Categories...")
        for i, genre in enumerate(data):
            print(f"{i + 1}) {genre}")
        print(f"Total Categories: {len(data)}")


data = load_data()
main()








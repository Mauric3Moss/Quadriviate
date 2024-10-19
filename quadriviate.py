import os
import re
import sys
import time
from difflib import SequenceMatcher
import nltk
from nltk.corpus import words

# Download the nltk word list if you don't have it
nltk.download("words")

def advanced_file_search(root_dir, keyword, search_contents=True, max_distance=0.5):
    """
    Performs an advanced file-system search for files, folders, and directories
    matching the given keyword or phrase, including variations.

    Args:
        root_dir: The root directory to search from.
        keyword: The keyword or phrase to search for.
        search_contents: Whether to search the contents of files for matches.
        max_distance: The maximum Levenshtein distance for variations.
    """

    # Define the output file path in the Downloads folder
    output_file = os.path.join(os.path.expanduser("~"), "Downloads", "search.txt")

    def is_close_match(word1, word2):
        """Check if two words are close matches based on stricter Levenshtein distance tolerance."""
        # Stricter ratio (increased from original to reduce variation count)
        return SequenceMatcher(None, word1, word2).ratio() >= 1 - max_distance / max(len(word1), len(word2))

    # Generate a list of potential variations of the keyword using nltk's word list
    english_words = set(words.words())

    # Find all words that are closer matches to the keyword (stricter matching)
    variations = [word for word in english_words if is_close_match(keyword, word)]

    # Update the search pattern to include variations
    search_pattern = "|".join(re.escape(kw) for kw in variations + [keyword])

    matches = []  # List to store all match results

    start_time = time.time()

    def search_directory(directory):
        """Search the directory recursively for matching files and file contents."""
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            if os.path.isdir(item_path):
                search_directory(item_path)

            elif os.path.isfile(item_path):
                # Check if the file name matches the keyword or its variations
                if re.search(search_pattern, item, re.IGNORECASE):
                    matches.append(f"Found matching file: {item_path}")

                if search_contents:
                    try:
                        with open(item_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Search the file content using the keyword and variations
                            if re.search(search_pattern, content, re.IGNORECASE):
                                matches.append(f"Found matching content in: {item_path}")
                    except UnicodeDecodeError:
                        matches.append(f"Error decoding file: {item_path}")

    # Start searching from the root directory
    search_directory(root_dir)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Notify that writing to the file has started
    print(f"Started writing results to: {output_file}")

    # Write results to the search.txt file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Total matches found: {len(matches)}\n")
        f.write(f"Search completed in {elapsed_time:.2f} seconds\n\n")

        # Print keyword and variations
        f.write(f"Keyword: {keyword}\n")
        f.write(f"Found variations: {', '.join(variations)}\n\n\n\n")

        # Print matching files and content matches
        for match in matches:
            f.write(match + "\n")

    # Notify that the operation is complete
    print("Operation complete. Results saved.")

    # Automatically open the output file after writing is done
    os.startfile(output_file)  # For Windows

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python advanced_file_search.py <keyword>")
        sys.exit()

    keyword = sys.argv[1]
    root_dir = "C:\\Users\\dtmin\\Downloads\\quadrivium-main"  # Example directory

    advanced_file_search(root_dir, keyword)
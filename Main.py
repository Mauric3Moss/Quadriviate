import os
import re
import sys
import time

def advanced_file_search(root_dir, keyword, search_contents=True):
    """
    Performs an advanced file-system search for files, folders, and directories
    matching the given keyword or phrase.

    Args:
        root_dir: The root directory to search from.
        keyword: The keyword or phrase to search for.
        search_contents: Whether to search the contents of files for matches.
    """

    start_time = time.time()

    def search_directory(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            if os.path.isdir(item_path):
                search_directory(item_path)

            elif os.path.isfile(item_path):
                if re.search(keyword, item, re.IGNORECASE):
                    print(f"Found matching file: {item_path}")

                if search_contents:
                    try:
                        with open(item_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if re.search(keyword, content, re.IGNORECASE):
                                print(f"Found matching content in: {item_path}")
                    except UnicodeDecodeError:
                        print(f"Error decoding file: {item_path}")

    search_directory(root_dir)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Search completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python advanced_file_search.py <root_directory> <keyword>")
        sys.exit(1)

    root_dir = sys.argv[1]
    keyword = sys.argv[2]

    advanced_file_search(root_dir, keyword)

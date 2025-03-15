from fuzzywuzzy import fuzz

import re


def check_kyedae_comment(string_comment):
    string_comment = string_comment.lower()
    string_comment = re.sub(r'[^a-zA-Z0-9\s]', ' ', string_comment)
    string_comment = string_comment.split()

    spellings = ["kyedae", "kyadae", "kaede"]
    
    for spelling in spellings:

        for word in string_comment:
            # print(f"{word} : {spelling}")
            
            if word == spelling:
                return True
            elif fuzz.ratio(word, spelling) >= 70 and word.startswith("k") and len(word) >= 5:
                print(f"\033[1mfuzz ratio: {fuzz.ratio(word, spelling)}\033[0m")
                return True

    return False


def main():
    if check_kyedae_comment(" memes review tas nakalive, kada tatawa si luna may parusa😹 "):
        print("Kyedae comment FOUND")
    else:
        print("Kyedae comment NOT FOUND")


if __name__ == "__main__":
    main()

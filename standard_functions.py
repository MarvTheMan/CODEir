
def get_list_from_file(file):
    wordlist = []
    with open(file, "r") as f:
        for line in f:
                wordlist.append(line.split().lower())
    return wordlist


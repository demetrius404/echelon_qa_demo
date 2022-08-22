with open("./ascii_art.txt") as file:
    for line in file.readlines():
        print(line.strip("\n"))

import sys

LENGTH_OF_SAMPLE = 500
OFFSET = 30


def read_file(file_name):
    with open(file_name) as text:
        string = text.read()
    return string


def scan_string(string):
    duplications = []
    sample_string = string[:LENGTH_OF_SAMPLE]
    char = ord('\u0370')

    for i in range(len(sample_string) - OFFSET):
        for j in range(i + 1, len(sample_string) - OFFSET):

            if sample_string[i] == sample_string[j] and sample_string[i + 1] == sample_string[j + 1]:

                n = 0
                word = []
                while sample_string[i + n] == sample_string[j + n]:
                    word.append(sample_string[i + n])
                    n += 1

                item = ("".join(word), chr(char))
                duplications.append(item)
                char += 1

    # Sort by longest word
    duplications.sort(key=lambda t: len(t[0]), reverse=True)

    # Print for testing only
    # for i in range(len(duplications)):
    #    print('"{0}" = "{1}"'.format(duplications[i][0], duplications[i][1]))
    # print(duplications)

    return duplications


def swap_duplications(string, duplications):
    key = []
    for i in range(len(duplications)):

        idx = string.find(duplications[i][0])
        while idx != -1:
            string = string.replace(duplications[i][0], duplications[i][1])
            if "|{0}={1}".format(duplications[i][0], duplications[i][1]) not in key:
                key.append("|{0}={1}".format(duplications[i][0], duplications[i][1]))
            idx = string.find(duplications[i][0])

    return "".join(key) + string


def write_to_file(string):
    with open("new_text.txt", "w") as file:
        file.write(string)


def main():
    if len(sys.argv) != 3:
        print("Not enough arguments!")
        return None

    if sys.argv[1] == "-compress":
        string = read_file(sys.argv[2])

        for i in range(5):
            duplications = scan_string(string)
            string = swap_duplications(string, duplications)

        write_to_file(string)
    elif sys.argv[1] == "-decompress":
        string = read_file(sys.argv[2])
    else:
        print("Wrong arguments!")


if __name__ == "__main__":
    main()

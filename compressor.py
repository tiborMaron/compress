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
    char = ord('\u0080')

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


def swap_duplications(string, duplications, mode="encode"):
    key = []
    for i in range(len(duplications)):

        idx = string.find(duplications[i][0])
        while idx != -1:
            string = string.replace(duplications[i][0], duplications[i][1])
            if "|{0}={1}".format(duplications[i][0], duplications[i][1]) not in key:
                key.append("|{0}={1}".format(duplications[i][0], duplications[i][1]))
            idx = string.find(duplications[i][0])

    if mode == "encode":
        return "".join(key) + "<#&#>" + string
    elif mode == "decode":
        return string


def decode(string):
    encode_marker = string.find("<#&#>")
    header = string[1:encode_marker]
    raw_list = header.split("|")

    duplications = []
    for item in raw_list:
        temp = item.split("=")
        duplications.append([temp[1], temp[0]])

    return swap_duplications(string[encode_marker + 5:], duplications, mode="decode")


def write_to_file(string):
    with open(str(sys.argv[2]), "w") as file:
        file.write(string)


def main():
    if len(sys.argv) != 3:
        print("Not enough arguments!")
        return None

    if sys.argv[1] == "-compress":
        string = read_file(sys.argv[2])
        orig_len = len(string)
        duplications = scan_string(string)
        string = swap_duplications(string, duplications)
        new_len = len(string)
        write_to_file(string)
        print("Original length: {0}"
              "\nNew length: {1}\n"
              "Compression rate: {2:.2f}%".format(orig_len, new_len, 100 - (new_len / orig_len * 100)))
    elif sys.argv[1] == "-decompress":
        string = read_file(sys.argv[2])
        string = decode(string)
        write_to_file(string)
    else:
        print("Wrong arguments!")


if __name__ == "__main__":
    main()

import sys
import os

LENGTH_OF_SAMPLE = 2500
STARTING_CHAR = '\u00a1'
MARKER = "<#&#>"


def read_file(file_name):
    with open(file_name) as text:
        string = text.read()
    return string


def swap(string, keys, mode="encode"):

    # ENCODE MODE
    if mode == "encode":
        final_keys = []
        for key in keys:

            pos = string.find(key[0])
            if pos != -1:
                while pos != -1:
                    string = string.replace(key[0], key[1])
                    pos = string.find(key[0])
                final_keys.append("|{0}={1}".format(key[0], key[1]))

        return "".join(final_keys) + MARKER + string

    # DECODE MODE
    elif mode == "decode":
        for key in keys:
            while True:
                string = string.replace(key[0], key[1])
                pos = string.find(key[0])
                if pos == -1:
                    break
        return string


def find_duplications(sample):
    duplications = []
    for i in range(len(sample)):
        for j in range(i + 1, len(sample)):

            try:
                if sample[i] == sample[j] and sample[i + 1] == sample[j + 1]:
                    n = 0
                    word = []
                    while sample[i + n] == sample[j + n]:
                        word.append(sample[i + n])
                        n += 1
                    word = "".join(word)
                    if word not in duplications:
                        duplications.append(word)
            except IndexError:
                pass

    duplications.sort()
    duplications.sort(key=len, reverse=True)
    return duplications


def encode(string):

    if string.find(MARKER) != -1:
        raise ValueError

    sample = string[:LENGTH_OF_SAMPLE]
    char_value = ord(STARTING_CHAR)

    duplications = find_duplications(sample)

    keys = []
    for item in duplications:
        while string.find(chr(char_value)) != -1:
            char_value += 1
        temp = (item, chr(char_value))
        keys.append(temp)
        char_value += 1

    return swap(string, keys)


def decode(string):
    pos_encode_marker = string.find(MARKER)

    if pos_encode_marker == -1:
        raise ValueError

    header = string[1:pos_encode_marker]
    raw_list = header.split("|")

    keys = []
    for key in raw_list:
        temp = key.split("=")
        keys.append([temp[1], temp[0]])

    return swap(string[pos_encode_marker + len(MARKER):], keys, mode="decode")


def write_to_file(string):
    with open(str(sys.argv[2]), "w") as file:
        file.write(string)


def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments!")
        return None

    # Encoding the file
    if sys.argv[1] == "-code":
        try:
            original_text_as_string = read_file(sys.argv[2])
        except FileNotFoundError:
            print("There is no file called '{0}'!".format(sys.argv[2]))
            return None

        orig_size = os.path.getsize(sys.argv[2])

        try:
            encoded_string = encode(original_text_as_string)
        except ValueError:
            print("File already encoded!")
            return None

        write_to_file(encoded_string)
        new_size = os.path.getsize(sys.argv[2])

        print("Original length: {0}\n"
              "New length: {1}\n"
              "Compression rate (by length): -{2:.2f}%\n".format(
                len(original_text_as_string), len(encoded_string),
                100 - (len(encoded_string) / len(original_text_as_string) * 100)))

        print("Original size: {0:.2f}KiB\n"
              "New size: {1:.2f}KiB\n"
              "Compression rate (by size): -{2:.2f}%".format(
                orig_size / 1024, new_size / 1024,
                100 - (new_size / orig_size * 100)))

    # Decoding the file
    elif sys.argv[1] == "-decode":
        try:
            compressed_text_as_string = read_file(sys.argv[2])
        except FileNotFoundError:
            print("There is no file called '{0}'!".format(sys.argv[2]))
            return None

        try:
            decoded_string = decode(compressed_text_as_string)
        except ValueError:
            print("File isn't encoded!")
            return None

        write_to_file(decoded_string)

    else:
        print("Wrong arguments!")


if __name__ == "__main__":
    main()

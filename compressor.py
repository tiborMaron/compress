import sys
import os

LENGTH_OF_SAMPLE = 1000
OFFSET = 30
MARKER = "<#&#>"
STARTING_CHAR = '\u0100'


def read_file(file_name):
    with open(file_name) as text:
        string = text.read()
    return string


def swap(string, duplications, mode="encode"):

    # ENCODE MODE
    if mode == "encode":
        final_keys = []
        for i in range(len(duplications)):
            while True:
                string = string.replace(duplications[i][0], duplications[i][1])
                key = "|{0}={1}".format(duplications[i][0], duplications[i][1])

                if key not in final_keys:
                    final_keys.append(key)

                pos = string.find(duplications[i][0])
                if pos == -1:
                    break
        return "".join(final_keys) + MARKER + string

    # DECODE MODE
    elif mode == "decode":
        for i in range(len(duplications)):
            while True:
                string = string.replace(duplications[i][0], duplications[i][1])
                pos = string.find(duplications[i][0])

                if pos == -1:
                    break
        return string


def encode(string):

    if string.find(MARKER) != -1:
        raise ValueError

    duplications = []
    sample = string[:LENGTH_OF_SAMPLE]
    char_value = ord(STARTING_CHAR)

    for i in range(len(sample) - OFFSET):
        for j in range(i + 1, len(sample) - OFFSET):

            if sample[i] == sample[j] and sample[i + 1] == sample[j + 1]:

                n = 0
                word = []
                while sample[i + n] == sample[j + n]:
                    word.append(sample[i + n])
                    n += 1

                while string.find(chr(char_value)) != -1:
                    char_value += 1

                item = ("".join(word), chr(char_value))
                duplications.append(item)
                char_value += 1

    duplications.sort(key=lambda t: len(t[0]), reverse=True)
    return swap(string, duplications)


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

def file_to_word_list(input_file, min_letters = 0):

    word_list = []

    with open(input_file, "r") as file:
        for line in file:
            stripped_line = line.strip().upper()

            if len(stripped_line) >= min_letters:
                word_list.append(stripped_line)

    return word_list

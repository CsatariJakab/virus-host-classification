def stream_through_dna_string_file(input_file, class_for_values, action):
    label = None
    actual_dna_string = None

    for line in input_file:
        if line.startswith('>'):
            # Apply action on previous
            if label is not None:
                class_for_values = action(label, actual_dna_string, class_for_values)

            label = line.replace('>', '', 1).replace('\n', '')
            actual_dna_string = ''
        elif label is None:
            raise ValueError("File did not start with the expected '>' character")
        else:
            actual_dna_string += line.replace('\n', '')
    # Apply action on last
    class_for_values = action(label, actual_dna_string, class_for_values)

    return class_for_values


def read_dna_strings_to_dict(input_file):
    return stream_through_dna_string_file(input_file, {}, __fill_dictionary)


def __fill_dictionary(label, dna_string, dictionary):
    dictionary[label] = dna_string
    return dictionary

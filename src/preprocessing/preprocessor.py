import pandas as pd
import time

from src.utils.fasta_reader import read_dna_strings_to_dict


def is_dna_string_complete(dna_string):
    return set(dna_string) <= {'A', 'C', 'G', 'T'}


def create_id_host_mapping(metadata_df):
    mapping = {}

    metadata_df.reset_index()
    for index, row in metadata_df.iterrows():
        accession_id = row['Accession']
        host = row['Host']
        mapping[accession_id] = host

    return mapping


def get_accession_id_from_label(label):
    return label.split('|')[0].split('.')[0].strip()


def filter_folder(folder, output_csv_file, virus_label_id, max_lines_written=None):
    csv_file = folder + "/sequences.csv"
    fasta_file = folder + "/sequences.fasta"

    metadata = pd.read_csv(csv_file, dtype={"Accession": "string", "Host": "string"}, usecols=["Accession", "Host"])
    num_rows = len(metadata.index)
    num_filtered_rows = 0

    with open(fasta_file) as file:

        id_host_dict = create_id_host_mapping(metadata)

        for label, dna_string in read_dna_strings_to_dict(file).items():
            if not is_dna_string_complete(dna_string):
                continue

            accession_id = get_accession_id_from_label(label)
            host = id_host_dict[accession_id]

            if not pd.isna(host):
                line = ','.join([dna_string, str(virus_label_id), str(host == "Homo sapiens")]) + '\n'
                output_csv_file.write(line)
                num_filtered_rows += 1

                if max_lines_written is not None and num_filtered_rows == max_lines_written:
                    break

    print("From {} entries left {} valid ones.".format(num_rows, num_filtered_rows))


with open("../../data/filtered_sequences.csv", mode='w') as filtered_output:
    print("Creating new file: ../../data/filtered_sequences.csv")
    timestamp = time.time()

    header = ','.join(["dna_string", "virus_id", "is_host_human"]) + '\n'
    filtered_output.write(header)

    print("Filtering Dengue virus.")
    filter_folder("../../data/dengue", filtered_output, 1)

    print("Filtering Ebolavirus.")
    filter_folder("../../data/ebola", filtered_output, 2)

    print("Filtering MERS coronavirus.")
    filter_folder("../../data/mers", filtered_output, 3)

    print("Filtering Rotavirus.")
    filter_folder("../../data/rota", filtered_output, 4)

    print("Filtering West Nile virus.")
    filter_folder("../../data/west-nile", filtered_output, 5)

    print("Filtering Zika virus.")
    filter_folder("../../data/zika", filtered_output, 6)

    # Ay influenzát kivettem az adathalmazból, mert túl nagy
    # print("Filtering Influenza virus.")
    # __filter_folder("../../data/influenza", filtered_output, 7)

    print("Creation of filtered_sequences.csv file is done, it took {} seconds.".format(time.time() - timestamp))

# Néhány példát generálok mégis az inluenzából, hogy az aggregált modell más vírusra történő
# általánosodását tudjam vizsgálni majd
with open("../../data/filtered_sequences_influenza.csv", mode='w') as filtered_output:
    print("Creating new file: ../../data/filtered_sequences_influenza.csv")
    timestamp = time.time()

    header = ','.join(["dna_string", "virus_id", "is_host_human"]) + '\n'
    filtered_output.write(header)

    filter_folder("../../data/influenza", filtered_output, 7, max_lines_written=2000)
    print("Creation of filtered_sequences_influenza.csv file is done, it took {} seconds.".format(time.time() - timestamp))

import argparse
from Bio import SeqIO, SeqRecord
import unittest
from io import StringIO
from typing import List


def add_nn_to_sequences(input_file: str, sequences_to_modify: List[str]) -> List:
    """
    This function receives input FASTA file, output FASTA file and a list of sequences to be modified.
    It then reads the input FASTA file, adds 'NN' to the start and end of the sequences specified in the list,
    and returns the modified FASTA records.
    """
    records = list(SeqIO.parse(input_file, "fasta"))
    for record in records:
        if record.id in sequences_to_modify:
            record.seq = "NN" + str(record.seq) + "NN"
    return records


class TestAddNN(unittest.TestCase):
    def test_adding_nn(self):
        input_file = StringIO(">sequence1\nACTG")

        sequences_to_modify = ["sequence1"]
        records_modified = add_nn_to_sequences(input_file, sequences_to_modify)
        self.assertEqual(str(records_modified[0].seq), 'NNACTGNN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add 'NN' to the start and end of specified sequences in a FASTA file.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input FASTA file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output FASTA file.")
    parser.add_argument("-s", "--sequences", required=True, help="File with sequences names to be modified")
    args = parser.parse_args()

    with open(args.sequences) as fh_in:
        sequences = [sequence_label.strip() for sequence_label in fh_in.readlines()]

    records_modified = add_nn_to_sequences(args.input, sequences)
    SeqIO.write(records_modified, args.output, "fasta")

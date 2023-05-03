#!/usr/bin/env python3

import itertools

from collections import defaultdict
import subprocess
import sys
from pathlib import Path

from Bio import SeqIO
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


def do_pca():
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    pca = PCA(n_components=2)
    pca.fit(X)
    pass


def main():
    # set up a pandas dataframe
    aa = [
        'A',
        'R',
        'N',
        'D',
        'C',
        'Q',
        'E',
        'G',
        'H',
        'I',
        'L',
        'K',
        'M',
        'F',
        'P',
        'S',
        'T',
        'W',
        'Y',
        'V',
        'B',
        'Z',
        'Q',
    ]
    columns = ['header', 'file'] + list([''.join(x) for x in itertools.product(aa, repeat=3)])
    df = pd.DataFrame(columns=columns)

    # get all fasta files in the current directory
    for file in Path().glob("*.fasta"):

        with open(file) as handle:
            # parse each fasta record
            for record in SeqIO.parse(handle, "fasta"):

                # set up a dictionary to store 3-mer counts
                kmer_dict = {x: 0 for x in columns}
                kmer_dict['header'] = record.name
                kmer_dict['file'] = file.stem

                # run the shell script to get 3-mers
                kmer_str = subprocess.run(
                    ["./get-kmers.sh", record.seq.__str__()],
                    universal_newlines=True,
                    capture_output=True,
                    text=True
                ).stdout

                kmer_list = kmer_str.split("\n")

                # add the 3-mers to the count dict.
                for kmer in kmer_list:
                    try:
                        kmer_dict[kmer] += 1
                    except KeyError:
                        pass

                # add the dict values to the data frame
                df.loc[len(df)] = kmer_dict

    print()


if __name__ == "__main__":
    sys.exit(main())

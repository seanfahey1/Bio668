#!/usr/bin/env python3

import itertools
import subprocess
import sys
from pathlib import Path

import numpy as np
import pickle as p
import plotly.express as px
from plotly.io import to_html
from Bio import SeqIO
from sklearn.decomposition import PCA


def do_pca(X, headers, files):
    print("Starting PCA..")
    # setting up and fitting to the data
    #   transposing because apparently scikit-learn PCA wants the data rotated from how I set it up

    pca = PCA()
    pca.fit(X.T)

    # graph explained variance per component for first 100 components
    fig1 = px.bar(
        y=pca.explained_variance_ratio_
    ).update_layout(
        title='PCA<br>Explained Variance per Principal Component',
        xaxis_title='principal component #',
        yaxis_title="percent variance explained",
        yaxis_tickformat=".1%"
    )
    fig1.show()
    with open('plots/variance-per-component.html', 'w') as fig_out:
        fig_out.write(to_html(fig1, include_plotlyjs='cdn'))

    # graph first 2 components of PCA colored by file
    fig2 = px.scatter(
        x=pca.components_[0],
        y=pca.components_[1],
        color=files,
        hover_name=headers
    ).update_traces(
        marker=dict(size=4, opacity=0.8)
    ).update_layout(
        title='PCA<br>Visualization of First 2 Components',
        xaxis_title='PC1',
        yaxis_title="PC2",
    )
    fig2.show()
    with open('plots/2D-PCA.html', 'w') as fig_out:
        fig_out.write(to_html(fig2, include_plotlyjs='cdn'))

    # graph first 3 components of PCA colored by file (3D)
    fig3 = px.scatter_3d(
        x=pca.components_[0],
        y=pca.components_[1],
        z=pca.components_[2],
        color=files,
        hover_name=headers
    ).update_traces(
        marker=dict(size=4, opacity=0.4),
    ).update_layout(
        title='PCA<br>Visualization of First 3 Components',
        scene=dict(
            xaxis_title='PC1',
            yaxis_title="PC2",
            zaxis_title="PC3"
        )
    )
    fig3.show()
    with open('plots/3D-PCA.html', 'w') as fig_out:
        fig_out.write(to_html(fig3, include_plotlyjs='cdn'))


def get_kmers():
    print("Getting 3-mers..")

    # set up an array and column ids
    aa = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    possible_kmers = list(["".join(x) for x in itertools.product(aa, repeat=3)])
    array = np.empty(shape=(0, len(possible_kmers)), dtype='int')
    headers_column = []
    files_column = []

    # get all fasta files in the current directory
    for file in Path().glob("sequences/*.fasta"):
        with open(file) as f:
            row_size = sum(1 for line in f if line.startswith(">"))
        temp_array = np.zeros([row_size, len(possible_kmers)])

        with open(file) as handle:
            cur_row = 0
            ii = 0
            # parse each fasta record
            for record in SeqIO.parse(handle, "fasta"):
                if ii % 20 == 0:
                    print(f'file: {file.name}\tparsing record: {ii}')
                ii += 1

                # run the shell script to get 3-mers
                kmer_out = subprocess.run(
                    ["./get-kmers.sh", record.seq.__str__()],
                    universal_newlines=True,
                    capture_output=True,
                    text=True,
                )
                # raise an error if it failed
                if kmer_out.stderr:
                    raise RuntimeError(kmer_out.stderr)

                # get the output 3-mer list, drop the last two partial 3-mers
                kmer_list = kmer_out.stdout.split("\n")[:-3]

                # add 3-mer count values to the array
                for kmer in kmer_list:
                    # get the column index for insertion
                    col_index = possible_kmers.index(kmer)

                    # increment the cell by 1
                    temp_array[cur_row, col_index] += 1

                # also track header and file for this row
                headers_column.append(record.description)
                files_column.append(file.stem)

                # increment to the next row
                cur_row += 1

        # concat temp array for the current file into the full array
        array = np.concatenate((array, temp_array), axis=0)

        # free up memory
        del temp_array

    # convert counts to relative frequencies
    # this takes the sum across each row, converts that from shape (x, ) to shape (x, 1), then divides the original
    # array by this column row-wise
    array = array / array.sum(axis=1)[:, None]

    return array, headers_column, files_column


def main():
    # create sequences,  and plots directories if they don't exist
    Path('plots/').mkdir(exist_ok=True)
    Path('sequences/').mkdir(exist_ok=True)

    # get the 3-mer array
    load = False

    if load:
        with open('array.p', 'rb') as obj1:
            X = p.load(obj1)
        with open('headers.p', 'rb') as obj2:
            headers = p.load(obj2)
        with open('files.p', 'rb') as obj3:
            files = p.load(obj3)

    else:
        X, headers, files = get_kmers()

        with open('array.p', 'wb') as obj1:
            p.dump(X, obj1)
        with open('headers.p', 'wb') as obj2:
            p.dump(headers, obj2)
        with open('files.p', 'wb') as obj3:
            p.dump(files, obj3)

    # do the PCA
    do_pca(X, headers, files)


if __name__ == "__main__":
    sys.exit(main())

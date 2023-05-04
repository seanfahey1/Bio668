# Bio668
[Bio668](https://kelleybioinfo.org/algorithms/about/about.php) @ SDSU final project submission

### <u>Sections</u>
- [Bio668](#bio668)
- [Assignment](#assignment)
- [Setup](#setup)
- [Input Data](#input-data)
- [Output](#output)
- [Notebook](#notebook)

<hr>

## Assignment 

Due May 11th 2023

1. Work on something relevant to your research project, or something that interests you. This part is very flexible.
2. Use things we covered in the semester (**bash**, **awk**, sed, **python**, regex, r, qiime2, etc.).
3. Preferably do it in a notebook format.

<hr>

## Setup
Navigate to the directory you want to store the code and plots in. Then run the following commands to create a virtual 
environment:

```bash 
git clone https://github.com/seanfahey1/Bio668.git
```

```bash 
cd Bio668
```

```bash 
./setup.sh
```

Next, add additional .fasta formatted files to the `sequences` directory (or remove unwanted files).

Finally, run the following command to produce the 3-mer PCA plots:

```bash 
./pca-of-kmers.py
```

<hr>

## Input Data

Four `.fasta` files are included for different classifications of phage structural proteins. These can be substituted 
for any fasta formatted files of protein sequences. The title of the file will be used for the color labels and legend 
of the output plots. 

<hr>

## Output

The python code opens each `.fasta` file in the `sequences` directory and calls the `get-kmers.sh` shell script. This 
collects a list of all 3-mers present in each sequence present in the file using a sliding window. The relative 
frequency of each 3-mer is then calculated for each sequence provided. These relative frequencies are then fit to a 
[PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html). 

The output of this code is 3 plots (produced using [plotly.express](https://plotly.com/python/plotly-express/)) that 
can be found in the `plots` folder:

- `variance-per-component.html` - A bar plot of the % of variance explained by each principal component.
- `2D-PCA.html` - The first 2 principal components.
- `3D-PCA.html` - The first 3 principal components plotted in a 3D scatterplot.

<hr>

## Notebook

The repo also includes an ipython jupyter notebook that can be used to run the code piece by piece. The notebook also
includes a random forest classifier model and plots the feature importance scores for the top 50 most important 3-mers.

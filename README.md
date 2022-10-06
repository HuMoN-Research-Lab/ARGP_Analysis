# ARGP_Analysis
Repo for the post-processing and analysis of Pupil, Qualisys, and Unity data that make up the ARGP *experience*

## Installation instructions:
- set up a python 3.9 environment, using your preferred method of environment building
- make sure the requirements are satisfied (only 4 libraries atm: numpy, matplotlib, pandas and seaborn)'
  - this might be handled by pycharm?
- and (in case it wasn't obvious), clone this repository and assign the python 3.9 environment as your interpreter

## Demo Data
- follow [this URL](https://drive.google.com/drive/folders/1dic0dFkEQCN648a0imlMrh2oLi4s2bnb?usp=sharing) to download a zip file containing all the demo files that you'll need
- this contains three files:
  1. `2022-08-29_Pilot_Data0002.tsv` <- qualisys data as a `.tsv` file
  2. `pupil_positions.csv` <- pupil labs data, currently not used
  3. `qualisys_dict.json` <- the code will create this, but you can point your paths at this file on line 32 of `main.py` and save yourself time

## Run Instructions:
1. fix your paths (lines 16-37 of `main.py`) so that your code is pointed at the correct data (see ***Demo Data***)
2. put a breakpoint at line 42 in `main.py`
3. run `main.py`
> the resulting output will be a frontal view of the 3D skeleton

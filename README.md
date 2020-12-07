# NTT_Analysis
Kim Lab - University of Washington

## Purpose
The purpose of this program is to analyze given Neuralynx NTT files. It will determine the firing rate, peak-valley times (PVT) of all 4 channels, the average PVT, the average peak-valley amplitudes (PVA) of all 4 channels, the max PVA, the channel number with the max PVA, and the PVT of the channel with the max PVA for every cell number in every NTT file provided.

## To use this program:
1. Clone this repository and change directory to the directory with the program
2. Run ntt.py with the file paths to the NTT files as arguments
3. The analyzed data will be exported as an excel file named 'NTT_Data.xlsx'

# Notes:
1. Use *.ntt and *.NTT to analyze all files that end in .ntt and .NTT
2. The code uses the NumPy and Pandas packages

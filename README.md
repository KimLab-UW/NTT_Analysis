# NTT_Analysis
Kim Lab - University of Washington

## Purpose
The purpose of this program is to analyze given Neuralynx NTT files. It will determine the firing rate, peak-valley times (PVT) of all 4 channels, the average PVT, the average peak-valley amplitudes (PVA) of all 4 channels, the max PVA, the channel number with the max PVA, and the PVT of the channel with the max PVA for every cell number in every NTT file provided.

## To use this program:
1.	Open the terminal or command prompt on your computer
2.	Navigate to the directory/folder that has the program
    1.	use 'cd [PATH]’ to change directories.
        1.	Example) cd Documents/NTT
    2.	Use ‘ls’ on Linux/Mac or ‘DIR’ on Windows to see all files and directories in the current directory
3.	Run the program in the terminal with the file path to the NTT files as the arguments
    1.	Use: ‘python ntt.py’
4.	If the NTT files are in a separate directory, enter the file path to the directory with the NTT files when prompted and press enter/return
    1.	If the NTT files are in the same directory as the .py file, just press enter/return without typing
    2.	If the directory is in the current working directory, you can simply just enter the name of the directory with the NTT files
5.	The analyzed data will be exported as an excel file called ‘NTT_Data.xlsx’


# Notes:
1. The code uses the numpy (v1.19.3), pandas, and openpyxl packages
2. It may be easier to have all NTT files in a separate folder/directory 
    1. For macOS, all the NTT files may have to end in “.NTT” (instead of “.ntt)


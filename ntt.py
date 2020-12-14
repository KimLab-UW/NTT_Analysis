# Kim Lab - University of Washington
# Reads Neuralynx NTT Files and outputs excel file with analyzed data

import sys
import os
import numpy as np
import pandas as pd
import glob

np.set_printoptions(threshold=np.inf)

class Neuralynx:
    # More info about header and data size/type can be found on Neuralynx website (preset values)
    HEADER_LENGTH = 16 * 1024  # 16 kilobytes of header

    NTT_RECORD = np.dtype([('TimeStamp',     np.uint64),           # Cheetah timestamp for this record. This value is in
                                                                   # microseconds.
                           ('ScNumber',      np.uint32),           # Tetrode number
                           ('CellNumber',    np.uint32),           # Cell number
                           ('dnParameters',  np.int32, 8),         # Max and min amplitude data
                           ('snData',        np.int16, (32, 4))])  # Time data


    def read_records(fid, record_dtype, record_skip=0, count=None):
        # Read count records (default all) from the file object fid skipping the first record_skip records. Restores the
        # position of the file object after reading.
        if count is None:
            count = -1


        pos = fid.tell()
        fid.seek(Neuralynx.HEADER_LENGTH, 0)
        fid.seek(record_skip * record_dtype.itemsize, 1)
        rec = np.fromfile(fid, record_dtype, count=count)
        fid.seek(pos)

        return rec

    def load_ntt(file_path):
        # Load a NTT file and read records

        file_path = os.path.abspath(file_path)
        with open(file_path, 'rb') as fid:
            print(file_path)
            records = Neuralynx.read_records(fid, Neuralynx.NTT_RECORD)
        return records

class Program:

    # Parses the filename of a filepath
    def parseFilename(filepath):
        index = filepath.rfind("/")
        if index == -1:
            index = filepath.rfind("\\")
        if index == -1:
            return filepath
        return filepath[index+1:]

    # Separates raw records file into dict separated by cell numbers as keys
    # dict format - cell number: (cell number, start time, end time, {timestamp: [[channel1, channel2, channel3, channel4], ...]})
    def separateCells(ntt):
        cells = {}
        cellList = set()
        length = len(ntt)
        for i in range(length):
            cellNum = ntt[i][2]
            # First time seeing this cell number
            if not (cellNum in cellList):
                newCell = [cellNum, ntt[i][0], ntt[i][0], {}]  # create new cell list: (cellnum, start, end, data)
                cells[cellNum] = newCell
                cellList.add(cellNum)
                cells[cellNum][3][ntt[i][0]] = ntt[i][4]  # add time and data
            else:
                cells[cellNum][3][ntt[i][0]] = ntt[i][4]  # add time and data
                cells[cellNum][2] = ntt[i][0]  # update end time
        return cells


    # Given the cell data and a channel number, calculates the average amplitudes of the 32 time intervals
    def average(cell, channel):
        sum = np.zeros(32, dtype=np.int64)
        for timestamp in cell:
            for i in range(32):
                sum[i] += cell[timestamp][i][channel]

        return np.divide(sum, len(cell))

    # Populates np array for a given NTT file with the analyzed data
    def process(ntt):
        # process raw data into dict
        cells = Program.separateCells(ntt)
        # tetrode number is same for 1 ntt file
        tetrodeNum = ntt[0][1]
        # np data array to export into excel
        data = np.zeros([len(cells), 15])
        col = 0;
        # loops through all cells in an NTT file
        for key in cells:
            curr = cells[key]
            data[col][0] = tetrodeNum # tetrode number
            data[col][1] = curr[0] # cell number
            data[col][2] = len(curr[3]) / ((curr[2] - curr[1])/1000000) # firing rate

            # get average peak value amplitude data for each channel
            channel0 = Program.average(curr[3], 0)
            channel1 = Program.average(curr[3], 1)
            channel2 = Program.average(curr[3], 2)
            channel3 = Program.average(curr[3], 3)

            # max and min
            max0 = max(channel0)
            max1 = max(channel1)
            max2 = max(channel2)
            max3 = max(channel3)
            min0 = min(channel0)
            min1 = min(channel1)
            min2 = min(channel2)
            min3 = min(channel3)

            # max average peak value amplitude
            data[col][8] = max0 - min0
            data[col][9] = max1 - min1
            data[col][10] = max2 - min2
            data[col][11] = max3 - min3

            pvas = [data[col][8], data[col][9], data[col][10], data[col][11]]
            data[col][12] = max(data[col][8], data[col][9], data[col][10], data[col][11]) # max avg amplitude for all channels
            data[col][13] = pvas.index(data[col][12]) + 1 # channel number with the max PVA

            # average peak value time, absolute value accounts for records that are inverted
            data[col][3] = abs(round(np.argmin(channel0)/32, 2) - round(np.argmax(channel0)/32, 2))
            data[col][4] = abs(round(np.argmin(channel1)/32, 2) - round(np.argmax(channel1)/32, 2))
            data[col][5] = abs(round(np.argmin(channel2)/32, 2) - round(np.argmax(channel2)/32, 2))
            data[col][6] = abs(round(np.argmin(channel3)/32, 2) - round(np.argmax(channel3)/32, 2))

            # calculate the average PVT of the 4 channels, using only non-zero PVTs
            avg_pvt = 0
            non_zero_count = 0
            for i in range(4):
                if data[col][i+3] != 0:
                    avg_pvt += data[col][i+3]
                    non_zero_count += 1
            avg_pvt /= non_zero_count
            data[col][7] = avg_pvt

            pvt_max = (int)(data[col][13] + 2)
            data[col][14] = data[col][pvt_max] # PVT of the channel with the max PVA

            col += 1
        return data

# Reads and analyzes NTT records of all files and exports as an excel file named NTT_Data
if __name__ == "__main__":
    allfile = np.empty((0,15))
    filenames = []

    # read all NTT files
    path = input('Enter the path to the directory with your NTT files: ')
    files = glob.glob(os.path.join(path, '*.NTT'))
    for file in files:
        ntt = Neuralynx.load_ntt(file)
        data = Program.process(ntt)
        allfile = np.append(allfile, data, axis=0)
        for j in range(data.shape[0]):
            filenames.append(Program.parseFilename(file))


    # convert to pd data frame
    excelData = pd.DataFrame(data=allfile, index=filenames,
                              columns=["Tetrode", "Cell", "Firing Rate", "PVT1", "PVT2", "PVT3", "PVT4",
                                         "Average PVT",
                                          "PVA1", "PVA2", "PVA3", "PVA4", "Max PVA", "Max PVA Channel #", "PVT Max Ch"])

    # export as excel

    df = excelData.fillna('')
    with pd.ExcelWriter('NTT_Data.xlsx') as writer:
        df.to_excel(writer, sheet_name='Analyzed')


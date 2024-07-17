import pandas as pd
#import numpy as np
import random


def initialize_dataset(x):
    """Function to initialize the dataset with one chip at position (x, 0)"""
    data = {'x': [0], 'y': [0], 'chips': [0], 'fired_count': [0]}
    return pd.DataFrame(data)

def new_n_dataset(previous_df, m=1):
    """Function to copy the previous dataset and add m chip at 'x': 0, 'y': 0"""
    df = previous_df.copy()
    #df['fired_count']=0
    index_of_row00 = df[(df['x'] == 0) & (df['y'] == 0)].index[0]
    df.loc[index_of_row00, 'chips'] += m
    return df



def chip_firing_df(df):
    """Function to execute the chip-firing game on a dataframe df, and returns a final version where nothing can be fired"""
    for index, row in df.iterrows():
        px, py, chips = row['x'], row['y'], row['chips']
        repeat=False
        # Check if the current position has 4 or more chips
        if chips >= 4:
            if repeat ==False:
                repeat=True
            k=chips//4
            # Remove 4k chips from the current position
            df.loc[index, 'chips'] -= 4*k
            df.loc[index, 'fired_count'] += k
            # Distribute 1 chip to the four neighboring positions
            # UP
            try:
                index_up = df.loc[( df['x'] == px ) & ( df['y'] == py+1 )]
                df.loc[index_up.index[0], 'chips']+=k
            except IndexError:
                df = df.append({'x': px, 'y': py+1, 'chips': 1, 'fired_count': 0}, ignore_index=True)
            # Down
            try:
                index_up = df.loc[( df['x'] == px ) & ( df['y'] == py-1 )]
                df.loc[index_up.index[0], 'chips']+=k
            except IndexError:
                df = df.append({'x': px, 'y': py-1, 'chips': 1, 'fired_count': 0}, ignore_index=True)
            # left
            try:
                index_up = df.loc[( df['x'] == px-1 ) & ( df['y'] == py )]
                df.loc[index_up.index[0], 'chips']+=k
            except IndexError:
                #print('add new row')
                df = df.append({'x': px-1, 'y': py, 'chips': 1, 'fired_count': 0}, ignore_index=True)
            # Down
            try:
                index_up = df.loc[( df['x'] == px +1 ) & ( df['y'] == py )]
                df.loc[index_up.index[0], 'chips']+=k
            except IndexError:
                df = df.append({'x': px+1, 'y': py, 'chips': 1, 'fired_count': 0}, ignore_index=True)
    if repeat == False:
        return df
    else:
        return chip_firing_df(df)

def chip_firing_sequence(num_iterations, jump=1):
    # Create an initial dataset with one chip at position (0, 0)
    firstdataset = initialize_dataset(0)
    
    # List to keep track of the dataset after each step
    datasets = [firstdataset]

    # Simulate the chip-firing game for 10 iterations
    #num_iterations = 2
    for i in range(num_iterations):
        previous_df=datasets[-1]
        dataset = chip_firing_df(new_n_dataset(previous_df, m=jump))
        #print(dataset)
        datasets.append(dataset)

    return datasets
# # Add a column for counting the number of times each position is fired
# for i, df in enumerate(datasets):
#     df['fired_count'] = i


if __name__=='__main__':
    print(chip_firing_sequence(40,jump=40))





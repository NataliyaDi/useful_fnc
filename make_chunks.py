import numpy as np
import pandas as pd


def calculate_ul_for_bins(df, nbins=10, col='uplift', groups_flag=False):
    """
    Count statistics for each bin in df
    :param df: pandas dataframe with scores
    :param nbins: number of bins
    :param col: column name with scores (in origin - uplift or propensity score)
    :param groups_flag: Is there flag for control/treatment group in df. In this code there is a flag 'is_control_group', 1 for control, 0 for treatment group. 
    :return: statistics in bins
    """
    df = df.sort_values(col, ascending=True)  # sort values in score column
    df.reset_index(inplace=True, drop=True)
    chunks = np.array_split(df.index, nbins)
    df_chunks = pd.DataFrame(np.zeros((nbins, 1)), columns=['chunk_size'])
    for idx in df_chunks.index:
        df_tmp = df.loc[chunks[idx]]
        df_chunks.loc[idx, 'chunk_size'] = df_tmp.shape[0]  # N samples in chunk
        df_chunks.loc[idx, 'min_'] = df_tmp[col].min()  # min value of score in chunk
        df_chunks.loc[idx, 'max_'] = df_tmp[col].max()   # max value of score in chunk
        df_chunks.loc[idx, 'purch_ratio'] = df_tmp.loc[:, 'target'].mean()  # mean target value in chunk
        if groups_flag:
            df_chunks.loc[idx, 'purch_ratio_control'] = df_tmp.loc[(df_tmp['is_control_group']==1), 'target'].mean()  # mean target in control group
            df_chunks.loc[idx, 'purch_ratio_treatment'] = df_tmp.loc[df_tmp['is_control_group']==0, 'target'].mean()  # mean target in treatment group
    return df_chunks

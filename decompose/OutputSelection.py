# coding=utf-8
"""
@File  : OutputSelection.py
@Author: ZC Zeng
@Date  : 2020/12/12 10:12
@Desc  : An alignment function finding optimal output variables for equations
"""


def optimalAlignment(event_matrix):
    """
    this function finds optimal alignments between parameters and equations
    @param event_matrix: event matrix of equations
    @return alignment_map: optimal alignment between parameters and equations
    """
    alignment_map = {}  # recording the mapping between equations and their optimal outputs
    while not event_matrix.empty:  # while event matrix is nonempty
        eq_id = ''  # row with the minimum number of 1
        param_id = ''  # column with the minimum number of 1
        param_id_list = event_matrix._stat_axis.values.tolist()
        eq_id_list = event_matrix.columns.values.tolist()
        # find row with the minimum number of 1
        min_num = len(eq_id_list) + 1
        for item in param_id_list:
            if event_matrix.loc[item].sum() < min_num:
                min_num = event_matrix.loc[item].sum()
                eq_id = item
        # find corresponding column with minimum number of 1
        min_num = len(param_id_list) + 1
        for item in eq_id_list:
            if event_matrix.loc[eq_id, item] == 1 and event_matrix[item].sum() < min_num:
                param_id = item
                min_num = event_matrix[item].sum()
        alignment_map[eq_id] = param_id
        event_matrix = event_matrix.drop(labels=eq_id)  # drop column (parameter)
        event_matrix = event_matrix.drop(labels=param_id, axis=1)  # drop row (equation)
    print("Optimal output variable selection\n" + '---------------------------------\n' + "%s\n" % alignment_map)
    return alignment_map

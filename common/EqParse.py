# coding=utf-8
"""
@File  : EqParse.py
@Author: ZC Zeng
@Date  : 2020/12/22 18:35
@Desc  : A String Parse function reformatting input equations into valid format
"""


def eqReformat(eq_string):
    """
    reformat equation in string format into dictionary format {'equation1':['variables_in_equation1'],...}
    @param eq_string: equation in string format
    @return eq_name: name of input equation
    @return variable_list: variables in input equation
    """
    if ':' in eq_string:
        eq_name = eq_string[0:eq_string.index(':')]
    else:
        raise Exception("Invalid input equation: equation name undefined")
    pos = []
    for i in range(len(eq_string)):
        if eq_string[i] == '\"':
            pos.append(i)  # find index for " in string
    if len(pos) == 0:
        raise Exception("Empty input: no variable recognized")
    if len(pos) % 2 != 0:  # invalid input
        raise Exception("Invalid input equation: quotation cannot be aligned")
    variable_list = []
    i = 0
    while i < len(pos):
        v = eq_string[pos[i] + 1:pos[i + 1]]
        if ('+' in v) or ('-' in v) or ('*' in v) or ('/' in v) or ('^' in v) or ('!' in v):
            raise Exception("Invalid variable: variable %s contains operator" % v)
        variable_list.append(v)
        i = i + 2
    variable_list = list(set(variable_list))
    return eq_name, variable_list


def eqsReformat(eqs_string):
    """
    reformat equations in string format into dictionary format
    @param eqs_string: list of equations in string format
    @return eqs_dict: list of equations in dictionary format
    """
    print("%s" % eqs_string + "\n")
    eq_list = eqs_string.splitlines()
    eq_dict = {}
    for i in range(len(eq_list)):
        name, var = eqReformat(eq_list[i])
        eq_dict[name] = var
    return eq_dict

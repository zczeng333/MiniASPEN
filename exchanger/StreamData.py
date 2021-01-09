# coding=utf-8
"""
@File  : StreamData.py
@Author: ZC Zeng
@Date  : 2021/1/3 13:30
@Desc  : Data structures for heat exchange network
"""


class S(object):
    def __init__(self, ts, tt, c, id):
        """
        initialize a stream
        @param ts: source temperature of the stream
        @param tt: target temperature of the stream
        @param c: heat-capacity flow rate of the stream
        @param id: id of the stream
        """
        self.ts = ts
        self.tt = tt
        self.c = c
        self.id = id


class SplitS(S):
    def __init__(self, ts, tt, c, id):
        """
        initialize a stream split by pinch
        @param ts: source temperature of the stream
        @param tt: target temperature of the stream
        @param c: heat-capacity flow rate of the stream
        @param id: id of the stream
        """
        super().__init__(ts, tt, c, id)
        self.heat = abs(ts - tt) * c  # heat should be exchanged inside this temperature interval
        self.heat_res = self.heat  # remaining heat for this stream inside this temperature interval
        self.complete = False  # a flag indicating whether current stream could be further matched

    def update(self, delta_h):
        """
        update parameters
        @param delta_h: delta heat exchanged
        @return:
        """
        self.heat_res = self.heat_res - delta_h  # update remaining heat
        if self.heat_res == 0.0:  # no more matches allowed
            self.complete = True


class Match(object):
    def __init__(self, hp_id, cp_id, hl, end):
        """
        initialize a match between hp and cp
        @param hp_id: id
        @param cp_id:
        @param hl:
        @param end:
        """
        self.hp_id = hp_id  # id of matched hot process stream
        self.cp_id = cp_id  # id of matched cold process stream
        self.hl = hl  # heat load inside this match
        self.end = end  # a boolean variable indicates whether in hot end (True) or cold end (False)

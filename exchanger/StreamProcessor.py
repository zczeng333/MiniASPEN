"""
@File  : StreamProcessor.py
@Author: ZC Zeng
@Date  : 2021/1/7 11:53
@Desc  : An input processor class for heat exchange network
"""

from exchanger.StreamData import S


class Processor(object):
    def __init__(self, problem_set):
        """
        initialize processor
        @param problem_set: input heat exchange network in dictionary format
        """
        self.streams = problem_set['streams']
        self.delta_t = problem_set['delta_t']
        self.stream_param = ['Tin', 'Tout', 'Fcp']  # parameters for streams
        self.stream_id = []  # ids of streams
        self.cp = []  # hot process streams
        self.hp = []  # cold process streams
        self.process()

    def process(self):
        """
        convert heat exchange network in dictionary format into StreamData format
        @return:
        """
        for item in self.streams:
            self.stream_id.append(item)
            stream = self.streams[item]
            new_stream = S(stream['ts'], stream['tt'], stream['c'], item)  # declare corresponding stream object
            if stream['ts'] > stream['tt']:  # hot process stream
                self.hp.append(new_stream)
            else:  # cold process stream
                self.cp.append(new_stream)

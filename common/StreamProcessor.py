"""
@File  : StreamProcessor.py
@Author: ZC Zeng
@Date  : 2021/1/3 11:53
@Desc  :
"""


class Processor(object):
    def __init__(self, problem_set):  # 对读入problem_set(dict形式)进行处理
        self.streams = problem_set['streams']
        self.delta_t = problem_set['delta_t']
        self.stream_param = ['Tin', 'Tout', 'Fcp']  # parameters for streams
        self.stream_name = []  # names of streams
        self.cp = []  # hot process streams
        self.hp = []  # cold process streams
        self.process()

    def process(self):
        for item in self.streams:
            self.stream_name.append(item)
            stream=self.streams[item]
            new_stream = DataStream(item, stream['ts'], stream['tt'], stream['c'])  # declare corresponding stream object
            if stream['ts'] > stream['tt']:  # hot process stream
                self.hp.append(new_stream)
            else:   # cold process stream
                self.cp.append(new_stream)


class DataStream:
    """docstring for """

    def __init__(self, name, ts, tt, c):
        self.name = name
        self.ts = ts
        self.tt = tt
        self.c = c


if __name__ == '__main__':  # for test
    fr = open('Streams.txt', 'r+')
    pro = eval(fr.read())  # 读取的str转换为字典
    fr.close()
    ob = Processor(pro)

"""
@File  : HENSolver.py
@Author: ZC Zeng
@Date  : 2021/1/7 13:26
@Desc  :
"""
from exchanger.StreamProcessor import Processor
from exchanger.StreamData import SplitS, Match


class HENSolver(object):
    def __init__(self, problem_set):
        """
        this function initializes variables and parameters for heat exchange network
        @param problem_set: heat exchange network defined in dictionary
        """
        pro = Processor(problem_set)  # process input
        self.delta_t = pro.delta_t  # temperature tolerance between hot process streams and cold process streams
        self.hp = pro.hp  # list of hot process streams
        self.cp = pro.cp  # list of cold process streams

        self.min_cu = 0  # minimum usage of cold utility
        self.min_hu = 0  # minimum usage of hot utility
        self.pinch_t_cold = 0  # pinch temperature for cold streams
        self.pinch_t_hot = 0  # pinch temperature for hot streams
        self.hp_he = []  # hot process streams in hot end (above pinch)
        self.hp_ce = []  # hot process streams in cold end (under pinch)
        self.cp_he = []  # cold process streams in hot end (above pinch)
        self.cp_ce = []  # cold process streams in cold end (under pinch)

        self.ce_match = []  # process stream matches in cold end
        self.he_match = []  # process stream matches in hot end

    def pinchFinder(self):
        """
        this function finds pinch, minimum hot utility and minmum cold utility for a heat exchange network
        """
        # construct temperature interval for defined problem set
        # hot process streams subtract delta_t, cold process streams add delta_t
        interval = []
        for item in self.hp:
            interval.append(item.ts - self.delta_t)
            interval.append(item.tt - self.delta_t)
        for item in self.cp:
            interval.append(item.ts)
            interval.append(item.tt)
        interval = list(set(interval))  # remove repeated temperature
        interval.sort()
        interval.reverse()  # interval in descending order
        t_diff = []  # store temperature difference of each interval
        for i in range(len(interval) - 1):
            t_diff.append(interval[i] - interval[i + 1])

        # calculate heat-capacity flow rate difference between hp and cp [sum(Fcp_hp)-sum(Fcp_cp)] for each subnetwork
        fcp_diff_list = []  # record
        sum_fcp_hp = 0.0  # sum of hps' heat-capacity flow rate
        sum_fcp_cp = 0.0  # sum of cps' heat-capacity flow rate
        for i in range(len(interval) - 1):  # for every temperature interval
            for item in self.hp:  # iterate every hot process stream
                # find hot process streams crossing current interval
                if item.ts - self.delta_t >= interval[i] and item.tt - self.delta_t < interval[i]:
                    sum_fcp_hp = sum_fcp_hp + item.c  # remaining enerey from hot process streams
            for item in self.cp:
                # find cold process streams crossing current interval
                if item.tt >= interval[i] and item.ts < interval[i]:
                    sum_fcp_cp = sum_fcp_cp + item.c  # remaining energy from cold process streams
            fcp_diff_list.append(sum_fcp_hp - sum_fcp_cp)
            sum_fcp_hp = 0.0
            sum_fcp_cp = 0.0

        # calculate deficiency for each subnetwork
        deficiency = []
        for i in range(len(fcp_diff_list)):
            # energy to be cancelled by hot/cold utility
            # positive: too much hp; negative: too much cp
            deficiency.append(fcp_diff_list[i] * t_diff[i])

        # find pinch
        min_utility = []  # record output of each subnetwork (from high T to low T)
        sum_q = 0.0
        for i in range(len(deficiency)):
            sum_q = sum_q + deficiency[i]
            min_utility.append(sum_q)
        min_hu = abs(min(min_utility))  # minmum energy needed from hot utility
        min_utility.insert(0, 0)
        for i in range(len(min_utility)):  # inject pinch's energy requirement
            min_utility[i] = min_utility[i] + min_hu
        min_cu = min_utility[-1]  # minmum energy need to be absorbed by cold utility
        self.min_cu = min_cu
        self.min_hu = min_hu
        pinch = min_utility.index(min(min_utility))  # index of pinch point
        self.pinch_t_cold = interval[pinch]  # pinch temperature for cps
        self.pinch_t_hot = self.pinch_t_cold + self.delta_t  # pinch temperature for hps

    def streamMatcher(self):
        """
        this function divide heat exchanger network into hot end and cold end based on ts, tt and pinch
        @return:
        """
        # streams in hot end
        for i in range(len(self.hp)):
            # hot process stream under pinch (Hot End)
            if self.hp[i].ts >= self.pinch_t_hot and self.hp[i].tt < self.pinch_t_hot:
                self.hp_ce.append(SplitS(self.pinch_t_hot, self.hp[i].tt, self.hp[i].c, self.hp[i].id))
            elif self.pinch_t_hot > self.hp[i].ts:
                self.hp_ce.append(SplitS(self.hp[i].ts, self.hp[i].tt, self.hp[i].c, self.hp[i].id))
            # hot process stream above pinch (Cold End)
            if self.hp[i].tt <= self.pinch_t_hot and self.pinch_t_hot < self.hp[i].ts:
                self.hp_he.append(SplitS(self.hp[i].ts, self.pinch_t_hot, self.hp[i].c, self.hp[i].id))
            elif self.pinch_t_hot < self.hp[i].tt:
                self.hp_he.append(SplitS(self.hp[i].ts, self.hp[i].tt, self.hp[i].c, self.hp[i].id))

        # streams in cold end
        for i in range(len(self.cp)):
            # cold process stream under pinch (Hot End)
            if self.cp[i].ts <= self.pinch_t_cold and self.pinch_t_cold < self.cp[i].tt:
                self.cp_he.append(SplitS(self.pinch_t_cold, self.cp[i].tt, self.cp[i].c, self.cp[i].id))
            elif self.pinch_t_cold < self.cp[i].ts:
                self.cp_he.append(
                    SplitS(self.cp[i].ts, self.cp[i].tt, self.cp[i].c, self.cp[i].id))
            # cold process stream above pinch (Cold End)
            if self.cp[i].tt >= self.pinch_t_cold and self.cp[i].ts < self.pinch_t_cold:
                self.cp_ce.append(SplitS(self.cp[i].ts, self.pinch_t_cold, self.cp[i].c, self.cp[i].id))
            elif self.pinch_t_cold > self.cp[i].tt:
                self.cp_ce.append(SplitS(self.cp[i].ts, self.cp[i].tt, self.cp[i].c, self.cp[i].id))

        # sort streams in hot/cold end according to heat-capacity flow rate in descending order
        self.hp_he.sort(key=lambda ele: ele.c, reverse=True)
        self.cp_he.sort(key=lambda ele: ele.c, reverse=True)
        self.hp_ce.sort(key=lambda ele: ele.c, reverse=True)
        self.cp_ce.sort(key=lambda ele: ele.c, reverse=True)

        # stream matches in hot end, ensure hot process streams cooling down to pinch temperature
        for hot_process in self.hp_he:
            for cold_process in self.cp_he:
                if not cold_process.complete:  # current cp has heat for exchanging
                    if hot_process.heat_res <= cold_process.heat_res:  # hp cools down to pinch temperature
                        heat_exchange = hot_process.heat_res
                        cold_process.update(heat_exchange)
                        hot_process.update(heat_exchange)
                        self.he_match.append(
                            Match(hot_process.id, cold_process.id, heat_exchange, True))  # record match
                        break
                    else:  # current cp completely exchanged, use next cp to cool down hp
                        heat_exchange = cold_process.heat_res
                        cold_process.update(heat_exchange)
                        hot_process.update(heat_exchange)
                        self.he_match.append(
                            Match(hot_process.id, cold_process.id, heat_exchange, True))  # record match

        # stream matches in cold end, ensure cold process streams warming up to pinch temperature
        for cold_process in self.cp_ce:
            for hot_process in self.hp_ce:
                if not hot_process.complete:  # current hp has remaining heat for exchanging
                    if cold_process.heat_res <= hot_process.heat_res:  # cp warms up to pinch temperature
                        heat_exchange = cold_process.heat_res
                        cold_process.update(heat_exchange)
                        hot_process.update(heat_exchange)
                        self.ce_match.append(
                            Match(hot_process.id, cold_process.id, heat_exchange, True))  # record match
                        break
                    else:  # current hp completely exchanged, use next hp to warm up cp
                        heat_exchange = hot_process.heat_res
                        cold_process.update(heat_exchange)
                        hot_process.update(heat_exchange)
                        self.ce_match.append(
                            Match(hot_process.id, cold_process.id, heat_exchange, True))  # record match

    def optimalHEN(self):
        self.pinchFinder()  # find pinch for heat exchange network
        self.streamMatcher()  # find heat exchange matches between hp and hp
        # format output string
        res_str = 'System Statistics:\n' + '------------------\n'
        res_str = res_str + 'stream' + '\t ts' + '\t Tt' + '\t fcp \n' + '----------------------------\n'
        for ele in self.hp:
            res_str = res_str + str(ele.id) + '\t ' + str(ele.ts) + '\t ' + str(ele.tt) + '\t ' + str(ele.c) + '\n'
        for ele in self.cp:
            res_str = res_str + str(ele.id) + '\t ' + str(ele.ts) + '\t ' + str(ele.tt) + '\t ' + str(ele.c) + '\n'
        res_str = res_str + '\nMinimum Heat Utility\n' + '--------------------\n'
        res_str = res_str + 'Minimum hot utility: ' + str(self.min_hu) + '\n'
        res_str = res_str + 'Minimum cold utility: ' + str(self.min_cu) + '\n'
        res_str = res_str + 'Pinch Temperature: ' + str(self.pinch_t_hot) + '(hot), ' + str(
            self.pinch_t_cold) + '(cold)\n'
        res_str = res_str + '\nHeat Exchange Network Design\n' + '----------------------------\n'
        res_str = res_str + 'Cold Side\n' + '#Match: ' + str(len(self.ce_match)) + '\n'
        for match in self.ce_match:
            res_str = res_str + match.hp_id + '->' + str(match.cp_id) + ', heat exchange: ' + str(match.hl) + '\n'
        count = 1
        for stream in self.hp_ce:
            if stream.heat_res > 0.0:
                res_str = res_str + 'Cold Utility %d' % count + '->' + stream.id + ', heat exchange: ' + str(
                    stream.heat_res) + '\n'
                count += 1
        res_str = res_str + '\nHot Side\n' + '#Match: ' + str(len(self.he_match)) + '\n'
        for match in self.he_match:
            res_str = res_str + match.hp_id + '->' + str(match.cp_id) + ', heat exchange: ' + str(match.hl) + '\n'
        count = 1
        for stream in self.cp_he:
            if stream.heat_res > 0.0:
                res_str = res_str + 'Hot Utility %d' % count + '->' + stream.id + ', heat exchange: ' + str(
                    stream.heat_res) + '\n'
                count += 1
        print(res_str)

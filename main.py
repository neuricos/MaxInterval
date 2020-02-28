from random import uniform
from pprint import pprint
from copy import deepcopy

__author__ = 'Devon Chen'

class Interval:
    def __init__(self, start, length):
        self._start = start
        self._length = length

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._start + self._length

    @property
    def length(self):
        return self._length

    def overlap(self, other):
        if other.start < self.start:
            if other.end < self.start:
                return False
            return True
        if other.start > self.end:
            return False
        return True

    def __len__(self):
        return self._length

    def __str__(self):
        return f"<Interval: start={self._start:.4f}, "\
            f"end={self._start + self._length:.4f}, "\
                f"length={self._length:.4f}>"

    def __repr__(self):
        return self.__str__()


def printBanner(title):
    print("=" * 30, f" {title} " + "=" * 30)


def runAlgo(func, intervals, show_intervals=False):
    if show_intervals:
        selected_intervals, tot = func(intervals, True)
    else:
        tot = func(intervals, False)
    printBanner(f" {func.__name__} ")
    if show_intervals:
        print(f"Selected Intervals:")
        pprint(selected_intervals)
        print()
    print(f"Total Length = {tot}")
    return tot


def greedyEarliest(intervals, show_intervals=False):
    # sort based on start point
    assert(len(intervals) > 0)
    sorted_intervals = sorted(intervals, key=lambda i: i.start)
    tot = sorted_intervals[0].length
    last_interval = sorted_intervals[0]
    if show_intervals:
        selected_intervals = [last_interval]
    for interval in sorted_intervals[1:]:
        if not last_interval.overlap(interval):
            if show_intervals:
                selected_intervals.append(interval)
            tot += interval.length
            last_interval = interval
    if show_intervals:
        return sorted(selected_intervals, key=lambda i: i.start), tot
    return tot


def greedyLongest(intervals, show_intervals=False):
    # sort based on length
    assert(len(intervals) > 0)
    sorted_intervals = sorted(intervals, key=lambda i: -i.length)
    tot = sorted_intervals[0].length
    selected_intervals = [sorted_intervals[0]]
    for interval in sorted_intervals[1:]:
        no_overlap = True
        for prev_interval in selected_intervals:
            if prev_interval.overlap(interval):
                no_overlap = False
                break
        if no_overlap:
            selected_intervals.append(interval)
            tot += interval.length
    if show_intervals:
        return sorted(selected_intervals, key=lambda i: i.start), tot
    return tot


def dynamicOptimal(intervals, show_intervals):
    # dynamically finding the best combination
    assert(len(intervals) > 0)
    sorted_intervals = sorted(intervals, key=lambda i: i.end)
    p = []
    for k, interval in enumerate(sorted_intervals):
        last_prev_index = -1
        for j in reversed(range(k)):
            if sorted_intervals[j].end < interval.start:
                last_prev_index = j
                break
        p.append(last_prev_index)
    m = [sorted_intervals[0].length]
    if show_intervals:
        selected_intervals_list = [[sorted_intervals[0]]]
    for j in range(1, len(p)):
        lhs = m[j - 1]
        rhs = sorted_intervals[j].length
        if p[j] > -1:
            rhs += m[p[j]]
        if lhs > rhs:
            if show_intervals:
                selected_intervals_list.append(deepcopy(selected_intervals_list[j - 1]))
            m.append(lhs)
        else:
            if show_intervals:
                selected_intervals = deepcopy(selected_intervals_list[p[j]])
                selected_intervals.append(sorted_intervals[j])
                selected_intervals_list.append(selected_intervals)
            m.append(rhs)
    if show_intervals:
        return selected_intervals_list[-1], m[-1]
    return m[-1]


if __name__ == '__main__':

    # Config
    config = {
        'N': 10000,
        'SR': (1, pow(10,6)),
        'LR': (1, 1000)
    }

    print(f"Config: N={config['N']}, Start Range={config['SR']}, Length Range={config['LR']}")
    print()

    # Initialize
    intervals = [
        Interval(uniform(config['SR'][0], config['SR'][1]),
        uniform(config['LR'][0],
        config['LR'][1]))
        for _ in range(config['N'])
    ]

    print(f"Randomly Generated Intervals")
    pprint(intervals)
    print()

    print(f"Running Algos...")
    print()

    # Notice that showing the intervals will make the program run significantly slower
    # Because the runtime complexity basically increased from O(N^2) to O(N^3)

    earlist_total = runAlgo(greedyEarliest, intervals)
    longest_total = runAlgo(greedyLongest, intervals)
    dynamic_total = runAlgo(dynamicOptimal, intervals)

    printBanner("Result")
    print(f"Greedy Earlist:  {earlist_total:.4f}")
    print(f"Greedy Longest:  {longest_total:.4f}")
    print(f"Dynamic Optimal: {dynamic_total:.4f}")
import math
from collections import defaultdict, namedtuple
from break_.pgbar import AnimatedProgressBar


def print_json(results):
    import json
    stats = calc_stats(results)
    print(json.dumps(stats._asdict()))


def print_errors(errors):
    if len(errors) == 0:
        return
    print('')
    print('-------- Errors --------')
    for error in errors:
        print(error)


RunStats = namedtuple(
    'RunStats', ['count', 'total_time', 'rps', 'avg', 'min',
                 'max', 'amp', 'stdev', 'rpm'])


def calc_stats(results):
    """Calculate stats (min, max, avg) from the given RunResults.

       The statistics are returned as a RunStats object.
    """
    all_res = []
    count = 0
    for values in results.status_code_counter.values():
        all_res += values
        count += len(values)

    cum_time = sum(all_res)

    if cum_time == 0 or len(all_res) == 0:
        rps = avg = min_ = max_ = amp = stdev = 0
        rpm = 0
    else:
        if results.total_time == 0:
            rps = 0
            rpm = 0
        else:
            rps = float(len(all_res)) / float(results.total_time)
            rpm = rps * 60
        avg = sum(all_res) / len(all_res)
        max_ = max(all_res)
        min_ = min(all_res)
        amp = max(all_res) - min(all_res)
        stdev = math.sqrt(sum((x-avg)**2 for x in all_res) / count)

    return (
        RunStats(count, results.total_time, rps, avg, min_, max_, amp, stdev,
                 rpm)
    )



def print_stats(results):
    stats = calc_stats(results)
    rps = stats.rps

    print('')
    print('-------- Results --------')

    print('Successful calls    \t\t%r' % stats.count)
    print('Total time          \t\t%.4f s  ' % stats.total_time)
    print('Average             \t\t%.4f s  ' % stats.avg)
    print('Fastest             \t\t%.4f s  ' % stats.min)
    print('Slowest             \t\t%.4f s  ' % stats.max)
    print('Amplitude           \t\t%.4f s  ' % stats.amp)
    print('Standard deviation  \t\t%.6f' % stats.stdev)
    print('Requests Per Second \t\t%.2f' % rps)
    print('Requests Per Minute \t\t%.2f' % stats.rpm)
    print('')
    print('-------- Status codes --------')
    for code, items in results.status_code_counter.items():
        print('Code %d          \t\t%d times.' % (code, len(items)))
    print('')


class RunResults(object):

    """Encapsulates the results of a single Boom run.

    Contains a dictionary of status codes to lists of request durations,
    a list of exception instances raised during the run, the total time
    of the run and an animated progress bar.
    """

    def __init__(self, num=1, quiet=False):
        self.status_code_counter = defaultdict(list)
        self.errors = []
        self.total_time = 0
        if num is not None:
            self._progress_bar = AnimatedProgressBar(
                end=num,
                width=65)
        else:
            self._progress_bar = None
        self.quiet = quiet

    def incr(self, status=200, duration=0):
        self.status_code_counter[status].append(duration)
        self.total_time += duration
        if self.quiet:
            return
        if self._progress_bar is not None:
            self._progress_bar + 1
            self._progress_bar.show_progress()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()

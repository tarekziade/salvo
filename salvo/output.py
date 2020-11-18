import sys
import math
import json
from collections import defaultdict, namedtuple

from salvo.pgbar import AnimatedProgressBar


RunStats = namedtuple(
    "RunStats",
    ["count", "total_time", "rps", "avg", "min", "max", "amp", "stdev", "rpm"],
)


def print_errors(errors, stream=sys.stdout):
    if len(errors) == 0:
        return
    stream.write("")
    stream.write("\n-------- Errors --------\n")
    for error in errors:
        stream.write(error + "\n")
    stream.flush()


class RunResults(object):
    """Encapsulates the results of a single Boom run.

    Contains a dictionary of status codes to lists of request durations,
    a list of exception instances raised during the run, the total time
    of the run and an animated progress bar.
    """

    def __init__(self, num=1, quiet=False):
        self.status_code_counter = defaultdict(list)
        self.errors = defaultdict(int)
        self.errors_desc = {}
        self.total_time = 0
        if num is not None:
            self._progress_bar = AnimatedProgressBar(end=num, width=65)
        else:
            self._progress_bar = None
        self.quiet = quiet

    def incr(self, status=200, duration=0):
        self.total_time += duration
        self.status_code_counter[status].append(duration)
        if self.quiet:
            return
        if self._progress_bar is not None:
            self._progress_bar + 1
            self._progress_bar.show_progress()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

    def _calc_stats(self):
        """Calculate stats (min, max, avg) from the given RunResults.

        The statistics are returned as a RunStats object.
        """
        all_res = []
        count = 0
        for values in self.status_code_counter.values():
            all_res += values
            count += len(values)

        cum_time = sum(all_res)

        if cum_time == 0 or len(all_res) == 0:
            rps = avg = min_ = max_ = amp = stdev = 0
            rpm = 0
        else:
            if self.total_time == 0:
                rps = 0
                rpm = 0
            else:
                rps = float(len(all_res)) / float(self.total_time)
                rpm = rps * 60
            avg = sum(all_res) / len(all_res)
            max_ = max(all_res)
            min_ = min(all_res)
            amp = max(all_res) - min(all_res)
            stdev = math.sqrt(sum((x - avg) ** 2 for x in all_res) / count)

        return RunStats(count, self.total_time, rps, avg, min_, max_, amp, stdev, rpm)

    def print_stats(self, stream=sys.stdout):
        stats = self._calc_stats()
        rps = stats.rps
        stream.write("\n-------- Results --------\n\n")
        stream.write("Successful calls    \t\t%r\n" % stats.count)
        stream.write("Total time          \t\t%.4f s\n" % stats.total_time)
        stream.write("Average             \t\t%.4f s\n" % stats.avg)
        stream.write("Fastest             \t\t%.4f s\n" % stats.min)
        stream.write("Slowest             \t\t%.4f s\n" % stats.max)
        stream.write("Amplitude           \t\t%.4f s\n" % stats.amp)
        stream.write("Standard deviation  \t\t%.6f\n" % stats.stdev)
        stream.write("Requests Per Second \t\t%.2f\n" % rps)
        stream.write("Requests Per Minute \t\t%.2f\n\n" % stats.rpm)
        stream.write("-------- Status codes --------\n")
        for code, items in self.status_code_counter.items():
            stream.write("Code %d          \t\t%d times.\n" % (code, len(items)))
        stream.write("\n")
        stream.flush()

    def print_json(self, stream=sys.stdout):
        stats = self._calc_stats()
        stream.write(json.dumps(stats._asdict()) + "\n")
        stream.flush()

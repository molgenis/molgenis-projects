import time
import math
import sys
import warnings


class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.time_running = 0
        self.bar = '[]'.format(' '* 100)
        self.percentage = self.get_percentage()
        self.number_of_stripes = 0
        self.number_of_spaces = 100

    def get_next(self, current):
        """NAME: get_next
        INPUT: current (the current total processed)
        PURPOSE: gets next step in progressbar and prints it"""
        if self.total != 0:
            old_percentage = int(self.percentage)
            self.current = current
            self.percentage = self.get_percentage()
            if (self.percentage == 0.0 or old_percentage < int(self.percentage)):
                self.print_progress()
        else:
            warnings.warn("Total is zero, instantly done")

    def get_percentage(self):
        """NAME: get_percentage
        PURPOSE: calculates the percentage of the current stage based on the total"""
        percentage = self.current / self.total * 100
        if percentage < 100:
            return percentage
        else:
            return 100

    def get_progress(self):
        """NAME: get_progress
        PURPOSE: saves the current progress (percentage, number of stripes, number of spaces, and bar) and calls the
        function that times the process"""
        self.number_of_stripes = math.floor(self.get_percentage())
        self.number_of_spaces = 100 - self.number_of_stripes
        self.time_progress()
        self.bar = '\r[{}{}] {}%'.format(self.number_of_stripes * '-', self.number_of_spaces * ' ', int(self.percentage))

    def get_done_message(self, type='sec'):
        """NAME: get_done_message
        INPUT: type (default: sec), possible options: "sec", "min", "h"
        PURPOSE: returns the message telling in how many time the process is finished
        WARNING: if unsupported type is given, still the message in seconds will be returned"""
        time_unit = 'seconds'
        runtime = self.time_running
        if type == "min":
            time_unit = 'minutes'
            runtime = self.time_running/60
        elif type == "h":
            time_unit = 'hours'
            runtime = self.time_running/3600
        elif type != 'sec':
            warnings.warn('unsupported type: {} instead of ["sec", "min", "h"], returning output in seconds'.format(type), stacklevel=2)
        return "\nDone in {} {}".format(str(runtime), str(time_unit))

    def print_progress(self):
        """NAME: print_progress
        PURPOSE: write current progress to sys.sdout"""
        self.get_progress()
        sys.stdout.write(self.bar)

    def time_progress(self):
        """NAME: time_progress
        PURPOSE: save the time running of the current state"""
        self.time_running = time.time() - self.start_time

    def __str__(self):
        return self.bar


def main():
    print("Demo")
    pb = ProgressBar(100)
    pb.get_next(0)
    time.sleep(0.5)
    pb.get_next(10)
    time.sleep(0.5)
    pb.get_next(15)
    time.sleep(0.5)
    pb.get_next(20)
    time.sleep(0.5)
    pb.get_next(30)
    time.sleep(0.5)
    pb.get_next(40)
    time.sleep(0.5)
    pb.get_next(50)
    time.sleep(0.5)
    pb.get_next(60)
    time.sleep(0.5)
    pb.get_next(70)
    time.sleep(0.5)
    pb.get_next(80)
    time.sleep(0.5)
    pb.get_next(90)
    time.sleep(0.5)
    pb.get_next(100)


if __name__ == '__main__':
    main()




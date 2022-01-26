import csv


class Process:
    _processes = []

    _total_time = 0
    _idle_time = 0

    @staticmethod
    def set_total_idle_time(total, idle):
        Process._total_time = total
        Process._idle_time = idle

    @staticmethod
    def get_all_processes():
        return Process._processes

    @staticmethod
    def reset_processes():
        p: Process
        for p in Process._processes:
            p.response_time = 0
            p.waiting_time = 0
            p.turnaround_time = 0
            p.start_time = -1
            p.end_time = -1
            p.state = 0
            p.second_start_time = -1
            p.burst = 0

        Process._total_time = 0
        Process._idle_time = 0
        return

    def __init__(self, pid, arrival, cpu1, io, cpu2):
        self.pid = pid
        self.arrival_time = arrival
        self.cpu_time_1 = cpu1
        self.cpu_time_2 = cpu2
        self.io_time = io
        # self.response_time = 0 ############
        self.state = 0
        self.second_start_time = -1
        self.waiting_time = 0
        # self.turnaround_time = 0  ###########
        self.start_time = -1
        self.end_time = -1
        self.burst = 0
        Process._processes.append(self)

    def __str__(self):
        return f'Process {self.pid}'

    def _response_time(self):
        return self.start_time - self.arrival_time

    def _turnaround_time(self):
        return self.end_time - self.arrival_time + 1

    def get_remaining_time(self):
        if self.state == 0:
            return self.cpu_time_1 - self.burst
        else:
            return self.cpu_time_2 - self.burst

    def get_remaining_time_total(self):
        return self.cpu_time_1+self.cpu_time_2

    @classmethod
    def display(cls, algo):
        print(f"{algo} Algorithm\n")
        print("pid", "start", "end", "response", "", "waiting", "turnaround", sep='    ')
        i: Process
        for i in cls._processes:
            print(i.pid, i.start_time, i.end_time, i._response_time(), "", i.waiting_time, "", i._turnaround_time(),
                  sep='\t\t')
        print("---------------------------------------------------------------")
        print("Total Time:", Process._total_time)
        print("Idle Time:", Process._idle_time - 1)
        print("Avg. Waiting Time:", Process._get_avg_waiting_time())
        print("Avg. Response Time:", Process._get_avg_response_time())
        print("Avg. Turnaround Time:", Process._get_avg_turnaround_time())
        print("CPU Utilization:", Process._get_cpu_utilization())
        print("CPU Throughput:", Process._get_throughput())

    @classmethod
    def _get_avg_waiting_time(cls):
        i: Process
        summ = 0
        for i in cls._processes:
            summ += i.waiting_time
        return summ / len(cls._processes)

    @classmethod
    def _get_avg_response_time(cls):
        i: Process
        summ = 0
        for i in cls._processes:
            summ += i._response_time()
        return summ / len(cls._processes)

    @classmethod
    def _get_avg_turnaround_time(cls):
        i: Process
        summ = 0
        for i in cls._processes:
            summ += i._turnaround_time()
        return summ / len(cls._processes)

    @classmethod
    def _get_cpu_utilization(cls):
        burst_time = cls._total_time - cls._idle_time + 1
        return str(burst_time / cls._total_time)[:4]

    @classmethod
    def _get_throughput(cls):
        return str((len(cls._processes) / cls._total_time) * 1000)[:4]


class PreProcess:
    @staticmethod
    def read_and_create_processes():
        file = open("proces_inputs.csv")
        csv_header = csv.reader(file)
        header = next(csv_header)
        for row in csv_header:
            a = [int(x) for x in row]
            Process(a[0], a[1], a[2], a[3], a[4])
        file.close()

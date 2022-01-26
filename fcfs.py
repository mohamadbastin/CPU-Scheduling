from typing import List

from utils import Process


class FCFS:
    not_started_queue = []
    bursting = None
    waiting_queue = []
    io_room = []
    done_room = []

    total_time = 0
    idle_time = 0

    @classmethod
    def set_processes(cls, processes):
        for i in processes:
            cls.not_started_queue.append(i)

    @classmethod
    def run(cls):

        t = 0

        while len(cls.not_started_queue) > 0 or len(cls.waiting_queue) > 0 or len(
                cls.io_room) > 0 or cls.bursting is not None:
            a = []
            for p in cls.not_started_queue:
                if p.arrival_time == t:
                    cls.waiting_queue.append(p)
                    a.append(p)
            for i in a:
                cls.not_started_queue.remove(i)
            # io
            i: Process
            b = []
            for i in cls.io_room:
                if i.start_time + i.io_time + i.cpu_time_1 == t:
                    cls.waiting_queue.append(i)
                    i.state = 1
                    b.append(i)
            for i in b:
                cls.io_room.remove(i)

            # burst
            if cls.bursting is not None:
                c: Process = cls.bursting
                if c.state == 0:
                    if c.start_time + c.cpu_time_1 == t:
                        cls.bursting = None
                        cls.io_room.append(c)

                elif c.state == 1:
                    if c.second_start_time + c.cpu_time_2 == t:
                        c.end_time = t
                        cls.bursting = None
                        cls.done_room.append(c)

            # waiting & ready queue
            if cls.bursting is None:
                if len(cls.waiting_queue) > 0:
                    if cls.waiting_queue[0].arrival_time <= t:
                        cls.bursting = cls.waiting_queue[0]
                        if cls.waiting_queue[0].state == 0:
                            cls.bursting.start_time = t
                        else:
                            cls.bursting.second_start_time = t
                        cls.waiting_queue.pop(0)
                else:
                    cls.idle_time += 1
            for p in cls.waiting_queue:
                p.waiting_time += 1

            cls.total_time = t

            t += 1
        Process.set_total_idle_time(cls.total_time, cls.idle_time)

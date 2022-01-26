from typing import List

from utils import Process


class SRT:
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
                    if c.cpu_time_1 == c.burst:
                        cls.bursting = None
                        c.burst = 0
                        cls.io_room.append(c)

                elif c.state == 1:
                    if c.cpu_time_2 == c.burst:
                        c.end_time = t
                        cls.bursting = None
                        cls.done_room.append(c)
                if cls.bursting is not None:
                    if len(cls.waiting_queue) > 0:
                        if cls.find_shortest_job()[1] < c.get_remaining_time():
                            cls.bursting = None
                            cls.waiting_queue.append(c)
                        else:
                            c.burst += 1
                    else:
                        c.burst += 1

            # waiting & ready queue
            if cls.bursting is None:
                if len(cls.waiting_queue) > 0:
                    # if cls.waiting_queue[0].arrival_time <= t:
                    #     cls.bursting = cls.waiting_queue[0]
                    #     if cls.waiting_queue[0].state == 0:
                    #         cls.bursting.start_time = t
                    #     else:
                    #         cls.bursting.second_start_time = t
                    #     cls.waiting_queue.pop(0)
                    sj: Process = cls.find_shortest_job()[0]
                    cls.bursting = sj
                    if sj.state == 0:
                        if sj.start_time == -1:
                            sj.start_time = t
                    else:
                        if sj.second_start_time == -1:
                            sj.second_start_time = t
                    cls.waiting_queue.remove(sj)
                    sj.burst += 1

                else:
                    cls.idle_time += 1
            for p in cls.waiting_queue:
                p.waiting_time += 1

            cls.total_time = t

            t += 1
        Process.set_total_idle_time(cls.total_time, cls.idle_time)

    @classmethod
    def find_shortest_job(cls):
        x: Process
        a = [x.get_remaining_time() for x in cls.waiting_queue]
        b = min(a)
        bi = a.index(b)

        return cls.waiting_queue[bi], b

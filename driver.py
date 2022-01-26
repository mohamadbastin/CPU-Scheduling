from pprint import pprint

from round_robin import RoundRobin, RoundRobin2
from sjf import SJF
from srt import SRT
from utils import Process, PreProcess
from fcfs import FCFS

PreProcess.read_and_create_processes()

FCFS.set_processes(Process.get_all_processes())
FCFS.run()
Process.display("FCFS")
Process.reset_processes()
print("+" * 100)

SRT.set_processes(Process.get_all_processes())
SRT.run()
Process.display("SRT")
Process.reset_processes()
print("+" * 100)

SJF.set_processes(Process.get_all_processes())
SJF.run()
Process.display("SJF")
Process.reset_processes()
print("+" * 100)

RoundRobin.set_processes(Process.get_all_processes())
RoundRobin.run()
Process.display("Round Robin")
Process.reset_processes()
print("+" * 100)

RoundRobin2.set_processes(Process.get_all_processes())
RoundRobin2.run()
Process.display("Round Robin 2")
Process.reset_processes()
print("+" * 100)

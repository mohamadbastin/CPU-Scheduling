from pprint import pprint

from round_robin import RoundRobin
from sjf import SJF
from srt import SRT
from utils import Process, PreProcess
from fcfs import FCFS

PreProcess.read_and_create_processes()

# FCFS.run(Process.get_all_processes())
# Process.display("FCFS")
# Process.reset_processes()
# print("+" * 100)
#
# SRT.run(Process.get_all_processes())
# Process.display("SRT")
# Process.reset_processes()
# print("+" * 100)
#
# SJF.run(Process.get_all_processes())
# Process.display("SJF")
# Process.reset_processes()
# print("+" * 100)

RoundRobin.run(Process.get_all_processes())
Process.display("Round Robin")
Process.reset_processes()
print("+" * 100)

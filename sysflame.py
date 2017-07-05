import sys, subprocess, os, time, getopt
from os import environ as env
from sys import platform
import argparse
import shlex

def printbanner():
	print("	         /~\|                ")
	print("	(~\  /(~-|- |/~~||/~\ /~\ /~/")
	print("	_) \/ _) |  |\__||   |   |\/_")
	print("	  _/                             v 1.0.0")

def createGraph(program, fgpath, outputfile, frequency, cfilter, color):
	cmd = " -c './" + program + "'" 
	dtrace_cmd = " "
	filenamearr = (program.split("/"))
	programname = filenamearr[len(filenamearr)-1]
	programname = '"'+ ((programname).split())[0] +'"'

	if cfilter:
		cfilter = " -e " + cfilter	
	if not color:
		color = "hot"	

	if platform == "darwin" :
		DTRACE_PATH = subprocess.check_output("which dtrace", shell=True).strip()
		dtrace_cmd = "sudo "+ DTRACE_PATH + " -q -x ustackframes=100 -n 'profile-"+str(frequency)+" /execname==" + programname + " && arg1/ { @[ustack()] = count(); }' " + cmd + " | " +fgpath+ "stackcollapse.pl | "+fgpath+"flamegraph.pl --colors '" + color + "' --title '"+programname+"' >  "+ outputfile
	elif platform == "linux" or platform == "linux2":
		PERF_PATH = subprocess.check_output("which perf", shell=True).strip()
		dtrace_cmd = PERF_PATH + " record -F "+str(frequency)+ cfilter + " --call-graph dwarf -ag ./" + program + " && sudo "+PERF_PATH+" script | " +fgpath+ "stackcollapse-perf.pl | grep "+programname+" | "+fgpath+"flamegraph.pl --colors '" + color + "' --title '"+programname+"' >  "+ outputfile
	print(">> Profiling " + programname + " ...")
	subprocess.call(dtrace_cmd, shell=True)
	print(">> done")	
	
if __name__ == "__main__":
	printbanner()
	parser = argparse.ArgumentParser()
	flamepath, command, outputfile = "", "", ""
	parser.add_argument("-f", "--flamegraph-path", type=str, action="store", help="path to flamegraph directory")
	parser.add_argument("-o", "--output", action="store" ,type=str, help="file to write contents to")
	parser.add_argument("-c", "--command", action="store", type=str, help="Command to profile with args, -c 'cmd arg1 arg2 ...'")
	parser.add_argument("-sf", "--samp_freq", action="store", type=int, help="frequency in hertz to sample stack traces")
	parser.add_argument("-fl", "--filter", action="store", type=str, help="if perf, trace special cpu event/events")
	parser.add_argument("-cl", "--color", action="store", type=str, help="color theme for flamegraph")
	args = parser.parse_args()

	if args.command and args.output and args.flamegraph_path and args.samp_freq:	
		createGraph(args.command, args.flamegraph_path, args.output, args.samp_freq, args.filter, args.color)	 	
	else:	
		print("python sysflame.py -f/--flamegraph-path <path> -o/--output <output_file> -c/--command '<command> <args>' -sf <samp_freq> -fl/--filter cpu event/events -cl/--color color")

		



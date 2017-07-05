# cpustack_flamegraph
The purpose of this script is to automize the creation of a flame graph by using the framework created by Brendan Greggs 

Sysflame collects cpu stack traces by dynamic tracing (perf on linux, dtrace on osx) and generates a flamegraph from collected data. 

The sysmap tool is intended for analysing stack trace rates of functions across multiple flamegraphs, and output the result
in a matrix, which can then be used in a plotting program of your choosing. 

# cpustack_flamegraph
script to automize the creation of a flame graph (Brendan Gregg style)

Collects cpu stack traces from dynamic tracing (perf on linux, dtrace on osx)

python sysflame.py -o 'outputfilename'.svg -f 'flamegraph directory' -c 'command' -sf 'sampling rate for collecting cpu stack frames as int (for example 99)'

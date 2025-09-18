# Master thesis: Improving TCP Slow Start pacing in Linux
## Stian Sundkvist
### University of Oslo

## This repository
This repository is used for analysing and plotting data from the Linux kernel I am working on  
for the master thesis "Improving TCP Slow Start pacing in Linux"

This repository consists of two main directories:  
- ***mininet*** which is used for simulations in mininet, essentially generating data to analyse  
- ***analysis*** which is where all the plots and packet analysis is done  

## Filename structure
The pcap files, and their respective pdf plots have the following structure:  

[kernel_version]\_[CC algorithm]_[topology]_[iperf duration]s.pcap  

***for example:***
6.12.1022_reno_topology1_60s.pcap  
Which means: 
- Kernel version used is 6.12.1022, note that 6.12.10 is the base linux version used, and 6.12.10(*)  
represents a custom implementation based on the 6.12.10 source code.  
- The congestion control algorithm used is TCP reno
- The topology and link configurations etc. the simulation was run on was topology1 which corresponds  
to the topology found in /mininet/topologies/topology1
- The iperf test was run for 60 seconds

## Commit message structure  
All commit messages (after 18.09.25) related to experiments run with a specific kernel version, should  
be prefixed with the kernel version. For example:  
***git commit -m "6.12.1017 run iperf simulation for 30 seconds"***
We then know which kernel version each commit belongs to.  
The same commit structure will be present on the repository where the code for the kernel itself is:  
https://github.com/StianHaSu/custom-linux
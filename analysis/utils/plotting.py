from xmlrpc.client import MAXINT

import numpy as np
from scapy.layers.inet import TCP
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from scapy.utils import rdpcap

plt.rcParams.update({
    'font.size': 16,          # base font size
    'axes.titlesize': 20,     # title size
    'axes.labelsize': 18,     # x and y labels
    'xtick.labelsize': 14,    # x-axis tick labels
    'ytick.labelsize': 14,    # y-axis tick labels
    'legend.fontsize': 14,    # legend text
    'figure.titlesize': 20    # figure title
})

def plot_packets_from_pcap_file(
        filename: str,
        title: str,
        include_acks: bool = True,
        save_plot: bool = False
):
    pcap = rdpcap(filename)
    packets = get_data_from_packets(pcap)

    plot_packets(packets[0], packets[1], packets[2], packets[3],
                 title, include_acks=include_acks, save=save_plot)

def get_data_from_packets(packets):
    data_x = []
    data_y = []
    ack_x = []
    ack_y = []

    start_time = None
    smallest_seq = MAXINT
    smallest_ack = MAXINT

    packs = 0
    acks = 0
    for pkt in packets:
        if TCP in pkt:
            tcp = pkt[TCP]

            #if tcp.seq < 2 or tcp.ack < 2:
            #    continue

            if start_time is None:
                start_time = pkt.time

            delta_ms = (pkt.time - start_time) * 1000 # Time since start in ms

            flags = tcp.flags

            if not "A" == flags:
                if tcp.seq < smallest_seq:
                    smallest_seq = tcp.seq

                data_x.append(delta_ms)
                data_y.append(packs)
                packs += 1
            else:
                if tcp.ack < smallest_ack:
                    smallest_ack = tcp.ack

                ack_x.append(delta_ms)
                ack_y.append(acks)
                acks += 1

    return data_x, data_y, ack_x, ack_y


def plot_packets(data_x, data_y, ack_x, ack_y, title: str, include_acks: bool, save: bool = False):
    plt.figure(figsize=(10, 6))

    cutoff = 300

    data_x = data_x[0:cutoff]
    data_y = data_y[0:cutoff]
    ack_x = ack_x[0:cutoff]
    ack_y = ack_y[0:cutoff]

    plt.scatter(data_x, data_y, color='blue', label='Data packets', alpha=0.6)
    if include_acks:
        plt.scatter(ack_x, ack_y, color='red', label='ACKs', alpha=0.6, marker="x")

    plt.xlabel('Time since beginning (ms)')
    plt.ylabel('Sequence / ACK Number')
    plt.title(title)
    plt.legend()
    plt.yscale('linear')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.grid(True)
    plt.tight_layout()

    if save:
        name = "_".join(title.split(" "))
        print("Name: ", name)
        plt.savefig(name + ".pdf")

    plt.show()



def normalize_y_axis(seq_nrs: list[int], low: int):
    normalized = []
    for seq_nr in seq_nrs:
        normalized.append(seq_nr - low)

    return normalized
#!/usr/bin/env python3

import json
import struct
from typing import Dict

from scapy.all import *


def extract_incoming_timestamps(dport: int, pcapf: str) -> Dict[int, list]:
    pkts = rdpcap(pcapf)
    processed_frames = dict()

    for pkt in pkts:
        if pkt[TCP].dport == dport and Raw in pkt:
            # pkt[TCP].show()
            data = bytes(pkt[TCP].payload)
            h_len_net = data[:4]
            # print(h_len_net)
            try:
                (h_len,) = struct.unpack('>I', h_len_net)
                # print(h_len)
                header_net = data[4:4 + h_len]
                (header,) = struct.unpack('>{}s'.format(h_len), header_net)
                d_header = json.loads(header.decode('utf-8'))

                # store all timestamps
                if d_header['frame_id'] not in processed_frames.keys():
                    processed_frames[d_header['frame_id']] = []

                processed_frames[d_header['frame_id']].append(pkt.time * 1000)


            except Exception as e:
                # print(e)
                continue

    return processed_frames

def extract_outgoing_timestamps(sport: int, pcapf: str) -> Dict[int, list]:
    pkts = rdpcap(pcapf)
    processed_frames = dict()

    for pkt in pkts:
        if pkt[TCP].sport == sport and Raw in pkt:
            # pkt[TCP].show()
            data = bytes(pkt[TCP].payload)
            h_len_net = data[:4]
            # print(h_len_net)
            try:
                (h_len,) = struct.unpack('>I', h_len_net)
                # print(h_len)
                header_net = data[4:4 + h_len]
                (header,) = struct.unpack('>{}s'.format(h_len), header_net)
                d_header = json.loads(header.decode('utf-8'))

                # store all timestamps
                if d_header['frame_id'] not in processed_frames.keys():
                    processed_frames[d_header['frame_id']] = []

                processed_frames[d_header['frame_id']].append(pkt.time * 1000)


            except Exception as e:
                # print(e)
                continue

    return processed_frames



if __name__ == '__main__':
    print(extract_incoming_timestamps(8999, 'tcp.pcap'))

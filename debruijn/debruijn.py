#!/bin/env python3
# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    A copy of the GNU General Public License is available at
#    http://www.gnu.org/licenses/gpl-3.0.html

"""Perform assembly based on debruijn graph."""

import argparse
import os
import sys
import networkx as nx
import matplotlib
from operator import itemgetter
import random
random.seed(9001)
from random import randint
import statistics


__author__ = "Your Name"
__copyright__ = "Universite Paris Diderot"
__credits__ = ["Your Name"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Your Name"
__email__ = "your@email.fr"
__status__ = "Developpement"

def isfile(path):
    """Check if path is an existing file.
      :Parameters:
          path: Path to the file
    """
    if not os.path.isfile(path):
        if os.path.isdir(path):
            msg = "{0} is a directory".format(path)
        else:
            msg = "{0} does not exist.".format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def get_arguments():
    """Retrieves the arguments of the program.
      Returns: An object that contains the arguments
    """
    # Parsing arguments
    parser = argparse.ArgumentParser(description=__doc__, usage=
                                     "{0} -h"
                                     .format(sys.argv[0]))
    parser.add_argument('-i', dest='fastq_file', type=isfile,
                        required=True, help="Fastq file")
    parser.add_argument('-k', dest='kmer_size', type=int,
                        default=21, help="K-mer size (default 21)")
    parser.add_argument('-o', dest='output_file', type=str,
                        default=os.curdir + os.sep + "contigs.fasta",
                        help="Output contigs in fasta file")
    return parser.parse_args()


def read_fastq(fastq_file):
    if(isfile(fastq_file)):
        with open(fastq_file, "r") as f:
            for line in f:
                yield next(f).replace('\n','')
                next(f)
                next(f)
                



def cut_kmer(read, kmer_size):
    i=0
    taillelimite = i+kmer_size
    while  ( taillelimite <len(read) +1):
        kmer = read[i:i+kmer_size]
        yield kmer
        i+=1
        taillelimite+=1 



def build_kmer_dict(fastq_file, kmer_size):
    dictio = dict()
    for gen in read_fastq(fastq_file):
        kmers = cut_kmer(gen,kmer_size)
        for kmer in kmers:
            if (kmer in dictio):
                dictio[kmer]+=1
            else:
                dictio[kmer]=1
    return dictio


def build_graph(kmer_dict):
    G=nx.DiGraph()
    for kmer,poid in kmer_dict.items():
        G.add_edge(kmer[:-1] ,kmer[1:], weight=poid)
    return G

    
def remove_paths(graph, path_list, delete_entry_node, delete_sink_node):
    G = nx.DiGraph(graph)
    for liste in path_list:
        for i in range(len(liste)-1):
            G.remove_edge(liste[i],liste[i+1])

            if (i != 0 and i != len(liste)-1):
                G.remove_node(liste[i])
            elif (i==0 and delete_entry_node==True):
                G.remove_node(liste[i])

        if delete_sink_node:
            G.remove_node(liste[-1])
    return G
    

def std(data):
    return statistics.stdev(data)


def select_best_path(graph, path_list, path_length, weight_avg_list, 
                     delete_entry_node=False, delete_sink_node=False):
    pass

def path_average_weight(graph, path):
    c=0
    n=0
    for i in range(len(path)-1):
        c += graph[path[i]][path[i+1]]["weight"]
        n+=1
    return c/n

def solve_bubble(graph, ancestor_node, descendant_node):
    pass

def simplify_bubbles(graph):
    pass

def solve_entry_tips(graph, starting_nodes):
    pass

def solve_out_tips(graph, ending_nodes):
    pass

def get_starting_nodes(graph):
    return [node for node,degree in graph.in_degree() if degree==0]

def get_sink_nodes(graph):
    return [node for node,degree in graph.out_degree() if degree ==0 ]
    

def get_contigs(graph, starting_nodes, ending_nodes):
    L=[]
    for i in starting_nodes:
        for j in ending_nodes:
            chemin = nx.shortest_path(graph, i, j)
            tmp = chemin[0]
            for k in range(1,len(chemin)):
                tmp += chemin[k][len(starting_nodes[0])-1]
            taille = len(tmp)
            L.append((tmp,taille))
    return L

def fill(text, width=80):
    """Split text with a line return to respect fasta format"""
    return os.linesep.join(text[i:i+width] for i in range(0, len(text), width))

def save_contigs(contigs_list, output_file):
    with open(output_file,'w') as f:
        c=0
        for contig,tailleContig in contigs_list:
            print(contig,tailleContig)
            f.write(f">contig_{c} len={tailleContig}\n")
            f.write(f"{fill(contig)}\n")
            c+=1
    pass

#==============================================================
# Main program
#==============================================================
def main():
    """
    Main program function
    """
    # Get arguments
    args = get_arguments()


if __name__ == '__main__':
    main()

import zerorpc
import json
import StringIO
import pandas as pd
import numpy as np

import logging
logging.basicConfig(filename='logs/graph.log',level=logging.DEBUG)

from slicematrixIO import SliceMatrix

class io_rpc(object):
    def __init__(self):
        logging.info("starting sliceserver io rpc server node")
        name_file = open("iso.name", "r")
        self.sm = SliceMatrix(open("../.env.example", "r").read().split("=")[-1].replace("\n",""))
        self.model_name = name_file.read()
        self.model = self.sm.Isomap(name = self.model_name)
        logging.info("loaded network graph model")
        
    def nodes(self):
        # get nodes for model
        nodes = self.model.nodes()
        logging.debug(nodes)
        return nodes

    def links(self):
        # get links for model
        links = self.model.edges()
        logging.debug(links)
        return links

    def embedding(self):
        # get embedding for nodes
        embedding = self.model.embedding()
        embedding.columns = ["x", "y"]
        return embedding.T.to_json()

    def rankNodes(self, statistic = "closeness_centrality"):
        # get node stats
        stats = self.model.rankNodes(statistic)[statistic]
        logging.debug(stats.T.to_json())
        return stats.to_json()

s = zerorpc.Server(io_rpc(), pool_size = 4, heartbeat = 30)
s.bind("tcp://127.0.0.1:5240")
s.run()


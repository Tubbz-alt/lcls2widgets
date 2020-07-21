import numpy as np
import zmq
import asyncio
import time
from collections import namedtuple
from multiprocessing import Process
from lcls2widgets.DisplayWidgets import ScatterWidget
from pyqtgraph.Qt import QtGui, QtCore
from asyncqt import QEventLoop


Addr = namedtuple('Addrs', ['name', 'view'])


def run_worker():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5557")

    while True:
        topic = 'view:graph:_auto_Projection.0.Out'
        socket.send_string(topic, zmq.SNDMORE)
        timestamp = 1  # currently unused on client side
        socket.send_pyobj(timestamp, zmq.SNDMORE)
        msg = np.random.randn(1024)
        socket.send_pyobj(msg)

        topic = 'view:graph:_auto_Projection.1.Out'
        socket.send_string(topic, zmq.SNDMORE)
        timestamp = 1
        socket.send_pyobj(timestamp, zmq.SNDMORE)
        msg = np.random.randn(1024)
        socket.send_pyobj(msg)

        time.sleep(0.1)

    ctx.destroy()


class PlotWindow(QtCore.QObject):

    def __init__(self):
        super().__init__()
        topics = {'Projection.0.Out': '_auto_Projection.0.Out',
                  'Projection.1.Out': '_auto_Projection.1.Out'}
        # Use the same topics for multiple traces in a plot
        # AsyncFetcher deduplicate and only makes as many sockets as needed
        terms = {'X': 'Projection.0.Out', 'Y': 'Projection.1.Out',
                 'X.1': 'Projection.1.Out', 'Y.1': 'Projection.0.Out'}

        self.app = QtGui.QApplication([])
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)

        self.win = QtGui.QMainWindow()

        addr = Addr('graph', 'tcp://127.0.0.1:5557')
        self.widget = ScatterWidget(topics, terms, addr, parent=self.win)
        self.task = asyncio.ensure_future(self.widget.update())

        self.win.setCentralWidget(self.widget)
        self.win.show()

        try:
            self.loop.run_forever()
        finally:
            if not self.task.done():
                self.task.cancel()

            self.widget.close()


if __name__ == "__main__":
    worker = Process(target=run_worker)
    worker.start()

    PlotWindow()

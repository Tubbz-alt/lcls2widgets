import numpy as np
import zmq
import asyncio
from collections import namedtuple
from multiprocessing import Process
from lcls2widgets.DisplayWidgets import LineWidget
from pyqtgraph.Qt import QtGui, QtCore
from asyncqt import QEventLoop


Addr = namedtuple('Addrs', ['name', 'view'])


def run_worker():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:5557")

    while True:
        topic = 'view:graph:_auto_Projection.0.Out'
        socket.send_string(topic, zmq.SNDMORE)
        msg = np.random.randn(1024)
        socket.send_pyobj(msg)

        topic = 'view:graph:_auto_Projection.1.Out'
        socket.send_string(topic, zmq.SNDMORE)
        msg = np.random.randn(1024)
        socket.send_pyobj(msg)

    ctx.destroy()


class PlotWindow(QtCore.QObject):

    def __init__(self):
        super().__init__()
        topics = {'Projection.0.Out': '_auto_Projection.0.Out',
                  'Projection.1.Out': '_auto_Projection.1.Out'}
        terms = {'X': 'Projection.0.Out', 'Y': 'Projection.1.Out'}

        self.app = QtGui.QApplication([])
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)

        self.win = QtGui.QMainWindow()

        addr = Addr('graph', 'tcp://127.0.0.1:5557')
        self.widget = LineWidget(topics, terms, addr, parent=self.win)
        self.task = asyncio.ensure_future(self.widget.update())

        self.win.setCentralWidget(self.widget)
        self.win.show()
        self.loop.run_forever()


if __name__ == "__main__":
    worker = Process(target=run_worker)
    worker.start()

    PlotWindow()

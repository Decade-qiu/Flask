import os
import signal
import psutil


connections = psutil.net_connections(kind='tcp')
for conn in connections:
    if conn.status == psutil.CONN_ESTABLISHED and conn.laddr.port == 1935:
        os.kill(conn.pid, signal.SIGTERM)
        break
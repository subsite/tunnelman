

from sshtunnel import SSHTunnelForwarder

class Tunnel():

    def __init__(self, profile):
        self.profile = profile
        self.server = None


    def open_tunnel(self):
        self.server = SSHTunnelForwarder(
            (profile['server'], profile['ssh_port']),
            ssh_username=profile['username'],
            local_bind_addresses=local_bind_addresses,
            remote_bind_addresses=remote_bind_addresses
        )
        self.server.start()

    def close_tunnel(self):
        self.server.stop()


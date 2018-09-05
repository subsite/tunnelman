

from sshtunnel import SSHTunnelForwarder
from app.config import Config 

config = Config()

class Tunnel():

    _all_tunnels = []

    def __init__(self, profile):
        Tunnel._all_tunnels.append(self)
        self.profile = profile
        self.app_conf = config.conf['app']
        self.status = { 'message': "Closed", 'tunnels': {} }
        # index profile tunnels by port1
        self.port_index = dict((d['port1'], dict(d, index=index)) for (index, d) in enumerate(profile['tunnels']))
        localhost = self.app_conf['localhost']
        self.local_bind_addresses = []
        self.remote_bind_addresses = []

        #print(profile)

        for t in profile['tunnels']:
            self.local_bind_addresses.append((localhost, t['port1']))
            self.remote_bind_addresses.append((t['host'], t['port2']))
            profile['ssh_port'] = profile.get('ssh_port', self.app_conf['default_ssh_port'])

        self.server = None

    def open_tunnel(self):

        try:
            self.server = SSHTunnelForwarder(
                (self.profile['server'], self.profile['ssh_port']),
                ssh_username=self.profile['username'],
                local_bind_addresses=self.local_bind_addresses,
                remote_bind_addresses=self.remote_bind_addresses,
                set_keepalive=self.app_conf['send_keepalive_seconds']
            )
        
            self.server.start()
            self.set_status()
            return True
        except Exception as e:
            self.set_status("Error")
            print(e)
            return e

    def close_tunnel(self):
        if self.server:
            self.server.stop()
            self.set_status("Closed")
            print("Closed tunnel {}".format(self.profile['name']))
        else:
            print("Can't close {}, Tunnel not open".format(self.profile['name']))

    
    def set_status(self, msg="Closed"):
        #print(self.profile['tunnels'])
        tunnels = []
        for t in self.server.tunnel_is_up:
            tunnelstatus = self.port_index[t[1]]
            tunnelstatus['open'] = self.server.tunnel_is_up[t]
            tunnels.append(tunnelstatus)
            #print("port:{}, open:{}".format(t))
        self.status = { 'message': msg, 'tunnels':  tunnels }
        return True

    
    


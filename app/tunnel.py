

from sshtunnel import SSHTunnelForwarder
import app.util

utl = app.util.Utl()


class Tunnel:

    profile_id = ""

    def __init__(self, profile):
        #Tunnel._all_tunnels.append(self)
        self.profile_id = profile["id"]
        self.profile = profile
        self.app_conf = utl.conf['app']
        self.status = { 'message': "Closed", 'tunnels': {} }
        self.is_open = False
        # index profile tunnels by port1
        self.port_index = utl.list_to_dict_by_key(profile['tunnels'], "port1")
        localhost = self.app_conf['localhost']
        self.local_bind_addresses = []
        self.remote_bind_addresses = []

        #print(profile)

        for t in profile['tunnels']:
            self.local_bind_addresses.append((localhost, t['port1']))
            self.remote_bind_addresses.append((t['host'], t['port2']))

        self.server = None

    def open_tunnel(self):

        try:
            self.server = SSHTunnelForwarder(
                (self.profile['server'], int(self.profile.get('ssh_port', 22))),
                ssh_username=self.profile['username'],
                local_bind_addresses=self.local_bind_addresses,
                remote_bind_addresses=self.remote_bind_addresses,
                set_keepalive=self.app_conf.get('send_keepalive_seconds', 0)
            )
        
            self.server.start()
            self.set_status("Open")
            self.is_open = True
            return True
        except Exception as e:
            self.set_status("Error")
            self.is_open = False
            print(e)
            return e

    def close_tunnel(self):
        if self.server:
            self.server.stop()
            self.set_status("Closed")
            self.is_open = False
            print("Closed tunnel {}".format(self.profile['name']))
        else:
            print("Can't close {}, Tunnel not open".format(self.profile['name']))
    
    def set_status(self, msg="Unknown"):
        #print(self.profile['tunnels'])
        tunnels = []
        
        for t in self.server.tunnel_is_up:
            tunnelstatus = self.port_index[t[1]]
            tunnelstatus['open'] = self.server.tunnel_is_up[t]
            tunnels.append(tunnelstatus)
            #print("port:{}, open:{}".format(t))
        self.status = { 'message': msg, 'tunnels':  tunnels }
        return True

    
    


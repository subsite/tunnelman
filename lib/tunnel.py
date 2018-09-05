

from sshtunnel import SSHTunnelForwarder

class Tunnel():

    _all_tunnels = []

    def __init__(self, profile):
        Tunnel._all_tunnels.append(self)
        self.profile = profile
        self.id = None 
        self.status = "Closed"

        localhost = "127.0.0.1"
        self.local_bind_addresses = []
        self.remote_bind_addresses = []

        #print(profile)

        for t in profile['tunnels']:
            localport = int(t['route'].split(":")[0])
            remote_addr = t['route'].split(":")[1]
            remote_port = int(t['route'].split(":")[2])    
            self.local_bind_addresses.append((localhost,localport))
            self.remote_bind_addresses.append((remote_addr,remote_port))


            profile['ssh_port'] = 22


        self.server = None


    def open_tunnel(self):

        try:
            self.server = SSHTunnelForwarder(
                (self.profile['server'], self.profile['ssh_port']),
                ssh_username=self.profile['username'],
                local_bind_addresses=self.local_bind_addresses,
                remote_bind_addresses=self.remote_bind_addresses
            )
        
            self.server.start()
            self.status = "Open"
            return "started"
        except Exception as e:
            return e


    def close_tunnel(self):
        if self.server:
            self.server.stop()
            self.status = "Closed"
            print("Closed tunnel {}".format(self.profile['name']))
        else:
            print("Can't close {}, Tunnel not open".format(self.profile['name']))

    
        



import subprocess
import time
from app.util import utl


class HostKeyError(Exception):
    """SSH encountered an unknown host key."""
    pass


class Tunnel:

    def __init__(self, profile):
        self.profile_id = profile["id"]
        self.profile = profile
        self.app_conf = utl.conf['app']
        self.status = {'message': "Closed"}
        self.is_open = False
        self._process = None

    def _build_cmd(self, trust_new_host=False):
        cmd = [
            'ssh', '-N',
            '-o', 'BatchMode=yes',
            '-o', 'ExitOnForwardFailure=yes',
        ]
        if trust_new_host:
            cmd += ['-o', 'StrictHostKeyChecking=accept-new']
        keepalive = self.profile.get(
            'send_keepalive_seconds',
            self.app_conf.get('send_keepalive_seconds', 0)
        )
        if keepalive:
            cmd += ['-o', f'ServerAliveInterval={int(keepalive)}',
                    '-o', 'ServerAliveCountMax=3']

        ssh_port = int(self.profile.get('ssh_port', 22))
        if ssh_port != 22:
            cmd += ['-p', str(ssh_port)]

        localhost = self.app_conf.get('localhost', '127.0.0.1')
        for t in self.profile['tunnels']:
            cmd += ['-L', f"{localhost}:{t['port1']}:{t['host']}:{t['port2']}"]

        cmd.append(f"{self.profile['username']}@{self.profile['server']}")
        return cmd

    def open_tunnel(self, trust_new_host=False):
        utl.log(f"[{self.profile['name']}] Connecting to {self.profile['server']}...")
        try:
            self._process = subprocess.Popen(
                self._build_cmd(trust_new_host),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            # Wait briefly: ExitOnForwardFailure means ssh exits fast on failure,
            # and stays running on success.
            time.sleep(2)
            rc = self._process.poll()
            if rc is not None:
                stderr = self._process.stderr.read().strip()
                self._process = None
                self.status = {'message': "Error"}
                self.is_open = False
                print(f"[{self.profile['name']}] {stderr or f'ssh exited with code {rc}'}")
                if 'Host key verification failed' in stderr:
                    return HostKeyError(stderr)
                return Exception(stderr or f"ssh exited with code {rc}")
            forwards = ', '.join(
                f"{t['port1']} → {t['host']}:{t['port2']}"
                for t in self.profile['tunnels']
            )
            utl.log(f"[{self.profile['name']}] Open ({forwards})")
            self.status = {'message': "Open"}
            self.is_open = True
            return True
        except Exception as e:
            if self._process:
                self._process.kill()
                self._process = None
            self.status = {'message': "Error"}
            self.is_open = False
            print(f"[{self.profile['name']}] {e}")
            return e

    def close_tunnel(self):
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None
        utl.log(f"[{self.profile['name']}] Closed")
        self.status = {'message': "Closed"}
        self.is_open = False

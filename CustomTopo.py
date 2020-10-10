from mininet.net import Mininet
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.node import UserSwitch
from mininet.node import RemoteController
from mininet.log import setLogLevel, info

class MyTopo(Topo):
    def __init__( self ):
        print('*'*10+' initialize topology '+'*'*10)
        # Initialize topology
        Topo.__init__( self )
		print('*'*10+' adding switch '+'*'*10)
        # Add hosts and switches
        
    	s3 = self.addSwitch('s3')
    	s8 = self.addSwitch('s8')
    	s2 = self.addSwitch('s2')
    	s11 = self.addSwitch('s11')
    	s6 = self.addSwitch('s6')
    	s5 = self.addSwitch('s5')
    	s4 = self.addSwitch('s4')
    	s10 = self.addSwitch('s10')
    	s7 = self.addSwitch('s7')
    	s12 = self.addSwitch('s12')
    	s9 = self.addSwitch('s9')
    	s1 = self.addSwitch('s1')
    	s13 = self.addSwitch('s13')
    
		print('*'*10+' adding hosts '+'*'*10)
		h15 = self.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None)
    	h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    	h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    	h5 = self.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    	h26 = self.addHost('h26', cls=Host, ip='10.0.0.26', defaultRoute=None)
    	h17 = self.addHost('h17', cls=Host, ip='10.0.0.17', defaultRoute=None)
    	h19 = self.addHost('h19', cls=Host, ip='10.0.0.19', defaultRoute=None)
    	h6 = self.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    	h20 = self.addHost('h20', cls=Host, ip='10.0.0.20', defaultRoute=None)
    	h27 = self.addHost('h27', cls=Host, ip='10.0.0.27', defaultRoute=None)
    	h18 = self.addHost('h18', cls=Host, ip='10.0.0.18', defaultRoute=None)
    	h9 = self.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    	h8 = self.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    	h13 = self.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None)
    	h22 = self.addHost('h22', cls=Host, ip='10.0.0.22', defaultRoute=None)
    	h16 = self.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None)
    	h23 = self.addHost('h23', cls=Host, ip='10.0.0.23', defaultRoute=None)
    	h10 = self.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    	h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    	h11 = self.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
    	h12 = self.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
    	h25 = self.addHost('h25', cls=Host, ip='10.0.0.25', defaultRoute=None)
    	h24 = self.addHost('h24', cls=Host, ip='10.0.0.24', defaultRoute=None)
    	h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    	h14 = self.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None)
    	h21 = self.addHost('h21', cls=Host, ip='10.0.0.21', defaultRoute=None)
    	h7 = self.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)

		# Add links
   		print('*'*10+' adding links '+'*'*10)
    	self.addLink(s5, s2)
    	self.addLink(s2, s6)
    	self.addLink(s2, s7)
    	self.addLink(s5, h1)
    	self.addLink(s5, h2)
    	self.addLink(s5, h3)
    	self.addLink(s6, h4)
    	self.addLink(s6, h5)
    	self.addLink(s6, h6)
    	self.addLink(s7, h7)
    	self.addLink(s7, h8)
    	self.addLink(s7, h9)
    	self.addLink(s3, s9)
    	self.addLink(s8, s3)
    	self.addLink(s8, h10)
    	self.addLink(s8, h11)
    	self.addLink(s8, h12)
    	self.addLink(s9, h13)
    	self.addLink(s9, h14)
    	self.addLink(s9, h15)
    	self.addLink(s3, s10)
    	self.addLink(s10, h16)
    	self.addLink(s10, h17)
    	self.addLink(s10, h18)
    	self.addLink(s4, s12)
    	self.addLink(s4, s11)
    	self.addLink(s11, h19)
    	self.addLink(s11, h20)
    	self.addLink(s11, h21)
    	self.addLink(s12, h22)
    	self.addLink(s12, h23)
    	self.addLink(s12, h24)
    	self.addLink(s13, h25)
    	self.addLink(s13, h26)
    	self.addLink(s13, h27)
    	self.addLink(s4, s13)
    	self.addLink(s1, s3)
    	self.addLink(s1, s4)
    	self.addLink(s2, s1)


if __name__ == '__main__':  
    topo = MyTopo()
    net = Mininet(topo=topo, switch=UserSwitch,controller=None)
    c0=net.addController(name='c0',controller=RemoteController,ip='127.0.0.1',port=6653)
    net.start()
    CLI(net)
    net.stop()


from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import random

def myNetwork():
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='192.168.56.103',
                      protocol='tcp',
                      port=6633)
    s0=net.addSwitch('s0',cls=OVSKernelSwitch)
    for i in range(3):
        #  aggregation switches with 100 bw and 7.5+-2.5 delay
        rand_delay_aggregation=round(random.uniform(0.1, 5),2)
        para1 = {'bw':100,'delay':'{}ms'.format(5+rand_delay_aggregation)}
        aggregation=net.addSwitch('s{0}'.format(i+1), cls=OVSKernelSwitch)
        net.addLink(aggregation, s0,cls=TCLink,**para1)
        for j in range(3):
                # edge switches with 40 bw and 10+-5 delay
            rand_delay_edge=round(random.uniform(0.1, 10),2)
            para2 = {'bw':40,'delay':'{}ms'.format(5+rand_delay_edge)}
            edge=net.addSwitch('s{0}'.format((3)+(3*i)+j+1), cls=OVSKernelSwitch)
            net.addLink(aggregation, edge,cls=TCLink,**para2)
            for k in range(3):
                    # host with 4+-1 bw and 37+-5 delay
                rand_delay_host=round(random.uniform(0.1, 10),2)
                rand_bw=round(random.uniform(0.1, 2),2)
                host=net.addHost('h{0}'.format((i*9)+(j*3)+k), ip='10.{0}.{1}.{2}'.format((i),(j),(k+1)),cls=Host,defaultRoute=None)
                linkopts = {'bw':(5-rand_bw),'delay':'{}ms'.format(32+rand_delay_host)}
                net.addLink(host, edge,cls=TCLink, **linkopts)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
    info( '*** Starting switches\n')
    for i in range(13):
        net.get('s{}'.format(i)).start([c0])
    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

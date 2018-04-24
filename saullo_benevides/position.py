#!/usr/bin/python

'Setting the position of nodes'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.wifi.node import OVSKernelAP
from mininet.wifi.link import wmediumd, _4address
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.wmediumdConnector import interference


def topology():

    "Create a network."
    net = Mininet_wifi( controller=Controller, accessPoint=OVSKernelAP,
                        link=wmediumd, wmediumd_mode=interference,
                        configure4addr=True, autoAssociation=False )

    print "*** Creating nodes"
    ap1 = net.addAccessPoint('ap1',_4addr='ap', ssid='new-ssid1', mode='g', channel='1',
                   position='25,25,0')
    ap2 = net.addAccessPoint('ap2',_4addr='client', ssid='new-ssid', mode='g', channel='1',
                   position='55,55,0')
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position='65,75,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8',
                   position='85,75,0')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8',
                   position='15,25,0')
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.8/8',
                   position='35,25,0')
    c1 = net.addController('c1', controller=Controller)
    h1 = net.addHost ('h1', ip='10.0.0.3/8')
    h2 = net.addHost ('h2', ip='10.0.0.5/8')

    net.propagationModel(model="logDistance", exp=4.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(ap1, h1)
    net.addLink(ap2, h2)
    net.addLink(ap1, ap2, cls=_4address)
    net.addLink(sta1, ap2)
    net.addLink(sta2, ap2)
    net.addLink(sta3, ap1)
    net.addLink(sta4, ap1)

    net.plotGraph(max_x=200, max_y=200)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    print "*** Running CLI"
    CLI_wifi(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()


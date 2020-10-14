from operator import attrgetter
from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, set_ev_cls
from ryu.lib import hub
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from webob import Response
import json

scadaRecorderName = 'scadaRecorderRESTapi'
portStatUrl = '/scada/status/port'
flowStatUrl = '/scada/status/flow'

class ScadaRecorderREST(simple_switch_13.SimpleSwitch13):
	_CONTEXTS = {'wsgi':WSGIApplication}
	def __init__(self, *args, **kwargs):
		super(ScadaRecorderREST, self).__init__(*args, **kwargs)
		self.datapaths = {}
		self.flowstatus = None
		self.portstatus = None
		self.monitor_thread = hub.spawn(self._monitor)
		self.portinfo = {}
		wsgi = kwargs['wsgi']
		wsgi.register(ScadaRecorderController,{scadaRecorderName: self})

	@set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER, DEAD_DISPATCHER])
	def _state_change_handler(self, ev):
		datapath = ev.datapath
		if ev.state == MAIN_DISPATCHER:
			if not datapath.id in self.datapaths:
				self.logger.debug('reg datapath: %016x', datapath.id)
				self.datapaths[datapath.id] = datapath
		elif ev.state == DEAD_DISPATCHER:
			if datapath.id in self.datapaths:
				self.logger.debug('unreg datapath: %016x',datapath.id)
				del self.datapaths[datapath.id]
	
	def _monitor(self):
		while True:
			for dp in self.datapaths.values():
				self._request_status(dp)
			hub.sleep(10)
	
	def _request_status(self, datapath):
		self.logger.debug('status request: %016x',datapath.id)
		ofproto = datapath.ofproto
		ofproto_parser = datapath.ofproto_parser

		req = ofproto_parser.OFPFlowStatsRequest(datapath)
		datapath.send_msg(req)
		
		req = ofproto_parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
		datapath.send_msg(req)

	@set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
	def _flow_stats_reply_handler(self, ev):
		self.flowstatus = json.dumps(ev.msg.to_jsondict(), ensure_ascii=True, indent=3, sort_keys=True)	

	@set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
	def _port_stats_reply_handler(self,ev):
		for stat in sorted(ev.msg.body, key=attrgetter('port_no')):
			idx = str(ev.msg.datapath.id)
			temp = {
				'rx_packets':stat.rx_packets, 
				'rx_bytes':stat.rx_bytes, 
				'rx_errors':stat.rx_errors,
				'tx_packets':stat.tx_packets, 
				'tx_bytes':stat.tx_bytes, 
				'tx_error':stat.tx_errors
			}

			if idx not in self.portinfo:
				self.portinfo[idx] = {}
			if stat.port_no not in self.portinfo[idx]:
				self.portinfo[idx][stat.port_no] = {}			
			self.portinfo[idx][stat.port_no] = temp
			
		self.portstatus = json.dumps(self.portinfo, ensure_ascii=True, indent=3, sort_keys=True)	
	
		
class ScadaRecorderController(ControllerBase):

	def __init__(self, req, link, data, **config):
		super(ScadaRecorderController, self).__init__(req, link, data, **config)
		self.recorderData = data[scadaRecorderName]

	@route('ScadaRecorder', portStatUrl, methods=['GET'])
	def list_Port_Stat(self, req, **kwargs):
		return Response(
			content_type='application/json; charset=UTF-8',
			body = self.recorderData.portstatus
		)
	
	@route('ScadaRecorder', flowStatUrl, methods=['GET'])
	def list_Flow_Stat(self, req, **kwargs):
		return Response(
			content_type='application/json; charset=UTF-8',
			body = self.recorderData.flowstatus
		)


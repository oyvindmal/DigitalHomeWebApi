import web
import json
import tellcore.telldus as td
import tellcore.constants as tdconst
import soco
from soco import SoCo

class rTelldusSensor:
	def __init__(self, id, temperature):
		self.id = id
		self.temperature = temperature

	def toJSON(self):
		return dict(id=self.id, temperature=self.temperature)

class rTelldusSwitch:
	def __init__(self, id, name, lastsent):
		self.id = id
		self.name = name
		self.lastsent = lastsent

	def toJSON(self):
		return dict(id = self.id, name = self.name, lastsent = self.lastsent)		

class SonosDevice:
	def __init__(self, name, ip):
		self.name = name
		self.ip = ip

	def toJSON(self):
		return dict(name=self.name, ip=self.ip)


urls = (
'/', 'index',
'/test/(\d+\.\d+\.\d+\.\d+)', 'test',
'/telldus/sensor/(\d+)', 'telldusSensor',
'/telldus/switch/(\d+)/(on|off|state)', 'telldusSwitchOnOff',
'/telldus/switches', 'telldusSwitchList',
'/sonos/players', 'sonosPlayerList',
'/sonos/(\d+\.\d+\.\d+\.\d+)', 'sonosPlayerInfo'
)

class index:
	def GET(self):
		return "Hello World!"

class telldusSensor:
	def GET(self, id):
		web.header('Content-Type', 'application/json')
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		core = td.TelldusCore()
		sensor = ""
		sensors = core.sensors()
		for (i, s) in enumerate(sensors):
			sensor_id = s.id
			if sensor_id == int(id):
				sensor = s

		so = rTelldusSensor(sensor.id, sensor.temperature().value)

		return json.dumps(so.toJSON())
		
class telldusSwitchOnOff:
	 def GET(self, id, action):
                core = td.TelldusCore()
		switch = "none"
		switches = core.devices()
		for (i, d) in enumerate(switches):
			switch_id = d.id
			if switch_id == int(id):
				switch = d
		
		if switch == "none":
			return "Switch not found"
			
			
		last =  switch.last_sent_command(tdconst.TELLSTICK_TURNON | tdconst.TELLSTICK_TURNOFF | tdconst.TELLSTICK_DIM)
		if last == tdconst.TELLSTICK_TURNON:
			cmd_str = "ON"
		elif last  == tdconst.TELLSTICK_TURNOFF:
			cmd_str = "OFF"
		elif last == tdconst.TELLSTICK_DIM:
			cmd_str = "DIMMED:{}".format(switch.last_sent_value())
		else:
			cmd_str = "UNKNOWN:{}".format(last)
			
			
		if action == "state":
			

			return cmd_str

			
		if action == "on":
			switch.turn_on()
			cmd_str = "ON"
			sobj = rTelldusSwitch(switch.id, switch.name, cmd_str)
			return json.dumps(sobj.toJSON())

		if action == "off":
			switch.turn_off()
			cmd_str = "OFF"
			sobj = rTelldusSwitch(switch.id, switch.name, cmd_str)
			return json.dumps(sobj.toJSON())

		return "No defined method"
		
		

class telldusSwitchList:
	def GET(self):
		return "Not implemented"

class sonosPlayerList:
	def GET(self):
		web.header('Content-Type', 'application/json')
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		deviceList = []
		for zone in soco.discover():
			o = SonosDevice(zone.player_name, zone.ip_address)
			deviceList.append(o)
		
		return json.dumps([item.toJSON() for item in deviceList])

class sonosPlayerInfo:
	def GET(self, ipadress):
		web.header('Content-Type', 'application/json')
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')

		sonos = SoCo(ipadress)
		track = sonos.get_current_track_info()

		return json.dumps(track)

class test:
	def GET(self, mode):
		return mode

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


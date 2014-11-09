import web
import json
import tellcore.telldus as td
import tellcore.constants as tdconst

class rTelldusSensor:
	def __init__(self, id, temperature):
		self.id = id
		self.temperature = temperature

	def toJSON(self):
		return dict(id=self.id, temperature=self.temperature)

urls = (
'/', 'index',
'/test/(on|off)/(\d+)', 'test',
'/telldus/sensor/(\d+)', 'telldusSensor',
'/telldus/switch/(\d+)/(on|off|state)', 'telldusSwitchOnOff',
'/telldus/switches", ' 'telldusSwitchList'
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

		if action == "state":
			last =  switch.last_sent_command(tdconst.TELLSTICK_TURNON | tdconst.TELLSTICK_TURNOFF | tdconst.TELLSTICK_DIM)
			if last == tdconst.TELLSTICK_TURNON:
				cmd_str = "ON"
			elif last  == tdconst.TELLSTICK_TURNOFF:
				cmd_str = "OFF"
			elif last == tdconst.TELLSTICK_DIM:
				cmd_str = "DIMMED:{}".format(switch.last_sent_value())
			else:
				cmd_str = "UNKNOWN:{}".format(last)

			return cmd_str

			
		if action == "on":
			switch.turn_on()
			return "Turning on"		

		if action == "off":
			switch.turn_off()
			return "Turning off"

		return "No defined method"
		
		

class telldusSwitchList:
	def GET(self):
		return "Not implemented"

class test:
	def GET(self, mode,  id):
		return mode + str(id);

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


import web
import tellcore.telldus as td
import tellcore.constants as tdconst

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
		
		core = td.TelldusCore()
		sensor = ""
		sensors = core.sensors()
		for (i, s) in enumerate(sensors):
			sensor_id = s.id
			if sensor_id == int(id):
				sensor = s

		return str(sensor.temperature().value)
		
class telldusSwitchOnOff:
	 def GET(self, id, action):
                core = td.TelldusCore()
		switch = ""
		switches = core.devices()
		for (i, d) in enumerate(switches):
			switch_id = d.id
			if switch_id == int(id):
				switch = d
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
		
		

class telldusSwitchList:
	def GET(self):
		return "Not implemented"

class test:
	def GET(self, mode,  id):
		return mode + str(id);

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


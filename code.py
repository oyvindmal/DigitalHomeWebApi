import web
import tellcore.telldus as td
import tellcore.constants as tdconst

urls = (
'/', 'index',
'/test/(on|off)/(\d+)', 'test',
'/telldus/sensor/(\d+)', 'telldusSensor',
'/telldus/switch/(\d+)/(on|off)', 'telldusSwitch'
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
		
class telldusSwitch:
	 def GET(self, id, action):
                return "Turning "  +  action + "  " +  str(id);


class test:
	def GET(self, mode,  id):
		return mode + str(id);

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


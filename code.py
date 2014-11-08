import web

urls = (
'/', 'index',
'/test/(\d+)', 'test'
)

class index:
	def GET(self):
		return "Hello World!"

class test:
	def GET(self, id):
		return id

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


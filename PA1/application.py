from aiohttp import web
import json

async def handle(request):
    response_obj = {'status':'success'}
    return web.Response(text=json.dumps(response_obj),status=200)

async def new_user(request):
    try:
        user = request.query['name']
        response_obj = {'status':'success','message':str(user)+' created successfully'}
        return web.Response(text=json.dumps(response_obj),status=200)
    except Exception as e:
        response_obj = {'status':'failed','message':str(e)}
        return web.Response(text=json.dumps(response_obj),status=500)

application = web.Application()
application.router.add_get('/',handle)
application.router.add_post('/user',new_user)
web.run_app(application)
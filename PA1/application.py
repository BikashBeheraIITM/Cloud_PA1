from aiohttp import web
import json
def fib (n,store={0:0,1:1}):
    if n not in store:
        store[n] = fib(n-1,store) + fib(n-2,store)
    return store[n]

async def handle(request):
    response_obj = {'status':'success'}
    return web.Response(text=json.dumps(response_obj),status=200)

async def post_handle(request):
    try:
        val = request.query['n']
        num = int(val)
        f = fib(num)
        response_obj = {'status':'success','message':'The '+str(num)+'th fibonacci number is: '+str(f)}
        return web.Response(text=json.dumps(response_obj),status=200)
    except Exception as e:
        response_obj = {'status':'failed','message':str(e)}
        return web.Response(text=json.dumps(response_obj),status=500)

application = web.Application()
application.router.add_get('/',handle)
application.router.add_post('/',post_handle)
web.run_app(application)
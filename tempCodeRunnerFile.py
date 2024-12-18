# Por omissão FastAPI gera JSON

@app.get('/')
async def index():
    return {'msg': 'Hello from FastAPI'}
#:
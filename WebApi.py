from sanic import Sanic
from sanic.response import json


app = Sanic('Web_Api')


def get_db():
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_uri = "mongodb://localhost:27017/MiniPractica"
    client = AsyncIOMotorClient(mongo_uri)
    return client['MiniPractica']


@app.route('/obtenerData', methods=['GET'])
async def get(request):
    db = get_db()
    docs = await db.estadoInterruptor.find().to_list(length=100)
    for doc in docs:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return json(docs)


@app.route('/guardarData', methods=['POST'])
async def new(request):
    doc = request.json
    print(doc)
    db = get_db()
    R = await db.estadoInterruptor.insert_one(doc)
    return json({'object_id': str(R)})


if __name__ == "__main__":
    app.run(host='192.168.8.2', port=8080)

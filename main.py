from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import db
app = FastAPI()




class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
        
        
        
        
        
        
    async def send_direct_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast_message(self, message: str, websocket: WebSocket):
        for con in self.active_connections:
            await con.send_text(message)


manager = ConnectionManager()





@app.get("/")
async def get():
    print("It is runnin!!! :)")
    return FileResponse('index.html')

@app.get("/work")
async def get():
    return {
        "message" : "It is working"
    }



@app.post("/login")
async def login_the_user(username: str, client_id: int):
    if username:
        print("The user ", username, " is added to db")
        db.add_user(username, client_id)
        return db.get_a_user_by("username", username)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id : int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text() 
            await manager.send_direct_message(f"you wrote {data}", websocket)
            await manager.broadcast_message(f"Client #{client_id} says: {data}", websocket)
    except WebSocketDisconnect:
        print(f"The user {client_id} is about to be deleted!")
        db.delete_user(client_id)
        manager.disconnect(websocket)
        await manager.broadcast_message(f"Client {client_id} has left the chat :( ")



            
    
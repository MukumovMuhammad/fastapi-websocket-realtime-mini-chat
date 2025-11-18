from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import db
app = FastAPI()




class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[WebSocket] = {}

    
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_private_message(self, sender_id: int, receiver_id: int, text: str):

        if receiver_id in self.active_connections:
            websocket = self.active_connections[receiver_id]
            await websocket.send_json({
                "from": sender_id,
                "text": text
            })
            
        
    
    async def broadcast(self, message: dict):
        for ws in self.active_connections.values():
            await ws.send_json(message)
    


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


@app.post("/sign_up")
async def sign_up(username: str, password: str):
    if db.is_user_exist(username):
        return {"message" : "The user already exists", "status" : False}
    return db.add_user(username, password)


@app.post("/login")
async def login_the_user(username: str, password: str):
    if username:
        if not db.is_user_exist(username):
            return {"message" : "The user doesn't exist", "status" : False}
        print("The user ", username, " with password : ", password,  " trying to login")
        if db.check_password(username, password):
            return db.get_a_user_by("username", username)
        return {"message": "Password or username is incorrect!", "status" : True}
        

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id : int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text() 
            receiver_id = data["to"]
            text = data["text"]
            # await manager.send_direct_message(f"you wrote {data}", websocket)
            await manager.send_private_message(
                sender_id=user_id,
                receiver_id=receiver_id,
                text=text
                )
    except WebSocketDisconnect:
        print(f"The user {user_id} is about to be deleted!")
        manager.disconnect(user_id=user_id)


            
    
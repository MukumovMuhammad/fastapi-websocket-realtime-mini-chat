from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import db

app = FastAPI()

class SignInUpRequest(BaseModel):
    username: str
    password: str



class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        
    
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    

    def disconnect(self, user_id: int):

        print(f"For some resean user with id {user_id} is disconnected :(")
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
    
    # async def Dissconnect_from_socket(self, user_id: int):
    #     if user_id in self.active_connections:
    #         websocket = self.active_connections[user_id]
    #         await websocket.send_json({
    #             "username": db.get_a_user_by("id", user_id)[1],
    #             "from": user_id,
    #             "text": "You are dissconnected"
    #         })
    
    async def send_private_message(self, sender_id: int, receiver_id: int, text: str):

        if receiver_id in self.active_connections:
            websocket = self.active_connections[receiver_id]
            await websocket.send_json({
                "username": db.get_a_user_by("id", sender_id)[1],
                "from": sender_id,
                "text": text
            })
            
        
    
    async def broadcast(self, message: dict):
        for ws in self.active_connections.values():
            await ws.send_json(message)
    


manager = ConnectionManager()



app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/work")
async def get():
    return {
        "message" : "It is working"
    }


@app.post("/sign_up")
async def sign_up(data: SignInUpRequest):
    username = data.username
    password = data.password
    if password ==  "" or username == "":
        return {"message" : "no username or password", "status" : False}
    if db.is_user_exist(username):
        return {"message" : "The user already exists", "status" : False}
    return db.add_user(username, password)

@app.post("/login")
async def login_the_user(data: SignInUpRequest):
    username = data.username
    password = data.password
    if password ==  "" or username == "":
        return {"message" : "no username or password", "status" : False}
    if username:
        if not db.is_user_exist(username):
            return {"message" : "The user doesn't exist", "status" : False}
        print("The user ", username, " with password : ", password,  " trying to login")
        if db.check_password(username, password):
            user = db.get_a_user_by("username", username)
            return {"username":user[1], "id": user[0], "message": "Your are logged in!", "status": True}
        return {"message": "Password or username is incorrect!", "status" : False}
        

@app.get("/all_users")
async def get_all_users():
    # user = db.get_a_user_by("id", id)
    return db.get_usernames() 




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id : int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            print(f"the id {user_id} is sending messages {data}")
            receiver_id = data["receiver_id"]
            text = data["text"]
            # await manager.send_direct_message(f"you wrote {data}", websocket)
            await manager.send_private_message(
                sender_id=user_id,
                receiver_id= int(receiver_id),
                text=text
                )
    except WebSocketDisconnect:
        print(f"The user {user_id} is disconnected!")
        # manager.disconnect(user_id)


    
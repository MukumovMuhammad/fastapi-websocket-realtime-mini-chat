from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import db
app = FastAPI()


html = """
<!DOCTYPE html>
<html>
        <head>
            <title> Web socket Demo </title>

           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
       </head>

      
    
    <body>

        <div class="main">
        <h1>FASTAPI WebSocket Chat</h1>


      
        <div class="container mt-3" id="login_div">
        <h2>Please Login </h2>

        <form action="" >
            <p>Username
            <input type="text" class="form-control" id="username" autocomplete="on"
            </p>
            <br>
            <button class="btn btn-outline-primary mt-2" onClick="login(event)"> Start Global Chat </button>
        </div>

        <div class="container mt-3 d-none" id="chat_room">
            
            <h2>Your ID: <span id="ws-id"></span> </h2>
            <form action="" >
                <input type="text" class="form-control" id="messageText" autocomplete="off"/>
                <button class="btn btn-outline-primary mt-2" onClick="sendMessage(event)"> Send </button>
            
            </form>

            <ul id='messages' ckass="mt-5">
            </ul>
        </div>

      </div>


         <script>

            var client_id = Date.now();


            
            var chat_div = document.getElementById("chat_room")
            var login_div = document.getElementById("login_div")
            var  ws = new WebSocket(`ws://192.168.123.40:8080/ws/${client_id}`);

            ws.onmessage = function(event){       
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function sendMessage(event){
            
               
                event.preventDefault()
                var input = document.getElementById("messageText")
                ws.send(input.value)
                
                input.value = ''
                
            }

           async function login(event) {
                console.log("You are trying to login")
                event.preventDefault()
                var the_username = document.getElementById("username").value
                if (username == "") {
                    alert("Please fill the username")
                    return
                }

        
            
                const url = `/login?username=${encodeURIComponent(the_username)}&client_id=${encodeURIComponent(client_id)}`;
                
                try {
                    const response = await fetch(url, {
                    method: 'POST', // Specify the method as POST
                });

                    if (!response.ok) {
                        // Handle HTTP errors
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    login_div.classList.add("d-none")
                    chat_div.classList.remove("d-none")
                        

                    const userData = await response.json();
                    console.log('Success:', userData);

                    document.querySelector("#ws-id").textContent = userData[1]

                   
                            
                    // You can now use the returned user data
                    return userData;

                } 
                catch (error) {
                    console.error('Error during login:', error);
                    // Handle network errors or other issues
            }
        }

        
    </script>

</html>


     

"""

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
    return HTMLResponse(html)

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
        db.delete_user(client_id)
        manager.disconnect(websocket)
        await manager.broadcast_message(f"Client {client_id} has left the chat :( ")



            
    
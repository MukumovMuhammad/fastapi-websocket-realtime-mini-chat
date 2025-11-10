from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
        <head>
            <title> Web socket Demo </title>

           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
       </head>

      
    
    <body>

    

        <div class="container mt-3">
            <h1>FASTAPI WebSocket Chat</h1>
            <h2>Your ID: <span id="ws-id"></span> </h2>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" class="form-control" id="messageText" autocomplete="off"/>
                <button class="btn btn-outline-primary mt-2" > Send </button>
            
            </form>

            <ul id='messages' ckass="mt-5">
            </ul>
        </div>


         <script>

            var client_id = Date.now();


            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://192.168.123.40:8080/ws/${client_id}`);

    
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

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id : int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text() 
            await manager.send_direct_message(f"you wrote {data}", websocket)
            await manager.broadcast_message(f"Client #{client_id} says: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_message(f"Client {client_id} has left the chat :( ")



            
    
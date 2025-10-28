from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
        <head>
            <title> Web socket Demo </title>

           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
       </head>

       <script>
            var ws = new WebSocket("ws://localhost:8000/ws");

    
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
    
    <body>

    

        <div class="container mt-3">
            <h1>FASTAPI WebSocket Chat</h1>

            <form action="" onsubmit="sendMessage(event)">
                <input type="text" class="form-control" id="messageText" autocomplete="off"/>
                <button class="btn btn-outline-primary mt-2" > Send </button>
            
            </form>

            <ul id='messages' ckass="mt-5">
            </ul>
        </div>

        


       
</html>


     

"""


@app.get("/")
async def get():
    print("It is runnin!!! :)")
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print("Websocket data was recieved ", data)
        await websocket.send_text(f"Message text was {data}")
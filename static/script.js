    let ws = null;
    let currentUserId = null;
    let messages = {}
    let selected_chat_id = null

    //------------------------------------------
    // SIGN UP
    //------------------------------------------
    async function signup(event) {
        event.preventDefault();

        const username = document.getElementById("username_inp").value;
        const password = document.getElementById("password_inp").value;

        const res = await fetch("/sign_up", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        if (res.ok) {
            const data = await res.json();
            alert(data.message);
            console.log(data)
            username.value = ""
            password.value = ""
           
        } else {
            alert("Error creating account.");
        }
    }
    //------------------------------------------
    // SIGN IN
    //------------------------------------------
    async function signin(event) {
        event.preventDefault();

        const username = document.getElementById("username_inp").value;
        const password = document.getElementById("password_inp").value;

        const res = await fetch("/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        if (res.ok) {
            const data = await res.json();
            // alert(data.message);
            console.log(data)

            if (data.status){
                get_all_users(event)
                document.getElementById("auth_div").classList.add("d-none");
                document.getElementById("chat_container").classList.remove("d-none");

                document.getElementById("user_profile_name").innerText = username
                currentUserId = data.id
            
                openWebSocket();
                // document.getElementById("user_id").textContent = currentUserId;
            }
            username.value = ""
            password.value = ""
            
           
        } else {
            alert("Error while loging account.");
        }

      
   
        
    }


    async function get_all_users(event) {
        event.preventDefault()

        const res = await fetch("/all_users", {
            method: "GET",
        });

        const user_list = document.getElementById("user_list")
        user_list.innerHTML = ""

        if (res.ok) {
            const data = await res.json();
            // alert(data);
            console.log("Here are all user datas")
            console.log(data)

            data.forEach(i => {
                if (i[1] != currentUserId){   
                    let li = document.createElement("li");
                    li.textContent = i[0]
                    li.setAttribute('data-user-id', i[1])
                    li.onclick = handleListClick
                    user_list.appendChild(li)
                }
               
            });
           
        } else {
            alert("Error while fetching  data.");
        }
    }

        function handleListClick(event){
            
            const clickedElement = event.target;
            selected_chat_id = clickedElement.getAttribute('data-user-id');
            const userName = clickedElement.textContent;
            console.log(`You clicked user ID: ${selected_chat_id} (${userName})`)
            document.getElementById("messageInput").classList.remove("d-none")

            // alert(`You clicked user ID: ${selected_chat_id} (${userName})`);
            ShowMessages(selected_chat_id)
        }
    
    
function openWebSocket() {

    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    ws = new WebSocket(`${protocol}://${window.location.host}/ws?user_id=${currentUserId}`);

    ws.onmessage = (event) => {
        console.log("Oh you received data! I mean message")
        const messageLists = document.getElementById("messages")
        const data = JSON.parse(event.data);
        console.log(`The recieved message ${data.username}`)

        // data.username is likely missing from your FastAPI payload right now (only 'from' and 'text')
        const sender = data.from == currentUserId ? "You" : `${data.username}`;
        
        let li = document.createElement("li");
        li.textContent = `${sender}: ${data.text}`
        messageLists.appendChild(li)
        if (messages[data.id]){
            messages[data.id] = [...messages[data.id], li]    
        }
        else{
            messages[data.id] = [li]
        }
        

    };
    // ... onclose handler ...
}


function ShowMessages(receiver_id){

        if (receiver_id != selected_chat_id){
            return
        }
        const messageLists = document.getElementById("messages")
        if (messages[receiver_id]){
            messages[receiver_id].forEach(message =>{
            messageLists.appendChild(message)
        })
        }
       
       
}

// Function to send a message
function sendMessage(event) {
    event.preventDefault()
    const inputElement = document.getElementById("messageText");
    const messageText = inputElement.value;
    console.log(`Sending message ${messageText} to ${selected_chat_id}` )


    if (ws.readyState === WebSocket.OPEN && messageText.trim() !== '') {
        // Prepare the message object that FastAPI will process
        const message = {
            receiver_id: selected_chat_id, 
            text: messageText
        };
        
        // Send the message as a JSON string
        ws.send(JSON.stringify(message));

        const messageLists = document.getElementById("messages")
        let li = document.createElement("li");
        li.textContent = `You: ${messageText}`
        messageLists.appendChild(li)
        if (messages[currentUserId]){
            messages[currentUserId] = [...messages[currentUserId], li]    
        }
        else{
            messages[currentUserId] = [li]
        }
        // Clear the input field
        inputElement.value = '';
    } else {
        console.error("WebSocket is not open or message is empty.");
    }
}

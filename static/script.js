 
 document.addEventListener('DOMContentLoaded', (event) => {
    console.log('The DOM is fully loaded. User just entered the page.');
    

    if (localStorage.getItem("userid") != null){
        document.getElementById("auth_div").classList.add("d-none");
        document.getElementById("chat_container").classList.remove("d-none");

        document.getElementById("user_profile_name").innerText = localStorage.getItem("username")
        currentUserId = localStorage.getItem("userid")
        get_all_users(event)
        openWebSocket()
    }
});

    let onlineUsers = new Set();
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
            if (data.status){
                signin(event)
            }
           
           
        } else {
            alert("Error creating account.");
            username.value = ""
            password.value = ""
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
                localStorage.setItem('userid', data.id);
                localStorage.setItem('username', data.username);
            
                openWebSocket();
                get_all_users(event)
                // document.getElementById("user_id").textContent = currentUserId;
            }
            username.value = ""
            password.value = ""
            
           
        } else {
            alert("Error while loging account.");
        }

      
   
        
    }


    function LogOut(event){
        localStorage.clear()
        window.location.reload();

    }

    async function get_all_users(event) {
    if (event) event.preventDefault();

    const res = await fetch("/all_users", { method: "GET" });
    const user_list = document.getElementById("user_list");
    user_list.innerHTML = "";

    if (!res.ok) {
        alert("Error while fetching data.");
        return;
    }

    const data = await res.json();
    console.log("Fetched users:", data);

    window.allUsers = data; // store globally
    refreshUserList();
}


function refreshUserList() {
    const user_list = document.getElementById("user_list");
    user_list.innerHTML = "";

    allUsers.forEach(([username, id]) => {
        if (id == currentUserId) return;

        const li = document.createElement("li");
        li.className = "list-group-item d-flex align-items-center";
        li.setAttribute("data-user-id", id);
        li.onclick = handleListClick;

        // Status indicator
        const dot = document.createElement("span");
        dot.className = "rounded-circle d-inline-block me-2";
        dot.style.width = "10px";
        dot.style.height = "10px";
        dot.classList.add(
            onlineUsers.has(id) ? "bg-success" : "bg-secondary"
        );

        // Username
        const nameEl = document.createElement("span");
        nameEl.textContent = username;

        li.appendChild(dot);
        li.appendChild(nameEl);

        user_list.appendChild(li);
    });
}



        function handleListClick(event){
            
            const clickedElement = event.target;
            selected_chat_id = clickedElement.getAttribute('data-user-id');
            const userName = clickedElement.textContent;
            console.log(`You clicked user ID: ${selected_chat_id} (${userName})`)
            document.getElementById("messageInput").classList.remove("d-none")
            document.getElementById("selected_user_chat").innerText = userName

            // alert(`You clicked user ID: ${selected_chat_id} (${userName})`);
            ShowMessages(selected_chat_id)
        }

function ShowMessages(receiver_id){
        // console.log(`Here are all messages`)
        // messages[receiver_id].forEach(i=>{
        //     console.log(i)
        // })
        const messageLists = document.getElementById("messages")
        messageLists.innerHTML = ""
        if (messages[receiver_id]){
            messages[receiver_id].forEach(message =>{
            messageLists.appendChild(message)
        })
        }
       
       
}
    
function openWebSocket() {

    console.log("trying to open WebSocket")
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    ws = new WebSocket(`${protocol}://${window.location.host}/ws?user_id=${currentUserId}`);
    

    ws.onmessage = (event) => {
        console.log("ws.onmessages says")
        console.log("Oh you received data! I mean message!!")
        const messageLists = document.getElementById("messages")
        const data = JSON.parse(event.data);
        console.log(data)
        if (data.type === "ping") {
            try {
                const parsed = data.online_users;
                console.log("the list of online users are updated here they are " + parsed )
                onlineUsers = new Set(parsed);  // store online IDs
            } catch (e) {
                console.error("Failed to parse online_users", e);
            }
        // Update UI after receiving new online users
        refreshUserList();
        return;
    }
        console.log(`The recieved message ${data.username}`)

        // data.username is likely missing from your FastAPI payload right now (only 'from' and 'text')
        const sender = data.from == currentUserId ? "You" : `${data.username}`;
        
        let li = document.createElement("li");
        li.innerText = `${sender}: ${data.text}`
        if (selected_chat_id == data.from){
          
            li.textContent = `${sender}: ${data.text}`
            messageLists.appendChild(li)
        }
        
    
         if (!messages[data.from]) {
            messages[data.from] = [];
        }

         messages[data.from].push(li);
      
        

    };
    // ... onclose handler ...
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
        if (!messages[selected_chat_id]) {
            messages[selected_chat_id] = [];
        }

        messages[selected_chat_id].push(li);
        // Clear the input field
        inputElement.value = '';
    } else {
        console.error("WebSocket is not open or message is empty.");
    }
}

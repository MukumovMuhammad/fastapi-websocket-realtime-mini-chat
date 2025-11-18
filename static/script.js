    let ws = null;
    let currentUserId = null;

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
            alert(data.message);
            console.log(data)

            if (data.status){
                get_all_users(event)
                document.getElementById("auth_div").classList.add("d-none");
                document.getElementById("chat_container").classList.remove("d-none");
                // document.getElementById("user_id").textContent = currentUserId;
            }
            username.value = ""
            password.value = ""
            
           
        } else {
            alert("Error while loging account.");
        }

      
        // openWebSocket();
        
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
                let li = document.createElement("li");
                li.textContent = i[0]
                user_list.appendChild(li)
            });
           
        } else {
            alert("Error while fetching  data.");
        }
        // openWebSocket();
    }




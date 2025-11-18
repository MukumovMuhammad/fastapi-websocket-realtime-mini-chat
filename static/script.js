
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
            username.value = ""
            password.value = ""
           
        } else {
            alert("Error while loging account.");
        }

        // document.getElementById("auth_div").classList.add("d-none");
        // document.getElementById("chat_room").classList.remove("d-none");
        // document.getElementById("user_id").textContent = currentUserId;

        // openWebSocket();
    }




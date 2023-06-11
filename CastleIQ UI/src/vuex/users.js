const REST_API = "https://10.10.10.14:8000"

export default {
    namespaced: true,
    state: {
        users: [],
    },
    mutations:{


    },
    actions: {
        async getUsers(state) {
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)

            await fetch(`${REST_API}/users/all`, { headers: headers, method: "GET" })
                .then(async response => {
                    const data = await response.json();
                    if (data.event_result) {
                        return data
                    }
                    // check for error response
                    if (!response.ok) {
                        // get error message from body or default to response statusText
                        const error = (data && data.message) || response.statusText;
                        return Promise.reject(error);
                    }

                })
                .then(async data => {
                    if (data.event_result) {
                        if (data.event_result == "Error") {
                            if (data.event_name == 'UserNotAuthorizedError' || data.event_name == "TokenExpiredError") {
                                this.commit("auth/changeUsername", "Unauthorized") 
                                this.commit("messages/show", { type: "warning", message: data.message })
                                this.commit("auth/changeLoggedIn", false)
                            }
                        }
                        else{
                            if (data.event_name == "GetMeEvent"){
                                this.commit("auth/changeUsername", data.user.username) 
                                this.commit("auth/changeLoggedIn", true)
                                
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error("There was an error!", error);
                    this.commit('messages/show', {type:"danger", message:error})
                });
        },

        logIn(state, credentials){
            fetch(`${REST_API}/users/login`, { method: "POST",headers: {
                "Content-Type": "application/json",
              }, body: JSON.stringify(credentials) })
                .then(async response => {
                    const data = await response.json();

                    if (data.event_result) {
                        return data
                    }
                    // check for error response
                    if (!response.ok) {
                        // get error message from body or default to response statusText
                        const error = (data && data.message) || response.statusText;
                        return Promise.reject(error);
                    }

                })
                .then(async data => {
                    if (data.event_result) {
                        if (data.event_result == "Error") {
                            if (data.event_name == 'WrongCredentialsError') {
                                this.commit("messages/show", { type: "danger", message: data.message })
                            }
                        }
                        else{
                            if (data.event_name == "LoggedInEvent"){
                                this.commit("auth/changeUsername", data.user.username) 
                                let token = `${data.token.token_type} ${data.token.access_token}`
                                localStorage.setItem("Token", token)

                                
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error("There was an error!", error);
                    this.commit('messages/show', {type:"danger", message:error})
                });
        },
    },
    getters: {
    },
}
const REST_API = "https://127.0.0.1:8000"

export default {
    namespaced: true,
    state: {
        devices: []
    },
    mutations:{
        changeDevices(state, devices){
            state.devices = devices
        },
    },
    actions: {
        async getAllDevices(state){
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)

            await fetch(`${REST_API}/dev_api/devices`, { headers: headers, method: "GET" })
                .then(async response => {
                    const data = await response.json();
                    console.log(response)
                    console.log(data)

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
                            if (data.event_name == "AllDevices"){
                                this.commit("devices/changeDevices", data.devices)                                 
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
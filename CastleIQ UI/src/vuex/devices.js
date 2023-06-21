const REST_API = "https://10.10.10.14:8000"

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

        async addDevice(sate, dev_info){
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)
            headers.append("Content-Type", "application/json",)
            await fetch(`${REST_API}/dev_api/connect_new`, { headers: headers, method: "POST", body: JSON.stringify(dev_info) })
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
                        else if (data.event_name == "ConnectionFailedError"){
                            this.commit("messages/show", { type: "warning", message: data.message })
                        }
                        else{
                            if (data.event_name == "DeviceInfo"){
                                await this.$store.dispatch("devices/getAllDevices")
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error("There was an error!", error);
                    this.commit('messages/show', {type:"danger", message:error})
                });
        },

        async forwardEvent(state, event_info){
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)
            headers.append("Content-Type", "application/json",)
            const forward_event = {
                event_name: "ForwardEvent",
                event_type: "RequestEvent",
                direction: "To device",
                device_id: event_info.device_id,
                event: event_info.event
            }
            console.log(JSON.stringify(forward_event))

            await fetch(`${REST_API}/ui_api/fire_event`, { headers: headers, method: "POST", body: JSON.stringify(forward_event) })
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
                            this.commit("messages/show", { type: "danger", message: data.message })
                        }
                        else{
                            
                        }
                    }
                })
                .catch(error => {
                    console.error("There was an error!", error);
                    this.commit('messages/show', {type:"danger", message:error})
                });
        }
    },
    getters: {
    },
}
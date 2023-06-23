const REST_API = "https://192.168.88.253:8000"

export default {
    namespaced: true,
    state: {
        automations: []
    },
    mutations:{
        changeAutomations(state, automations){
            state.automations = automations
        },
    },
    actions: {
        async getAllAutomations(state){
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)

            await fetch(`${REST_API}/automations/all`, { headers: headers, method: "GET" })
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
                            if (data.event_name == "AllAutomations"){
                                this.commit("automations/changeAutomations", data.automations)                                 
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error("There was an error!", error);
                    this.commit('messages/show', {type:"danger", message:error})
                });
        },

        async addAutomation(sate, automation_info){
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)
            headers.append("Content-Type", "application/json",)
            await fetch(`${REST_API}/automations/create`, { headers: headers, method: "POST", body: JSON.stringify(automation_info) })
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
                            if (data.event_name == "AllAutomations"){
                                this.commit("automations/changeAutomations", data.automations)      
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error("There was an error!", error);
                    this.commit('messages/show', {type:"danger", message:error})
                });
        },

        async updateAutomations(sate){
            let headers = new Headers()
            let token = localStorage.getItem("Token")
            headers.append("Authorization", token)
            headers.append("Content-Type", "application/json",)
            await fetch(`${REST_API}/automations/update`, { headers: headers, method: "GET"})
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
                            if (data.event_name == "AutomationsUpdated"){
                                this.commit('messages/show', {type:"success", message: data.message})
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
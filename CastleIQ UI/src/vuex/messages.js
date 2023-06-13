export default {
    namespaced: true,
    state: {
        messages: []
    },
    mutations: {
        show(state, payload) {
            state.messages.push(payload)
        },
        close(state, index) {
            if (index >= 0 && index < state.messages.ltngth) 
                state.messages.splice(index, 1);
        }
    }
}
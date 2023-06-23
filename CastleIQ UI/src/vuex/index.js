import {createStore} from 'vuex'
import messages from './messages';
import auth from './auth'
import devices from './devices';
import automations from './automations';

const REST_API = "https://192.168.88.253:8000";

const store = createStore({
    state: {
        
    },
    mutations: {
        
    },
    actions: {

    },
    getters: {

    },
    modules:{
        messages,
        auth,
        devices,
        automations
    }
});

export default store;
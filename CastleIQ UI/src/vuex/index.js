import {createStore} from 'vuex'
import messages from './messages';
import auth from './auth'
import devices from './devices';

const REST_API = "https://10.10.10.14:8000";

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
    }
});

export default store;
import {createStore} from 'vuex'
import messages from './messages';
import auth from './auth'
import devices from './devices';

const REST_API = 'https://127.0.0.1:8000/';

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
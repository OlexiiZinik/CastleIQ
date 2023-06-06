<template>
    <!-- style="width: 18rem;" -->
    <!-- p-2  -->
    <div class="p-2 col col-sm-12 col-md-5 col-lg-3 col-xl-3">
        <div class="card p-0">
            <div class="card-header d-flex">
                <h5 class="card-title my-auto">{{ device.name }}</h5>
                <!-- <a href="#" class=" btn btn-primary ms-auto ">Card link</a> -->
                <div class="form-check form-switch ms-auto">
                    <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault">
                </div>
            </div>
            <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">{{ device.room }}</h6>
                <p class="card-text">{{ device.description }}</p>


                <div v-for="event in device.events">
                    <h3>{{ event.name }}</h3>
                    <div v-for="[field, description] of Object.entries(event.event_schema.properties)" :field="field">
                        <div v-if="description.$ref">
                            <FormControl :referensed="getReferensed(event, description.$ref)" v-model="events_constructed[event.name][field]"></FormControl>                           
                        </div>
                        <div v-if="!['event_name'].includes(field)">
                            <FormControl :field="field" :description="description" v-model="events_constructed[event.name][field]"></FormControl>
                        </div>
                        <p>{{ events_constructed[event.name][field] }}</p>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import FormControl from './formControl.vue'
export default {
    data() {
        return {
            events_constructed: {}
        }
    },
    props: {
        device: Object
    },
    methods: {
        getReferensed(event, ref) {
            let key = ref.split('/').slice(-1)[0]
            return event.event_schema.definitions[key]
        },
    },
    components: {
        FormControl
    },
    created(){
        for(let i = 0; i<this.device.events.length; i++){
            this.events_constructed[this.device.events[i].name] = {}
        }
    }
}
</script>
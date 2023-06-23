<template>
    <!-- style="width: 18rem;" -->
    <!-- p-2  -->
    <div class="p-2 col col-sm-12 col-md-5 col-lg-3 col-xl-3">
        <div class="card p-0">
            <div class="card-header d-flex">
                <h5 class="card-title my-auto">{{ device.name }}</h5>
                <!-- <a href="#" class=" btn btn-primary ms-auto ">Card link</a> -->
                <div class="form-check form-switch ms-auto">
                    <input v-if="!loading" class="form-check-input" type="checkbox" role="switch"
                        :id="`${device.id}_status`" v-model="status" v-on:change="somethingChanged">
                    <div v-else class="spinner-border text-primary w-100 h-100" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">{{ device.room }}</h6>
                <p class="card-text">{{ device.description }}</p>
                <div v-for="event in device.events">
                    <!-- <h3 v-if="!event.outgoing">{{ event.name }}</h3> -->
                    <div v-if="!event.outgoing"
                        v-for="[field, description] of Object.entries(event.event_schema.properties)" :field="field">

                        <div v-if="description.$ref && getReferensed(event, description.$ref) && getReferensed(event, description.$ref).enum"
                            class="form-outline mb-4">

                            <label class="form-label" :for="`${device.id}_${event.name}_${field}`">{{ getReferensed(event,
                                description.$ref).title
                            }}</label>
                            <select class="form-select" :id="`${device.id}_${event.name}_${field}`"
                                :aria-label="getReferensed(event, description.$ref).title"
                                v-model="events_constructed[event.name][field]" v-on:change="somethingChanged">
                                <option v-for="value in getReferensed(event, description.$ref).enum" :value="value">{{ value
                                }}</option>
                            </select>
                        </div>
                        <div v-if="description.$ref && getReferensed(event, description.$ref) && getReferensed(event, description.$ref).title == 'Color'"
                            class="form-outline mb-4">
                            <label class="form-label" :for="`${device.id}_${event.name}_${field}`">{{ getReferensed(event,
                                description.$ref).title
                            }}</label>
                            <input type="color" class="form-control form-control-color w-100"
                                :id="`${device.id}_${event.name}_${field}`"
                                :title="getReferensed(event, description.$ref).title"
                                v-model="events_constructed[event.name][`${field}_raw`]" v-on:change="somethingChanged" />
                        </div>
                        <div v-if="description && field && !['event_name', 'event_type'].includes(field)">

                            <div v-if="description.type == 'string'" class="form-outline mb-4">
                                <label class="form-label" :for="`${device.id}_${event.name}_${field}`">{{ description.title
                                }}</label>
                                <input class="form-control" type="text" :id="`${device.id}_${event.name}_${field}`"
                                    :placeholder="description.title" v-model="events_constructed[event.name][field]"
                                    v-on:change="somethingChanged" />
                            </div>
                            <div v-if="description.type == 'boolean'" class="form-check mb-4">
                                <label class="form-check-label" :for="`${device.id}_${event.name}_${field}`">
                                    {{ description.title }}
                                </label>
                                <!-- <input class="form-check-input" type="checkbox" role="switch"
                                    :id="`${device.id}_${event.name}_${field}`" v-model="events_constructed[event.name][field]" v-on:change="somethingChanged"> -->
                                <input class="form-check-input" type="checkbox" role="switch" value=""
                                    :id="`${device.id}_${event.name}_${field}`"
                                    v-model="events_constructed[event.name][field]" v-on:change="somethingChanged" />
                            </div>
                            <div v-if="description.type == 'integer'" class="mb-4 form-outline">
                                <label class="form-label" :for="`${device.id}_${event.name}_${field}`">{{ description.title
                                }}</label>
                                <input type="number" :id="`${device.id}_${event.name}_${field}`" class="form-control"
                                    v-model="events_constructed[event.name][field]" v-on:change="somethingChanged" />
                            </div>
                        </div>
                    </div>
                    <!-- <div v-else v-for="[field, description] of Object.entries(event.event_schema.properties)">
                        <div v-if="!['event_name', 'event_type', 'event_result', 'message', 'status_code'].includes(field)">
                            <label class="form-check-label" :for="`${device.id}_${event.name}_${field}`">
                                {{ description.title }}
                            </label>
                            <h6>value</h6>
                        </div>
                    </div> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            events_constructed: {},
            status: true,
            loading: false,
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
        async somethingChanged(event) {
            const event_name = event.target.id.split("_")[1]
            const event_field = event.target.id.split("_")[2]
            if (event.target.type == "color") {
                this.events_constructed[event_name][event_field] = this.hexToColor(event.target.value)
            }
            console.log(event)
            console.log(this.status)
            console.log(this.events_constructed)
            this.loading = true
            await this.$store.dispatch("devices/forwardEvent", {
                device_id: this.device.id,
                event: this.events_constructed[event_name],
            })
            this.loading = false

        },
        hexToColor(hex) {
            hex = hex.replace('#', '');

            const r = parseInt(hex.substring(0, 2), 16);
            const g = parseInt(hex.substring(2, 4), 16);
            const b = parseInt(hex.substring(4, 6), 16);

            return { R: r, G: g, B: b };
        },
    },
    components: {
    },

    created() {
        for (let i = 0; i < this.device.events.length; i++) {
            this.events_constructed[this.device.events[i].name] = {}
            console.log("event.properties")
            console.log(this.device.events[i].event_schema.properties)
            Object.entries(this.device.events[i].event_schema.properties).forEach(([field, description]) => {
                if (!description.$ref)
                    this.events_constructed[this.device.events[i].name][field] = description.default
                else
                    this.events_constructed[this.device.events[i].name][field] = undefined
            })

            // for([field, description] of Object.entries(this.device.events[i].event_schema.properties)){
            //     if(!description.$ref)
            //         this.events_constructed[this.device.events[i].name][field] = description.default
            //     else
            //         this.events_constructed[this.device.events[i].name][field] = undefined
            // }

            // for(let j = 0; j<this.device.events[i].event_schema.properties.length; j++){
            //     this.events_constructed[this.device.events[i].name][]
            // }
        }
    }
}
</script>
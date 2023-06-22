<template>
    <div class="d-flex mt-5 mb-3">
        <h1 class="">Пристрої</h1>
        <!-- <a href="#" class="btn btn-primary ms-auto my-auto">Додати пристрій</a> -->
        <button type="button" class="btn btn-primary ms-auto my-auto" data-bs-toggle="modal"
            data-bs-target="#addDeviceModal">
            Додати пристрій
        </button>

        <!-- Modal -->
        <div class="modal fade" id="addDeviceModal" tabindex="-1" aria-labelledby="addDeviceModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="addDeviceModal">Додавання пристрою</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form class="" @submit.prevent="addDevice">
                        <div class="modal-body">
                            <label class="form-label" for="protocol">Протокол</label>
                            <select class="form-select mb-2" id="protocol" aria-label="protocol" v-model="protocol">
                                <option selected value="http">HTTP</option>
                                <option value="https">HTTPS</option>
                            </select>
                            <label class="form-label" for="ip">IP пристрою</label>
                            <input type="text" id="ip" class="form-control mb-2" placeholder="IP пристрою" v-model="ip" />
                            <label class="form-label" for="port">Порт</label>
                            <input type="number" id="port" class="form-control mb-2" placeholder="Порт" v-model="port" />
                            <label class="form-label" for="webhookPath">Шлях до вебхуку</label>
                            <input type="text" id="webhookPath" class="form-control mb-2" placeholder="Шлях до вебхуку"
                                v-model="webhookPath" />
                            <label class="form-label" for="room">Кімната</label>
                            <input type="text" id="room" class="form-control mb-2" placeholder="Кімната" v-model="room" />
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Відмінити</button>
                            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Додати</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

    </div>
    <div class="row">
        <Device :device="device" v-for="device in this.$store.state.devices.devices"></Device>
    </div>
</template>

<script>
import Device from '../components/Device.vue'

export default {
    data() {
        return {
            protocol: "http",
            ip: "",
            port: 8000,
            webhookPath: "/fire_event",
            room: "",

        }
    },

    methods: {
        async addDevice(event) {
            await this.$store.dispatch("devices/addDevice", {
                event_type: "RequestEvent",
                event_name: "ConnectNewDevice",
                webhook:{
                    protocol: this.protocol,
                    ip: this.ip,
                    port: this.port,
                    path: this.webhookPath,
                },
                room: this.room,
            })
        }
    },
    components: {
        Device
    },
    async mounted() {
        await this.$store.dispatch("devices/getAllDevices")
        console.log(this.$store.state.devices.devices)
    }
}
</script>
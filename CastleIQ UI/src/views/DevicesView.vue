<template>
    <div class="d-flex mt-5 mb-3">
        <h1 class="">Пристрої</h1>
        <a href="#" class="btn btn-primary ms-auto my-auto">Додати пристрій</a>
    </div>
    <div class="row" >
        <Device :device="device" v-for="device in this.$store.state.devices.devices"></Device>
    </div>
</template>

<script>
    import Device from '../components/Device.vue'

    export default{
        data(){
            return {

            }
        },

        methods:{

        },
        components:{
            Device
        },
        async mounted(){
            await this.$store.dispatch("devices/getAllDevices")
            console.log(this.$store.state.devices.devices)
        }
    }
</script>
<template>
    <div id="liveAlertPlaceholder">
        
        <!-- obj in this.$store.state.messages.messages -->
        <div v-for="[index, obj] of this.$store.state.messages.messages.entries()">
            <div :class="['alert', 'alert-'+obj.type, 'alert-dismissible', 'mx-4']" role="alert">
                <div>{{ obj.message }}</div>
                <button @click="this.$store.commit('messages/close', index)" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>


    </div>
</template>

<script>
export default {
    data() {
        return {

        }
    },

    methods: {


    }
}
</script>
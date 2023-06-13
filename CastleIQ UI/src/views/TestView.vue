<script>
    import Alertbox from '../components/Alertbox.vue';
    export default{
        components:{
            Alertbox,
        },
        methods:{
            btnClick(){
                
            }
        }
    }
</script>

<template>
    <div>

        
        <h1>Hello world</h1>
        <p>This is Test</p>
        <button class="btn btn-primary" @click="btnClick">test</button>
    </div>
</template>
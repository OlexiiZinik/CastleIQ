<script setup>
import {RouterView} from 'vue-router'
import Navbar from './components/Navbar.vue';
import Alertbox from './components/Alertbox.vue';

</script>

<template>
  <header>
    <Navbar/>
  </header>
  <Alertbox/>
  <div class="container">
    <RouterView />
  </div>

</template>

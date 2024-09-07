<template>
    <div id="app">
      <MainVue />
    </div>
  </template>
  
  <script>
  import MainVue from './components/Main.vue';
  
  export default {
    components: {
        MainVue,
    },
  };
  </script>
  
  <style>
  #app {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%
  }
  </style>
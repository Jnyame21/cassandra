<script setup lang="ts">
import {ref } from "vue";

const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()


const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="sections-container">
    <TheLoader class="no-data" v-if="!userAuthStore.headDepartments || userAuthStore.headDepartments && userAuthStore.headDepartments.length ===0 " />

    <div v-if="userAuthStore.headDepartments && userAuthStore.headDepartments.length >0 " class="section-nav-container">
      <button v-for="(department, index) in userAuthStore.headDepartments" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      ><span>{{department['department']['name']}}</span>
    </button>
    </div>
  
    <div v-if="userAuthStore.headDepartments && userAuthStore.headDepartments.length >0 "  class="sections">
      <div class="h-100" v-for="(department, index) in userAuthStore.headDepartments" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <HeadDepartmentPage :department="department"/>
      </div>
    </div>
  </div>
</template>


<style scoped>

@media screen and (min-width: 576px) {
  .nav-btn-1{
    margin: 0em 2em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    margin: 0em 3em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 991px) {
  .nav-btn-1{
    margin: 0em 4em !important;
    font-size: .7rem !important;
  }
}

</style>
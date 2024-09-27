<script setup lang="ts">
import {ref} from "vue";


const sectionPage = ref(1)


const changeTerm = (page: number)=>{
  sectionPage.value = page
}


</script>

<template>
  <div class="section-nav-container">
    <button class="nav-btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">
      <v-icon icon="mdi-account" />
      ALL APPLICATIONS
      </button>
    <button class="nav-btn-1" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">
      <v-icon icon="mdi-book-open" />
      APPLY
      </button>
  </div>

  <div class="sections">
    <div class="h-100" :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
      <StudentAllApplications />
    </div>
    <div class="h-100" :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
      <StudentApplicationApply />
    </div>
  </div>
</template>

<style scoped>

.nav-btn-1{
  font-size: .6rem !important;
}


</style>
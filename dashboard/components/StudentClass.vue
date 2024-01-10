<script setup lang="ts">
import {ref} from "vue";


const userAuthStore = useUserAuthStore()
const sectionPage = ref(1)


const changeTerm = (page: number)=>{
  sectionPage.value = page
}


</script>

<template>
  <div class="section-nav-container">
    <button class="nav-btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">STUDENTS</button>
    <button class="nav-btn-1" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">SUBJECTS</button>
  </div>

  <div class="sections">
    <div class="h-100" :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
      <StudentClassStudents />
    </div>
    <div class="h-100" :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
      <StudentClassSubjects />
    </div>
  </div>
</template>

<style scoped>

.nav-btn-1{
  font-size: .6rem !important;
}


</style>
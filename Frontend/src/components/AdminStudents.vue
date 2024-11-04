
<script setup lang="ts">
import {ref} from "vue";


const userAuthStore = useUserAuthStore()
const sectionPage = ref(1)


const changeTerm = (term: number)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="section-nav-container">
    <button class="nav-btn-1 btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">CREATE CLASS</button>
    <button class="nav-btn-1 btn-2" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">ADMISSION</button>
    <button class="nav-btn-1 btn-3" @click="changeTerm(3)" :class="{'nav-btn-1-active': sectionPage===3}">ALL ADMITTED STUDENTS</button>
  </div>

  <div class="sections">
    <div class="h-100" :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
      <AdminStudentsAddClass />
    </div>
    <div class="h-100" :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
      <AdminStudentsAdmission />
    </div>
    <div class="h-100" :style="sectionPage===3 ? {'display': 'flex'}: {'display': 'none'}">
      <AdminStudentsViewAdmittedStudents />
    </div>
  </div>
</template>

<style scoped>

.nav-btn-1{
  font-size: .6rem !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    font-size: .65rem !important;
  }
  .btn-1{
    margin-right: 3em !important;
  }
  .btn-2{
    margin-left: 3em !important;
  }
  .btn-3{
    margin-left: 3em !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    font-size: .7rem !important;
  }
  .btn-1{
    margin-right: 4em !important;
  }
  .btn-2{
    margin-left: 4em !important;
  }
  .btn-3{
    margin-left: 4em !important;
  }
}


</style>
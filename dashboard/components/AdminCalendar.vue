
<script setup lang="ts">
import {ref} from "vue";


const sectionPage = ref(1)


const changeTerm = (term: number)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="section-nav-container">
    <button class="nav-btn-1 btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">ADD ACADEMIC YEAR</button>
    <button class="nav-btn-1 btn-2" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">ALL ACADEMIC YEARS</button>
  </div>

  <div class="sections">
    <div class="h-100" :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
      <AdminAddAcademicYear />
    </div>
    <div class="h-100" :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
      <AdminAllAcademicYears />
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
    margin-right: 2em !important;
  }
  .btn-2{
    margin-left: 2em !important;
  }
  
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    font-size: .7rem !important;
  }
  .btn-1{
    margin-right: 3em !important;
  }
  .btn-2{
    margin-left: 3em !important;
  }
  
}


</style>
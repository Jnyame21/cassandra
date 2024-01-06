<script setup lang="ts">
import {ref} from "vue";


const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()


const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="sections-container">
    <v-sheet class="section-nav-container" elevation="0">
      <button class="nav-btn-1 btn-1" @click="changeSection('section1')" :class="{'nav-btn-1-active': sectionPage==='section1'}">
        <v-icon icon="mdi-account"/>
        PROFILE
      </button>
      <button class="nav-btn-1 btn-2" @click="changeSection('section2')" :class="{'nav-btn-1-active': sectionPage==='section2'}">
        <v-icon icon="mdi-clipboard-check"/>
        ASSIGN SUBJECTS</button>
      <button class="nav-btn-1 btn-3" @click="changeSection('section3')" :class="{'nav-btn-1-active': sectionPage==='section3'}">
        <v-icon icon="mdi-book-open-outline"/>
        ALL SUBJECTS ASSIGNMENT</button>
    </v-sheet>
  
    <div class="sections">
      <div class="h-100" :style="sectionPage==='section1' ? {'display': 'flex'}: {'display': 'none'}">
        <HodTeachersProfile :staff="userAuthStore.hodSubjectAssignmentUpload.staff" />
      </div>
      <div class="h-100" :style="sectionPage==='section2' ? {'display': 'flex'}: {'display': 'none'}">
        <HodSubjectAssignmentUpload />
      </div>
      <div class="h-100" :style="sectionPage==='section3' ? {'display': 'flex'}: {'display': 'none'}">
        <HodViewSubjectAssignment />
      </div>
    </div>
  </div>
</template>

<style scoped>

@media screen and (min-width: 576px) {
  .nav-btn-1{
    font-size: .65rem !important;
  }
  .btn-1{
    margin-right: 1em !important;
  }
  .btn-2{
    margin-left: 1em !important;
  }
  .btn-3{
    margin-left: 1em !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    font-size: .7rem !important;
  }
  .btn-1{
    margin-right: 2em !important;
  }
  .btn-2{
    margin-left: 2em !important;
  }
  .btn-3{
    margin-left: 2em !important;
  }
}

</style>


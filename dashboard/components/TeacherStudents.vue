<script setup lang="ts">
import {ref} from "vue";


const sectionPage = ref('section1')

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="sections-container">
    <v-sheet class="section-nav-container" elevation="0">
      <button class="nav-btn-1 btn-1" @click="changeSection('section1')" :class="{'nav-btn-1-active': sectionPage==='section1'}">
        <v-icon icon="mdi-account-multiple-check"/>
        ATTENDANCE</button>
      <button class="nav-btn-1 btn-2" @click="changeSection('section2')" :class="{'nav-btn-1-active': sectionPage==='section2'}">
        <v-icon icon="mdi-upload-box"/>
        UPLOAD RESULTS</button>
      <button class="nav-btn-1 btn-3" @click="changeSection('section3')" :class="{'nav-btn-1-active': sectionPage==='section3'}">
        <v-icon icon="mdi-view-list"/>
        ALL UPLOADED RESULTS</button>
    </v-sheet>
  
    <div class="sections">
      <div class="h-100" :style="sectionPage==='section1' ? {'display': 'flex'}: {'display': 'none'}">
        <TeacherStudentsAttendance />
      </div>
      <div class="h-100" :style="sectionPage==='section2' ? {'display': 'flex'}: {'display': 'none'}">
        <TeacherStudentsResultsUpload />
      </div>
      <div class="h-100" :style="sectionPage==='section3' ? {'display': 'flex'}: {'display': 'none'}">
        <TeacherStudentsViewResults/>
      </div>
    </div>
  </div>
</template>

<style scoped>

.nav-btn-1{
  font-size: .55rem !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    font-size: .6rem !important;
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

@media screen and (min-width: 767px) {
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



</style>




<script setup lang="ts">
import {ref} from "vue";


const userAuthStore = useUserAuthStore()
const sectionPage = ref(userAuthStore.activeTerm)


const changeTerm = (term: number)=>{
  sectionPage.value = term
}


</script>

<template>
  <!-- semester -->
  <div class="section-nav-container" v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">
    <button class="nav-btn-1 btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">SEMESTER 1</button>
    <button class="nav-btn-1 btn-2" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">SEMESTER 2</button>
  </div>
  <!-- trimester -->
  <div class="section-nav-container" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">
    <button class="nav-btn-1 btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">TRIMESTER 1</button>
    <button class="nav-btn-1 btn-2" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">TRIMESTER 2</button>
    <button class="nav-btn-1 btn-3" @click="changeTerm(3)" :class="{'nav-btn-1-active': sectionPage===3}">TRIMESTER 3</button>
  </div>

  <div class="sections">
    <div class="h-100" :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
      <TeacherTermCourseWork :term="'termOne'" :term-number="1" />
    </div>
    <div class="h-100" :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
      <TeacherTermCourseWork :term="'termTwo'" :term-number="2" />
    </div>
    <div class="h-100" :style="sectionPage===3 ? {'display': 'flex'}: {'display': 'none'}"
    v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']"
    >
      <TeacherTermCourseWork :term="'termThree'" :term-number="3" />
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
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    font-size: .7rem !important;
  }
  .btn-1{
    margin-right: 5em !important;
  }
  .btn-2{
    margin-left: 5em !important;
  }
}

</style>
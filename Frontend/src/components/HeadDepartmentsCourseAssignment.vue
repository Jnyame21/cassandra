<script setup lang="ts">
import {ref} from "vue";


interface Props {
  subjectAssignment: {
    term_one: any;
    term_two: any;
    term_three: any;
  }
}

const { subjectAssignment } = defineProps<Props>()

const userAuthStore = useUserAuthStore()
const sectionPage = ref(userAuthStore.activeTerm)

const changeTerm = (term: number)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    <!-- semesters -->
    <div class="subsection-nav-container" v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">
      <button class="nav-btn-2" @click="changeTerm(1)" :class="{'nav-btn-2-active': sectionPage===1}">SEMESTER 1</button>
      <button class="nav-btn-2" @click="changeTerm(2)" :class="{'nav-btn-2-active': sectionPage===2}">SEMESTER 2</button>
    </div>

      <!-- trimesters -->
    <div class="subsection-nav-container" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">
      <button class="nav-btn-2" @click="changeTerm(1)" :class="{'nav-btn-2-active': sectionPage===1}">TRIMESTER 1</button>
      <button class="nav-btn-2" @click="changeTerm(2)" :class="{'nav-btn-2-active': sectionPage===2}">TRIMESTER 2</button>
      <button class="nav-btn-2" @click="changeTerm(3)" :class="{'nav-btn-2-active': sectionPage===3}">TRIMESTER 3</button>
    </div>

    <div class="subsections">
      <div class="h-100" :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
        <HeadDepartmentTermCourseAssignment  :term="subjectAssignment.term_one"/>
      </div>
      <div class="h-100" :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
        <HeadDepartmentTermCourseAssignment :term="subjectAssignment.term_two"/>
      </div>
      <div class="h-100" :style="sectionPage===3 ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']"
      >
        <HeadDepartmentTermCourseAssignment :term="subjectAssignment.term_three"/>
      </div>
    </div>
  </div>
</template>

<style scoped>


</style>
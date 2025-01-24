<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import { computed } from 'vue';
import TheLoader from './TheLoader.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const headTeacher = computed(()=>{
  return userAuthStore.studentData.headTeacher
})

const students = computed(()=>{
  return userAuthStore.studentData.students
})

const subjects = computed(()=>{
  return userAuthStore.studentData.subjects
})

const maleStudents = computed(()=>{
  return students.value?.filter(item => item.gender.toLocaleLowerCase() === 'male').length || 0
})

const femaleStudents = computed(()=>{
  return students.value?.filter(item => item.gender.toLocaleLowerCase() === 'female').length || 0
})

const showOverlay = (element:string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'flex'
  }
}

const closeBtn = (element:string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'none'
  }
}

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'StudentClassStudents'"
  :class="{ 'is-active-page': elementsStore.activePage === 'StudentClassStudents'}">
    
    <div id="teacherInfoOverlay" class="overlay">
      <div class="info-container">
        <v-btn @click="closeBtn('teacherInfoOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="flex-all-c ma-5 mt-15">
          <p v-if="!headTeacher">No head teacher has been assigned to this class yet</p>
          <div class="teacher-info" v-if="headTeacher">
            <h4  class="title">CLASS HEAD TEACHER INFORMATION</h4>
            <p class="title">NAME: <strong>{{ headTeacher.user }}</strong></p>
            <p class="title">GENDER: <strong>{{ headTeacher.gender }}</strong></p>
            <p class="title">PHONE NO: <strong>{{ headTeacher.contact}}</strong></p>
            <p class="title" v-if="headTeacher.email">EMAIL: <strong>{{ headTeacher.email}}</strong></p>
            <p class="title"><img class="teacher-img" :src="headTeacher.img"></p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- subjects overlay -->
    <div id="SubjectOverlay" class="overlay" v-if="subjects.length > 0">
      <div class="overlay-card subjects">
        <v-btn @click="closeBtn('SubjectOverlay')" color="red" variant="flat" size="small" class="close-btn">X</v-btn>
        <div class="overlay-card-content-container">
          <v-table fixed-header class="table">
            <thead>
            <tr>
              <th class="table-head">SUBJECT</th>
              <th class="table-head">TEACHER NAME</th>
              <th class="table-head">TEACHER GENDER</th>
              <th class="table-head">TEACHER CONTACT</th>
              <th class="table-head">TEACHER EMAIL</th>
              <th class="table-head">IMAGE</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(_subject, i) in subjects" :key="i">
              <td class="table-data">{{_subject.name}}</td>
              <td class="table-data">{{_subject.teacher}}<span style="color: red" v-if="!_subject.teacher">No teacher has been assgined yet</span></td>
              <td class="table-data">{{_subject.teacher_gender}}</td>
              <td class="table-data">{{_subject.teacher_contact}}</td>
              <td class="table-data">{{_subject.teacher_email}}</td>
              <td class="table-data" v-if="_subject.teacher_img"><img class="profile-img" :src="_subject.teacher_img"></td>
            </tr>
            </tbody>
          </v-table>
        </div>
      </div>
    </div>
    <TheLoader v-if="!students" />
    <div class="content-header" v-if="students">
      <h4 class="content-header-title">{{ userAuthStore.userData['st_class'] }}</h4>
    </div>
    <div class="content-header stats" v-if="students">
      <div class="content-header-text">
        TOTAL NUMBER OF STUDENTS:
        <span class="content-header-text-value">
          {{ students.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STUDENTS:
        <span class="content-header-text-value">
          {{ maleStudents }} [{{ ((maleStudents / students.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STUDENTS:
        <span class="content-header-text-value">
          {{ femaleStudents }} [{{ ((femaleStudents / students.length) * 100).toFixed(1) }}%]
        </span>
      </div>
    </div>
    <div class="content-header" v-if="students">
      <v-btn class="mr-2" :size="elementsStore.btnSize1" @click="showOverlay('teacherInfoOverlay')" color="blue">HEAD TEACHER</v-btn>
      <v-btn class="ml-2" v-if="subjects.length > 0" :size="elementsStore.btnSize1" @click="showOverlay('SubjectOverlay')" color="blue">SUBJECTS</v-btn>
    </div>
    <v-table fixed-header class="table" v-if="students">
      <thead>
      <tr>
        <th class="table-head">NAME</th>
        <th class="table-head">GENDER</th>
        <th class="table-head">PHONE NO</th>
        <th class="table-head">IMAGE</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(st, i) in students" :key="i">
        <td class="table-data">{{st.user}}</td>
        <td class="table-data">{{st.gender}}</td>
        <td class="table-data">{{st.contact}}</td>
        <td class="table-data"><img class="profile-img" :src="st.img"></td>
      </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.subjects .overlay-card{
  max-width: 1200px !important;
}
.subjects .overlay-card-content-container{
  margin-top: 4em;
}
.stats{
  height: 30% !important;
}
.table{
  min-height: 50% !important;
}
.info-container{
  position: relative;
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  border-radius: .3em;
  max-width: 500px;
}
.teacher-info h4{
  font-size: .8rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: red;
  border: 2px solid black;
}
.title{
  font-size: .8rem;
  margin-top: .5em;
  text-align: center;
  font-weight: bold;
}
.title strong{
  color: seagreen;
}
.teacher-img{
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

@media screen and (min-width: 460px) {
  .stats{
    height: 20% !important;
  }
}

@media screen and (min-width: 720px) {
  .stats{
    height: 10% !important;
  }
}

</style>
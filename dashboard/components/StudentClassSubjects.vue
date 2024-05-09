<script setup lang="ts">
import { ref } from 'vue'


const userAuthStore = useUserAuthStore()
const subjectName = ref('')
const teacherName: any = ref(null)
const teacherImg: any = ref(null)
const teacherGender: any = ref(null)
const teacherContact: any = ref(null)
const teacherEmail: any = ref(null)
const teacherDepartment: any = ref(null)

const subjectInfo = (subject: string, teacher: string, img: any, gender: any, email: any, contact: any, department: any)=>{
  subjectName.value = subject
  if (teacher !== 'null'){
    teacherName.value = teacher
    teacherImg.value = img
    teacherGender.value = gender
    teacherContact.value = contact
    teacherEmail.value = email
    teacherDepartment.value = department
  }
  const overlay = document.getElementById('subjectOverlay')
  overlay ? overlay.style.display = 'flex' : null
}

const closeBtn = ()=>{
  const overlay = document.getElementById('subjectOverlay')
  teacherName.value = null
  teacherImg.value = ''
  teacherGender.value = ''
  teacherContact.value = ''
  teacherEmail.value = ''
  teacherDepartment.value = ''
  overlay ? overlay.style.display = 'none' : null
}


</script>

<template>
  <div id="subjectOverlay" class="overlay">
    <div class="info-container">
      <v-btn @click="closeBtn" color="red" size="small" class="close-btn">X</v-btn>
      <div class="flex-all-c ma-5 mt-15">
        <h4 class="subject-name"><strong>{{subjectName}}</strong></h4>
        <p class="title message" v-if="!teacherName && userAuthStore.userData['school']['semesters']">No teacher has been assigned to teach this subject yet for the {{userAuthStore.activeAcademicYear}} academic year, semeter {{userAuthStore.activeTerm}}</p>
        <p class="title message" v-if="!teacherName && !userAuthStore.userData['school']['semesters']">No teacher has been assigned to teach this subject yet for the {{userAuthStore.activeAcademicYear}} academic year, trimester {{userAuthStore.activeTerm}}</p>
        <div class="teacher-info" v-if="teacherName">
          <h4  class="title">TEACHER INFO</h4>
          <p class="title">NAME: <strong>{{teacherName}}</strong></p>
          <p class="title" v-if="teacherGender">GENDER: <strong>{{teacherGender}}</strong></p>
          <p class="title" v-if="teacherDepartment">DEPARTMENT: <strong>{{teacherDepartment}}</strong></p>
          <p class="title" v-if="teacherContact">PHONE NO: <strong>{{teacherContact}}</strong></p>
          <p class="title" v-if="teacherEmail">EMAIL: <strong>{{teacherEmail}}</strong></p>
          <p class="title"  v-if="teacherImg"><img class="teacher-img" :src="teacherImg"></p>
        </div>
      </div>
    </div>
  </div>
<section class="d-flex flex-column h-100 w-100 justify-center align-center">
  <TheLoader v-if="userAuthStore.studentData && !userAuthStore.studentData['subjects']" />
  <p class="notice" v-if="userAuthStore.userData && userAuthStore.userData['current_yr'] === 'COMPLETED'">YOU HAVE COMPLETED SCHOOL</p>
  <div v-if="userAuthStore.userData && userAuthStore.userData['current_yr'] !== 'COMPLETED' && userAuthStore.studentData && userAuthStore.studentData['subjects']"  class="subject-container">
    <v-card v-for="(subject, index) in userAuthStore.studentData.subjects" @click="subjectInfo(subject['name'], subject['teacher'], subject['teacher_img'], subject['teacher_gender'], subject['teacher_email'], subject['teacher_contact'], subject['teacher_department'])" class="subject-card" :key="index">
      <v-icon icon="mdi-calculator-variant" v-if="subject['name']==='CORE MATHEMATICS' "/>
      <v-icon icon="mdi-function-variant" v-if="subject['name']==='ELECTIVE MATHEMATICS' "/>
      <v-icon icon="mdi-microscope" v-if="subject['name']==='BIOLOGY' "/>
      <v-icon icon="mdi-flask" v-if="subject['name']==='CHEMISTRY' "/>
      <v-icon icon="mdi-currency-usd" v-if="subject['name']==='FINANCIAL ACCOUNTING' "/>
      <v-icon icon="mdi-chart-bar" v-if="subject['name']==='BUSINESS MANAGEMENT' "/>
      <v-icon icon="mdi-book-open-variant" v-if="subject['name']==='ENGLISH LANGUAGE' "/>
      <v-icon icon="mdi-account-group" v-if="subject['name']==='SOCIAL STUDIES' "/>
      <v-icon icon="mdi-scale" v-if="subject['name']==='INTEGRATED SCIENCE' "/>
      <v-icon icon="mdi-book-cross" v-if="subject['name']==='CHRISTIAN RELIGIOUS STUDIES (CRS)' "/>
      <v-icon icon="mdi-library" v-if="subject['name']==='LITERATURE' "/>
      <v-icon icon="mdi-history" v-if="subject['name']==='HISTORY' "/>
      <v-icon icon="mdi-briefcase-account" v-if="subject['name']==='GOVERNMENT' "/>
      <v-icon icon="mdi-earth" v-if="subject['name']==='GEOGRAPHY' "/>
      <v-icon icon="mdi-atom" v-if="subject['name']==='PHYSICS' "/>
      <v-icon icon="mdi-desktop-tower-monitor" v-if="subject['name']==='ELECTIVE ICT' "/>
      <v-icon icon="mdi-cash-register" v-if="subject['name']==='COST ACCOUNTING' "/>
      <v-icon icon="mdi-finance" v-if="subject['name']==='ECONOMICS' "/>
      <p class="subject-title">{{subject['name']}}</p>
    </v-card>
  </div>
</section>
</template>

<style scoped>

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

.notice{
  color: green;
  font-size: .6rem;
}

.teacher-info h4{
  font-size: .8rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: red;
}

.title{
  font-size: .8rem;
  margin-top: .5em;
  text-align: center;
  font-weight: bold;
}
.subject-name{
  font-size: 1.2rem;
  color: seagreen;
  text-transform: uppercase;
}
.title strong{
  color: seagreen;
}
.teacher-img{
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.message{
  color: red !important;
  text-align: center !important;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.subject-container{
  display: flex;
  flex-wrap: wrap;
  height: 100%;
  overflow-y: auto;
  align-items: center;
  justify-content: center;
}

.subject-card{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  width: 300px;
  cursor: pointer;
  height: 100px;
  margin: 1em;
}

.subject-title{
  font-size: .4rem;
  text-align: center;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  text-transform: uppercase;
  font-weight: bold;
  color: seagreen;
}

.subject-card:hover {
  box-shadow: 1px 1px 5px black;
}

.overlay{
  position: absolute;
  background: rgba(0, 0, 0, .5);
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: 5;
  align-items: center;
  justify-content: center;
  display: none;
}

@media screen and (min-width: 576px) {
  .subject-card{
    height: 150px;
    width: 300px;
  }
  .subject-title{
    font-size: .5rem;
  }
  .notice{
    font-size: .7rem;
  }
}

@media screen and (min-width: 767px) {

  .subject-title{
    font-size: .55rem;
  }

}
@media screen and (min-width: 2000px) {
  subject-card{
    height: 200px;
    width: 400px;
  }
  .subject-title{
    font-size: .65rem;
  }

}



</style>
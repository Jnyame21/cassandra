<script setup lang="ts">
import { ref } from 'vue'
import { useUserAuthStore } from '@/stores/userAuthStore';

const userAuthStore = useUserAuthStore()
const subjectName = ref('')
const teacherName: any = ref(null)
const teacherImg: any = ref(null)
const teacherGender: any = ref(null)
const teacherContact: any = ref(null)
const teacherEmail: any = ref(null)
const teacherDepartment: any = ref(null)

const subjectInfo = (subject: string, teacher: string, img: any, gender: any, email: any, contact: any, department: any) => {
  subjectName.value = subject
  if (teacher !== 'null') {
    teacherName.value = teacher
    teacherImg.value = img
    teacherGender.value = gender
    teacherContact.value = contact
    teacherEmail.value = email
    teacherDepartment.value = department
  }
  const overlay = document.getElementById('subjectOverlay')
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeBtn = () => {
  const overlay = document.getElementById('subjectOverlay')
  teacherName.value = ''
  teacherImg.value = ''
  teacherGender.value = ''
  teacherContact.value = ''
  teacherEmail.value = ''
  teacherDepartment.value = ''
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper">
    <div id="subjectOverlay" class="overlay">
      <div class="info-container">
        <v-btn @click="closeBtn" color="red" size="small" class="close-btn">X</v-btn>
        <div class="flex-all-c ma-5 mt-15">
          <h4 class="subject-name"><strong>{{ subjectName }}</strong></h4>
          <p class="title message" v-if="teacherName === 'none'">No teacher has been assigned to teach this subject yet
            for the {{ userAuthStore.activeAcademicYear }} academic year,
            {{ userAuthStore.userData['academic_year']['period_division'] }} {{ userAuthStore.activeTerm }}</p>
          <div class="teacher-info" v-if="teacherName !== 'none'">
            <h4 class="title">TEACHER INFORMATION</h4>
            <p class="title">NAME: <strong>{{ teacherName }}</strong></p>
            <p class="title" v-if="teacherGender">GENDER: <strong>{{ teacherGender }}</strong></p>
            <p class="title" v-if="teacherDepartment !== 'none'">DEPARTMENT: <strong>{{ teacherDepartment }}</strong></p>
            <p class="title" v-if="teacherContact">PHONE NO: <strong>{{ teacherContact }}</strong></p>
            <p class="title" v-if="teacherEmail">EMAIL: <strong>{{ teacherEmail }}</strong></p>
            <p class="title" v-if="teacherImg"><img class="teacher-img" :src="teacherImg"></p>
          </div>
        </div>
      </div>
    </div>
    <TheLoader v-if="userAuthStore.studentData && !userAuthStore.studentData['subjects']" />
    <p class="notice" v-if="userAuthStore.userData && userAuthStore.userData['current_yr'] === 'COMPLETED'">YOU HAVE
      COMPLETED SCHOOL</p>
    <div
      v-if="userAuthStore.userData && userAuthStore.userData['current_yr'] !== 'COMPLETED' && userAuthStore.studentData && userAuthStore.studentData['subjects']"
      class="subject-container">
      <v-card v-for="(subject, index) in userAuthStore.studentData.subjects" class="subject-card"
        @click="subjectInfo(subject['name'], subject['teacher'], subject['teacher_img'], subject['teacher_gender'], subject['teacher_email'], subject['teacher_contact'], subject['teacher_department'])"
        :key="index">
        <v-icon class="card-icon" icon="mdi-calculator-variant-outline" v-if="subject['name'] === 'CORE MATHEMATICS'" />
        <v-icon class="card-icon" icon="mdi-function-variant" v-if="subject['name'] === 'ELECTIVE MATHEMATICS'" />
        <v-icon class="card-icon" icon="mdi-microscope" v-if="subject['name'] === 'BIOLOGY'" />
        <v-icon class="card-icon" icon="mdi-flask" v-if="subject['name'] === 'CHEMISTRY'" />
        <v-icon class="card-icon" icon="mdi-currency-usd" v-if="subject['name'] === 'FINANCIAL ACCOUNTING'" />
        <v-icon class="card-icon" icon="mdi-chart-bar" v-if="subject['name'] === 'BUSINESS MANAGEMENT'" />
        <v-icon class="card-icon" icon="mdi-book-open-variant-outline" v-if="subject['name'] === 'ENGLISH LANGUAGE'" />
        <v-icon class="card-icon" icon="mdi-account-group" v-if="subject['name'] === 'SOCIAL STUDIES'" />
        <v-icon class="card-icon" icon="mdi-scale" v-if="subject['name'] === 'INTEGRATED SCIENCE'" />
        <v-icon class="card-icon" icon="mdi-book-cross" v-if="subject['name'] === 'CHRISTIAN RELIGIOUS STUDIES (CRS)'" />
        <v-icon class="card-icon" icon="mdi-library" v-if="subject['name'] === 'LITERATURE'" />
        <v-icon class="card-icon" icon="mdi-history" v-if="subject['name'] === 'HISTORY'" />
        <v-icon class="card-icon" icon="mdi-briefcase-account" v-if="subject['name'] === 'GOVERNMENT'" />
        <v-icon class="card-icon" icon="mdi-earth" v-if="subject['name'] === 'GEOGRAPHY'" />
        <v-icon class="card-icon" icon="mdi-atom" v-if="subject['name'] === 'PHYSICS'" />
        <v-icon class="card-icon" icon="mdi-desktop-tower-monitor" v-if="subject['name'] === 'ELECTIVE ICT'" />
        <v-icon class="card-icon" icon="mdi-cash-register" v-if="subject['name'] === 'COST ACCOUNTING'" />
        <v-icon class="card-icon" icon="mdi-finance" v-if="subject['name'] === 'ECONOMICS'" />
        <p class="subject-title">{{ subject['name'] }}</p>
      </v-card>
    </div>
  </div>
</template>

<style scoped>
.info-container {
  position: relative;
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  border-radius: .3em;
  max-width: 500px;
}

.notice {
  color: green;
  font-size: .8rem;
  font-weight: bold;
}

.teacher-info h4 {
  font-size: .8rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: red;
  border: 2px solid black;
}

.title {
  font-size: .8rem;
  margin-top: .5em;
  text-align: center;
  font-weight: bold;
}

.subject-name {
  font-size: 1.2rem;
  color: seagreen;
  text-transform: uppercase;
}

.title strong {
  color: seagreen;
}

.teacher-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.message {
  color: red !important;
  text-align: center !important;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.subject-container {
  display: flex;
  flex-wrap: wrap;
  height: 100%;
  overflow-y: auto;
  align-items: center;
  justify-content: center;
}

.subject-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  width: 300px;
  cursor: pointer;
  height: 100px;
  margin: 1em;
  background-color: #333333;
}

.card-icon {
  color: white;
}

.subject-title {
  font-size: .55rem;
  text-align: center;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  text-transform: uppercase;
  font-weight: bold;
  color: white;
}

.subject-card:hover {
  border: 2px solid yellow;
  border-radius: .5em;
}

.overlay {
  position: absolute;
  background: rgba(0, 0, 0, .5);
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: 10 !important;
  align-items: center;
  justify-content: center;
  display: none;
}

@media screen and (min-width: 576px) {
  .subject-card {
    width: 230px;
  }

  .subject-title {
    font-size: 0.6rem;
  }
}

@media screen and (min-width: 767px) {
  .subject-title {
    font-size: 0.7rem;
  }

  .notice {
    font-size: .9em;
  }
}

@media screen and (min-width: 1000px) {
  .subject-title {
    font-size: 0.8rem;
  }

  .notice {
    font-size: 1em;
  }
}

@media screen and (min-width: 2000px) {
  .subject-card {
    height: 150px;
    width: 300px;
  }

  .subject-title {
    font-size: .9rem;
  }
}
</style>
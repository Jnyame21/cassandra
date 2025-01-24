<script setup lang="ts">
import { computed } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import NoData from './NoData.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  className: string;
}

const props = defineProps<Props>()
const className = props.className

const classData = computed(()=>{
    return userAuthStore.headData.classes[className]
})

const students = computed(()=>{
    return classData.value.students || []
})

const subjects = computed(()=>{
    return classData.value.subjects || []
})

const headTeacher = computed(()=>{
    return classData.value.head_teacher
})

const maleStudents = computed(()=>{
  return students.value.filter(_st => _st.gender.toLowerCase() === 'male').length
})

const femaleStudents = computed(()=>{
  return students.value.filter(_st => _st.gender.toLowerCase() === 'female').length
})

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStudents,${className}`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStudents,${className}` }">
    
    <!-- head teahcer overlay -->
    <div :id="`ClassHeadTeacherOverlay${className}`" class="overlay">
        <div class="overlay-card">
          <v-btn @click="closeOverlay(`ClassHeadTeacherOverlay${className}`)" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
          <div class="flex-all-c ma-5 mt-15">
            <p style="color: red; font-weight: bold; text-align: center" v-if="!headTeacher">No head teacher has been assigned to this class yet</p>
            <div class="teacher-info" v-if="headTeacher">
              <h4  class="title">CLASS HEAD TEACHER</h4>
              <p class="title">{{ headTeacher.user }}</p>
              <p style="text-align: center"><img class="profile-img2" :src="headTeacher.img"></p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- subjects overlay -->
      <div :id="`HeadStudentClassSubjectsOverlay${className}`" class="overlay subjects" v-if="subjects.length > 0">
        <div class="overlay-card">
          <v-btn @click="closeOverlay(`HeadStudentClassSubjectsOverlay${className}`)" color="red" variant="flat" size="small" class="close-btn">X</v-btn>
          <div class="overlay-card-content-container">
            <v-table fixed-header class="table">
              <thead>
              <tr>
                <th class="table-head">SUBJECT</th>
                <th class="table-head">TEACHER NAME</th>
                <th class="table-head">TEACHER IMAGE</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(_subject, i) in subjects" :key="i">
                <td class="table-data">{{_subject.name}}</td>
                <td class="table-data">{{_subject.teacher}}<span style="color: red" v-if="!_subject.teacher">No teacher has been assigned yet</span></td>
                <td class="table-data" v-if="_subject.teacher_img"><img class="profile-img" :src="_subject.teacher_img"></td>
              </tr>
              </tbody>
            </v-table>
          </div>
        </div>
      </div>
    
    <div class="content-header">
      <h4 class="content-header-title">{{ className }}</h4>
    </div>
    <div class="content-header info">
      <div class="content-header-text">
        TOTAL NUMBER OF STUDENTS:
        <span class="content-header-text-value">
          {{ students.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STUDENTS:
        <span class="content-header-text-value">
          {{ maleStudents }} <span v-if="students.length > 0">[{{ ((maleStudents / students.length) * 100).toFixed(1) }}%]</span>
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STUDENTS:
        <span class="content-header-text-value">
          {{ femaleStudents }} <span v-if="students.length > 0">[{{ ((femaleStudents / students.length) * 100).toFixed(1) }}%]</span>
        </span>
      </div>
      <h4 class="content-header-text">
        STUDENTS YEAR:
        <span class="content-header-text-value">{{ classData.students_year }}</span>
      </h4>
      <h4 class="content-header-text">
        PROGRAM:
        <span class="content-header-text-value" v-if="classData.program">{{ classData.program }}</span>
      </h4>
    </div>
    <div class="content-header btn-container">
      <v-btn @click="showOverlay(`ClassHeadTeacherOverlay${className}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        HEAD TEACHER
      </v-btn>
      <v-btn @click="showOverlay(`HeadStudentClassSubjectsOverlay${className}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECTS
      </v-btn>
    </div>
    <NoData v-if="students.length === 0" message="There are no student in this class. Contact your school administrator"/>
    <v-table fixed-header class="table" v-if="students.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['index_no']">INDEX NO</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">DATE ENROLLED</th>
          <th class="table-head">RELIGION</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">PLACE OF BIRTH</th>
          <th class="table-head">REGION/STATE</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">RESIDENTIAL ADDRESS</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">GUARDIAN</th>
          <th class="table-head">GUARDIAN GENDER</th>
          <th class="table-head">GUARDIAN OCCUPATION</th>
          <th class="table-head">GUARDIAN CONTACT</th>
          <th class="table-head">GUARDIAN NATIONALITY</th>
          <th class="table-head">GUARDIAN RESIDENTIAL ADDRESS</th>
          <th class="table-head">GUARDIAN EMAIL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in students" :key="index">
          <td class="table-data">
            {{ st['user'] }}<v-icon icon="mdi-pencil"/>
            <v-list-item-subtitle>
              {{ st['st_id'] }}
            </v-list-item-subtitle>
          </td>
          <td class="table-data" v-if="userAuthStore.userData['school']['index_no']">{{ st['index_no'] }}</td>
          <td class="table-data">
            {{ st['gender'] }}
          </td>
          <td class="table-data">
            {{ st['dob'] }}
          </td>
          <td class="table-data">
            {{ st['date_enrolled'] }}
          </td>
          <td class="table-data">
            {{ st['religion'] }}
          </td>
          <td class="table-data">
            {{ st['contact'] }}
          </td>
          <td class="table-data">
            {{ st['pob'] }}
          </td>
          <td class="table-data">
            {{ st['region'] }}
          </td>
          <td class="table-data">
            {{ st['nationality'] }}
          </td>
          <td class="table-data">
            {{ st['address'] }}
          </td>
          <td class="table-data">
            <img class="profile-img" :src="st['img']">
          </td>
          <td class="table-data">
            {{ st['guardian'] }}
          </td>
          <td class="table-data">
            {{ st['guardian_gender'] }}
          </td>
          <td class="table-data">
            {{ st['guardian_occupation'] }}
          </td>
          <td class="table-data">
            {{ st['guardian_contact'] }}
          </td>
          <td class="table-data">
            {{ st['guardian_nationality'] }}
          </td>
          <td class="table-data">
            {{ st['guardian_address'] }}
          </td>
          <td class="table-data">
            {{ st['guardian_email'] }}
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 10% !important;
}
.info{
  height: 30% !important;
}
.btn-container {
  min-height: 10% !important;
}
.overlay-card{
  max-width: 500px !important;
}
.subjects .overlay-card{
  max-width: 1000px !important;
}
.subjects .overlay-card-content-container{
  margin-top: 4em;
}
.teacher-info h4{
  font-size: .8rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: red;
  border: 2px solid black;
}
.title{
  font-size: 1rem;
  margin-top: 2em;
  text-align: center;
  font-weight: bold;
  color: seagreen;
}



</style>
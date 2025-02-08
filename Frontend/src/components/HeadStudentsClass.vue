<script setup lang="ts">
import { computed } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  className: string;
  classIndex: number;
  subjects: string[];
  students_year: number;
  program: string | null;
}

const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const subjects = props.subjects
const students_year = props.students_year
const program = props.program || null

const students = computed(() => {
  return userAuthStore.headData.classes[classIndex].students || []
})

const maleStudents = computed(() => {
  return students.value.filter(item => item.gender.toLowerCase() === 'male').length
})

const femaleStudents = computed(() => {
  return students.value.filter(item => item.gender.toLowerCase() === 'female').length
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
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStudentsClass,${className},${classIndex}`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStudentsClass,${className},${classIndex}` }">

    <!-- class subjects overlay -->
    <div :id="`HeadStudentClassSubjectsOverlay${className}${classIndex}`" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`HeadStudentClassSubjectsOverlay${className}${classIndex}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">
            SUBJECTS[{{ subjects.length }}]</h3>
          <p class="subject-card" v-for="(_subject, index) in subjects" :key="index">
            {{ _subject }}
          </p>
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
          {{ maleStudents }} <span v-if="students.length > 0">[{{ ((maleStudents / students.length) * 100).toFixed(1)}}%]</span>
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
        <span class="content-header-text-value">{{ students_year }}</span>
      </h4>
      <h4 class="content-header-text">
        PROGRAM:
        <span class="content-header-text-value" v-if="program">{{ program }}</span>
      </h4>
    </div>
    <div class="content-header">
      <v-btn @click="showOverlay(`HeadStudentClassSubjectsOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECT(S)
      </v-btn>
    </div>
    <div class="no-data" v-if="students.length === 0">
      <p>There are no student in this class</p>
    </div>
    <v-table fixed-header class="table" v-if="students.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head" v-if="userAuthStore.userData['current_role']['level']['index_no']">INDEX NO</th>
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
            {{ st['user'] }}
            <v-list-item-subtitle>{{ st['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data" v-if="userAuthStore.userData['school']['index_no']">{{ st['index_no'] }}</td>
          <td class="table-data">{{ st['gender'] }}</td>
          <td class="table-data">{{ st['dob'] }}</td>
          <td class="table-data">{{ st['date_enrolled'] }}</td>
          <td class="table-data">{{ st['religion'] }}</td>
          <td class="table-data">{{ st['contact'] }}</td>
          <td class="table-data">{{ st['pob'] }}</td>
          <td class="table-data">{{ st['region'] }}</td>
          <td class="table-data">{{ st['nationality'] }}</td>
          <td class="table-data">{{ st['address'] }}</td>
          <td class="table-data">
            <img class="profile-img" :src="st['img']">
          </td>
          <td class="table-data">{{ st['guardian'] }}</td>
          <td class="table-data">{{ st['guardian_gender'] }}</td>
          <td class="table-data">{{ st['guardian_occupation'] }}</td>
          <td class="table-data">{{ st['guardian_contact'] }}</td>
          <td class="table-data">{{ st['guardian_nationality'] }}</td>
          <td class="table-data">{{ st['guardian_address'] }}</td>
          <td class="table-data">{{ st['guardian_email'] }}</td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header {
  min-height: 10% !important;
}
.info {
  min-height: 15% !important;
}
.overlay-card {
  max-width: 500px !important;
}


</style>
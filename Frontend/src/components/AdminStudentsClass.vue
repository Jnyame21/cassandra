<script setup lang="ts">
import { AxiosError } from 'axios';
import { ref } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const femaleStudents = ref(0)
const maleStudents = ref(0)
const subjectSelected: any = ref(null)
const toClass:any = ref(null)
const formErrorMessage = ref('')


interface Props {
  className: string;
  classIndex: number;
  students: any[];
  subjects: string[];
  students_year: number;
  program?: string;
}

const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const students = props.students
const subjects = props.subjects
const students_year = props.students_year
const program = props.program || null
const selectedHeadTeacher = ref('')

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  formErrorMessage.value = ''
  subjectSelected.value = null
  toClass.value = null
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

students.forEach((item: any) => {
  if (item['gender'].toLowerCase() === 'male') {
    maleStudents.value += 1
  }
  else if (item['gender'].toLowerCase() === 'female') {
    femaleStudents.value += 1
  }
})

const linkClass = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('fromClass', className);
  formData.append('toClass', toClass.value);

  try {
    const response = await axiosInstance.post('school-admin/linked-class', formData)
    userAuthStore.adminData.linkedClasses.unshift(response.data)
    closeOverlay(`AdminAddLinkedClassOverlay${className}${classIndex}`)
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Success', 'green', null, null)
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const assignClassHeadTeacher = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'assignClassHeadTeacher')
  formData.append('studentsClass', className);
  formData.append('teacherId', selectedHeadTeacher.value);

  try {
    const response = await axiosInstance.post('school-admin/data', formData)
    userAuthStore.adminData.classes[classIndex]['head_teacher'] = response.data
    closeOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `AdminStudentsClass,${className},${classIndex}`"
    :class="{ 'is-active-page': elementsStore.activePage === `AdminStudentsClass,${className},${classIndex}` }"
    >

    <!-- class subjects overlay -->
    <div :id="`AdminStudentClassSubjectsOverlay${className}${classIndex}`" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">SUBJECTS
            CLASS [{{ subjects.length }}]</h3>
          <p class="subject-card" v-for="(_subject, index) in subjects" :key="index">
            {{ _subject }}
          </p>
        </div>
      </div>
    </div>
    
     <!-- assign class head teacher overlay -->
    <div :id="`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="userAuthStore.adminData.staff.filter((_staff: any)=> _staff['role'].toLowerCase() === 'teacher' || _staff['role'].toLowerCase() === 'hod').map((_staff: any) => ({'name': _staff['user'], 'staff_id': _staff['staff_id']}))" label="HEAD TEACHER" v-model="selectedHeadTeacher" 
          item-title="name" item-value="staff_id" variant="solo-filled" density="comfortable" persistent-hint hint="Select the teacher you want to assign to this class as the head teacher">
          <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :subtitle="(item as any).raw.staff_id"></v-list-item>
          </template>
          </v-select>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="assignClassHeadTeacher()" :disabled="!selectedHeadTeacher" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- link class overlay -->
    <div :id="`AdminAddLinkedClassOverlay${className}${classIndex}`" class="overlay" v-if="students_year !== Number(userAuthStore.userData['school']['level']['years_to_complete'])">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAddLinkedClassOverlay${className}${classIndex}`)" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
        </div>
        <div class="overlay-card-content-container" style="min-height: 100px" v-if="userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)">
          <h4>LINKED TO:<span class="subject-card">{{ userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)['to_class'] }}</span></h4>
        </div>
        <div class="overlay-card-content-container" v-if="!userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)">
          <v-select class="select" :items="userAuthStore.adminData.classes.filter((_class: any)=> _class['name'] !== className && _class['program'] === program && _class['students_year'] === students_year+1).map((_class: any) => _class['name'])" label="LINK TO CLASS" v-model="toClass" 
          variant="solo-filled" density="comfortable" persistent-hint hint="Select the class students from this class will be promoted to" 
          />
        </div>
        <div class="overlay-card-action-btn-container" v-if="!userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)">
          <v-btn @click="linkClass()" :disabled="!toClass" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
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
          {{ maleStudents }} [{{ ((maleStudents / students.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STUDENTS:
        <span class="content-header-text-value">
          {{ femaleStudents }} [{{ ((femaleStudents / students.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <h4 class="content-header-text">
        STUDENTS YEAR:
        <span class="content-header-text-value">{{students_year}}</span>
      </h4>
      <h4 class="content-header-text">
        PROGRAM:
        <span class="content-header-text-value" v-if="program">{{program}}</span>
      </h4>
    </div>
    <div class="content-header btn-container">
      <h4 class="content-header-text flex-all pointer" v-if="userAuthStore.adminData.classes[classIndex]['head_teacher']" @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)">
          HEAD TEACHER:
          <span class="content-header-text-value ml-1">
            {{ userAuthStore.adminData.classes[classIndex]?.head_teacher?.user }}
          </span>
          <img class="profile-img ml-1" :src="userAuthStore.adminData.classes[classIndex]?.head_teacher?.img">
      </h4>
      <v-btn v-if="!userAuthStore.adminData.classes[classIndex]['head_teacher']" @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)" color="blue"
        :size="elementsStore.btnSize1">
        ASSIGN HEAD TEACHER
      </v-btn>
      <v-btn @click="showOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECT(S)
      </v-btn>
      <v-btn @click="showOverlay(`AdminAddLinkedClassOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1" v-if="students_year !== Number(userAuthStore.userData['school']['level']['years_to_complete'])">
        LINK CLASS
      </v-btn>
    </div>
    <v-table fixed-header class="table">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['index_no']">INDEX NO</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">DATE ENROLLED</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">GUARDIAN</th>
          <th class="table-head">GUARDIAN NATIONALITY</th>
          <th class="table-head">GUARDIAN CONTACT</th>
          <th class="table-head">GUARDIAN EMAIL</th>
          <th class="table-head">GUARDIAN ADDRESS</th>
          <th class="table-head">IMAGE</th>
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
          <td class="table-data">{{ st['nationality'] }}</td>
          <td class="table-data">{{ st['guardian'] }}</td>
          <td class="table-data">{{ st['guardian_nationality'] }}</td>
          <td class="table-data">{{ st['guardian_contact'] }}</td>
          <td class="table-data">{{ st['guardian_email'] }}</td>
          <td class="table-data">{{ st['guardian_address'] }}</td>
          <td class="table-data"><img class="profile-img" :src="st['img']"></td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header{
  min-height: 10% !important;
}
.btn-container{
  min-height: 15% !important;
}
.info {
  min-height: 25% !important;
}
.table {
  min-height: 45% !important;
}
.overlay-card {
  height: max-content !important;
  max-width: 500px !important;
}
.overlay-card-info-container {
  height: 100% !important;
  margin-top: 4em !important;
}
.upload .overlay-card {
  max-width: 700px !important;
}

@media screen and (min-width: 500px) {
  .info {
    min-height: 20% !important;
  }
}

@media screen and (min-width: 576px) {
  .btn-container{
    min-height: 12% !important;
  }
}

@media screen and (min-width: 767px) {
  .info {
    min-height: 15% !important;
  }
}

@media screen and (min-width: 1200px) {
  .btn-container {
    min-height: 15% !important;
  }
  .title {
    min-height: 10% !important;
  }
  .table {
    height: 60% !important;
  }
}

</style>
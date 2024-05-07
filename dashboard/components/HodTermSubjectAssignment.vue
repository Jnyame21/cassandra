<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '../utils/axiosInstance';

const userAuthStore = useUserAuthStore()
const loading = ref(false)
const formErrorMessage = ref('')
const subject = ref('')
const studentsClass = ref('')
const teacherID = ref('')

interface Props {
  term: number;
  data: string;
}

const { term, data } = defineProps<Props>()

const hidOverlay = ()=>{
  const overlay = document.getElementById(`delete${term}`)
  overlay ? overlay.style.display = "none" : null
  formErrorMessage.value = ''
  subject.value = ''
  studentsClass.value = ''
  teacherID.value = ''

}

const continueDeletion = async()=>{
  loading.value = true
  const formData = new FormData
  formData.append('subject_name', subject.value)
  formData.append('students_class_name', studentsClass.value)
  formData.append('teacher_id', teacherID.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('type', 'delete')
  formData.append('term', term.toString())
  
  try {
    const response = await axiosInstance.post('hod/data', formData)
    if (response.status===200){
      const hodSubjectAssignment = userAuthStore.hodSubjectAssignment[data].find(c => c['subject']['name']===subject.value && c['students_class']['name']===studentsClass.value && c['teacher']['staff_id']===teacherID.value)
      if (hodSubjectAssignment){
        const index = userAuthStore.hodSubjectAssignment[data].indexOf(hodSubjectAssignment)
        userAuthStore.hodSubjectAssignment[data].splice(index, 1)
      }

      const teacherSubjectAssignment = userAuthStore.staffSubjectAssignment[data].find(c => c['subject']['name']===subject.value && c['students_class']['name']===studentsClass.value && c['teacher']['staff_id']===teacherID.value)
      if (teacherSubjectAssignment){
        const index = userAuthStore.staffSubjectAssignment[data].indexOf(teacherSubjectAssignment)
        userAuthStore.staffSubjectAssignment[data].splice(index, 1)
      }

      await userAuthStore.getTeacherStudentResults()
      hidOverlay()
      loading.value = false
    }
  }

  catch(e) {
    formErrorMessage.value = "Oops! something went wrong. Check your internet connection and try again"
    loading.value = false
  }
}


const deletesubjectAssignment = async(subjectName: string, studentsClassName: string, teacherId: string)=>{
  const overlay = document.getElementById(`delete${term}`)
  subject.value = subjectName
  studentsClass.value = studentsClassName
  teacherID.value = teacherId
  overlay ? overlay.style.display = 'flex' : null

}


</script>

<template>
  <div :id="`delete${term}`" class="overlay">
    <v-card class="d-flex flex-column align-center">
      <v-card-text style="font-size: .8rem; font-family: sans-serif; text-align: left; line-height: 1.2; font-weight: bold">
        <p>Continue to delete ?</p>
        <p v-if="formErrorMessage" class="mt-5" style="color: red">{{ formErrorMessage }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn :loading="loading" class="mr-5" elevation="4" @click="continueDeletion" color="red" >YES</v-btn>
        <v-btn :disabled="loading" class="ml-5" elevation="4" @click="hidOverlay" color="blue" >NO</v-btn>
      </v-card-actions>
    </v-card>
  </div>
    <div style="width: 100%; position: relative; height: 100%">
      <h4 class="no-data flex-all" v-if="userAuthStore.hodSubjectAssignment[data] && userAuthStore.hodSubjectAssignment[data].length === 0">
        <p v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">You have not uploaded any subject-assignment for semester {{ term }} yet</p>
        <p v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">You have not uploaded any subject-assignment for trimester {{ term }} yet</p>
      </h4>
      <v-table fixed-header height="320px" v-if="userAuthStore.hodSubjectAssignment[data] && userAuthStore.hodSubjectAssignment[data].length > 0">
        <thead>
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">FORM</th>
          <th class="table-head">TEACHER</th>
          <th class="table-head">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(assign, i) in userAuthStore.hodSubjectAssignment[data]" :key="i">
            <td class="table-data">{{assign['subject']['name']}}</td>
            <td class="table-data">{{assign['students_class']['name']}}</td>
            <td class="table-data">{{assign['students_class']['students_year']}}</td>
            <td class="table-data">{{assign['teacher']['user']['first_name']}} {{assign['teacher']['user']['last_name']}} [{{assign['teacher']['staff_id']}}]</td>
            <td v-if="userAuthStore.activeTerm===term"><v-btn @click="deletesubjectAssignment(assign['subject']['name'], assign['students_class']['name'], assign['teacher']['staff_id'])" color="red" size="small" >Delete</v-btn></td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


.overlay{
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.7);
  align-items: center;
  justify-content: center;
  z-index: 10;
}


</style>


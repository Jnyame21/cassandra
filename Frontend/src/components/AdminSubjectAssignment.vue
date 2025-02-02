<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const classSelected: any = ref(null)
const subjectsSelected = ref([])
const teacherSelected: any = ref(null)


const studentClasses = computed(() => {
  return userAuthStore.adminData.classes.map(item=> ({'name': item['name'], 'subjects': item['subjects']}))
})

const subjectAssignments = computed(() => {
  return userAuthStore.adminData.subjectAssignments
})

const teachers = computed(() => {
  return userAuthStore.adminData.staff?.filter(item=> item.roles.includes(item.roles.filter(subItem=> subItem.toLowerCase() === `teacher | ${userAuthStore.userData['current_role']['level']['identifier'].toLowerCase()}`)[0])).map(item=> ({'user': item['user'], 'staff_id': item['staff_id']}))
})

const uploadSubjectAssignment = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'upload')
  formData.append('studentsClassName', classSelected.value);
  formData.append('subjects', JSON.stringify(subjectsSelected.value));
  formData.append('teacher', teacherSelected.value);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    const response = await axiosInstance.post('school-admin/subject-assignment', formData)
    userAuthStore.adminData.subjectAssignments.push(response.data)
    teacherSelected.value = null
    subjectsSelected.value = []
    classSelected.value = null
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful!', 'green', null, null)
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

const deleteSubjectAssignment = async (index: number, assignment_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', assignment_id.toString());
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    await axiosInstance.post('school-admin/subject-assignment', formData)
    userAuthStore.adminData.subjectAssignments.splice(index, 1)
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

const closeOverlay = (element: string) => {
  teacherSelected.value = null
  subjectsSelected.value = []
  classSelected.value = null
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'AdminSubjectAssignment'" :class="{ 'is-active-page': elementsStore.activePage === 'AdminSubjectAssignment' }">
   
    <!-- subject assignment upload overlay -->
    <div id="AdminSubjectAssignmentOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminSubjectAssignmentOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-content-container">
          <v-select clearable chips v-model="teacherSelected" class="select" label="TEACHER"
            :items="teachers" item-title="user" item-value="staff_id" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the teacher who will teach the subject(s)">
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.staff_id"></v-list-item>
            </template>
          </v-select>
          <v-select class="select" :items="studentClasses" label="CLASS" v-model="classSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the class you want the teaacher to teach" item-title="name" item-value="name"
          />
          <div v-for="(_class, index) in studentClasses" :key="index">
            <v-select class="select" v-if="_class.name === classSelected" :items="_class.subjects" label="SUBJECT(S)" v-model="subjectsSelected"
            multiple chips variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the subject(s) you want the teacher to teacher" 
            />
          </div>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="uploadSubjectAssignment"
            :disabled="!(teacherSelected && subjectsSelected.length > 0 && classSelected)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    
    <div class="content-header">
      <v-btn @click="showOverlay('AdminSubjectAssignmentOverlay')" color="blue"
        :size="elementsStore.btnSize1">
        ASSIGN SUBJECT(S)
      </v-btn>
    </div>
    <div class="no-data" v-if="subjectAssignments.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="subjectAssignments.length > 0">
      <thead>
        <tr>
          <th class="table-head">TEACHER</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">SUBJECT(S)</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_assign, index) in subjectAssignments" :key="index">
          <td class="table-data">
            {{ _assign['teacher']['user'] }}
            <v-list-item-subtitle>{{ _assign['teacher']['staff_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            {{ _assign['students_class'] }}
          </td>
          <td class="table-data">
            <p v-for="(_subject, ind) in _assign['subjects']" :key="ind">{{ _subject }}</p>
          </td>
          <td class="table-data">
            <v-btn
              @click="elementsStore.ShowDeletionOverlay(() => deleteSubjectAssignment(index, _assign.id), 'Are you sure you want to delete this subject assignment?')"
              variant="flat" icon="mdi-delete" size="x-small" color="red" 
            />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.overlay-card{
  max-width: 600px !important;
}
.overlay-card-content-container{
  margin-top: 3em !important;
}


</style>
<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import NoData from './NoData.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const subjectsSelected = ref<string[]>([])
const teacherSelectedId = ref('')
const classSelectedName = ref('')

const departmentData = computed(()=>{
  return userAuthStore.teacherData.departmentData
})

const subjectAssignments = computed(()=>{
  return userAuthStore.hodData.subjectAssignments
})

const studentsClasses = computed(()=>{
  return userAuthStore.hodData.studentClasses
})

const uploadSubjectAssignment = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'upload')
  formData.append('studentsClassName', classSelectedName.value);
  formData.append('subjects', JSON.stringify(subjectsSelected.value));
  formData.append('teacherId', teacherSelectedId.value);
  formData.append('year', userAuthStore.activeAcademicYearID.toString());
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    const response = await axiosInstance.post('hod/subject-assignment', formData)
    if (teacherSelectedId.value === userAuthStore.userData['staff_id']){
      await userAuthStore.getTeacherData()
    }
    else{
      userAuthStore.hodData.subjectAssignments.push(response.data)
    }
    
    subjectsSelected.value = []
    classSelectedName.value = ''
    teacherSelectedId.value = ''
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful!', 'green')
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const deleteSubjectAssignment = async (index: number, assignment_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', assignment_id.toString());
  formData.append('year', userAuthStore.activeAcademicYearID.toString());
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    await axiosInstance.post('hod/subject-assignment', formData)
    if (userAuthStore.hodData.subjectAssignments[index].teacher.staff_id === userAuthStore.userData['staff_id']){
      await userAuthStore.getTeacherData()
    }
    userAuthStore.hodData.subjectAssignments.splice(index, 1)
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const showOverlay = (element: string) => {
  classSelectedName.value = ''
  subjectsSelected.value = []
  teacherSelectedId.value = ''
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
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherDepartment`" :class="{ 'is-active-page': elementsStore.activePage === `TeacherDepartment` }">

    <!-- department subjects overlay -->
    <div id="TeacherDepartmentSubjectsOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('TeacherDepartmentSubjectsOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subjects, index) in departmentData?.subjects" :key=index>{{subjects}}</p>
        </div>
      </div>
    </div>

    <!-- all subject assignment overlay -->
    <div id="TeacherAllSubjectAssignmentOverlay" v-if="departmentData && departmentData.hod?.staff_id === userAuthStore.userData['staff_id']" class="overlay all-assignments">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('TeacherAllSubjectAssignmentOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <NoData v-if="subjectAssignments.length === 0"/>
        </div>
        <div class="overlay-card-content-conatiner">
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
                  {{ _assign.teacher.user }}
                  <v-list-item-subtitle>{{ _assign.teacher.staff_id }}</v-list-item-subtitle>
                </td>
                <td class="table-data">
                  {{ _assign.students_class }}
                </td>
                <td class="table-data">
                  <p v-for="(_subject, ind) in _assign.subjects" :key="ind">{{ _subject }}</p>
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
      </div>
    </div>

    <!-- subject assignment upload overlay -->
    <div id="TeacherSubjectAssignmentUploadOverlay" v-if="departmentData && departmentData.hod?.staff_id === userAuthStore.userData['staff_id']" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('TeacherSubjectAssignmentUploadOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <v-select clearable chips v-model="teacherSelectedId" class="select" label="TEACHER"
            :items="departmentData.teachers" item-title="user" item-value="staff_id" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the teacher who will teach the subject(s)">
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.staff_id"></v-list-item>
            </template>
          </v-select>
          <v-select class="select" :items="studentsClasses" label="CLASS" v-model="classSelectedName" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the class you want the teacher to teach"
          />
          <v-select class="select" :items="departmentData.subjects" label="SUBJECT(S)" v-model="subjectsSelected"
            multiple chips variant="solo-filled" density="comfortable" persistent-hint hint="Select the subject(s) you want the teaacher to teacher" 
            />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="uploadSubjectAssignment"
            :disabled="!(teacherSelectedId && subjectsSelected.length > 0 && classSelectedName)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header" v-if="departmentData">
      <h4 class="content-header-title">{{ departmentData.name }} DEPARTMENT</h4>
    </div>
    <div class="content-header" v-if="departmentData">
      <h4 class="mr-2">HOD: <v-chip v-if="!departmentData.hod">NONE</v-chip> <v-chip v-if="departmentData.hod">{{ departmentData.hod.user }} [ {{ departmentData.hod.staff_id }} ]</v-chip></h4>
    </div>
    <div class="content-header btn-container" v-if="departmentData">
      <v-btn class="ml-2" @click="showOverlay('TeacherDepartmentSubjectsOverlay')" color="blue" :size="elementsStore.btnSize1">
        DEPARTMENT SUBJECTS
      </v-btn>
      <v-btn class="ml-2" v-if="departmentData && departmentData.hod?.staff_id === userAuthStore.userData['staff_id']" @click="showOverlay('TeacherSubjectAssignmentUploadOverlay')" color="blue" :size="elementsStore.btnSize1">
        ASSIGN SUBJECT(S)
      </v-btn>
      <v-btn class="ml-2" v-if="departmentData && departmentData.hod?.staff_id === userAuthStore.userData['staff_id']" @click="showOverlay('TeacherAllSubjectAssignmentOverlay')" color="blue" :size="elementsStore.btnSize1">
        SUBJECT ASSIGNMENTS
      </v-btn>
    </div>
    <v-table fixed-header class="table" v-if="departmentData">
      <thead>
        <tr>
          <th class="table-head">TEACHERS</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(teacher, index) in departmentData.teachers" :key="index">
          <td class="table-data">
            {{ teacher.user }}
            <v-list-item-subtitle>{{ teacher.staff_id }}</v-list-item-subtitle>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>


.overlay-card-info-container {
  margin-top: 3em !important;
}
.overlay-card {
  max-width: 600px !important;
}
.btn-container{
  height: 15% !important;
}
.all-assignments .overlay-card{
  max-width: 700px !important;
}


</style>
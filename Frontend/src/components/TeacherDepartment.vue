<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { reactive, ref, watch } from 'vue'
import TheLoader from './TheLoader.vue';
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const maleTeachers = ref(0)
const femaleTeachers = ref(0)
const formErrorMessage = ref('')
const classSelected:any = ref(null)
const subjectsSelected = ref([])
const teacherSelected:any = ref(null)

interface Teacher {
  name: string;
  staff_id: string;
  subjects: string[];
  role: string;
  img: string;
  contact: string;
  gender: string;
  email: string;
}

const data = reactive({
  departmentName: userAuthStore.staffData.departmentData?.name || '',
  departmentTeachers: userAuthStore.staffData.departmentData?.teachers as Teacher[] || [],
  departmentSubjects: userAuthStore.staffData.departmentData?.subjects || [],
  studentsClasses: userAuthStore.staffData.hodData.subjectAssignmentData?.student_classes || [],
  subjectAssignments: userAuthStore.staffData.hodData.subjectAssignmentData?.subject_assignments || [],
})

watch(()=> userAuthStore.staffData.departmentData, (newValue:any)=>{
  if (newValue){
    data.departmentName = newValue.name
    data.departmentSubjects = newValue.subjects
    data.departmentTeachers = newValue.teachers
    if (newValue.teachers?.length > 0){
      newValue.teachers.forEach((item: any) => {
        if (item['gender'].toLowerCase() === 'male') {
          maleTeachers.value += 1
        }
        else if (item['gender'].toLowerCase() === 'female') {
          femaleTeachers.value += 1
        }
      })
    }
  }
})
watch(()=> userAuthStore.staffData.hodData.subjectAssignmentData, (newValue:any)=>{
  if (newValue){
    data.studentsClasses = newValue.student_classes
    data.subjectAssignments = newValue.subject_assignments
  }
})

userAuthStore.staffData.departmentData?.teachers.forEach((item: any) => {
  if (userAuthStore.staffData.departmentData.teachers?.length !== (femaleTeachers.value + maleTeachers.value)){
    if (item['gender'].toLowerCase() === 'male') {
      maleTeachers.value += 1
    }
    else if (item['gender'].toLowerCase() === 'female') {
      femaleTeachers.value += 1
    }
  }
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
    const response = await axiosInstance.post('hod/data', formData)
    userAuthStore.staffData.hodData.subjectAssignmentData?.subject_assignments.push(response.data)
    if (userAuthStore.userData['staff_id'] === teacherSelected.value){
      await userAuthStore.getstaffData()
      await userAuthStore.getTeacherStudentsAssessments()
      await userAuthStore.getTeacherStudentsExams()
      await userAuthStore.getTeacherStudentResults()
    }
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

const deleteSubjectAssignment = async (index:number, teacherId:string, stClass:string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('studentsClassName', stClass);
  formData.append('teacher', teacherId);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    await axiosInstance.post('hod/data', formData)
    userAuthStore.staffData.hodData.subjectAssignmentData?.subject_assignments.splice(index, 1)
    if (userAuthStore.userData['staff_id'] === teacherId){
      await userAuthStore.getstaffData()
      await userAuthStore.getTeacherStudentsAssessments()
      await userAuthStore.getTeacherStudentsExams()
      await userAuthStore.getTeacherStudentResults()
    }
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
  <div class="content-wrapper"
    v-show="elementsStore.activePage === 'TeacherDepartment'"
    :class="{ 'is-active-page': elementsStore.activePage === 'TeacherDepartment' }"
    >
    <!-- deparment subject overlay -->
    <div id="departmentSubjectOverlay" class="overlay subject-card">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('departmentSubjectOverlay')" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">
            SUBJECTS THIS DEPARTMENT TEACHES
            [{{ data.departmentSubjects?.length }}]
          </h3>
        </div>
        <div class="overlay-card-content-container">
          <p class="department-subject" v-for="(_subject, index) in data.departmentSubjects" :key="index">
            {{ _subject }}
          </p>
        </div>
      </div>
    </div>

    <!-- all subject assignment overlay -->
    <div id="departmentAllSubjectAssignmentOverlay" class="overlay all-assignments" v-if="userAuthStore.userData['staff_role'].toLowerCase() === 'hod'">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('departmentAllSubjectAssignmentOverlay')" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <div class="no-data" v-if="data.subjectAssignments?.length === 0">
            <p>NO DATA</p>
          </div>
          <v-table fixed-header class="table" v-if="data.subjectAssignments?.length > 0">
            <thead>
              <tr>
                <th class="table-head">TEACHER</th>
                <th class="table-head">CLASS</th>
                <th class="table-head">SUBJECT(S)</th>
                <th class="table-head">ACTION</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(_assign, index) in data.subjectAssignments" :key="index">
                <td class="table-data">
                  {{ _assign['teacher']['name'] }}
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
                    @click="elementsStore.ShowDeletionOverlay(() => deleteSubjectAssignment(index, _assign['teacher']['staff_id'], _assign['students_class']), 'Are you sure you want to delete this subject assignment?')"
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
    <div id="departmentSubjectAssignmentOverlay" class="overlay upload" v-if="userAuthStore.userData['staff_role'].toLowerCase() === 'hod'">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('departmentSubjectAssignmentOverlay')" color="red"
          size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-content-container">
          <v-select clearable chips v-model="teacherSelected" class="select" label="TEACHER"
            :items="data.departmentTeachers" item-title="name" item-value="staff_id" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select the teacher you want to assign the subject to">
            <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :subtitle="item.raw.staff_id"></v-list-item>
            </template>
          </v-select>
          <v-select class="select" :items="data.studentsClasses" label="CLASS" v-model="classSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the class you want the teaacher to teach" 
          />
          <v-select class="select" :items="data.departmentSubjects" label="SUBJECT" v-model="subjectsSelected" multiple chips variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject you want the teaacher to teacher" 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="uploadSubjectAssignment" :disabled="!teacherSelected || !subjectsSelected || !classSelected" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    <TheLoader v-if="!data.departmentName"/>
    <div class="content-header" v-if="data.departmentName">
      <span class="content-header-title"> {{ data.departmentName }} DEPARTMENT</span>
    </div>
    <div class="content-header stats" v-if="data.departmentName">
      <div class="content-header-text">
        TOTAL NUMBER OF TEACHERS:
        <span class="content-header-text-value">
          {{ data.departmentTeachers.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE TEACHERS:
        <span class="content-header-text-value">
          {{ maleTeachers }} [{{ ((maleTeachers / data.departmentTeachers.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE TEACHERS:
        <span class="content-header-text-value">
          {{ femaleTeachers }} [{{ ((femaleTeachers / data.departmentTeachers.length) * 100).toFixed(1) }}%]
        </span>
      </div>
    </div>
    <div class="content-header btn-container" v-if="data.departmentName">
      <v-btn @click="showOverlay('departmentSubjectOverlay')" class="ma-1" color="blue"
        :size="elementsStore.btnSize1">
        DEPARTMENT SUBJECTS
      </v-btn>
      <v-btn @click="showOverlay('departmentSubjectAssignmentOverlay')" class="ma-1" color="blue"
        :size="elementsStore.btnSize1" v-if="userAuthStore.userData['staff_role'].toLowerCase() === 'hod'">
        ASSIGN SUBJECTS
      </v-btn>
      <v-btn @click="showOverlay('departmentAllSubjectAssignmentOverlay')" class="ma-1" color="blue"
        :size="elementsStore.btnSize1" v-if="userAuthStore.userData['staff_role'].toLowerCase() === 'hod' && data.subjectAssignments?.length > 0">
        ALL SUBJECTS ASSIGNMENTS
      </v-btn>
    </div>
    <v-table fixed-header class="table" v-if="data.departmentName">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">ROLE</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">EMAIL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_staff, index) in data.departmentTeachers" :key="index">
          <td class="table-data">
            {{ _staff['name'] }}
            <v-list-item-subtitle>{{ _staff['staff_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <span v-if="_staff['role']?.toLocaleLowerCase() === 'teacher'">{{ _staff['role'] }}</span>
            <v-btn v-if="_staff['role']?.toLocaleLowerCase() === 'hod'" size="x-small" variant="flat" color="black">
              {{ _staff['role'] }}
            </v-btn>
          </td>
          <td class="table-data">
            {{ _staff['gender'] }}
          </td>
          <td class="table-data">
            {{ _staff['contact'] }}
          </td>
          <td class="table-data">
            <p v-for="(_subject, ind) in _staff['subjects']" :key="ind">{{ _subject }}</p>
          </td>
          <td class="table-data">
            <img class="profile-img" :src="_staff['img']">
          </td>
          <td class="table-data">
            {{ _staff['email'] }}
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
.stats, .btn-container {
  min-height: 15% !important;
}
.table {
  height: 65% !important;
}
.all-assignments .overlay-card{
  height: max-content !important;
}
.all-assignments .table{
  margin-top: 3em !important;
  max-height: 90% !important;
}
.all-assignments .overlay-card-content-container, .upload .overlay-card-content-container{
  margin-top: 3em !important;
}
.upload .overlay-card{
  max-height: 500px !important;
}
.department-subject {
  color: white;
  margin: .3em;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  padding: .5em;
  background-color: #333333;
  font-weight: bold;
  border-radius: .2em;
  font-size: .8rem;
}
.subject-card .overlay-card{
  height: max-content !important;
  max-height: 90% !important;
  width: 95% !important;
  max-width: 600px !important;
}
.subject-card .overlay-card .overlay-card-info-container{
  margin-top: 3em !important;
  min-height: max-content !important;
}
@media screen and (min-width: 400px) {
  .content-header-text {
    font-size: .75rem !important;
  }
}
@media screen and (min-width: 576px) {
  .content-header-title {
    font-size: .9rem !important;
  }

  .content-header-text {
    font-size: .8rem !important;
  }
}

@media screen and (min-width: 767px) {
  .content-header-title {
    font-size: 1rem !important;
  }

  .content-header-text {
    font-size: .85rem !important;
  }
}

@media screen and (min-width: 1000px) {
  .content-header-title {
    font-size: .9rem !important;
  }

  .content-header-text {
    font-size: .9rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .content-header-title {
    font-size: 1.1rem !important;
  }

  .content-header-text {
    font-size: 1rem !important;
  }
}


</style>
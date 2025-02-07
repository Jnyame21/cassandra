<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { ref } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { defineProps } from 'vue'
import { computed } from 'vue'
import NoData from '@/components/NoData.vue';
import { downloadFile } from '@/utils/util';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const studentName = ref('')
const studentId = ref('')
const previousScore: any = ref(null)
const studentScore: any = ref(null)
const uploadTypeSelected = ref('')
const fileToUpload: any = ref(null)
const selectedStudents = ref([])
const newTotalScore: any = ref(null)
const editType = ref('')

interface Props {
  className: string;
  subjectName: string;
}
const props = defineProps<Props>()
const className = props.className
const subjectName = props.subjectName

const uploadOptions = [
  { 'option': 'INPUT DATA HERE', 'value': 'noFile' },
  { 'option': 'USE AN EXCEL FILE', 'value': 'file' },
]

const examsData = computed(()=>{
  return userAuthStore.teacherData.studentsExams[className][subjectName]
})

const showErrorMessage = (message: string) => {
  formErrorMessage.value = message
  setTimeout(() => {
    formErrorMessage.value = ''
  }, 10000)
}

const fileChange = (event: any) => {
  const file = event.target.files[0]
  fileToUpload.value = file || null
}

// Generate an excel file
const generateFile = async () => {
  formErrorMessage.value = ''
  if (Object.keys(examsData.value.students_without_exams).length === 0) {
    showErrorMessage(`You have already uploaded all the ${subjectName} Exams scores for all students in this class`)
    return;
  }
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('studentsClassName', className)
  formData.append('subject', subjectName)
  formData.append('selectedStudents', JSON.stringify(Object.values(examsData.value.students_without_exams)))
  formData.append('type', 'getFile')
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm.toString())

  try {
    const response = await axiosInstance.post('teacher/exams', formData, {'responseType': 'blob'})
    downloadFile(response.headers, response.data, `${subjectName}-${className}-Exams`)
    elementsStore.HideLoadingOverlay();
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        }
        else {
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

const upload = async () => {
  formErrorMessage.value = ''
  const formData = new FormData()
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm.toString())
  formData.append('studentsClassName', className)
  formData.append('subject', subjectName)
  formData.append('totalScore', examsData.value.total_score?.toString())
  if (uploadTypeSelected.value === 'file') {
    if (Object.keys(examsData.value.students_without_exams).length === 0) {
      showErrorMessage(`You have already uploaded all the ${subjectName} Exams scores for all students in this class`)
      return;
    }
    formData.append('file', fileToUpload.value)
    formData.append('type', 'uploadWithFile')
  }
  else if (uploadTypeSelected.value === 'noFile') {
    if (studentScore.value < 0) {
      showErrorMessage("The students' exams score cannot be negative")
      return;
    } 
    else if (Number(studentScore.value) > Number(examsData.value.total_score)) {
      showErrorMessage("The students' score must not exceed the total score of the exams")
      return;
    }
    formData.append('selectedStudents', JSON.stringify(selectedStudents.value))
    formData.append('type', 'uploadWithoutFile')
    formData.append('score', studentScore.value)
  }
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('teacher/exams', formData)
    const students_data = response.data['data']
    students_data.forEach((st: any) => {
      const student_id = st['st_id']
      userAuthStore.teacherData.studentsExams[className][subjectName].students_with_exams[student_id] = st
      delete userAuthStore.teacherData.studentsExams[className][subjectName].students_without_exams[student_id]
    })
    selectedStudents.value = []
    studentScore.value = null
    fileToUpload.value = null
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay(response.data.message, 'green')
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        }
        else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else if (error.code === 'ERR_NETWORK' && navigator.onLine) {
        elementsStore.ShowOverlay('The excel file was modified. Please re-select the file before uploading.', 'red')
        fileToUpload.value = null
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const deleteExam = async () => {
  if (Object.keys(userAuthStore.teacherData.studentsResults[className][subjectName].student_results || {}).length > 0) {
    elementsStore.ShowOverlay(`You have already generated the students' ${subjectName} results for this class. You cannot delete the exams data`, 'red')
    return;
  }
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'deleteExam')
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    await axiosInstance.post('teacher/exams', formData)
    userAuthStore.teacherData.studentsExams[className][subjectName].total_score = 0
    userAuthStore.teacherData.studentsExams[className][subjectName].percentage = 0
    userAuthStore.teacherData.studentsExams[className][subjectName].students_with_exams = {}
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

const editExam = async () => {
  formErrorMessage.value = ''
  if (Object.keys(userAuthStore.teacherData.studentsResults[className][subjectName].student_results || {}).length > 0) {
    showErrorMessage(`Results for ${subjectName} in this class have already been generated. Please delete the existing results data and try again.`)
    return;
  }
  const formData = new FormData()
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  if (editType.value === 'studentScore') {
    if (studentScore.value < 0) {
      showErrorMessage("Exam scores cannot be negative")
      return;
    }
    else if (studentScore.value > Number(examsData.value.total_score)) {
      showErrorMessage("Exam scores must not exceed the total exams score")
      return;
    }
    formData.append('score', studentScore.value);
    formData.append('type', 'editExamScore');
    formData.append('studentId', studentId.value);
  }
  else if (editType.value === 'totalScore') {
    if (newTotalScore.value <= 0) {
      showErrorMessage('The total score of the exams cannot be negative or zero(0)')
      return;
    }
    for (let i = 0; i < Object.values(examsData.value.students_with_exams).length; i++) {
      const st_data = Object.values(examsData.value.students_with_exams)[i]
      if (Number(st_data.score) > Number(newTotalScore.value)) {
        showErrorMessage(`The score of student ${st_data.name} is greater than the new total score of the exams`)
        return;
      }
    }
    formData.append('totalScore', newTotalScore.value)
    formData.append('type', 'editTotalScore')
  }

  elementsStore.ShowLoadingOverlay()
  try {
    await axiosInstance.post('teacher/exams', formData)
    if (editType.value === 'studentScore') {
      userAuthStore.teacherData.studentsExams[className][subjectName].students_with_exams[studentId.value].score = Number(studentScore.value.toFixed(2))
    }
    else if (editType.value === 'totalScore') {
      userAuthStore.teacherData.studentsExams[className][subjectName].total_score = Number(newTotalScore.value.toFixed(2))
    }
    
    closeOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`)
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

const isUploadFormValid = computed(() => {
  if (uploadTypeSelected.value === 'file') {
    return !(fileToUpload.value)
  } 
  else if (uploadTypeSelected.value === 'noFile') {
    return !(selectedStudents.value.length > 0 && studentScore.value)
  }
  return true;
})

const closeOverlay = (element: string) => {
  studentScore.value = null
  formErrorMessage.value = ''
  studentId.value = ''
  studentName.value = ''
  selectedStudents.value = []
  previousScore.value = null
  uploadTypeSelected.value = ''
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string, type: string, stName: string = '', stId: any = null, prevScore: any = null) => {
  studentId.value = stId
  studentName.value = stName
  previousScore.value = prevScore
  editType.value = type
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherStudentsExams,${className},${subjectName}`" :class="{ 'is-active-page': elementsStore.activePage === `TeacherStudentsExams,${className},${subjectName}` }">
    
    <!-- upload overlay -->
    <div :id="`teacherStudentsExamsUploadOverlay${className}${subjectName}`" class="overlay upload-overlay"
      v-if="Number(examsData.total_score) > 0 && examsData.students_without_exams">
      <form class="overlay-card">
        <v-btn @click.prevent="closeOverlay(`teacherStudentsExamsUploadOverlay${className}${subjectName}`)" color="red"
          variant="flat" size="small" class="close-btn flex-all">X</v-btn>
        <h2 v-if="formErrorMessage" class="form-error-message" style="color: red">{{ formErrorMessage }}</h2>
        <div class="overlay-card-info-container">
          <h2 class="info-text">CLASS: <span class="info-text-value"> {{ className }}</span></h2>
          <h2 class="info-text">SUBJECT: <span class="info-text-value"> {{ subjectName }}</span></h2>
        </div>
        <div class="overlay-card-content-container">
          <v-select v-model="uploadTypeSelected" class="select" label="DATA" variant="solo-filled"
            :items="uploadOptions" item-title="option" item-value="value" density="comfortable" persistent-hint
            hint="Select whether you want to input the data here or use an excel file">
          </v-select>

          <!-- no file -->
          <v-select v-if="uploadTypeSelected === 'noFile'" multiple clearable v-model="selectedStudents" chips
            class="select" label="STUDENT(S)" variant="solo-filled" :items="Object.values(examsData.students_without_exams)"
            item-title="name" item-value="st_id" density="comfortable" persistent-hint
            hint="Select the student(s) you want to upload exam for">
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
            </template>
          </v-select>
          <v-text-field v-if="uploadTypeSelected === 'noFile'" type="number" v-model.number="studentScore"
            class="input-field" variant="solo-filled" density="comfortable" persistent-hint
            hint="Enter the student(s) score" label="STUDENT(S) SCORE" />

          <!-- file -->
          <div class="flex-all-c mt-5" v-if="uploadTypeSelected === 'file'">
            <v-btn @click.prevent="generateFile()" color="blue" variant="flat" class="submit-btn" size="small">GET
              FILE</v-btn>
            <p class="info-text">Click to get an excel file that contains the students data</p>
          </div>
          <hr class="mb-5 mt-5" v-if="uploadTypeSelected === 'file'">
          <v-file-input v-if="uploadTypeSelected === 'file'" @change="fileChange" class="select mt"
            label="Choose an excel file" clearable density="comfortable" variant="solo-filled"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
          </v-file-input>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click.prevent="upload" :disabled="isUploadFormValid" :ripple="false" variant="flat" type="submit"
            color="black" size="small" append-icon="mdi-checkbox-marked-circle">SUBMIT</v-btn>
        </div>
      </form>
    </div>

    <!-- edit student score overlay -->
    <div :id="`TeacherStudentsExamsEditOverlay${className}${subjectName}`" class="overlay edit-overlay"
      v-if="Number(examsData.total_score) > 0">
      <form class="overlay-card">
        <v-btn @click.prevent="closeOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`)"
          class="close-btn" size="small" variant="flat" color="red">X</v-btn>
        <h2 v-if="formErrorMessage" class="form-error-message" style="color: red">{{ formErrorMessage }}</h2>
        <div class="overlay-card-info-container">
          <h2 class="info-text">CLASS:<span class="info-text-value"> {{ className }}</span></h2>
          <h2 class="info-text">SUBJECT:<span class="info-text-value"> {{ subjectName }}</span></h2>
          <h2 class="info-text" v-if="editType === 'studentScore'">STUDENT:<span class="info-text-value"> {{ studentName
              }}
              [{{ studentId }}]</span></h2>
          <h2 class="info-text" v-if="editType === 'studentScore'">PREVIOUS SCORE:<span class="info-text-value">
              {{ previousScore }}</span></h2>
          <h2 class="info-text" v-if="editType === 'totalScore'">PREVIOUS TOTAL SCORE:<span class="info-text-value">{{
            examsData.total_score }}</span></h2>
        </div>
        <div class="overlay-card-content-container" v-if="editType === 'studentScore'">
          <v-text-field v-model.number="studentScore" type="number" class="input-field" density="comfortable"
            persistent-hint hint="Enter the student's new score" label="NEW SCORE" variant="solo-filled" />
        </div>
        <div class="overlay-card-content-container" v-if="editType === 'totalScore'">
          <v-text-field v-model.number="newTotalScore" type="number" class="input-field" density="comfortable"
            persistent-hint hint="Enter the new total score of the exams" label="NEW TOTAL SCORE"
            variant="solo-filled" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn :disabled="editType === 'studentScore' && !studentScore || editType === 'totalScore' && !newTotalScore"
            @click.prevent="editExam()" type="submit" color="black" variant="flat" size="small">SUBMIT</v-btn>
        </div>
      </form>
    </div>
    <div class="content-header" v-if="Number(examsData.total_score) > 0">
      <h4 class="content-header-title">{{ className }} {{ subjectName }} EXAMS</h4>
    </div>
    <div class="content-header" v-if="Number(examsData.total_score) > 0">
      <h4 class="content-header-text">
        TOTAL SCORE:
        <span class="content-header-text-value">{{ examsData.total_score }}</span>
        <v-icon class="ml-1"
          @click="showOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`, 'totalScore')"
          icon="mdi-pencil" variant="flat" color="blue" />
      </h4>
      <h4 class="content-header-text" v-if="Number(examsData.percentage) > 0">PERCENTAGE: <span
        class="content-header-text-value">{{ examsData.percentage }}%</span></h4>
    </div>
    <div class="content-header btn-container" v-if="Number(examsData.total_score) > 0">
      <v-btn v-if="examsData.students_without_exams"
        @click="showOverlay(`teacherStudentsExamsUploadOverlay${className}${subjectName}`, 'upload')"
        :size="elementsStore.btnSize1" color="blue" varaint="flat">
        ADD STUDENT(S) EXAMS
      </v-btn>
      <v-btn class="ml-5"
        @click="elementsStore.ShowDeletionOverlay(() => deleteExam(), `Are you sure you want to delete all the ${subjectName} exams data you have uploaded for this class?`)"
        append-icon="mdi-delete" variant="flat" :size="elementsStore.btnSize1" color="red">
        DELETE
      </v-btn>
    </div>
    <NoData v-if="Object.keys(examsData.students_with_exams).length === 0" />
    <v-table fixed-header class="table" v-if="Object.keys(examsData.students_with_exams).length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">SCORE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in Object.values(examsData.students_with_exams).sort((a, b)=> b.score - a.score)" :key="index">
          <td class="table-data">
            {{ st.name }}
            <v-list-item-subtitle>{{ st.st_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn
              @click="showOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`, 'studentScore', st.name, st.st_id, st.score)"
              size="small" variant="flat" color="black">
              {{ st.score }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.table {
  height: 70% !important;
}

.upload-overlay .no-students {
  height: fit-content !important;
}

.upload-overlay .overlay-card {
  max-width: 600px !important;
  max-height: 600px !important;
}

.upload-overlay .overlay-card-info-container {
  height: 15% !important;
}

.upload-overlay .overlay-card-content-container {
  height: 60% !important;
}

.upload-overlay .overlay-card-action-btn-container {
  height: 15% !important;
}

.edit-overlay .overlay-card {
  max-width: 600px !important;
  max-height: 500px !important;
}

.edit-overlay .overlay-card-info-container {
  height: 35% !important;
}

.edit-overlay .overlay-card-content-container {
  height: 30% !important;
}

.edit-overlay .overlay-card-action-btn-container {
  height: 15% !important;
}

.info-text,
.info-text-value {
  font-size: .75rem !important;
}

@media screen and (min-width: 400px) {
  .overlay-card {
    width: 95% !important;
  }
}



</style>
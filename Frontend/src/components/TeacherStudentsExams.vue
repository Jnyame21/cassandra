<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { ref } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { defineProps } from 'vue'
import { computed } from 'vue'

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
  classIndex: number;
  subjectName: string;
  subjectIndex: number;
  examsData: {
    'subject': string;
    'total_score': number;
    'percentage': number;
    'students_with_exams': {
      'name': string;
      'st_id': any;
      'score': any;
    }[];
    'students_without_exams': {
      'name': string;
      'st_id': any;
    }[];
  }
}
const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const subjectName = props.subjectName
const subjectIndex = props.subjectIndex || 0
const examsData = props.examsData

const uploadOptions = [
  { 'option': 'INPUT DATA HERE', 'value': 'noFile' },
  { 'option': 'USE AN EXCEL FILE', 'value': 'file' },
]

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
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('studentsClassName', className)
  formData.append('subject', subjectName)
  formData.append('selectedStudents', JSON.stringify(examsData['students_without_exams']))
  formData.append('type', 'getFile')
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm)

  try {
    const response = await axiosInstance.post('teacher/exams', formData)
    const link = document.createElement('a');
    link.href = response.data.file_path;
    link.setAttribute('download', response.data.filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    elementsStore.HideLoadingOverlay();
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        }
        else {
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

const upload = async () => {
  formErrorMessage.value = ''
  const formData = new FormData()
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm)
  formData.append('studentsClassName', className)
  formData.append('subject', subjectName)
  if (uploadTypeSelected.value === 'file') {
    formData.append('file', fileToUpload.value)
    formData.append('type', 'uploadWithFile')
  }
  else if (uploadTypeSelected.value === 'noFile') {
    if (studentScore.value < 0) {
      showErrorMessage("The students' exams score cannot be negative")
      return;
    } else if (studentScore.value > 100) {
      showErrorMessage("The students' score must not exceed 100")
      return;
    }
    formData.append('selectedStudents', JSON.stringify(selectedStudents.value))
    formData.append('type', 'uploadWithoutFile')
    formData.append('score', studentScore.value)
  }
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('teacher/exams', formData)
    if (uploadTypeSelected.value === 'file') {
      const students_data = response.data['data']
      students_data.forEach((st: any) => {
        userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'].push(st)
        const _student = userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_without_exams'].find((item: any) => item['st_id'] === st['st_id'])
        if (_student) {
          const _studentIndex = userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_without_exams'].indexOf(_student)
          userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_without_exams'].splice(_studentIndex, 1)
        }
      })
    }
    else if (uploadTypeSelected.value === 'noFile') {
      selectedStudents.value.forEach((st_id: any) => {
        const _student = userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_without_exams'].find((item: any) => item['st_id'] === st_id)
        if (_student) {
          const _studentIndex = userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_without_exams'].indexOf(_student)
          userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'].push({ 'name': _student['name'], 'st_id': _student['st_id'], 'score': Number(studentScore.value.toFixed(2)) })
          userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_without_exams'].splice(_studentIndex, 1)
        }
      })
    }
    userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'].sort((a: any, b: any) => b.score - a.score)
    selectedStudents.value = []
    studentScore.value = null
    fileToUpload.value = null
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay(response.data.message, 'green', null, null)
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        }
        else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else if (error.code === 'ERR_NETWORK' && navigator.onLine) {
        elementsStore.ShowOverlay('The excel file was modified. Please re-select the file before uploading.', 'red', null, null)
        fileToUpload.value = null
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const deleteExam = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'deleteExam')
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    await axiosInstance.post('teacher/exams', formData)
    userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['total_score'] = 0
    userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['percentage'] = 0
    userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'] = []
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

const editExam = async () => {
  formErrorMessage.value = ''
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
    else if (studentScore.value > Number(examsData['total_score'])) {
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
    for (let i = 0; i < examsData['students_with_exams'].length; i++) {
      if (Number(examsData['students_with_exams'][i]['score']) > Number(newTotalScore.value)) {
        showErrorMessage(`The score of student ${examsData['students_with_exams'][i]['name']} is greater than the new total score of the exams`)
        return;
      }
    }
    formData.append('totalScore', newTotalScore.value)
    formData.append('type', 'editTotalScore')
  }

  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('teacher/exams', formData)
    const data = response.data
    if (editType.value === 'studentScore') {
      const _student = userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'].find((item: any) => item['st_id'] === studentId.value)
      if (_student) {
        const _studentIndex = userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'].indexOf(_student)
        userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'][_studentIndex]['score'] = Number(studentScore.value.toFixed(2))
        userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['students_with_exams'].sort((a: any, b: any) => b.score - a.score)
      }
      const resultStudent = userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'].find((item: any) => item['student']['st_id'] === studentId.value)
      if (resultStudent) {
        const resultStudentIndex = userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'].indexOf(resultStudent)
        userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'][resultStudentIndex]['result'] = data['new_result']
        userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'][resultStudentIndex]['remark'] = data['new_remark']
        userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'][resultStudentIndex]['grade'] = data['new_grade']
        userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'][resultStudentIndex]['exam_score'] = data['new_exam_score']
        userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'].sort((a: any, b: any) => b.result - a.result)
      }
    }
    else if (editType.value === 'totalScore') {
      userAuthStore.staffData.studentsExams[classIndex]['exams'][subjectIndex]['total_score'] = Number(newTotalScore.value.toFixed(2))
      if (userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results']?.length > 0) {
        userAuthStore.staffData.studentsResults[classIndex]['results'][subjectIndex]['student_results'] = data
      }
    }
    closeOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`)
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

const isUploadFormValid = computed(() => {
  if (uploadTypeSelected.value === 'file') {
    return !(fileToUpload.value)
  } else if (uploadTypeSelected.value === 'noFile') {
    return !(selectedStudents.value.length > 0 && studentScore.value)
  }
  return false
})

const closeOverlay = (element: string) => {
  studentScore.value = null
  formErrorMessage.value = ''
  studentId.value = ''
  studentName.value = ''
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
  <div class="content-wrapper"
    v-show="elementsStore.activePage === `TeacherStudentsExams,${className},${subjectName},${subjectIndex}`"
    :class="{ 'is-active-page': elementsStore.activePage === `TeacherStudentsExams,${className},${subjectName},${subjectIndex}` }">
    <!-- upload overlay -->
    <div :id="`teacherStudentsExamsUploadOverlay${className}${subjectName}`" class="overlay upload-overlay"
      v-if="Number(examsData['total_score']) > 0 && examsData['students_without_exams'].length > 0">
      <form class="overlay-card">
        <v-btn @click.prevent="closeOverlay(`teacherStudentsExamsUploadOverlay${className}${subjectName}`)" color="red"
          variant="flat" size="small" class="close-btn flex-all">X</v-btn>
        <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{ formErrorMessage }}</h2>
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
            class="select" label="STUDENT(S)" variant="solo-filled" :items="examsData['students_without_exams']"
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
      v-if="Number(examsData['total_score']) > 0">
      <form class="overlay-card">
        <v-btn @click.prevent="closeOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`)"
          class="close-btn" size="small" variant="flat" color="red">X</v-btn>
        <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{ formErrorMessage }}</h2>
        <div class="overlay-card-info-container">
          <h2 class="info-text">CLASS:<span class="info-text-value"> {{ className }}</span></h2>
          <h2 class="info-text">SUBJECT:<span class="info-text-value"> {{ subjectName }}</span></h2>
          <h2 class="info-text" v-if="editType === 'studentScore'">STUDENT:<span class="info-text-value"> {{ studentName
              }}
              [{{ studentId }}]</span></h2>
          <h2 class="info-text" v-if="editType === 'studentScore'">PREVIOUS SCORE:<span class="info-text-value">
              {{ previousScore }}</span></h2>
          <h2 class="info-text" v-if="editType === 'totalScore'">PREVIOUS TOTAL SCORE:<span
              class="info-text-value">{{ examsData['total_score'] }}</span></h2>
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
    <div class="content-header" v-if="Number(examsData['total_score']) > 0">
      <h4 class="content-header-title">{{ className }} {{ subjectName }} EXAMS</h4>
    </div>
    <div class="content-header" v-if="Number(examsData['total_score']) > 0">
      <h4 class="content-header-text">
        TOTAL SCORE:
        <span class="content-header-text-value">{{ examsData['total_score'] }}</span>
        <v-icon class="ml-1"
          @click="showOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`, 'totalScore')"
          icon="mdi-pencil" variant="flat" color="blue" />
      </h4>
      <h4 class="content-header-text" v-if="Number(examsData['percentage']) > 0">PERCENTAGE: <span
          class="content-header-text-value">{{ examsData['percentage'] }}</span></h4>
    </div>
    <div class="content-header btn-container" v-if="Number(examsData['total_score']) > 0">
      <v-btn v-if="examsData['students_without_exams'].length > 0"
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
    <h4 class="no-data" v-if="examsData['students_with_exams']?.length === 0">
      <p>NO DATA</p>
    </h4>
    <v-table fixed-header class="table" v-if="examsData['students_with_exams']?.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">SCORE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in examsData['students_with_exams']" :key="index">
          <td class="table-data">
            {{ st['name'] }}
            <v-list-item-subtitle>{{ st['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn
              @click="showOverlay(`TeacherStudentsExamsEditOverlay${className}${subjectName}`, 'studentScore', st['name'], st['st_id'], st['score'])"
              size="small" variant="flat" color="black">
              {{ st['score'] }}
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
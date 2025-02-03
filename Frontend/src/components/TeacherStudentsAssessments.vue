<script setup lang="ts">
import { AxiosError } from 'axios';
import axiosInstance from '../utils/axiosInstance';
import { ref } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { defineProps } from 'vue'
import { computed } from 'vue'
import { downloadFile } from '@/utils/util';


const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const studentName = ref('')
const studentId = ref('')
const previousScore: any = ref(null)
const previousComment = ref('')
const newScore: any = ref(null)
const newTitle: any = ref(null)
const newDescription: any = ref(null)
const newTotalScore: any = ref(null)
const academicYearStartDate = new Date(userAuthStore.userData['academic_year']['start_date'])
const academicYearEndDate = new Date(userAuthStore.userData['academic_year']['end_date'])
const newDate: any = ref(null)
const newComment = ref('')
const editType = ref('')
const fileToUpload: any = ref(null)
const uploadTypeSelected: any = ref(null)
const studentScore: any = ref(null)
const selectedStudents: any = ref([])
const comment = ref('')

interface Props {
  className: string;
  subjectName: string;
  assessmentTitle: string;
}
const props = defineProps<Props>()
const className = props.className
const subjectName = props.subjectName
const assessmentTitle = props.assessmentTitle

const assessmentData = computed(()=>{
  return userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle]
})

const clearMessage = () => {
  setTimeout(() => {
    formErrorMessage.value = ''
  }, 8000)
}

const showErrorMessage = (message: string) => {
  formErrorMessage.value = message
  clearMessage()
}

const uploadOptions = [
  { 'option': 'INPUT DATA HERE', 'value': 'noFile' },
  { 'option': 'USE AN EXCEL FILE', 'value': 'file' },
]

const fileChange = (event: any) => {
  const file = event.target.files[0]
  fileToUpload.value = file || null
}

// Generate an excel file
const generateFile = async () => {
  formErrorMessage.value = ''
  if (Object.keys(assessmentData.value.students_without_assessment).length === 0) {
    showErrorMessage(`You have already uploaded all the students assessment for the assessment titled [ ${assessmentTitle} ] under ${subjectName}`)
    return;
  }
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('studentsClassName', className)
  formData.append('subject', subjectName)
  formData.append('selectedStudents', JSON.stringify(Object.values(assessmentData.value.students_without_assessment)))
  formData.append('type', 'getFile')
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm.toString())
  formData.append('title', assessmentData.value.title)
  formData.append('totalScore', assessmentData.value.total_score.toString())

  try {
    const response = await axiosInstance.post('teacher/assessments', formData, {'responseType': 'blob'})
    downloadFile(response.headers, response.data, `${assessmentData.value.title}`)
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
  formData.append('term', userAuthStore.activeTerm.toString())
  formData.append('studentsClassName', className)
  formData.append('subject', subjectName)
  formData.append('title', assessmentData.value.title)
  formData.append('percentage', assessmentData.value.percentage.toString())
  formData.append('totalScore', assessmentData.value.total_score.toString())
  formData.append('description', assessmentData.value.description)
  formData.append('date', assessmentData.value.assessment_date)
  if (uploadTypeSelected.value === 'file') {
    if (Object.keys(assessmentData.value.students_without_assessment).length === 0) {
      showErrorMessage(`You have already uploaded all the students assessment for the assessment titled [ ${assessmentTitle} ] under ${subjectName}`)
      return;
    }
    formData.append('file', fileToUpload.value)
    formData.append('type', 'uploadWithFile')
  }
  else if (uploadTypeSelected.value === 'noFile') {
    if (comment.value.length > 100) {
      showErrorMessage("The comment must not exceed 100 characters")
      return;
    } else if (studentScore.value < 0) {
      showErrorMessage("The students' score cannot be negative")
      return;
    } else if (studentScore.value > assessmentData.value.total_score) {
      showErrorMessage("The students' score cannot be greater than the total assessment score")
      return;
    }
    formData.append('selectedStudents', JSON.stringify(selectedStudents.value))
    formData.append('type', 'uploadWithoutFile')
    formData.append('score', studentScore.value)
    formData.append('comment', comment.value)
  }
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('teacher/assessments', formData)
    const students_data = response.data['data']
    students_data.forEach((st: any) => {
      const student_id:string = st['st_id']
      userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].students_with_assessment[student_id] = st
      delete userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].students_without_assessment[student_id]
    })
    
    selectedStudents.value = []
    studentScore.value = null
    comment.value = ''
    fileToUpload.value = null
    if (uploadTypeSelected.value === 'file'){
      closeOverlay(`teacherStudentsAssessmentUploadOverlay,${className},${subjectName},${assessmentTitle}`)
    }
    else{
      elementsStore.ShowOverlay('Assessment data uploaded successfully!', 'green', null, null)
    }
    elementsStore.HideLoadingOverlay()
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

const editAssessment = async () => {
  formErrorMessage.value = ''
  const formData = new FormData()
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());
  formData.append('type', 'editAssessment');
  formData.append('title', assessmentData.value.title);

  if (editType.value === 'score') {
    if (Object.keys(userAuthStore.teacherData.studentsResults[className][subjectName].student_results || {}).length > 0) {
      showErrorMessage(`Results for ${subjectName} in this class have already been generated. Please delete the existing results data and try again.`)
      return;
    }
    if (assessmentData.value.total_score >= newScore.value && newScore.value >= 0) {
      formData.append('newScore', newScore.value);
      formData.append('editType', 'score');
      formData.append('studentId', studentId.value);
    }
    else {
      if (newScore.value < 0) {
        formErrorMessage.value = "The student's score cannot be negative"
      } 
      else if (newScore.value > Number(assessmentData.value.total_score)) {
        formErrorMessage.value = "The student's score cannot be greater than the total assessment score"
      } 
      else if (newScore.value === previousScore.value) {
        formErrorMessage.value = "The new student's score must be different from the old students's score"
      }
      clearMessage()
      return;
    }
  }
  else if (editType.value === 'comment') {
    if (newComment.value.length > 100) {
      showErrorMessage("The maximum characters must not exceed 100")
      return;
    } else if (newComment.value === previousComment.value) {
      showErrorMessage("The new comment must be different from the old comment")
      return;
    }
    formData.append('newComment', newComment.value);
    formData.append('editType', 'comment');
    formData.append('studentId', studentId.value);
  }
  else if (editType.value === 'title') {
    if (newTitle.value.length > 50) {
      showErrorMessage("The maximum characters for the title must not exceed 50")
      return;
    } else if (newTitle.value === assessmentData.value.title) {
      showErrorMessage("The new title must be different from the old assessment title")
      return;
    }
    formData.append('newTitle', newTitle.value);
    formData.append('editType', 'title');
  }
  else if (editType.value === 'description') {
    if (newDescription.value === assessmentData.value.description) {
      showErrorMessage("The new description must be different from the old assessment description")
      return;
    } else if (newDescription.value.length > 100) {
      showErrorMessage("The maximum characters for the description must not exceed 100")
      return;
    }
    formData.append('newDescription', newDescription.value);
    formData.append('editType', 'description');
  }
  else if (editType.value === 'totalScore') {
    if (Object.keys(userAuthStore.teacherData.studentsResults[className][subjectName].student_results || {}).length > 0) {
      showErrorMessage(`Results for ${subjectName} in this class have already been generated. Please delete the existing results data and try again.`)
      return;
    }
    if (newTotalScore.value <= 0) {
      showErrorMessage('The total assessment score cannot be negative or zero(0)')
      return;
    }
    else if (newTotalScore.value === Number(assessmentData.value.total_score)) {
      showErrorMessage("The new total score must be different from the old assessment total score")
      return;
    }
    else if (newTotalScore.value < Math.max(...Object.values(assessmentData.value.students_with_assessment).map(st=> st.score))) {
      showErrorMessage(`The total assessment score cannot be less than the maximum score of a student. Ensure each student's score is less than ${newTotalScore.value}`)
      return;
    }
    formData.append('newTotalScore', newTotalScore.value);
    formData.append('editType', 'totalScore');
  }
  else if (editType.value === 'date') {
    if (newDate.value === assessmentData.value.assessment_date) {
      showErrorMessage('The new date must be different from the old assessment date')
      return;
    }
    else if (new Date(newDate.value) < academicYearStartDate || new Date(newDate.value) > academicYearEndDate) {
      showErrorMessage(`The assessment date must be between the academic year start date and end date, which are ${academicYearStartDate.toDateString()} and ${academicYearEndDate.toDateString()} respectively.`)
      return;
    }
    formData.append('newDate', newDate.value);
    formData.append('editType', 'date');
  }

  elementsStore.ShowLoadingOverlay()
  try {
    await axiosInstance.post('teacher/assessments', formData)
    if (editType.value === 'score') {
      userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].students_with_assessment[studentId.value].score = Number(newScore.value.toFixed(2))
    }
    else if (editType.value === 'comment') {
      userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].students_with_assessment[studentId.value].comment = newComment.value
    }
    else {
      if (editType.value === 'title') {
        const oldTitle = userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].title
        userAuthStore.teacherData.studentsAssessments[className][subjectName][newTitle.value] = userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle]
        userAuthStore.teacherData.studentsAssessments[className][subjectName][newTitle.value].title = newTitle.value
        delete userAuthStore.teacherData.studentsAssessments[className][subjectName][oldTitle]
        elementsStore.activePage = `TeacherStudentsAssessments,${className},${subjectName},${newTitle.value}`
      }
      else if (editType.value === 'description') {
        userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].description = newDescription.value
      }
      else if (editType.value === 'totalScore') {
        userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].total_score = Number(newTotalScore.value.toFixed(2))
      }
      else if (editType.value === 'date') {
        userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle].assessment_date = newDate.value
      }
    }
    closeOverlay(`TeacherStudentsAssessmentEditOverlay,${className},${subjectName},${assessmentTitle}`)
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

const deleteAssessment = async () => {
  if (Object.keys(userAuthStore.teacherData.studentsResults[className][subjectName].student_results || {}).length > 0) {
    elementsStore.ShowOverlay(`Results for ${subjectName} in this class have already been generated. Please delete the existing results data and try again.`, 'red', null, null)
    return;
  }
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());
  formData.append('type', 'deleteAssessment');
  formData.append('title', assessmentData.value.title);

  try {
    await axiosInstance.post('teacher/assessments', formData)
    delete userAuthStore.teacherData.studentsAssessments[className][subjectName][assessmentTitle]
    elementsStore.activePage = `TeacherCoursework,${className}`
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
    return !(studentScore.value && selectedStudents.value.length > 0)
  } else {
    return true;
  }
})

const isEditFormValid = computed(() => {
  if (editType.value === 'score') {
    return !(newScore.value)
  } else if (editType.value === 'title') {
    return !(newTitle.value)
  } else if (editType.value === 'totalScore') {
    return !(newTotalScore.value)
  } else if (editType.value === 'date') {
    return !(newDate.value)
  } else if (editType.value === 'comment') {
    return false
  } else if (editType.value === 'description') {
    return false
  } else {
    return true;
  }
})

const closeOverlay = (element: string) => {
  newScore.value = null
  newComment.value = ''
  previousScore.value = null
  previousComment.value = ''
  formErrorMessage.value = ''
  newTitle.value = ''
  newDescription.value = ''
  newTotalScore.value = ''
  newDate.value = ''
  editType.value = ''
  studentId.value = ''
  studentName.value = ''
  selectedStudents.value = []
  comment.value = ''
  uploadTypeSelected.value = null
  studentScore.value = null
  fileToUpload.value = null
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

const showEditForm = (type: string, stName: string = '', stId: string = '') => {
  editType.value = type
  studentId.value = stId
  studentName.value = stName
  const overlay = document.getElementById(`TeacherStudentsAssessmentEditOverlay,${className},${subjectName},${assessmentTitle}`)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherStudentsAssessments,${className},${subjectName},${assessmentTitle}`" :class="{ 'is-active-page': elementsStore.activePage === `TeacherStudentsAssessments,${className},${subjectName},${assessmentTitle}` }">
    
    <!-- upload overlay -->
    <div :id="`teacherStudentsAssessmentUploadOverlay,${className},${subjectName},${assessmentTitle}`"
      class="overlay upload-overlay" v-if="assessmentData.students_without_assessment">
      <form class="overlay-card upload-card">
        <v-btn @click.prevent="closeOverlay(`teacherStudentsAssessmentUploadOverlay,${className},${subjectName},${assessmentTitle}`)"
          color="red" variant="flat" size="small" class="close-btn flex-all">X</v-btn>
        <h2 v-if="formErrorMessage" class="form-error-message" style="color: red">{{ formErrorMessage }}</h2>
        <div class="overlay-card-info-container">
          <h2 class="info-text">ASSESSMENT: <span class="info-text-value"> {{ assessmentData.title }}</span></h2>
          <h2 class="info-text">TOTAL SCORE: <span class="info-text-value"> {{ assessmentData.total_score }}</span></h2>
        </div>
        <div class="overlay-card-content-container">
          <v-select v-model="uploadTypeSelected" class="select" label="DATA" variant="solo-filled"
            :items="uploadOptions" item-title="option" item-value="value" density="comfortable" persistent-hint
            hint="Select whether you want to input the data here or use an excel file">
          </v-select>

          <!-- no file -->
          <v-select v-show="uploadTypeSelected === 'noFile'" multiple clearable v-model="selectedStudents" chips
            class="select" label="STUDENT(S)" variant="solo-filled" :items="Object.values(assessmentData.students_without_assessment)"
            item-title="name" item-value="st_id" density="comfortable" persistent-hint
            hint="Select the student(s) you want to upload assessment for">
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
            </template>
          </v-select>
          <v-text-field v-show="uploadTypeSelected === 'noFile'" type="number" v-model.number="studentScore"
            class="input-field" variant="solo-filled" density="comfortable" persistent-hint
            hint="Enter the student(s) score" label="STUDENT(S) SCORE" />
          <v-text-field v-show="uploadTypeSelected === 'noFile'" v-model="comment" class="input-field"
            density="comfortable" variant="solo-filled" persistent-hint hint="Comment on the student(s) score if any"
            label="COMMENT" />

          <!-- file -->
          <div class="flex-all-c mt-5" v-show="uploadTypeSelected === 'file'">
            <v-btn @click.prevent="generateFile()" color="blue" variant="flat" class="submit-btn" size="small">GET
              FILE</v-btn>
            <p class="info-text">Click to get an excel file that contains the students data</p>
          </div>
          <hr class="mb-5 mt-5" v-show="uploadTypeSelected === 'file'">
          <v-file-input v-show="uploadTypeSelected === 'file'" @change="fileChange" class="select mt"
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

    <!-- edit assessment overlay -->
    <div :id="`TeacherStudentsAssessmentEditOverlay,${className},${subjectName},${assessmentTitle}`"
      class="overlay edit-overlay">
      <form style="position: relative" class="overlay-card">
        <v-btn
          @click.prevent="closeOverlay(`TeacherStudentsAssessmentEditOverlay,${className},${subjectName},${assessmentTitle}`)" class="close-btn" size="small" variant="flat" color="red">
          X
        </v-btn>
        <h2 v-if="formErrorMessage" class="form-error-message" style="color: red">{{ formErrorMessage }}</h2>
        <div class="overlay-card-info-container">
          <h2 class="info-text" v-if="editType === 'score' || editType === 'comment'">
            STUDENT: <span class="info-text-value"> {{ studentName }} [{{ studentId }}]</span>
          </h2>
        </div>
        <div class="overlay-card-content-container">
          <v-text-field v-if="editType === 'score'" v-model.number="newScore" type="number" class="input-field"
            persistent-hint hint="Enter the student's new score" label="NEW SCORE" variant="solo-filled" />
          <v-text-field v-if="editType === 'totalScore'" v-model.number="newTotalScore" type="number"
            class="input-field" persistent-hint hint="Enter a new total score" label="NEW TOTAL SCORE"
            variant="solo-filled" />
          <v-text-field v-if="editType === 'comment'" v-model="newComment" class="input-field" persistent-hint
            hint="Enter a new comment(Max characters, 100)" label="NEW COMMENT" variant="solo-filled" />
          <v-text-field v-if="editType === 'title'" v-model="newTitle" class="input-field" persistent-hint
            hint="Enter a new title(Max characters, 50)" label="NEW TITLE" variant="solo-filled" />
          <v-text-field v-if="editType === 'description'" v-model="newDescription" class="input-field" persistent-hint
            hint="Enter a new description(Max characters, 100)" label="NEW DESCRIPTION" variant="solo-filled" />
          <v-text-field v-if="editType === 'date'" v-model="newDate" class="input-field" type="date" persistent-hint
            hint="Select a new date" label="NEW DATE" variant="solo-filled" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn :disabled="isEditFormValid" @click.prevent="editAssessment" type="submit" color="black" size="small" variant="flat" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </form>
    </div>

    <div class="content-header">
      <div class="content-header-text">
        TITLE: <span class="content-header-text-value">{{ assessmentTitle }}</span>
        <v-icon class="ml-1" @click="showEditForm('title')" color="blue" icon="mdi-pencil" />
      </div>
      <div class="content-header-text">
        DESCRIPTION: <span class="content-header-text-value">{{ assessmentData.description }}</span>
        <v-icon class="ml-1" @click="showEditForm('description')" color="blue" icon="mdi-pencil" />
      </div>
      <div class="content-header-text">
        TOTAL SCORE: <span class="content-header-text-value">{{ assessmentData.total_score }}</span>
        <v-icon class="ml-1" @click="showEditForm('totalScore')" color="blue" icon="mdi-pencil" />
      </div>
      <div class="content-header-text" v-if="assessmentData.percentage !== 0">
        PERCENTAGE: <span class="content-header-text-value">{{ assessmentData.percentage }}%</span>
      </div>
      <div class="content-header-text">
        DATE: <span class="content-header-text-value">{{ assessmentData.assessment_date }}</span>
        <v-icon class="ml-1" @click="showEditForm('date')" color="blue" icon="mdi-pencil" />
      </div>
    </div>
    <div class="content-header btn-container">
      <v-btn v-if="assessmentData.students_without_assessment"
        @click="showOverlay(`teacherStudentsAssessmentUploadOverlay,${className},${subjectName},${assessmentTitle}`)"
        :size="elementsStore.btnSize1" color="blue" varaint="flat">
        ADD STUDENT(S) ASSESSMENT
      </v-btn>
      <v-btn class="ml-5"
        @click="elementsStore.ShowDeletionOverlay(() => deleteAssessment(), `Are you sure you want to delete the assessment [${assessmentTitle} ] and all it's data you have uploaded? You will be redirected to the ${className} class when the process is complete`)"
        :size="elementsStore.btnSize1" append-icon="mdi-delete" color="red" varaint="flat">
        DELETE
      </v-btn>
    </div>
    <h4 class="no-data" v-if="Object.keys(assessmentData.students_with_assessment || {}).length === 0">
      <p>NO DATA</p>
    </h4>
    <v-table fixed-header class="table" v-if="Object.keys(assessmentData.students_with_assessment || {}).length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">SCORE</th>
          <th class="table-head">COMMENT</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(st, index) in Object.values(assessmentData.students_with_assessment).sort((a, b)=> b.score - a.score)" :key="index">
          <td class="table-data">
            {{ st.name }}
            <v-list-item-subtitle>{{ st.st_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn @click="showEditForm('score', st.name, st.st_id)" size="small" color="black" variant="flat">{{ st.score }}</v-btn>
          </td>
          <td class="table-data st-comment">
            {{ st.comment }}
            <v-btn @click="showEditForm('comment', st.name, st.st_id)" size="x-small" variant="flat" icon="mdi-pencil"></v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 25% !important;
}

.btn-container {
  min-height: 10% !important;
}

.table {
  height: 65% !important;
}

.overlay-card-info-container{
  margin-top: 3em !important;
}
.upload-overlay .no-students {
  height: fit-content !important;
}

.upload-overlay .upload-card {
  max-width: 600px !important;
  height: 90% !important;
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
  height: 90% !important;
  max-width: 600px !important;
  max-height: 450px !important;
}

.edit-overlay .overlay-card-info-container {
  height: 25% !important;
}

.edit-overlay .overlay-card-content-container {
  height: 30% !important;
}

.edit-overlay .overlay-card-action-btn-container {
  height: 20% !important;
}
.st-comment {
  text-transform: none !important;
}
.info-text,
.info-text-value {
  font-size: .75rem !important;
}

@media screen and (min-width: 400px) {
  .overlay-card {
    width: 95% !important;
  }

  .info-text,
  .info-text-value {
    font-size: .8rem !important;
  }
}

@media screen and (min-width: 576px) {
  .content-header-text {
    font-size: .75rem !important;
  }

  .info-text,
  .info-text-value {
    font-size: .85rem !important;
  }
}

@media screen and (min-width: 767px) {
  .content-header-text {
    font-size: .8rem !important;
  }

  .info-text,
  .info-text-value {
    font-size: .9rem !important;
  }
}

@media screen and (min-width: 992px) {}

@media screen and (min-width: 1200px) {
  .content-header-text {
    font-size: .9rem !important;
  }

  .info-text,
  .info-text-value {
    font-size: 1rem !important;
  }
}


</style>
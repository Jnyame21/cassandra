<script setup lang="ts">
import { AxiosError } from 'axios';
import { ref, computed, watch } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import type { states } from '@/stores/userAuthStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const subjectSelected = ref('')
const assessmentTitle = ref('')
const assessmentTotalScore: any = ref(null)
const assessmentDescription = ref('')
const assessmentDate = ref('')
const academicYearStartDate = new Date(userAuthStore.userData['academic_year']['start_date'])
const academicYearEndDate = new Date(userAuthStore.userData['academic_year']['end_date'])
const formErrorMessage = ref('')
const examsPercentage = ref<number>(0)
const resultGenerationErrorType = ref('')
const loading = ref(false)
const typeSelected = ref('')
const examsTotalScore: any = ref(null)
const studentAssessmentsData = ref<states['teacherData']['studentsAssessments'][string]>({})

interface Props {
  className: string;
}
const props = defineProps<Props>()
const className = props.className


const showErrorMessage = (message: string) => {
  formErrorMessage.value = message
  loading.value = false
  setTimeout(() => {
    formErrorMessage.value = ''
  }, 10000)
}

const typeOptions = [
  { 'label': 'EXAM', 'value': 'exams' },
  { 'label': 'ASSESSMENT', 'value': 'assessments' },
]

const students = computed(()=>{
  return userAuthStore.teacherData.courseWork[className]?.students_class.students || []
})

const subjects = computed(()=>{
  return userAuthStore.teacherData.courseWork[className]?.subjects || []
})

const maleStudents = computed(()=>{
  return students.value.filter((item:any)=> item['gender'].toLowerCase() === 'male').length
})

const femaleStudents = computed(()=>{
  return students.value.filter((item:any)=> item['gender'].toLowerCase() === 'female').length
})

const allAssessments = computed(()=>{
  return userAuthStore.teacherData.studentsAssessments[className] || {}
})

watch(()=>userAuthStore.teacherData.studentsAssessments[className], (newAssessment) => {
  studentAssessmentsData.value = newAssessment || {}
}, {deep: 2, immediate: true})

const createAssessmentAndExam = async () => {
  formErrorMessage.value = ''
  loading.value = true
  const formData = new FormData()
  if (typeSelected.value === 'assessments') {
    if (assessmentTotalScore.value <= 0) {
      showErrorMessage('The total score of the assessment cannot be negative or zero(0)')
      return;
    } else if (assessmentTotalScore.value >= 10000) {
      showErrorMessage('The total score of the assessment must be less than 10000')
      return;
    } else if (assessmentDescription.value.length > 100) {
      showErrorMessage("The maximum characters for the description must not exceed 100")
      return;
    } else if (assessmentTitle.value.length > 50) {
      showErrorMessage("The maximum characters for the title must not exceed 50")
      return;
    } else if (new Date(assessmentDate.value) < academicYearStartDate || new Date(assessmentDate.value) > academicYearEndDate) {
      showErrorMessage(`The assessment date must be between the academic year start date and end date, which are ${academicYearStartDate.toDateString()} and ${academicYearEndDate.toDateString()} respectively.`)
      return;
    }
    if (allAssessments.value?.[className]) {
      const assessmentSubjectData = Object.values(allAssessments.value[className])
      for (let i=0; i < assessmentSubjectData.length; i++){
        if (assessmentSubjectData[i].title === assessmentTitle.value) {
          showErrorMessage(`Assessment with title '${assessmentTitle.value}' already exists! Use a different title`)
          return;
        }
      }
    }
    formData.append('title', assessmentTitle.value)
    formData.append('description', assessmentDescription.value)
    formData.append('totalScore', assessmentTotalScore.value)
    formData.append('date', assessmentDate.value)
    formData.append('type', 'createAssessment')
  }
  else if (typeSelected.value === 'exams') {
    if (examsTotalScore.value <= 0) {
      showErrorMessage('The total score of the exams cannot be negative or zero(0)')
      return;
    } else if (examsTotalScore.value >= 10000) {
      showErrorMessage('The total score of the exams must be less than 10000')
      return;
    }
    formData.append('totalScore', examsTotalScore.value)
    formData.append('type', 'createExams')
  }
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm.toString())
  formData.append('studentsClassName', className)
  formData.append('subject', subjectSelected.value)
  loading.value = false
  elementsStore.ShowLoadingOverlay()
  try {
    if (typeSelected.value === 'assessments') {
      const response = await axiosInstance.post('teacher/assessments', formData)
      const _assessmentData = {
        'title': assessmentTitle.value,
        'total_score': assessmentTotalScore.value,
        'description': assessmentDescription.value,
        'percentage': 0,
        'id': response.data.id,
        'assessment_date': assessmentDate.value,
        'students_with_assessment': {},
        'students_without_assessment': Object.fromEntries(students.value?.map(item => [item.st_id, {name: item.user, st_id: item.st_id}]) || []) || {},
      }
      if (userAuthStore.teacherData.studentsAssessments?.[className]?.[subjectSelected.value]) {
        userAuthStore.teacherData.studentsAssessments[className][subjectSelected.value][assessmentTitle.value] = _assessmentData
      }
      assessmentTitle.value = ''
      assessmentDescription.value = ''
      assessmentDate.value = ''
      assessmentTotalScore.value = null
      elementsStore.HideLoadingOverlay()
      elementsStore.ShowOverlay(response.data.message, 'green', null, null)
    }
    else if (typeSelected.value === 'exams') {
      const response = await axiosInstance.post('teacher/exams', formData)
      if (userAuthStore.teacherData.studentsExams?.[className]?.[subjectSelected.value]) {
        const _examsData = {
        'total_score': examsTotalScore.value,
        'percentage': 0,
        'students_with_exams': {},
        'students_without_exams': Object.fromEntries(students.value?.map(item => [item.st_id, {name: item.user, st_id: item.st_id}]) || []) || {},
      }
        userAuthStore.teacherData.studentsExams[className][subjectSelected.value] = _examsData
      }
      
      elementsStore.HideLoadingOverlay()
      examsTotalScore.value = null
      subjectSelected.value = ''
      elementsStore.ShowOverlay(response.data.message, 'green', null, null)
    }
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

const checkStudentAssessmentsExams = () => {
  let validation = true
  const studentAssessmentsDataArray = computed(()=>{
    return Object.values(studentAssessmentsData.value?.[subjectSelected.value] || {})
  })
  for (let i=0; i < studentAssessmentsDataArray.value.length; i++){
    if (Object.keys(studentAssessmentsDataArray.value[i].students_with_assessment || {}).length === 0) {
      validation = false
      resultGenerationErrorType.value = studentAssessmentsDataArray.value[i].title
      break;
    }
  }
  if (validation) {
    const studentExams = userAuthStore.teacherData.studentsExams?.[className][subjectSelected.value]
    if (Object.keys(studentExams.students_without_exams || {}).length > 0) {
      validation = false
      resultGenerationErrorType.value = 'exams'
    }
  }
  return validation
}

const generateResults = async () => {
  formErrorMessage.value = ''
  loading.value = true
  if (Object.keys(userAuthStore.teacherData.studentsResults[className][subjectSelected.value].student_results || {}).length > 0) {
    showErrorMessage(`You have already generated the students ${subjectSelected.value} results`)
    return;
  }
  const studentAssessmentsExamsValidation = checkStudentAssessmentsExams()
  if (!studentAssessmentsExamsValidation) {
    if (resultGenerationErrorType.value === 'exams') {
      showErrorMessage(`You have not uploaded the ${subjectSelected.value} exams data for some students.  Please ensure all students have their data uploaded before proceeding.`)
      return;
    } else {
      showErrorMessage(`The assessment titled "${resultGenerationErrorType.value}" under ${subjectSelected.value} is incomplete because some students do not have assessment data. Please ensure all students have their data uploaded before proceeding.`)
      return;
    }
  }
  let totalAssessmentPercentage = 0
  let validInput:boolean = true
  const resultsData: any = { 'examsPercentage': examsPercentage.value, 'assessments': [], 'exams': 'yes'}
  const assessmentData = allAssessments.value?.[subjectSelected.value]
  if (Object.keys(assessmentData || {}).length > 0) {
    for (let i=0; i < Object.values(assessmentData).length; i++){
      const item = Object.values(assessmentData)[i]
      if (item.percentage) {
        totalAssessmentPercentage += item.percentage
      }
      else {
        validInput = false
        break;
      }
      resultsData['assessments'].push(item)
    }
  }
  else {
    if (Object.keys(userAuthStore.teacherData.studentsExams?.[className]?.[subjectSelected.value].students_with_exams || {}).length === 0) {
      showErrorMessage(`There are no exams data for ${subjectSelected.value}. Please upload the exams data for the students before proceeding.`)
      return;
    }
  }
  if (Object.keys(userAuthStore.teacherData.studentsExams?.[className]?.[subjectSelected.value].students_with_exams || {}).length === 0) {
    resultsData['exams'] = 'no'
  }
  if (!validInput) {
    showErrorMessage("The assessments percentages must be greater than 0")
    return;
  }
  else if (userAuthStore.teacherData.studentsExams[className][subjectSelected.value].total_score === 0 && totalAssessmentPercentage !== 100 || totalAssessmentPercentage + examsPercentage.value !== 100) {
    showErrorMessage("The total percentage must be 100.")
    return;
  }
  resultsData['totalAssessmentPercentage'] = totalAssessmentPercentage
  loading.value = false
  const formData = new FormData()
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm.toString())
  formData.append('studentsClassName', className)
  formData.append('subject', subjectSelected.value)
  formData.append('resultsData', JSON.stringify(resultsData))
  formData.append('type', 'generateResults')
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('teacher/students-result', formData)
    const studentAssessments = userAuthStore.teacherData.studentsAssessments?.[className]?.[subjectSelected.value]
    if (Object.keys(studentAssessments || {}).length > 0) {
      Object.values(studentAssessmentsData.value[subjectSelected.value]).forEach(item =>{
        studentAssessments[item.title].percentage = item.percentage
      })
    }
    if (userAuthStore.teacherData.studentsExams?.[className]?.[subjectSelected.value]?.total_score) {
      userAuthStore.teacherData.studentsExams[className][subjectSelected.value].percentage = examsPercentage.value
    }
    if (userAuthStore.teacherData.studentsResults?.[className]?.[subjectSelected.value]) {
      userAuthStore.teacherData.studentsResults[className][subjectSelected.value].exam_percentage = response.data['exam_percentage']
      userAuthStore.teacherData.studentsResults[className][subjectSelected.value].total_assessment_percentage = response.data['total_assessment_percentage']
      userAuthStore.teacherData.studentsResults[className][subjectSelected.value].student_results = response.data['student_results']
    }
    subjectSelected.value = ''
    examsPercentage.value = 0
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Results generated successfully', 'green', null, null)
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

const isResultGenerationFormValid = computed(()=>{
  if (Object.keys(allAssessments.value[subjectSelected.value] || {}).length > 0){
    return !(examsPercentage.value === 0 || examsPercentage.value);
  }
  return !(examsPercentage.value);
})

const isAssessmentExamsFormValid = computed(() => {
  if (typeSelected.value === 'assessments') {
    return !(subjectSelected.value && assessmentTitle.value && assessmentTotalScore.value && assessmentDate.value)
  }
  else if (typeSelected.value === 'exams') {
    return !(examsTotalScore.value)
  }
  else {
    return true;
  }
})

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  subjectSelected.value = ''
  examsPercentage.value = 0
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherCoursework,${className}`" :class="{ 'is-active-page': elementsStore.activePage === `TeacherCoursework,${className}` }">
    <div :id="`teacherSubjectsOverlay${className}`" class="overlay" v-if="subjects.length > 0">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`teacherSubjectsOverlay${className}`)" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">SUBJECT(S) ASSIGNED TO THIS CLASS [{{ subjects.length }}]</h3>
          <p class="teacher-subject" v-for="(_subject, index) in subjects" :key="index">{{ _subject }}</p>
        </div>
      </div>
    </div>

    <!-- assessment/exams creation overlay -->
    <div :id="`teacherAssessmentExamsCreationOverlay${className}`" class="overlay upload"
      v-if="students && students.length > 0">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`teacherAssessmentExamsCreationOverlay${className}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container">
          <h4 class="info-text">CLASS: <span class="info-text-value">{{ className }}</span></h4>
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="typeOptions" label="SELECT" v-model="typeSelected" item-title="label"
            item-value="value" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select whether you want to create assessment or exam" />
          <v-select class="select" :items="subjects" label="SUBJECT" v-model="subjectSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject you want to create the assessment for" />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model="assessmentTitle"
            label="TITLE" variant="solo-filled" placeholder="Eg. History Essay: The Impact of World War II"
            density="comfortable" persistent-hint hint="Enter a title for the assessment" />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model="assessmentDescription"
            label="DESCRIPTION(OPTIONAL)" placeholder="Eg. Examines WWII's effects on politics and society."
            density="comfortable" variant="solo-filled" persistent-hint hint="Enter a description for the assessment" />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model.number="assessmentTotalScore"
            label="TOTAL SCORE" placeholder="Eg. 40" density="comfortable" type="number" variant="solo-filled"
            persistent-hint hint="Enter the total score of the assessment" />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model="assessmentDate" label="DATE"
            density="comfortable" type="date" variant="solo-filled" persistent-hint
            hint="Select the date the assessment was conducted" />
          <v-text-field class="input-field" v-if="typeSelected === 'exams'" v-model.number="examsTotalScore"
            label="TOTAL SCORE" placeholder="Eg. 40" density="comfortable" type="number" variant="solo-filled"
            persistent-hint hint="Enter the total score of the exam" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createAssessmentAndExam" :disabled="isAssessmentExamsFormValid" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">SUBMIT</v-btn>
        </div>
      </div>
    </div>

    <!-- results Generation overlay -->
    <div :id="`teacherStudentsResultsCreationOverlay${className}`" class="overlay upload" v-if="students.length > 0">
      <div class="overlay-card">
        <v-btn :disabled="loading"
          @click="closeOverlay(`teacherStudentsResultsCreationOverlay${className}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container">
          <h4 class="info-text">CLASS: <span class="info-text-value">{{ className }}</span></h4>
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="subjects" label="SUBJECT" v-model="subjectSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject for the results" 
          />
          <div v-for="[_subject, _subject_data] in Object.entries(studentAssessmentsData)" :key="_subject">
            <div v-if="_subject === subjectSelected">
              <v-text-field class="input-field" v-for="(_assessment, ind) in Object.values(_subject_data)" :key="ind"
                v-model.number="_assessment.percentage" :label="_assessment.title" type="number" placeholder="Eg. 20"
                variant="solo-filled" density="comfortable" persistent-hint
                hint="Enter the percentage you want this assessment to contribute to the overall results" />
            </div>
          </div>
          <v-text-field v-if="subjectSelected && userAuthStore.teacherData.studentsExams[className][subjectSelected]?.total_score !== 0" class="input-field" v-model.number="examsPercentage"
            label="EXAMS PERCENTAGE" placeholder="Eg. 30" density="comfortable" type="number" variant="solo-filled"
            persistent-hint hint="Enter the percentage you want the exams to contribute to the overall results" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="generateResults" :loading="loading" :disabled="isResultGenerationFormValid" :ripple="false"
            variant="flat" type="submit" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle">SUBMIT</v-btn>
        </div>
      </div>
    </div>
    <div class="content-header title">
      <h4 class="content-header-title">{{ className }}</h4>
    </div>
    <div class="content-header">
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
    </div>
    <div class="content-header btn-container">
      <v-btn @click="showOverlay(`teacherSubjectsOverlay${className}`)" class="ma-1" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECT(S)
      </v-btn>
      <v-btn @click="showOverlay(`teacherAssessmentExamsCreationOverlay${className}`)" class="ma-1"
      v-if="students.length > 0" color="blue" :size="elementsStore.btnSize1">
        CREATE ASSESSMENT/EXAM
      </v-btn>
      <v-btn @click="showOverlay(`teacherStudentsResultsCreationOverlay${className}`)" class="ma-1"
      v-if="students.length > 0" color="blue" :size="elementsStore.btnSize1">
        GENERATE RESULTS
      </v-btn>
    </div>
    <div class="no-data" v-if="students.length === 0">
      <p>There are no student in this class. Contact your school administrator</p>
    </div>
    <v-table fixed-header class="table" v-if="students.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">GUARDIAN CONTACT</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in students" :key="index">
          <td class="table-data">
            {{ st.user }}
            <v-list-item-subtitle>{{ st.st_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">{{ st.gender }}</td>
          <td class="table-data"><img class="profile-img" :src="st.img"></td>
          <td class="table-data">{{ st.contact }}</td>
          <td class="table-data">{{ st.guardian_contact }}</td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 20% !important;
}

.title {
  min-height: 10% !important;
}

.btn-container {
  min-height: 15% !important;
}

.table {
  height: 55% !important;
}

.overlay-card {
  height: max-content !important;
  max-width: 500px !important;
}

.overlay-card-info-container {
  height: 100% !important;
  margin-top: 4em !important;
}

.teacher-subject {
  color: white;
  margin: .3em;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  padding: .5em;
  background-color: #333333;
  font-weight: bold;
  border-radius: .2em;
  font-size: .8rem;
}

.upload .overlay-card {
  max-width: 700px !important;
  height: 90% !important;
  max-height: 600px !important;
}

.upload .overlay-card-info-container {
  height: 10% !important;
}

.upload .overlay-card-content-container {
  height: 60% !important;
}

@media screen and (min-width: 450px) {
  .content-header {
    min-height: 15% !important;
  }

  .btn-container,
  .title {
    min-height: 10% !important;
  }

  .table {
    height: 65% !important;
  }
}

@media screen and (min-width: 480px) {
  .content-header-text {
    font-size: .75rem !important;
  }
}

@media screen and (min-width: 576px) {
  .content-header-text {
    font-size: .8rem !important;
  }
}

@media screen and (min-width: 767px) {
  .content-header-text {
    font-size: .9rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .content-header-text {
    font-size: 1rem !important;
  }

  .content-header,
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
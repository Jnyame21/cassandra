<script setup lang="ts">
import { AxiosError } from 'axios';
import { ref, computed, watch } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue'

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const femaleStudents = ref(0)
const maleStudents = ref(0)
const subjectSelected: any = ref(null)
const assessmentTitle = ref('')
const assessmentTotalScore: any = ref(null)
const assessmentDescription = ref('')
const assessmentDate = ref('')
const academicYearStartDate = new Date(userAuthStore.userData['academic_year']['start_date'])
const academicYearEndDate = new Date(userAuthStore.userData['academic_year']['end_date'])
const formErrorMessage = ref('')
const examsPercentage: any = ref(null)
const assessmentsAll: any = ref([])
const resultUploadErrorType = ref('')
const loading = ref(false)
const typeSelected = ref('')
const examsTotalScore: any = ref(null)

interface Props {
  className?: string;
  classIndex?: number;
  students?: any[];
  subjects?: string[];
}
interface assessmentSubjectData {
  subject: string;
  assessments: {
    'title': string;
    'percentage': any;
    'totalScore': number;
  }[]
}
const props = defineProps<Props>()
const className = props.className || 'Class'
const classIndex = props.classIndex || 0
const students = props.students || []
const subjects = props.subjects || []

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

watch(() => userAuthStore.staffData?.studentsAssessments?.[classIndex]?.assignments, (newValue) => {
  if (newValue?.length > 0) {
    const newAssessments: any = []
    newValue.forEach((item: any) => {
      const assessmentSubject: assessmentSubjectData = { 'subject': item['subject'], 'assessments': [] }
      if (item.assessments?.length > 0) {
        item.assessments.forEach((_assess: any) => {
          assessmentSubject.assessments.push({
            'title': _assess['title'],
            'percentage': null,
            'totalScore': Number(_assess['total_score'])
          })
        })
      }
      newAssessments.push(assessmentSubject)
    })
    assessmentsAll.value = newAssessments
  }
}, { 'deep': 4, 'immediate': true })

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
    const _assessmentClass = userAuthStore.staffData.studentsAssessments.find((item: any) => item['class_name'] === className)
    if (_assessmentClass) {
      const _assessmentSubject = _assessmentClass['assignments'].find((item: any) => item['subject'] === subjectSelected.value)
      if (_assessmentSubject) {
        const _assessmentsTitles: any = []
        _assessmentSubject['assessments'].forEach((item: any) => {
          _assessmentsTitles.push(item['title'])
        })
        if (_assessmentsTitles.includes(assessmentTitle.value)) {
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
  formData.append('term', userAuthStore.activeTerm)
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
        'assessment_date': assessmentDate.value,
        'students_with_assessment': [],
        'students_without_assessment': students.map(item => ({ 'name': item['name'], 'st_id': item['st_id'] })),
      }
      const assessmentSubject = userAuthStore.staffData.studentsAssessments[classIndex]['assignments'].find((item: any) => item['subject'] === subjectSelected.value)
      if (assessmentSubject) {
        const assessmentSubjectIndex = userAuthStore.staffData.studentsAssessments[classIndex]['assignments'].indexOf(assessmentSubject)
        userAuthStore.staffData.studentsAssessments[classIndex]['assignments'][assessmentSubjectIndex]['assessments'].unshift(_assessmentData)
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
      const examSubject = userAuthStore.staffData.studentsExams[classIndex]['exams'].find((item: any) => item['subject'] === subjectSelected.value)
      if (examSubject) {
        const examSubjectIndex = userAuthStore.staffData.studentsExams[classIndex]['exams'].indexOf(examSubject)
        userAuthStore.staffData.studentsExams[classIndex]['exams'][examSubjectIndex]['total_score'] = examsTotalScore.value
      }
      elementsStore.HideLoadingOverlay()
      examsTotalScore.value = null
      subjectSelected.value = null
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

const checkResultUpload = () => {
  let uploadResults = true
  const assessmentSubject = userAuthStore.staffData.studentsAssessments[classIndex]['assignments'].find((item: any) => item['subject'] === subjectSelected.value)
  if (assessmentSubject) {
    assessmentSubject['assessments'].forEach((item: any) => {
      if (item['students_without_assessment'].length > 0) {
        uploadResults = false
        resultUploadErrorType.value = item['title']
      }
    })
  }
  if (uploadResults) {
    const examSubject = userAuthStore.staffData.studentsExams[classIndex]['exams'].find((item: any) => item['subject'] === subjectSelected.value)
    if (examSubject?.students_without_exams?.length > 0) {
      uploadResults = false
      resultUploadErrorType.value = 'exams'
    }
  }
  return uploadResults
}

const generateResults = async () => {
  formErrorMessage.value = ''
  loading.value = true
  const uploadResults = checkResultUpload()
  if (!uploadResults) {
    if (resultUploadErrorType.value === 'exams') {
      showErrorMessage(`The exam data for the subject ${subjectSelected.value} is incomplete. Please upload the missing data for all students before proceeding.`)
      return;
    } else {
      showErrorMessage(`The assessment titled "${resultUploadErrorType.value}" for the subject ${subjectSelected.value} is incomplete because some students do not have assessment data. Please ensure all students have their data uploaded before proceeding.`)
      return;
    }
  }
  let totalAssessmentPercentage = 0
  let validInput: any = 1
  const resultsData: any = { 'examsPercentage': examsPercentage.value, 'assessments': [] }
  const assessmentsAllSubject = assessmentsAll.value.find((item: any) => item['subject'] === subjectSelected.value)
  if (assessmentsAllSubject) {
    const assessmentsAllSubjectIndex = assessmentsAll.value.indexOf(assessmentsAllSubject)
    assessmentsAll.value[assessmentsAllSubjectIndex]['assessments'].forEach((item: any) => {
      if (item['percentage']) {
        totalAssessmentPercentage += item['percentage']
      }
      else {
        validInput = null
      }
      resultsData['assessments'].push(item)
    })
  }
  if (!validInput || examsPercentage.value <= 0) {
    showErrorMessage("All the values(percentages) must be greater than 0")
    return;
  }
  else if ((totalAssessmentPercentage + examsPercentage.value) !== 100) {
    showErrorMessage("The total percentage must be 100.")
    return;
  }
  resultsData['totalAssessmentPercentage'] = totalAssessmentPercentage
  loading.value = false
  const formData = new FormData()
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm)
  formData.append('studentsClassName', className)
  formData.append('subject', subjectSelected.value)
  formData.append('resultsData', JSON.stringify(resultsData))
  formData.append('type', 'createResults')
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('teacher/students-result', formData)
    const assessmentSubject = userAuthStore.staffData.studentsAssessments[classIndex]['assignments'].find((item: any) => item['subject'] === subjectSelected.value)
    if (assessmentSubject) {
      const assessmentSubjectIndex = userAuthStore.staffData.studentsAssessments[classIndex]['assignments'].indexOf(assessmentSubject)
      if (assessmentsAllSubject['assessments']?.length > 0) {
        assessmentsAllSubject['assessments'].forEach((item: any) => {
          const assessmentTitle = assessmentSubject['assessments'].find((title: any) => title['title'] === item['title'])
          if (assessmentTitle) {
            const assessmentTitleIndex = assessmentSubject['assessments'].indexOf(assessmentTitle)
            userAuthStore.staffData.studentsAssessments[classIndex]['assignments'][assessmentSubjectIndex]['assessments'][assessmentTitleIndex]['percentage'] = item['percentage']
          }
        })
      }
    }
    const examSubject = userAuthStore.staffData.studentsExams[classIndex]['exams'].find((item: any) => item['subject'] === subjectSelected.value)
    if (examSubject) {
      const examSubjectIndex = userAuthStore.staffData.studentsExams[classIndex]['exams'].indexOf(examSubject)
      userAuthStore.staffData.studentsExams[classIndex]['exams'][examSubjectIndex]['percentage'] = examsPercentage.value
    }
    const resultSubject = userAuthStore.staffData.studentsResults[classIndex]['results'].find((item: any) => item['subject'] === subjectSelected.value)
    if (resultSubject) {
      const resultSubjectIndex = userAuthStore.staffData.studentsResults[classIndex]['results'].indexOf(resultSubject)
      userAuthStore.staffData.studentsResults[classIndex]['results'][resultSubjectIndex]['exam_percentage'] = response.data['exam_percentage']
      userAuthStore.staffData.studentsResults[classIndex]['results'][resultSubjectIndex]['total_assessment_percentage'] = response.data['total_assessment_percentage']
      userAuthStore.staffData.studentsResults[classIndex]['results'][resultSubjectIndex]['student_results'] = response.data['student_results']
    }
    clearAsessmentPercentages()
    subjectSelected.value = null
    examsPercentage.value = null
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation Successful', 'green', null, null)
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

const isResultsFormValid = computed(() => {
  return !(examsPercentage.value)
})

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const clearAsessmentPercentages = () => {
  assessmentsAll.value.forEach((item: any) => {
    item.assessments.forEach((_asesss: any) => {
      _asesss.percentage = null
    })
  })
}
const closeOverlay = (element: string) => {
  formErrorMessage.value = ''
  subjectSelected.value = null
  assessmentTitle.value = ''
  typeSelected.value = ''
  assessmentTotalScore.value = null
  assessmentDescription.value = ''
  examsTotalScore.value = null
  examsPercentage.value = null
  assessmentDate.value = ''
  if (element === `teacherStudentsResultsCreationOverlay${className}${classIndex}`) {
    clearAsessmentPercentages()
  }
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


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherCoursework,${className},${classIndex}`"
    :class="{ 'is-active-page': elementsStore.activePage === `TeacherCoursework,${className},${classIndex}` }"
    >
    <div :id="`teacherSubjectsOverlay${className}${classIndex}`" class="overlay" v-if="subjects.length > 0">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`teacherSubjectsOverlay${className}${classIndex}`)" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">SUBJECT(S) ASSIGNED TO THIS
            CLASS [{{ subjects.length }}]</h3>
          <p class="teacher-subject" v-for="(_subject, index) in subjects" :key="index">
            {{ _subject }}
          </p>
        </div>
      </div>
    </div>

    <!-- assessment/exams creation overlay -->
    <div :id="`teacherAssessmentExamsCreationOverlay${className}${classIndex}`" class="overlay upload"
      v-if="userAuthStore.staffData.courseWork?.length > 0">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`teacherAssessmentExamsCreationOverlay${className}${classIndex}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <p class="form-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container">
          <h4 class="info-text">CLASS: <span class="info-text-value">{{ className }}</span></h4>
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="typeOptions" label="SELECT" v-model="typeSelected" item-title="label"
            item-value="value" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select whether you want to create assessment or exam" 
          />
          <v-select class="select" :items="subjects" label="SUBJECT" v-model="subjectSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject you want to create the assessment for" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model="assessmentTitle"
            label="TITLE" variant="solo-filled" placeholder="Eg. History Essay: The Impact of World War II"
            density="comfortable" persistent-hint hint="Enter a title for the assessment" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model="assessmentDescription"
            label="DESCRIPTION(OPTIONAL)" placeholder="Eg. Examines WWII's effects on politics and society."
            density="comfortable" variant="solo-filled" persistent-hint hint="Enter a description for the assessment" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model.number="assessmentTotalScore"
            label="TOTAL SCORE" placeholder="Eg. 40" density="comfortable" type="number" variant="solo-filled"
            persistent-hint hint="Enter the total score of the assessment" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'assessments'" v-model="assessmentDate" label="DATE"
            density="comfortable" type="date" variant="solo-filled" persistent-hint
            hint="Select the date the assessment was conducted" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'exams'" v-model.number="examsTotalScore"
            label="TOTAL SCORE" placeholder="Eg. 40" density="comfortable" type="number" variant="solo-filled"
            persistent-hint hint="Enter the total score of the exam" 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createAssessmentAndExam" :disabled="isAssessmentExamsFormValid" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">SUBMIT</v-btn>
        </div>
      </div>
    </div>

    <!-- results creation overlay -->
    <div :id="`teacherStudentsResultsCreationOverlay${className}${classIndex}`" class="overlay upload"
      v-if="userAuthStore.staffData.courseWork?.length > 0">
      <div class="overlay-card">
        <v-btn :disabled="loading"
          @click="closeOverlay(`teacherStudentsResultsCreationOverlay${className}${classIndex}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <p class="form-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container">
          <h4 class="info-text">CLASS: <span class="info-text-value">{{ className }}</span></h4>
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="subjects" label="SUBJECT" v-model="subjectSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject for the results" />
          <div v-for="(_subject, index) in assessmentsAll" :key="index">
            <div v-if="_subject['subject'] === subjectSelected">
              <v-text-field class="input-field" v-for="(_assessment, ind) in _subject['assessments']" :key="ind"
                v-model.number="_assessment.percentage" :label="_assessment['title']" type="number" placeholder="Eg. 20"
                variant="solo-filled" density="comfortable" persistent-hint
                hint="Enter the percentage you want this assessment to contribute to the overall results" />
            </div>
          </div>
          <v-text-field v-if="subjectSelected" class="input-field" v-model.number="examsPercentage"
            label="EXAMS PERCENTAGE" placeholder="Eg. 30" density="comfortable" type="number" variant="solo-filled"
            persistent-hint hint="Enter the percentage you want the exams to contribute to the overall results" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="generateResults" :loading="loading" :disabled="isResultsFormValid" :ripple="false"
            variant="flat" type="submit" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle">SUBMIT</v-btn>
        </div>
      </div>
    </div>

    <TheLoader v-if="!userAuthStore.staffData.courseWork" />
    <div class="no-data" v-if="userAuthStore.staffData.courseWork?.length === 0">
      <p>YOU HAVE NOT BEEN ASSIGNED TO A CLASS FOR THE {{ userAuthStore.activeAcademicYear }} ACADEMIC YEAR {{userAuthStore.userData['academic_year']['period_division']}} {{userAuthStore.activeTerm}}</p>
    </div>
    <div class="content-header title" v-if="students.length > 0">
      <h4 class="content-header-title">{{ className }}</h4>
    </div>
    <div class="content-header" v-if="students.length > 0">
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
    </div>
    <div class="content-header btn-container" v-if="students.length > 0">
      <v-btn @click="showOverlay(`teacherSubjectsOverlay${className}${classIndex}`)" class="ma-1" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECT(S)
      </v-btn>
      <v-btn @click="showOverlay(`teacherAssessmentExamsCreationOverlay${className}${classIndex}`)" class="ma-1"
        color="blue" :size="elementsStore.btnSize1">
        CREATE ASSESSMENT/EXAM
      </v-btn>
      <v-btn @click="showOverlay(`teacherStudentsResultsCreationOverlay${className}${classIndex}`)" class="ma-1"
        color="blue" :size="elementsStore.btnSize1">
        GENERATE RESULTS
      </v-btn>
    </div>
    <v-table fixed-header class="table" v-if="students.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">IMAGE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in students" :key="index">
          <td class="table-data">
            {{ st['name'] }}
            <v-list-item-subtitle>{{ st['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">{{ st['gender'] }}</td>
          <td class="table-data"><img class="profile-img" :src="st['img']"></td>
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
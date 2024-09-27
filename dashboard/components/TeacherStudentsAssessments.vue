<script setup lang="ts">
import { AxiosError } from 'axios';
import axiosInstance from '../utils/axiosInstance';
import { ref } from 'vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const studentName = ref('')
const studentId = ref('')
const previousScore: any = ref(null)
const previousComment = ref('')
const newScore:any = ref(null)
const previousTitle: any = ref(null)
const previousDescription: any = ref(null)
const previousPercentage: any = ref(null)
const previousTotalScore: any = ref(null)
const previousDate: any = ref(null)
const newTitle: any = ref(null)
const newDescription: any = ref(null)
const newPercentage: any = ref(null)
const newTotalScore: any = ref(null)
const newDate: any = ref(null)
const newComment = ref('')
const editType = ref('')



const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
  }, 8000)
}

watch(()=>userAuthStore.teacherData.studentsWithAssessments, (newValue, oldValue)=>{
  if (newValue){
    const className = elementsStore.activePage.split(',')[1]
    const subjectName = elementsStore.activePage.split(',')[2]
    const title = elementsStore.activePage.split(',')[3]
    const assessment = newValue.find(item => item['class_name'] === className)
    if (assessment){
      const assessmentSubject = assessment['assignments'].find(item => item['subject'] === subjectName)
      if (assessmentSubject){
        const assessmentTitle = assessmentSubject['assessments'].find(item => item['title'] === title)
        assessmentTitle ? userAuthStore.teacherData.currentAssessments = assessmentTitle : null
      }
    }
  }
})

const deleteAssessment = async(st_id:string)=>{
  elementsStore.ShowLoadingOverlay()
  const className = elementsStore.activePage.split(',')[1]
  const subjectName = elementsStore.activePage.split(',')[2]
  const formData = new FormData()
  formData.append('type', 'deleteAssessment')
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('studentId', st_id); 
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());
  formData.append('title', userAuthStore.teacherData.currentAssessments['title']);

  try{
    await axiosInstance.post('teacher/assessments', formData)
    const student = userAuthStore.teacherData.currentAssessments['students'].find(item => item['st_id'] === st_id)
    if (student){
      const studentIndex = userAuthStore.teacherData.currentAssessments['students'].indexOf(student)
      userAuthStore.teacherData.currentAssessments['students'].splice(studentIndex, 1)
      const _assessmentTitle = elementsStore.activePage.split(',')[3]
      const assessment = userAuthStore.teacherData.studentsWithoutAssessments.find(item => item['class_name'] === className)
      if (assessment){
        const assessmentIndex = userAuthStore.teacherData.studentsWithoutAssessments.indexOf(assessment)
        const assessmentSubject = assessment['assignments'].find(item => item['subject'] === subjectName)
        if (assessmentSubject){
          const assessmentSubjectIndex = assessment['assignments'].indexOf(assessmentSubject)
          const assessmentTitle = assessmentSubject['assessments'].find(item => item['title'] === _assessmentTitle)
          if (assessmentTitle){
            const assessmentTitleIndex = assessmentSubject['assessments'].indexOf(assessmentTitle)
            userAuthStore.teacherData.studentsWithoutAssessments[assessmentIndex]['assignments'][assessmentSubjectIndex]['assessments'][assessmentTitleIndex]['students'].unshift(student)
          }
        }
      }
    }
    elementsStore.HideLoadingOverlay()
  }
  catch (error){
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError){
      error.response?.status === 400 && error.response.data.message ? elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)  : elementsStore.ShowOverlay('Oops! something went wrong. try again', 'red', null, null)
    }
  }
}

const editAssessment = async()=>{
  formErrorMessage.value = ''
  const className = elementsStore.activePage.split(',')[1]
  const subjectName = elementsStore.activePage.split(',')[2]
  const formData = new FormData()
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());
  formData.append('type', 'editAssessment');
  formData.append('title', userAuthStore.teacherData.currentAssessments['title']);

  if (editType.value === 'score'){
    if (userAuthStore.teacherData?.currentAssessments['total_score'] >= newScore.value && newScore.value >=0){
      formData.append('newScore', newScore.value);
      formData.append('editType', 'score');
      formData.append('studentId', studentId.value);
    }else{
      if (newScore.value <0){
        formErrorMessage.value = 'The assessment score cannot be negative'
      }
      else if (newScore.value > userAuthStore.teacherData?.currentAssessments['total_score']){
        formErrorMessage.value = "The student's score cannot be greater than the total assessment score"
      }
      clearMessage()
      return;
    }
  }
  else if (editType.value === 'comment'){
    if (newComment.value.length >200){
      formErrorMessage.value = "The maximum characters must not exceed 200"
      clearMessage()
      return;
    }
    formData.append('newComment', newComment.value);
    formData.append('editType', 'comment');
    formData.append('studentId', studentId.value);
  }
  else if (editType.value === 'title'){
    if (newTitle.value.length >100){
      formErrorMessage.value = "The maximum characters must not exceed 100"
      clearMessage()
      return;
    }
    formData.append('newTitle', newTitle.value);
    formData.append('editType', 'title');
  }
  else if (editType.value === 'description'){
    if (newDescription.value.length >150){
      formErrorMessage.value = "The maximum characters must not exceed 100"
      clearMessage()
      return;
    }
    formData.append('newDescription', newDescription.value);
    formData.append('editType', 'description');
  }
  else if (editType.value === 'totalScore'){
    if (newTotalScore.value <0){
      formErrorMessage.value = 'The total assessment score cannot be negative'
      clearMessage()
      return;
    }else if (newTotalScore.value < Math.max(...userAuthStore.teacherData.currentAssessments['students'].map(st => Number(st.score)))){
      formErrorMessage.value = `The total assessment score cannot be less than the maximum score of a student. Ensure each student's score is less than ${newTotalScore.value}`
      clearMessage()
      return;
    }
    else {
      formData.append('newTotalScore', newTotalScore.value);
      formData.append('editType', 'totalScore');
    }
  }
  else if (editType.value === 'percentage'){
    if (100 >= newPercentage.value && newPercentage.value >=0){
      formData.append('newPercentage', newPercentage.value);
      formData.append('editType', 'percentage');
    }else{
      if (newPercentage.value <0){
        formErrorMessage.value = 'The assessment percentage cannot be negative'
      }
      else if (newPercentage.value > 100){
        formErrorMessage.value = 'The assessment percentage cannot be greater than 100'
      }
      clearMessage()
      return;
    }
  }
  else if (editType.value === 'date'){
    formData.append('newDate', newDate.value);
    formData.append('editType', 'date');
  }

  elementsStore.ShowLoadingOverlay()
  try{
    await axiosInstance.post('teacher/assessments', formData)
    if (['score', 'comment'].includes(editType.value)){
      const student = userAuthStore.teacherData.currentAssessments['students'].find(item => item['st_id'] === studentId.value)
      if (student){
        const studentIndex = userAuthStore.teacherData.currentAssessments['students'].indexOf(student)
        if(editType.value === 'score'){
          userAuthStore.teacherData.currentAssessments['students'][studentIndex]['score'] = newScore.value
          userAuthStore.teacherData.currentAssessments['students'].sort((a, b) => b.score - a.score)
        }
        editType.value === 'comment' ? userAuthStore.teacherData.currentAssessments['students'][studentIndex]['comment'] = newComment.value : null
      }
    }else{
      const _title = userAuthStore.teacherData.currentAssessments['title']
      editType.value === 'title' ? updateAssessmentData(className, subjectName, _title, editType.value, newTitle.value) : null
      editType.value === 'description' ? updateAssessmentData(className, subjectName, _title, editType.value, newDescription.value) : null
      editType.value === 'totalScore' ? updateAssessmentData(className, subjectName, _title, editType.value, newTotalScore.value) : null
      editType.value === 'percentage' ? updateAssessmentData(className, subjectName, _title, editType.value, newPercentage.value) : null
      editType.value === 'date' ? updateAssessmentData(className, subjectName, _title, editType.value, newDate.value) : null
    }
    closeOverlay()
    elementsStore.HideLoadingOverlay()
  }
  catch (error){
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError){
      error.response?.status === 400 && error.response.data.message ? elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)  : elementsStore.ShowOverlay('Oops! something went wrong. try again later', 'red', null, null)
    }
  }
}

const updateAssessmentData = (_className: string, _subjectName: string,  _title: string, updateType: string, newValue: any) => {
  const updateAssessment = (assessmentsArray: any[]) => {
    const _assessment = assessmentsArray.find(item => item['class_name'] === _className);
    if (_assessment) {
      const _assessmentIndex = assessmentsArray.indexOf(_assessment);
      const assessmentSubject = _assessment['assignments'].find(item => item['subject'] === _subjectName);
      if (assessmentSubject) {
        const assessmentSubjectIndex = _assessment['assignments'].indexOf(assessmentSubject);
        const _assessmentTitle = assessmentSubject['assessments'].find(item => item['title'] === _title);
        if (_assessmentTitle) {
          const _assessmentTitleIndex = assessmentSubject['assessments'].indexOf(_assessmentTitle);
          updateType === 'title' ? assessmentsArray[_assessmentIndex]['assignments'][assessmentSubjectIndex]['assessments'][_assessmentTitleIndex]['title'] = newValue : null
          updateType === 'description' ? assessmentsArray[_assessmentIndex]['assignments'][assessmentSubjectIndex]['assessments'][_assessmentTitleIndex]['description'] = newValue : null
          updateType === 'totalScore' ? assessmentsArray[_assessmentIndex]['assignments'][assessmentSubjectIndex]['assessments'][_assessmentTitleIndex]['total_score'] = newValue : null
          updateType === 'percentage' ? assessmentsArray[_assessmentIndex]['assignments'][assessmentSubjectIndex]['assessments'][_assessmentTitleIndex]['percentage'] = newValue : null
          updateType === 'date' ? assessmentsArray[_assessmentIndex]['assignments'][assessmentSubjectIndex]['assessments'][_assessmentTitleIndex]['date'] = newValue : null
        }
      }
    }
  };
  updateAssessment(userAuthStore.teacherData.studentsWithAssessments);
  updateType === 'title' ? updateAssessment(userAuthStore.teacherData.studentsWithoutAssessments) : null
};


const isFormValid = computed(()=>{
  if (editType.value === 'score') {
    return !(newScore.value)
  }else if (editType.value === 'title'){
    return !(newTitle.value)
  }else if (editType.value === 'totalScore'){
    return !(newTotalScore.value)
  }else if (editType.value === 'percentage'){
    return !(newPercentage.value)
  }else if (editType.value === 'date'){
    return !(newDate.value)
  }else if (editType.value === 'comment'){
    return false
  }else if (editType.value === 'description'){
    return false
  }else{
    return true;
  }
})

const closeOverlay = ()=>{
  newScore.value = null
  newComment.value = ''
  previousScore.value = null
  previousComment.value = ''
  formErrorMessage.value = ''
  previousTitle.value = ''
  previousDescription.value = ''
  previousPercentage.value = ''
  previousTotalScore.value = ''
  previousDate.value = ''
  newTitle.value = ''
  newDescription.value = ''
  newPercentage.value = ''
  newTotalScore.value = ''
  newDate.value = ''
  editType.value = ''
  studentId.value = ''
  studentName.value = ''
  const overlay = document.getElementById('TeacherStudentsAssessmentEdit')
  overlay ? overlay.style.display = 'none' : null
}

const showForm = (type:string, prevValue:any, stName: string='', stId: string='',  )=>{
  editType.value = type
  if (type === 'score' || type === 'comment'){
    studentId.value = stId
    studentName.value = stName
    type === 'score' ? previousScore.value = prevValue : previousComment.value = prevValue
  }else{
    type === 'title' ? previousTitle.value = prevValue : null
    type === 'description' ? previousDescription.value = prevValue : null
    type === 'totalScore' ? previousTotalScore.value = prevValue : null
    type === 'percentage' ? previousPercentage.value = prevValue : null
    type === 'date' ? previousDate.value = prevValue : null
  }
  const formOverlay = document.getElementById('TeacherStudentsAssessmentEdit')
  formOverlay ? formOverlay.style.display = 'flex' : null
}


</script>

<template>
  <div class="content-wrapper" >
    <div id="TeacherStudentsAssessmentEdit" class="overlay" v-if="userAuthStore.teacherData.currentAssessments && userAuthStore.teacherData.currentAssessments['students'].length > 0">
        <form style="position: relative" class="overlay-form">
            <v-btn @click.prevent="closeOverlay" class="close-btn" size="small" variant="flat" color="red">X</v-btn>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <h2 class="info" v-if="editType === 'score' || editType === 'comment' "><strong>STUDENT:</strong> {{studentName}} [{{studentId}}]</h2>
            <h2 class="info" v-if="editType === 'title'"><strong>PREVIOUS TITLE:</strong> {{previousTitle}}</h2>
            <h2 class="info" v-if="editType === 'description'"><strong>PREVIOUS DESCRIPTION:</strong> {{previousDescription}}</h2>
            <h2 class="info" v-if="editType === 'totalScore'"><strong>PREVIOUS TOTAL SCORE:</strong> {{previousTotalScore}}</h2>
            <h2 class="info" v-if="editType === 'percentage'"><strong>PREVIOUS PERCENTAGE:</strong> {{previousPercentage}}</h2>
            <h2 class="info" v-if="editType === 'date'"><strong>PREVIOUS DATE:</strong> {{previousDate}}</h2>
            <h2 class="info" v-if="editType === 'score'"><strong>PREVIOUS SCORE:</strong> {{previousScore}}</h2>
            <h2 class="info" v-if="editType === 'comment'"><strong>PREVIOUS COMMENT:</strong> {{previousComment}}</h2>
            
            <v-text-field v-if="editType === 'score'" v-model="newScore" type="number" class="input-field" persistent-hint hint="Enter the student's new score" label="NEW SCORE" variant="outlined"/>
            <v-text-field v-if="editType === 'percentage'" v-model="newPercentage" type="number" class="input-field" persistent-hint hint="Enter a new percentage value" label="NEW PERCENTAGE" variant="outlined"/>
            <v-text-field v-if="editType === 'totalScore'" v-model="newTotalScore" type="number" class="input-field" persistent-hint hint="Enter a new total score" label="NEW TOTAL SCORE" variant="outlined"/>

            <v-text-field v-if="editType === 'comment'" v-model="newComment" class="input-field" persistent-hint hint="Enter a new comment(Max characters, 200)" label="NEW COMMENT" variant="outlined"/>
            <v-text-field v-if="editType === 'title'" v-model="newTitle" class="input-field" persistent-hint hint="Enter a new title(Max characters, 100)" label="NEW TITLE" variant="outlined"/>
            <v-text-field v-if="editType === 'description'" v-model="newDescription" class="input-field" persistent-hint hint="Enter a new description(Max characters, 150)" label="NEW DESCRIPTION" variant="outlined"/>
            <v-text-field v-if="editType === 'date'" v-model="newDate" class="input-field" type="date" persistent-hint hint="Select a new date" label="NEW DATE" variant="outlined"/>
            <v-btn :disabled="isFormValid" @click.prevent="editAssessment" type="submit" color="black" class="mt-10 mb-5" size="small" variant="flat" append-icon="mdi-checkbox-marked-circle">SUBMIT</v-btn>
        </form>
    </div>
      
    <TheLoader v-if="!userAuthStore.teacherData.studentsWithAssessments" />
    <h4 class="no-data" v-if="!userAuthStore.teacherData.currentAssessments || userAuthStore.teacherData.currentAssessments && userAuthStore.teacherData.currentAssessments['students'].length === 0">
      <p>NO DATA</p>
    </h4>
    <div class="info-wrapper" v-if="userAuthStore.teacherData.currentAssessments && userAuthStore.teacherData.currentAssessments['students'].length > 0">
      <h3>
        TITLE: <strong>{{ userAuthStore.teacherData.currentAssessments['title'] }}</strong>
        <v-icon class="ml-1" @click="showForm('title', userAuthStore.teacherData.currentAssessments['title'])" icon="mdi-pencil" />
      </h3>
      <h3>
        DESCRIPTION: <strong>{{ userAuthStore.teacherData.currentAssessments['description'] }}</strong>
        <v-icon class="ml-1" @click="showForm('description', userAuthStore.teacherData.currentAssessments['description'])" icon="mdi-pencil" />
      </h3>
      <h3>
        TOTAL SCORE: <strong>{{ userAuthStore.teacherData.currentAssessments['total_score'] }}</strong>
        <v-icon class="ml-1" @click="showForm('totalScore', userAuthStore.teacherData.currentAssessments['total_score'])" icon="mdi-pencil" />
      </h3>
      <h3>
        PERCENTAGE: <strong>{{ userAuthStore.teacherData.currentAssessments['percentage'] }}%</strong>
        <v-icon class="ml-1" @click="showForm('percentage', userAuthStore.teacherData.currentAssessments['percentage'])" icon="mdi-pencil" />
      </h3>
      <h3>
        DATE: <strong>{{ userAuthStore.teacherData.currentAssessments['date'] }}</strong>
        <v-icon class="ml-1" @click="showForm('date', userAuthStore.teacherData.currentAssessments['date'])" icon="mdi-pencil" />
      </h3>
    </div>
    <v-table fixed-header class="table" v-if="userAuthStore.teacherData.currentAssessments && userAuthStore.teacherData.currentAssessments['students'].length > 0">
      <thead>
      <tr>
        <th class="table-head">NAME</th>
        <th class="table-head">SCORE</th>
        <th class="table-head">COMMENT</th>
        <th class="table-head">ACTION</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in userAuthStore.teacherData.currentAssessments['students']" :key="index">
          <td class="table-data">
            {{ st['name'] }}
            <v-list-item-subtitle>{{ st['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn @click="showForm('score', st['score'], st['name'], st['st_id'])" size="small" color="black" variant="flat" >{{ st['score'] }}</v-btn>
          </td>
          <td class="table-data">
            {{ st['comment'] }}
            <v-btn @click="showForm('comment', st['comment'], st['name'], st['st_id'])" size="x-small" variant="flat" icon="mdi-pencil"></v-btn>
          </td>
          <td class="table-data">
            <v-btn @click="deleteAssessment(st['st_id'])" size="x-small" variant="flat" icon="mdi-delete" color="red"></v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.info-wrapper{
  height: 30% !important;
}
.table{
  height: 70% !important;
  overflow-x: auto !important;
}
.score{
  background-color: green;
  padding: .5em;
  border-radius: .5em;
  color: white;
}
.overlay{
  position: absolute;
  background: rgba(0, 0, 0, .5);
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  display: flex;
  z-index: 3;
  align-items: center;
  justify-content: center;
  display: none;
}
.overlay-form{
  background-color: white;
  padding: .5em 1em;
  border-radius: .3em;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 95%;
  max-width: 500px;
}
h3{
  font-size: .8em !important;
}
h3 strong{
  font-size: .8rem;
  font-weight: normal;
  color: yellow;
}
.info{
  font-size: .8rem;
  text-align: center;
  margin-top: 2.5em;
  color: seagreen;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.info strong{
  font-size: .8rem;
  color: black;
}
.input-field{
  margin-top: 1em;
  min-width: 300px;
}
.submit-btn{
  font-weight: bold;
  margin-top: 1em;
  margin-bottom: 1em;
}

@media screen and (min-width: 576px) {
  h3, h3 strong{
    font-size: .85rem !important;
  }
}
@media screen and (min-width: 767px) {
  h3, h3 strong{
    font-size: .9rem !important;
  }
}
@media screen and (min-width: 992px) {
  h3, h3 strong{
    font-size: .95rem !important;
  }
}
@media screen and (min-width: 1200px) {
  h3, h3 strong{
    font-size: 1rem !important;
  }
}



</style>
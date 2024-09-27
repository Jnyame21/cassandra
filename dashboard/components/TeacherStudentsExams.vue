
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { ref } from 'vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const studentName = ref('')
const studentId = ref('')
const previousScore: any = ref(null)
const score:any = ref(null)


const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
  }, 8000)
}

watch(()=>userAuthStore.teacherData.studentsWithExams, (newValue, oldValue)=>{
  if (newValue){
    const className = elementsStore.activePage.split(',')[1]
    const subjectName = elementsStore.activePage.split(',')[2]
    const exams = newValue.find(item => item['class_name'] === className)
    if (exams){
      const examIndex = newValue.indexOf(exams)
      const examSubject = newValue[examIndex]['exams'].find(item => item['subject'] === subjectName)
      examSubject ? userAuthStore.teacherData.currentExams = examSubject : null
    }
  }
})

const deleteExam = async(st_id:string)=>{
  elementsStore.ShowLoadingOverlay()
  // Get the student's class and subject and append data to the formData
  const className = elementsStore.activePage.split(',')[1]
  const subjectName = elementsStore.activePage.split(',')[2]
  const formData = new FormData()
  formData.append('type', 'deleteExam')
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('studentId', st_id); 
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  await axiosInstance.post('teacher/exams', formData)
  .then(response =>{
    // Find the student in the current Exams list
    const _student = userAuthStore.teacherData.currentExams['students'].find(item => item['st_id'] === st_id)
    
    if (_student){
      // Remove the student from the list
      const _studentIndex = userAuthStore.teacherData.currentExams['students'].indexOf(_student)
      userAuthStore.teacherData.currentExams['students'].splice(_studentIndex, 1)
      
      // Move the student to the 'studentsWithoutExams' list 
      const _exams = userAuthStore.teacherData.studentsWithoutExams.find(item => item['class_name'] === className)
      if (_exams){
        const examsIndex = userAuthStore.teacherData.studentsWithoutExams.indexOf(_exams)
        const examsSubject = _exams['exams'].find(item => item['subject'] === subjectName)
        if (examsSubject){
          const examsSubjectIndex = _exams['exams'].indexOf(examsSubject)
          userAuthStore.teacherData.studentsWithoutExams[examsIndex]['exams'][examsSubjectIndex]['students'].unshift(_student)
        }
      }
    }
    closeOverlay()
    elementsStore.HideLoadingOverlay()
    })
  .catch(error =>{
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError){
      if(error.response){
        if (error.response.status === 400 && error.response.data.message){
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        }else{
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else{
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  })
}

const editExamScore = async()=>{
  formErrorMessage.value = ''

  if (100 >= score.value && score.value >=0){

    // Get the student's class and subject and append data to the formData
    const className = elementsStore.activePage.split(',')[1]
    const subjectName = elementsStore.activePage.split(',')[2]
    const formData = new FormData()
    formData.append('score', score.value);
    formData.append('type', 'editExamScore');
    formData.append('studentsClassName', className);
    formData.append('subject', subjectName);
    formData.append('studentId', studentId.value); 
    formData.append('year', userAuthStore.activeAcademicYear);
    formData.append('term', userAuthStore.activeTerm.toString());
    elementsStore.ShowLoadingOverlay()

    await axiosInstance.post('teacher/exams', formData)
    .then(response =>{
      // Find the student in the current Exams list
      const _student = userAuthStore.teacherData.currentExams['students'].find(item => item['st_id'] === studentId.value)
      
      if (_student){
        // Change the student's exams score and sort the list
        const _studentIndex = userAuthStore.teacherData.currentExams['students'].indexOf(_student)
        userAuthStore.teacherData.currentExams['students'][_studentIndex]['score'] = score.value
        userAuthStore.teacherData.currentExams['students'].sort((a, b) => b.score - a.score)
      }
      closeOverlay()
      elementsStore.HideLoadingOverlay()
    })
    .catch(error =>{
      elementsStore.HideLoadingOverlay()
      if (error instanceof AxiosError){
        if(error.response){
          if (error.response.status === 400 && error.response.data.message){
            elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
          }else{
            elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
          }
        }
        else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
          elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
        }
        else{
          elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
        }
      }
    })
  }else{
    if (score.value <0){
      formErrorMessage.value = 'The exam score cannot be negative'
    }
    else if (score.value >100){
      formErrorMessage.value = 'The exam score cannot be more than 100'
    }
    clearMessage()
    return;
  }
}

const closeOverlay = ()=>{
  score.value = null
  formErrorMessage.value = ''
  studentId.value = ''
  studentName.value = ''
  previousScore.value = null
  const overlay = document.getElementById('TeacherStudentsExamsEdit')
  overlay ? overlay.style.display = 'none' : null
}

const showForm = (stName: string, stId: string, prevScore: number)=>{
  studentId.value = stId
  studentName.value = stName
  previousScore.value = prevScore
  const formOverlay = document.getElementById('TeacherStudentsExamsEdit')
  formOverlay ? formOverlay.style.display = 'flex' : null
}


</script>

<template>
  <div class="content-wrapper">
    <div id="TeacherStudentsExamsEdit" class="overlay" v-if="userAuthStore.teacherData.currentExams && userAuthStore.teacherData.currentExams['students'].length > 0">
        <form style="position: relative" class="overlay-form">
            <v-btn @click.prevent="closeOverlay" class="close-btn" size="small" variant="flat" color="red">X</v-btn>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            
            <h2 class="info"><strong>CLASS:</strong> {{elementsStore.activePage.split(',')[1]}}</h2>
            <h2 class="info"><strong>SUBJECT:</strong> {{elementsStore.activePage.split(',')[2]}}</h2>
            <h2 class="info"><strong>STUDENT:</strong> {{studentName}} [{{studentId}}]</h2>
            <h2 class="info" v-if="previousScore"><strong>PREVIOUS SCORE:</strong> {{previousScore}}</h2>
            <v-text-field v-model="score" type="number" class="input-field" density="comfortable" persistent-hint hint="Enter the student's new score" label="NEW SCORE" variant="outlined"/>
            <v-btn :disabled="!score" @click.prevent="editExamScore()" type="submit" color="green" variant="flat" size="small" class="mt-10 mb-3">SUBMIT</v-btn>
        </form>
    </div>
      
    <TheLoader v-if="!userAuthStore.teacherData.studentsWithExams" />
    <h4 class="no-data" v-if="!userAuthStore.teacherData.currentExams || userAuthStore.teacherData.currentExams && userAuthStore.teacherData.currentExams['students'].length === 0">
      <p>NO DATA</p>
    </h4>
    <div class="info-wrapper" v-if="userAuthStore.teacherData.currentExams && userAuthStore.teacherData.currentExams['students'].length > 0">
      {{ userAuthStore.teacherData.currentExams['subject'] }} EXAMS DATA
    </div>
    <v-table fixed-header class="table" v-if="userAuthStore.teacherData.currentExams && userAuthStore.teacherData.currentExams['students'].length > 0">
      <thead>
      <tr>
        <th class="table-head">NAME</th>
        <th class="table-head">SCORE</th>
        <th class="table-head">ACTION</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in userAuthStore.teacherData.currentExams['students']" :key="index">
          <td class="table-data">
            {{ st['name'] }}
            <v-list-item-subtitle>{{ st['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn @click="showForm(st['name'], st['st_id'], st['score'])" size="small" variant="flat" color="black">{{ st['score'] }}</v-btn>
          </td>
          <td class="table-data">
            <v-btn @click="deleteExam(st['st_id'])" icon="mdi-delete" variant="flat" size="x-small" color="red"/>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

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
.info{
  font-size: .7rem;
  text-align: center;
  margin: .5em 0;
  color: seagreen;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.info strong{
  font-size: .8rem;
  color: black;
}
.input-field{
  margin-top: 1em;
}
.submit-btn{
  font-weight: bold;
  margin-top: 2em;
  margin-bottom: .5em;
}



</style>
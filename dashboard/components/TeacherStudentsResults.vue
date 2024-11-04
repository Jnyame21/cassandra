
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  className: string;
  classIndex: number;
  subjectName: string;
  subjectIndex: number;
  resultData: {
    'subject': string;
    'total_assessment_percentage': any;
    'exam_percentage': any;
    'student_results': {
      'remark': string;
      'grade': string;
      'result': any;
      'student': {'name': string, 'st_id': string}
    }[];
  }
}
const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const subjectName = props.subjectName
const subjectIndex = props.subjectIndex || 0
const resultData = props.resultData

const deleteResults = async()=>{
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'deleteResults')
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try{
    const response = await axiosInstance.post('teacher/students-result', formData)
    userAuthStore.teacherData.studentsResults[classIndex]['results'][subjectIndex]['total_assessment_percentage'] = 0
    userAuthStore.teacherData.studentsResults[classIndex]['results'][subjectIndex]['exam_percentage'] = 0
    userAuthStore.teacherData.studentsResults[classIndex]['results'][subjectIndex]['student_results'] = [] 
    elementsStore.HideLoadingOverlay()
  }
  catch (error){
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
  }
}

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherStudentsResults,${className},${subjectName},${subjectIndex}`" :class="{'is-active-page': elementsStore.activePage === `TeacherStudentsResults,${className},${subjectName},${subjectIndex}`}" >
    <div class="no-data" v-if="resultData['student_results']?.length === 0">
      <p>NO DATA</p>
    </div>
    <div class="content-header" v-if="resultData['student_results']?.length > 0">
      <span class="content-header-title">{{ className }} {{ subjectName }} STUDENT RESULTS</span>
    </div>
    <div class="content-header" v-if="resultData['student_results']?.length > 0">
        <h4 class="content-header-text">TOTAL ASSESSMENT PERCENTAGE: <span class="content-header-text-value">{{ resultData['total_assessment_percentage'] }}</span></h4>
        <h4 class="content-header-text">PERCENTAGE OF EXAMS: <span class="content-header-text-value">{{ resultData['exam_percentage'] }}</span></h4>
    </div>
    <div class="content-header btn-container" v-if="resultData['student_results']?.length > 0">
      <v-btn @click="elementsStore.ShowDeletionOverlay(()=>deleteResults(), `Are you sure you want to delete all the ${subjectName} results data you have uploaded for this class? You will be redirected to the ${className} class when the process is complete`)" color="red" size="small" append-icon="mdi-delete" varaint="flat" >DELETE RESULTS</v-btn>
    </div>
    <v-table fixed-header class="table" v-if="resultData['student_results']?.length > 0">
      <thead>
      <tr>
        <th class="table-head">NAME</th>
        <th class="table-head">SCORE</th>
        <th class="table-head">GRADE</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in resultData['student_results']" :key="index">
          <td class="table-data">
            {{ st['student']['name'] }}
            <v-list-item-subtitle>{{ st['student']['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">
              {{ Number(st['result']) }}
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn variant="flat" size="small" :color="getGradeColor(st['grade'])">
                {{ st['grade'] }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header{
  height: 10% !important;
}
.table{
  height: 70% !important;
}

@media screen and (min-width: 400px) {
  .content-header-text{
    font-size: .75rem !important;
  }
}
@media screen and (min-width: 576px) {
  .content-header-title{
    font-size: .9rem !important;
  }
  .content-header-text{
    font-size: .8rem !important;
  }
}
@media screen and (min-width: 767px) {
  .content-header-title{
    font-size: 1rem !important;
  }
  .content-header-text{
    font-size: .85rem !important;
  }
}
@media screen and (min-width: 1000px) {
  .content-header-title{
    font-size: .9rem !important;
  }
  .content-header-text{
    font-size: .9rem !important;
  }
}
@media screen and (min-width: 1200px) {
  .content-header-title{
    font-size: 1.1rem !important;
  }
  .content-header-text{
    font-size: 1rem !important;
  }
}



</style>
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, defineProps } from 'vue'
import { getGradeColor } from '@/utils/util';
import NoData from '@/components/NoData.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  className: string;
  subjectName: string;
}
const props = defineProps<Props>()
const className = props.className
const subjectName = props.subjectName

const resultData =  computed(()=>{
  return userAuthStore.teacherData.studentsResults[className][subjectName]
})

const deleteResults = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'deleteResults')
  formData.append('studentsClassName', className);
  formData.append('subject', subjectName);
  formData.append('year', userAuthStore.activeAcademicYear);
  formData.append('term', userAuthStore.activeTerm.toString());

  try {
    await axiosInstance.post('teacher/students-result', formData)
    userAuthStore.teacherData.studentsResults[className][subjectName] = {
      'total_assessment_percentage': 0,
      'exam_percentage': 0,
      'student_results': {}
    }
    if (Object.keys(userAuthStore.teacherData.studentsAssessments?.[className]?.[subjectName] || {}).length > 0) {
      Object.values(userAuthStore.teacherData.studentsAssessments[className][subjectName]).forEach(item => {
      item.percentage = 0
    })
    }
    if (Object.keys(userAuthStore.teacherData.studentsExams?.[className]?.[subjectName] || {}).length > 0) {
      userAuthStore.teacherData.studentsExams[className][subjectName].percentage = 0
    }
    
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

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `TeacherStudentsResults,${className},${subjectName}`" :class="{ 'is-active-page': elementsStore.activePage === `TeacherStudentsResults,${className},${subjectName}` }">
    <NoData message="You have not generated students results yet" v-if="Object.keys(resultData.student_results).length === 0"/>
    <div class="content-header" v-if="Object.keys(resultData.student_results).length > 0">
      <span class="content-header-title">{{ className }} STUDENT RESULTS ({{ subjectName }})</span>
    </div>
    <div class="content-header btn-container" v-if="Object.keys(resultData.student_results).length > 0">
      <v-btn
        @click="elementsStore.ShowDeletionOverlay(() => deleteResults(), `Are you sure you want to delete all the ${subjectName} results data you have uploaded for this class?`)"
        color="red" :size="elementsStore.btnSize1" append-icon="mdi-delete" varaint="flat">DELETE RESULTS</v-btn>
    </div>
    <v-table fixed-header class="table" v-if="Object.keys(resultData.student_results).length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">ASSESSMENTS({{ resultData.total_assessment_percentage }}%)</th>
          <th class="table-head">EXAMS({{ resultData.exam_percentage }}%)</th>
          <th class="table-head">TOTAL</th>
          <th class="table-head">POSITION</th>
          <th class="table-head">GRADE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in Object.values(resultData.student_results || {}).sort((a, b)=> b.result - a.result)" :key="index">
          <td class="table-data">
            {{ st.student.name }}
            <v-list-item-subtitle>{{ st.student.st_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">
              {{ Number(st.total_assessment_score) }}
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">
              {{ Number(st.exam_score) }}
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">
              {{ Number(st.result) }}
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">
              {{ st.position }}
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn variant="flat" size="small" :color="getGradeColor(st.grade)">
              {{ st.grade }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 15% !important;
}

.btn-container {
  min-height: 10% !important;
}

.table {
  height: 75% !important;
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
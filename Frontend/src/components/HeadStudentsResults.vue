<script setup lang="ts">
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
  return userAuthStore.headData.studentsResults[className][subjectName]
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStudentsResults,${className},${subjectName}`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStudentsResults,${className},${subjectName}` }">
    
    <NoData message="NO DATA" v-if="Object.keys(resultData.student_results).length === 0"/>
    <div class="content-header" v-if="Object.keys(resultData.student_results).length > 0">
      <span class="content-header-title">{{ className }} STUDENT RESULTS ({{ subjectName }})</span>
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
            <v-btn size="small" variant="flat" color="black">{{ Number(st.total_assessment_score) }}</v-btn>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">{{ Number(st.exam_score) }}</v-btn>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">{{ Number(st.result) }}</v-btn>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">{{ st.position }}</v-btn>
          </td>
          <td class="table-data">
            <v-btn variant="flat" size="small" :color="getGradeColor(st.grade)">{{ st.grade }}</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header{
    min-height: 15% !important;
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
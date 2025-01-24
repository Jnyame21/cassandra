<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed } from 'vue';
import NoData from './NoData.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  yearName: string
  termName: string
}

const props = defineProps<Props>()
const yearName = props.yearName
const termName = props.termName

const resultsData = computed(()=>{
  return userAuthStore.studentData.results[yearName][termName]
})


</script>

<template>
<div class="content-wrapper" v-show="elementsStore.activePage === `StudentResults,${yearName},${termName}`"
:class="{ 'is-active-page': elementsStore.activePage === `StudentResults,${yearName},${termName}`}">
  <NoData v-if="resultsData.length === 0" :message="`Results for the ${yearName} academic year ${termName} has not been released yet`" />
  <div v-if="resultsData.length > 0" class="content-header">
    {{ yearName }} {{ termName }} RESULTS
  </div>
  <v-table v-if="resultsData.length > 0" fixed-header class="table">
    <thead>
    <tr>
      <th class="table-head">SUBJECT</th>
      <th class="table-head">ASSESSMENTS</th>
      <th class="table-head">EXAMS</th>
      <th class="table-head">TOTAL</th>
      <th class="table-head">GRADE</th>
      <th class="table-head">REMARK</th>
      <th class="table-head">POSITION</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(result, i) in resultsData" :key="i">
      <td class="table-data">{{result.subject}}</td>
      <td class="table-data">{{result.total_assessment_score}}/{{ result.total_assessment_percentage }}</td>
      <td class="table-data">{{result.exam_score}}/{{ result.exam_percentage }}</td>
      <td class="table-data">{{result.result}}</td>
      <td class="table-data">{{result.grade.label}}</td>
      <td class="table-data">{{result.grade.remark}}</td>
      <td class="table-data">{{result.position}}</td>
    </tr>
    </tbody>
  </v-table>
</div>
</template>

<style scoped>


</style>
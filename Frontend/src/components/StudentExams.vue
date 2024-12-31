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

const examsData = computed(()=>{
  return userAuthStore.studentData.exams[yearName][termName]
})


</script>

<template>
<div class="content-wrapper" v-show="elementsStore.activePage === `StudentExams,${yearName},${termName}`"
:class="{ 'is-active-page': elementsStore.activePage === `StudentExams,${yearName},${termName}`}">
  <NoData v-if="examsData.length === 0" message="No exams data yet"/>
  <div v-if="examsData.length > 0" class="content-header">
    {{ yearName }} {{ termName }} EXAMS
  </div>
  <v-table v-if="examsData.length > 0" fixed-header class="table">
    <thead>
    <tr>
      <th class="table-head">SUBJECT</th>
      <th class="table-head">SCORE</th>
      <th class="table-head">TOTAL SCORE</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(exams, i) in examsData" :key="i">
      <td class="table-data">{{exams.subject}}</td>
      <td class="table-data">{{exams.score}}</td>
      <td class="table-data">{{exams.total_score}}</td>
    </tr>
    </tbody>
  </v-table>
</div>
</template>

<style scoped>


</style>
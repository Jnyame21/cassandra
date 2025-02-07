<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
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

const assessmentData = computed(()=>{
  return userAuthStore.studentData.assessments[yearName][termName]
})

</script>

<template>
  
  
<div class="content-wrapper" v-show="elementsStore.activePage === `StudentAssessments,${yearName},${termName}`" :class="{ 'is-active-page': elementsStore.activePage === `StudentAssessments,${yearName},${termName}`}">
  <NoData v-if="assessmentData.length === 0" :message="`No assessment record has been uploaded yet for the ${yearName} academic year ${termName}`"/>
  <div v-if="assessmentData.length > 0" class="content-header">
    {{ yearName }} {{ termName }} ASSESSMENTS
  </div>
  <v-table v-if="assessmentData.length > 0" fixed-header class="table">
    <thead>
    <tr>
      <th class="table-head">SUBJECT</th>
      <th class="table-head">TITLE</th>
      <th class="table-head">DESCRIPTION</th>
      <th class="table-head">SCORE</th>
      <th class="table-head">COMMENT</th>
      <th class="table-head">DATE</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(assessments, i) in assessmentData" :key="i">
      <td class="table-data">{{assessments.subject}}</td>
      <td class="table-data">{{assessments.title}}</td>
      <td class="table-data">{{assessments.description}}</td>
      <td class="table-data">{{assessments.score}}</td>
      <td class="table-data">{{assessments.comment}}</td>
      <td class="table-data">{{assessments.assessment_date}}</td>
    </tr>
    </tbody>
  </v-table>
</div>
</template>

<style scoped>


</style>
<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


</script>

<template>
  
  
<div class="content-wrapper">
  <TheLoader v-if="!userAuthStore.studentData.academicYearsData"/>
  <h4 class="no-data" v-if="userAuthStore.studentData.currentAssessments?.length === 0">
    <p>No assessment record has been uploaded yet for the {{ elementsStore.activePage.split(',')[1] }} academic year {{ elementsStore.activePage.split(',')[2] }} {{ elementsStore.activePage.split(',')[3] }}</p>
  </h4>
  <div v-if="userAuthStore.studentData.currentAssessments?.length > 0" class="content-header">
    {{ elementsStore.activePage.split(',')[1] }} {{ elementsStore.activePage.split(',')[2] }} {{ elementsStore.activePage.split(',')[3] }} ASSESSMENTS
  </div>
  <v-table v-if="userAuthStore.studentData.currentAssessments?.length > 0" fixed-header class="table">
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
    <tr v-for="(assessments, i) in userAuthStore.studentData.currentAssessments" :key="i">
      <td class="table-data">{{assessments['subject']}}</td>
      <td class="table-data">{{assessments['title']}}</td>
      <td class="table-data">{{assessments['description']}}</td>
      <td class="table-data">{{assessments['score']}}</td>
      <td class="table-data">{{assessments['comment']}}</td>
      <td class="table-data">{{assessments['date']}}</td>
    </tr>
    </tbody>
  </v-table>
</div>
</template>

<style scoped>


</style>
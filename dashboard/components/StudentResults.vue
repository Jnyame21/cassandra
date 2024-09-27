<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


</script>

<template>
<div class="content-wrapper">
  <TheLoader v-if="!userAuthStore.studentData.academicYearsData"/>
  <h4 class="no-data" v-if="userAuthStore.studentData.currentResults?.length === 0">
    <p>Results for the {{ elementsStore.activePage.split(',')[1] }} academic year {{ elementsStore.activePage.split(',')[2] }} {{ elementsStore.activePage.split(',')[3] }} has not been released yet</p>
  </h4>
  <div v-if="userAuthStore.studentData.currentResults?.length > 0" class="info-wrapper">
    {{ elementsStore.activePage.split(',')[1] }} {{ elementsStore.activePage.split(',')[2] }} {{ elementsStore.activePage.split(',')[3] }} RESULTS
  </div>
  <v-table v-if="userAuthStore.studentData.currentResults?.length > 0" fixed-header class="table">
    <thead>
    <tr>
      <th class="table-head">SUBJECT</th>
      <th class="table-head">SCORE</th>
      <th class="table-head">GRADE</th>
      <th class="table-head">REMAKR</th>
      <th class="table-head">POSITION</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(result, i) in userAuthStore.studentData.currentResults" :key="i">
      <td class="table-data">{{result['subject']}}</td>
      <td class="table-data">{{result['score']}}</td>
      <td class="table-data">{{result['grade']['label']}}</td>
      <td class="table-data">{{result['grade']['remark']}}</td>
      <td class="table-data">{{result['position']}}</td>
    </tr>
    </tbody>
  </v-table>
</div>
</template>

<style scoped>


</style>
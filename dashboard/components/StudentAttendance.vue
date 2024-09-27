<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


</script>

<template>
  <div class="content-wrapper">
    <TheLoader v-if="!userAuthStore.studentData.academicYearsData"/>
    <h4 class="no-data" v-if="userAuthStore.studentData.currentAttendance?.length === 0">
      <p>No attendance has been uploaded yet for the {{ elementsStore.activePage.split(',')[1] }} academic year {{ elementsStore.activePage.split(',')[2] }} {{ elementsStore.activePage.split(',')[3] }}</p>
    </h4>
    <div v-if="userAuthStore.studentData.currentAttendance?.length > 0" class="info-wrapper">
      {{ elementsStore.activePage.split(',')[1] }} {{ elementsStore.activePage.split(',')[2] }} {{ elementsStore.activePage.split(',')[3] }} ATTENDANCE
    </div>
    <v-table v-if="userAuthStore.studentData.currentAttendance?.length > 0" fixed-header class="table">
      <thead>
      <tr>
        <th class="table-head">DATE</th>
        <th class="table-head">ATTENDANCE STATUS</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(attendance, i) in userAuthStore.studentData.currentAttendance" :key="i">
        <td class="table-data">{{attendance['date']}}</td>
        <td class="table-data" style="color: green;" v-if="attendance['status'] === 'PRESENT' ">{{attendance['status']}}</td>
        <td class="table-data" style="color: red;" v-if="attendance['status'] === 'ABSENT' ">{{attendance['status']}}</td>
      </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

</style>
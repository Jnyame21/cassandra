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

const attendanceData = computed(()=>{
  return userAuthStore.studentData.attendances[yearName][termName]
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `StudentAttendance,${yearName},${termName}`" :class="{ 'is-active-page': elementsStore.activePage === `StudentAttendance,${yearName},${termName}`}">
    <NoData v-if="attendanceData.length === 0" :message="`No attendance has been uploaded yet for the ${yearName} academic year ${termName}`"/>
    <div v-if="attendanceData.length > 0" class="content-header">
      {{ yearName }} ACADEMIC YEAR {{ termName }} ATTENDANCE
    </div>
    <v-table v-if="attendanceData.length > 0" fixed-header class="table">
      <thead>
      <tr>
        <th class="table-head">DATE</th>
        <th class="table-head">ATTENDANCE STATUS</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(attendance, i) in attendanceData" :key="i">
        <td class="table-data">{{attendance.date}}</td>
        <td class="table-data" style="color: green;" v-if="attendance.status === 'PRESENT' ">{{attendance.status}}</td>
        <td class="table-data" style="color: red;" v-if="attendance.status === 'ABSENT' ">{{attendance.status}}</td>
      </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>


</style>
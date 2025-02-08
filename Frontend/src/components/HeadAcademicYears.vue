<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed } from 'vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const academicYearsData = computed(()=>{
  return userAuthStore.headData.academicYears
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'HeadAcademicYears'" :class="{ 'is-active-page': elementsStore.activePage === 'HeadAcademicYears' }">
    <div class="content-header"></div>
    <div v-if="academicYearsData.length === 0 " class="no-data">NO DATA</div>
    <v-table fixed-header class="table" v-if="academicYearsData.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">START DATE</th>
          <th class="table-head">END DATE</th>
          <th class="table-head">{{ userAuthStore.userData['academic_year']['period_division'] }} 1 END DATE</th>
          <th class="table-head">{{ userAuthStore.userData['academic_year']['period_division'] }} 2 START DATE</th>
          <th class="table-head">{{ userAuthStore.userData['academic_year']['period_division'] }} 2 END DATE</th>
          <th class="table-head" v-if="userAuthStore.userData['academic_year']['no_divisions'] === 3">{{userAuthStore.userData['academic_year']['period_division'] }} 3 START DATE</th>
          <th class="table-head" v-if="userAuthStore.userData['academic_year']['no_divisions'] === 3">{{userAuthStore.userData['academic_year']['period_division'] }} 3 END DATE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_year, index) in academicYearsData" :key="index">
          <td class="table-data">{{ _year.name }}</td>
          <td class="table-data">{{ _year.start_date }}</td>
          <td class="table-data">{{ _year.end_date }}</td>
          <td class="table-data">{{ _year.term_1_end_date }}</td>
          <td class="table-data">{{ _year.term_2_start_date }}</td>
          <td class="table-data">{{ _year.term_2_end_date }}</td>
          <td class="table-data" v-if="userAuthStore.userData['academic_year']['no_divisions'] === 3 && _year.term_3_start_date">{{ _year.term_3_start_date }}</td>
          <td class="table-data" v-if="userAuthStore.userData['academic_year']['no_divisions'] === 3 && _year.term_3_end_date">{{ _year.term_3_end_date }}</td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>


</style>
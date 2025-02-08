<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const releasedResults = computed(() => {
  return userAuthStore.headData.releasedResults
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'HeadReleasedResults'" :class="{ 'is-active-page': elementsStore.activePage === 'HeadReleasedResults' }">
   
    <div class="content-header"></div>
    <div class="no-data" v-if="releasedResults.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="releasedResults.length > 0">
      <thead>
        <tr>
          <th class="table-head">CLASS</th>
          <th class="table-head">ACADEMIC YEAR</th>
          <th class="table-head">{{ userAuthStore.userData['academic_year']['period_division'] }}</th>
          <th class="table-head">DATE</th>
          <th class="table-head">RELEASED BY</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(release, index) in releasedResults" :key="index">
          <td class="table-data">{{ release.students_class_name }}</td>
          <td class="table-data">{{ release.academic_year }}</td>
          <td class="table-data">{{ release.academic_term }}</td>
          <td class="table-data">{{ release.date }}</td>
          <td class="table-data">{{ release.released_by }}</td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>



</style>
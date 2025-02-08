<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const subjectAssignments = computed(() => {
  return userAuthStore.headData.subjectAssignments
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'HeadSubjectAssignments'" :class="{ 'is-active-page': elementsStore.activePage === 'HeadSubjectAssignments' }">
   
    <div class="content-header" v-if="subjectAssignments.length > 0"></div>
    <div class="no-data" v-if="subjectAssignments.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="subjectAssignments.length > 0">
      <thead>
        <tr>
          <th class="table-head">TEACHER</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">SUBJECT(S)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_assign, index) in subjectAssignments" :key="index">
          <td class="table-data">
            {{ _assign['teacher']['user'] }}
            <v-list-item-subtitle>{{ _assign['teacher']['staff_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            {{ _assign['students_class'] }}
          </td>
          <td class="table-data">
            <p v-for="(_subject, ind) in _assign['subjects']" :key="ind">{{ _subject }}</p>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>


</style>
<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { defineProps } from 'vue'
import { computed } from 'vue'
import NoData from '@/components/NoData.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  className: string;
  subjectName: string;
}
const props = defineProps<Props>()
const className = props.className
const subjectName = props.subjectName

const examsData = computed(()=>{
  return userAuthStore.headData.studentsExams[className][subjectName]
})

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStudentsExams,${className},${subjectName}`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStudentsExams,${className},${subjectName}` }">
    
    <div class="content-header" v-if="Number(examsData.total_score) > 0">
      <h4 class="content-header-title">{{ className }} {{ subjectName }} EXAMS</h4>
    </div>
    <div class="content-header" v-if="Number(examsData.total_score) > 0">
      <h4 class="content-header-text">
        TOTAL SCORE:
        <span class="content-header-text-value">{{ examsData.total_score }}</span>
      </h4>
      <h4 class="content-header-text" v-if="Number(examsData.percentage) > 0">
        PERCENTAGE: <span class="content-header-text-value">{{ examsData.percentage }}%</span></h4>
    </div>
    <NoData v-if="Object.keys(examsData.students_with_exams).length === 0" />
    <v-table fixed-header class="table" v-if="Object.keys(examsData.students_with_exams).length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">SCORE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in Object.values(examsData.students_with_exams).sort((a, b)=> b.score - a.score)" :key="index">
          <td class="table-data">
            {{ st.name }}
            <v-list-item-subtitle>{{ st.st_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn size="small" variant="flat" color="black">{{ st.score }}</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.info-text,
.info-text-value {
  font-size: .75rem !important;
}



</style>
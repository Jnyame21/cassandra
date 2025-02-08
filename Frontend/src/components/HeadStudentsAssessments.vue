<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { defineProps } from 'vue'
import { computed } from 'vue'

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  className: string;
  subjectName: string;
  assessmentTitle: string;
}

const props = defineProps<Props>()
const className = props.className
const subjectName = props.subjectName
const assessmentTitle = props.assessmentTitle

const assessmentData = computed(()=>{
  return userAuthStore.headData.studentsAssessments[className][subjectName][assessmentTitle]
})



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStudentsAssessments,${className},${subjectName},${assessmentTitle}`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStudentsAssessments,${className},${subjectName},${assessmentTitle}` }">
    
    <div class="content-header">
      <div class="content-header-text">
        TITLE: <span class="content-header-text-value">{{ assessmentTitle }}</span>
      </div>
      <div class="content-header-text">
        DESCRIPTION: <span class="content-header-text-value">{{ assessmentData.description }}</span>
      </div>
      <div class="content-header-text">
        TOTAL SCORE: <span class="content-header-text-value">{{ assessmentData.total_score }}</span>
      </div>
      <div class="content-header-text" v-if="assessmentData.percentage !== 0">
        PERCENTAGE: <span class="content-header-text-value">{{ assessmentData.percentage }}%</span>
      </div>
      <div class="content-header-text">
        DATE: <span class="content-header-text-value">{{ assessmentData.assessment_date }}</span>
      </div>
    </div>
    <h4 class="no-data" v-if="Object.keys(assessmentData.students_with_assessment || {}).length === 0">
      <p>NO DATA</p>
    </h4>
    <v-table fixed-header class="table" v-if="Object.keys(assessmentData.students_with_assessment || {}).length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">SCORE</th>
          <th class="table-head">COMMENT</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(st, index) in Object.values(assessmentData.students_with_assessment).sort((a, b)=> b.score - a.score)" :key="index">
          <td class="table-data">
            {{ st.name }}
            <v-list-item-subtitle>{{ st.st_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            <v-btn size="small" color="black" variant="flat">{{ st.score }}</v-btn>
          </td>
          <td class="table-data st-comment">
            {{ st.comment }}
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 25% !important;
}

.st-comment {
  text-transform: none !important;
}
.info-text,
.info-text-value {
  font-size: .75rem !important;
}

@media screen and (min-width: 400px) {
  .overlay-card {
    width: 95% !important;
  }

  .info-text,
  .info-text-value {
    font-size: .8rem !important;
  }
}

@media screen and (min-width: 576px) {
  .content-header-text {
    font-size: .75rem !important;
  }

  .info-text,
  .info-text-value {
    font-size: .85rem !important;
  }
}

@media screen and (min-width: 767px) {
  .content-header-text {
    font-size: .8rem !important;
  }

  .info-text,
  .info-text-value {
    font-size: .9rem !important;
  }
}

@media screen and (min-width: 992px) {}

@media screen and (min-width: 1200px) {
  .content-header-text {
    font-size: .9rem !important;
  }

  .info-text,
  .info-text-value {
    font-size: 1rem !important;
  }
}


</style>
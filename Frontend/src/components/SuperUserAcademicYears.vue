<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const academicYearName = ref('')
const periodDivision = ref('')
const noDivisions = ref('')
const startDate = ref('')
const endDate = ref('')
const termOneEndDate = ref('')
const termTwoStartDate = ref('')
const termTwoEndDate = ref('')
const termThreeStartDate = ref('')
const termThreeEndDate = ref('')
const studentsGraduationDate = ref('')
const academicYearLevelIdentifer = ref('')

interface Props {
  schoolIdentifier: string;
}
const props = defineProps<Props>()
const schoolIdentifier = props.schoolIdentifier

const academicYears = computed(() => {
  return userAuthStore.superUserData.academicYears[schoolIdentifier]
})

const createAcademicYear = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', academicYearName.value);
  formData.append('levelIdentifier', academicYearLevelIdentifer.value);
  formData.append('schoolIdentifier', schoolIdentifier);
  formData.append('startDate', startDate.value);
  formData.append('endDate', endDate.value);
  formData.append('termOneEndDate', termOneEndDate.value);
  formData.append('termTwoStartDate', termTwoStartDate.value);
  formData.append('termTwoEndDate', termTwoEndDate.value);
  formData.append('termThreeStartDate', termThreeStartDate.value);
  formData.append('termThreeEndDate', termThreeEndDate.value);
  formData.append('periodDivision', periodDivision.value);
  formData.append('noDivisions', noDivisions.value);
  formData.append('studentsGraduationDate', studentsGraduationDate.value);

  try {
    const response = await axiosInstance.post('superuser/academic_years', formData)
    userAuthStore.superUserData.academicYears[schoolIdentifier].unshift(response.data)
    academicYearName.value = ''
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful!', 'green', null, null)
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const deleteAcademicYear = async (index: number, academic_year_id: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', academic_year_id);

  try {
    await axiosInstance.post('superuser/academic_years', formData)
    userAuthStore.superUserData.academicYears[schoolIdentifier].splice(index, 1)
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}


const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `SuperUserAcademicYears,${schoolIdentifier}`"
    :class="{ 'is-active-page': elementsStore.activePage === `SuperUserAcademicYears,${schoolIdentifier}` }">

    <!-- academicYear creation overlay -->
    <div :id="`SuperUserCreateAcademicYearOverlay,${schoolIdentifier}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserCreateAcademicYearOverlay,${schoolIdentifier}`)" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="academicYearName" label="NAME" clearable />
          <v-select class="select"
            :items="userAuthStore.superUserData.levels.filter(item => item.schools.includes(schoolIdentifier)).map(item => item.identifier)"
            label="LEVEL" v-model="academicYearLevelIdentifer" density="comfortable" persistent-hint
            hint="Select the level" variant="solo-filled" clearable />
          <v-text-field class="input-field" v-model="startDate" type="date" label="START DATE" clearable />
          <v-text-field class="input-field" v-model="endDate" type="date" label="END DATE" clearable />
          <v-text-field class="input-field" v-model="studentsGraduationDate" type="date"
            label="EXPECTED FINAL YEAR STUDENTS GRADUATION DATE" clearable />
          <v-select class="select" :items="['2', '3']" label="NUMBER OF DIVISIONS" v-model="noDivisions"
            density="comfortable" persistent-hint hint="Select the number of divisions in the academic year"
            variant="solo-filled" clearable />
          <v-select class="select" v-if="noDivisions === '2'" :items="['TERM', 'SEMESTER']" label="PERIOD DIVISION NAME"
            v-model="periodDivision" density="comfortable" persistent-hint hint="What name do you call each division"
            variant="solo-filled" clearable />
          <v-select class="select" v-if="noDivisions === '3'" :items="['TERM', 'TRIMESTER']"
            label="PERIOD DIVISION NAME" v-model="periodDivision" density="comfortable" persistent-hint
            hint="What name do you call each division" variant="solo-filled" clearable />
          <v-text-field class="input-field" v-if="periodDivision" v-model="termOneEndDate" type="date"
            :label="`${periodDivision} 1 END DATE`" clearable />
          <v-text-field class="input-field" v-if="periodDivision" v-model="termTwoStartDate" type="date"
            :label="`${periodDivision} 2 START DATE`" clearable />
          <v-text-field class="input-field" v-if="periodDivision" v-model="termTwoEndDate" type="date"
            :label="`${periodDivision} 2 END DATE`" clearable />
          <v-text-field class="input-field" v-if="periodDivision && noDivisions === '3'" v-model="termThreeStartDate"
            type="date" :label="`${periodDivision} 3 END DATE`" clearable />
          <v-text-field class="input-field" v-if="periodDivision && noDivisions === '3'" v-model="termThreeEndDate"
            type="date" :label="`${periodDivision} 3 END DATE`" clearable />
          <v-text-field class="input-field" v-if="periodDivision && noDivisions === '3'" v-model="termThreeEndDate"
            type="date" :label="`${periodDivision} 3 END DATE`" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createAcademicYear" :disabled="!(academicYearName && academicYearLevelIdentifer)"
            :ripple="false" variant="flat" type="submit" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header">
      <v-btn @click="showOverlay(`SuperUserCreateAcademicYearOverlay,${schoolIdentifier}`)" color="blue"
        :size="elementsStore.btnSize1">
        CREATE ACADEMIC YEAR
      </v-btn>
    </div>
    <div class="no-data" v-if="academicYears.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="academicYears.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">START DATE</th>
          <th class="table-head">END DATE</th>
          <th class="table-head">TERM ONE END DATE</th>
          <th class="table-head">TERM TWO START DATE</th>
          <th class="table-head">TERM TWO START DATE</th>
          <th class="table-head">TERM THREE START DATE</th>
          <th class="table-head">TERM THREE END DATE</th>
          <th class="table-head">STUDENTS GRADUATION DATE</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(academicYear, index) in academicYears" :key="index">
          <td class="table-data">{{ academicYear.name }}</td>
          <td class="table-data">{{ academicYear.level }}</td>
          <td class="table-data">{{ academicYear.start_date }}</td>
          <td class="table-data">{{ academicYear.end_date }}</td>
          <td class="table-data">{{ academicYear.term_1_end_date }}</td>
          <td class="table-data">{{ academicYear.term_2_start_date }}</td>
          <td class="table-data">{{ academicYear.term_2_end_date }}</td>
          <td class="table-data">{{ academicYear.term_3_start_date }}</td>
          <td class="table-data">{{ academicYear.term_3_end_date }}</td>
          <td class="table-data">{{ academicYear.students_graduation_date }}</td>
          <td class="table-data flex-all" style="display: flex">
            <v-btn class="ma-2"
              @click="elementsStore.ShowDeletionOverlay(() => deleteAcademicYear(index, academicYear.id.toString()), 'Are you sure you want to delete this academic year. The process cannot be reversed')"
              variant="flat" icon="mdi-delete" size="x-small" color="red" />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.overlay-card {
  max-width: 600px !important;
}

.overlay-card-content-container {
  margin-top: 3em !important;
}
</style>
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const classSelected = ref('')
const academicYearSelected = ref('')
const academicTermSelected = ref('')

const studentClasses = computed(() => {
  return userAuthStore.adminData.classes.map(item=> item.name)
})

const releasedResults = computed(() => {
  return userAuthStore.adminData.releasedResults
})

const academicYears = computed(() => {
  return userAuthStore.adminData.academicYears.map(item=> item.name)
})

const academicYearPeriodDivision = computed(()=>{
  return userAuthStore.adminData.academicYears.find(item=> item.name === academicYearSelected.value)?.period_division || ''
})

const uploadReleasedResults = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'upload')
  formData.append('studentsClassName', classSelected.value);
  formData.append('year', academicYearSelected.value);
  formData.append('term', academicTermSelected.value);

  try {
    const response = await axiosInstance.post('school-admin/released_results', formData)
    userAuthStore.adminData.releasedResults.push(response.data)
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay(`${classSelected.value} students resutls for the ${academicYearSelected.value} ${academicYearPeriodDivision.value} ${academicTermSelected.value} has been released successfully`, 'green', null, null)
    
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

const deleteReleasedResults = async (index: number, released_result_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', released_result_id.toString());
  formData.append('year', userAuthStore.activeAcademicYearID.toString());

  try {
    await axiosInstance.post('school-admin/released_results', formData)
    userAuthStore.adminData.releasedResults.splice(index, 1)
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
  academicYearSelected.value = ''
  academicTermSelected.value = ''
  classSelected.value = ''
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'AdminReleasedResults'" :class="{ 'is-active-page': elementsStore.activePage === 'AdminReleasedResults' }">
   
    <!-- released results upload overlay -->
    <div id="AdminUploadReleasedResultsOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminUploadReleasedResultsOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <v-select clearable chips v-model="academicYearSelected" class="select" label="ACADEMIC YEAR" :items="academicYears" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the academic year">
          </v-select>
          <div v-for="(year, index) in userAuthStore.adminData.academicYears" :key="index">
            <v-select class="select" v-if="year.name === academicYearSelected" :items="[...Array(year.no_divisions)].map((_, i)=> `${ i + 1}`)" :label="year.period_division " v-model="academicTermSelected" variant="solo-filled"
              density="comfortable" persistent-hint :hint="`Select the ${year.period_division}`"
            />
          </div>
          <v-select v-if="academicYearSelected" class="select" :items="studentClasses" label="CLASS" v-model="classSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the class you want to release their results"
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="uploadReleasedResults" :disabled="!(academicYearSelected && academicTermSelected && classSelected)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    
    <div class="content-header">
      <v-btn @click="showOverlay('AdminUploadReleasedResultsOverlay')" color="blue"
        :size="elementsStore.btnSize1">
        RELEASE STUDENTS RESULTS
      </v-btn>
    </div>
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
          <td class="table-data">
            {{ release.students_class_name }}
          </td>
          <td class="table-data">
            {{ release.academic_year }}
          </td>
          <td class="table-data">
            {{ release.academic_term }}
          </td>
          <td class="table-data">
            {{ release.date }}
          </td>
          <td class="table-data">
            {{ release.released_by }}
          </td>
          <td class="table-data">
            <v-btn
              @click="elementsStore.ShowDeletionOverlay(() => deleteReleasedResults(index, release.id), 'Are you sure you want to rollback the released students results?')"
              variant="flat" icon="mdi-delete" size="x-small" color="red" 
            />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.overlay-card{
  max-width: 600px !important;
}
.overlay-card-info-container{
  margin-top: 3em !important;
}


</style>
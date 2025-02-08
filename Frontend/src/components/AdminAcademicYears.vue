<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { ref, computed } from 'vue'
import { AxiosError } from 'axios';
import axiosInstance from '@/utils/axiosInstance';
import { academicYearOptions } from '@/utils/util';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const now = new Date();
const utcDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()))
const startDate = ref(utcDate.toISOString().split('T')[0]); 
const endDate = ref('')
const term1EndDate = ref('')
const term2StartDate = ref('')
const term2EndDate = ref('')
const term3StartDate = ref('')
const term3EndDate = ref('')
const currentEndDate = new Date(userAuthStore.userData['academic_year']['end_date'])
const formErrorMessage = ref('')
const academicYearSelected = ref('')
const academicYearPeriodDivisionSelected: any = ref(null)
const term3DivisionSelected = ref('')
const graduationDate = ref('')
const selectedClass = ref('')
const selectedStudents: any = ref([])

const academicYearsData = computed(()=>{
  return userAuthStore.adminData.academicYears
})

const academicYearPeriodDivisionOptions = [
  { 'label': 2, 'value': 2 },
  { 'label': 3, 'value': 3 },
]
const term3DivisionOptions = [
  { 'label': 'TERM', 'value': 'term' },
  { 'label': 'TRIMESTER', 'value': 'trimester' },
]

const showErrorMessage = (message: string) => {
  formErrorMessage.value = message
  setTimeout(() => {
    formErrorMessage.value = ''
  }, 10000)
}

const createAcademicYear = async () => {
  formErrorMessage.value = ''
  const formData = new FormData
  if (new Date(startDate.value) <= currentEndDate) {
    showErrorMessage('The academic year start date must be greater than the current academic year end date')
    return;
  }
  if (new Date(term1EndDate.value) <= new Date(startDate.value)) {
    const periodDivisionName = academicYearPeriodDivisionSelected.value === 2 ? 'semester' : term3DivisionSelected.value
    showErrorMessage(`${periodDivisionName} 1 end date must be greater than the academic year start date`)
    return;
  }
  if (new Date(term2StartDate.value) <= new Date(term1EndDate.value)) {
    const periodDivisionName = academicYearPeriodDivisionSelected.value === 2 ? 'semester' : term3DivisionSelected.value
    showErrorMessage(`${periodDivisionName} 2 start date must be greater than the ${periodDivisionName} 1 end date`)
    return;
  }
  if (new Date(term2EndDate.value) <= new Date(term2StartDate.value)) {
    const periodDivisionName = academicYearPeriodDivisionSelected.value === 2 ? 'semester' : term3DivisionSelected.value
    showErrorMessage(`${periodDivisionName} 2 end date must be greater than the ${periodDivisionName} 2 start date`)
    return;
  }
  if (academicYearPeriodDivisionSelected.value === 2) {
    if (new Date(endDate.value) <= new Date(term2EndDate.value)) {
      showErrorMessage('The academic year end date must be greater than the semester 2 end date')
      return;
    }
    formData.append('periodDivisionName', 'SEMESTER')
  }
  if (academicYearPeriodDivisionSelected.value === 3) {
    if (new Date(term3StartDate.value) <= new Date(term2EndDate.value)) {
      showErrorMessage(`${term3DivisionSelected.value} 3 start date must be greater than the ${term3DivisionSelected.value} 2 end date`)
      return;
    }
    if (new Date(term3EndDate.value) <= new Date(term3StartDate.value)) {
      showErrorMessage(`${term3DivisionSelected.value} 3 end date must be greater than the ${term3DivisionSelected.value} 3 start date`)
      return;
    }
    if (new Date(term3EndDate.value) <= new Date(endDate.value)) {
      showErrorMessage(`The academic year end date must be greater than the ${term3DivisionSelected.value} 3 end date`)
      return;
    }
    formData.append('periodDivisionName', term3DivisionSelected.value)
    formData.append('term3StartDate', term3StartDate.value)
    formData.append('term3EndDate', term3EndDate.value)
  }
  formData.append('periodDivision', academicYearPeriodDivisionSelected.value)
  formData.append('startDate', startDate.value)
  formData.append('endDate', endDate.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('type', 'create')
  formData.append('newYear', academicYearSelected.value)
  formData.append('graduationDate', graduationDate.value)
  formData.append('repeatedStudents', JSON.stringify(selectedStudents.value))
  formData.append('term1EndDate', term1EndDate.value)
  formData.append('term2StartDate', term2StartDate.value)
  formData.append('term2EndDate', term2EndDate.value)
  formData.append('term', userAuthStore.activeTerm.toString())
  elementsStore.ShowLoadingOverlay()

  try {
    await axiosInstance.post("school-admin/academic_years", formData)
    await userAuthStore.getUserData()
    await userAuthStore.getAdminData()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const deleteAcademicYear = async () => {
  formErrorMessage.value = ''
  const formData = new FormData
  formData.append('type', 'delete')
  elementsStore.ShowLoadingOverlay()

  try {
    await axiosInstance.post("school-admin/academic_years", formData)
    await userAuthStore.getUserData()
    await userAuthStore.getAdminData()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const checkInput = computed(() => {
  if (academicYearPeriodDivisionSelected.value === 2) {
    return !(academicYearSelected.value && startDate.value && endDate.value && term1EndDate.value && term2StartDate.value && term2EndDate.value)
  }
  else if (academicYearPeriodDivisionSelected.value === 3) {
    return !(academicYearSelected.value && startDate.value && endDate.value && term1EndDate.value && term2StartDate.value && term2EndDate.value && term3StartDate.value && term3EndDate.value)
  }
  else {
    return true;
  }
})

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'AdminAcademicYears'" :class="{ 'is-active-page': elementsStore.activePage === 'AdminAcademicYears' }">
    
    <!-- admin academic year creation overlay -->
    <div id="AdminAddAcademicYearOverlay" class="overlay"
      v-if="userAuthStore.adminData.classes.length > 0">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminAddAcademicYearOverlay')" color="red" size="small" variant="flat"
          class="close-btn">X</v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container">
          <v-select class="select" :items="userAuthStore.adminData.classes?.map((_class: any) => _class['name'])"
            label="REPEATED STUDENTS CLASS" v-model="selectedClass" variant="solo-filled" density="comfortable" clearable />
          <div v-for="(_class, index) in userAuthStore.adminData.classes" :key="index">
            <v-select class="select" v-if="selectedClass === _class['name']"
              :items="_class['students'].map((_student: any) => ({ name: _student['user'], st_id: _student['st_id'] }))"
              label="REPEATED STUDENTS" v-model="selectedStudents" multiple chips item-title="name" item-value="st_id"
              variant="solo-filled" density="comfortable" clearable persistent-hint
              hint="Select the students who should be repeated">
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :subtitle="(item as any).raw.st_id"></v-list-item>
              </template>
            </v-select>
          </div>
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="academicYearOptions" label="ACADEMIC YEAR" v-model="academicYearSelected"
            variant="solo-filled" density="comfortable" persistent-hint hint="Select the new academic year" 
          />
          <v-select class="select" :items="academicYearPeriodDivisionOptions" label="NUMBER OF DIVISIONS"
            v-model.number="academicYearPeriodDivisionSelected" item-title="label" item-value="value"
            variant="solo-filled" density="comfortable" persistent-hint
            hint="How many division is in the academic year" 
          />
          <v-select class="select" v-if="academicYearPeriodDivisionSelected === 3" :items="term3DivisionOptions"
            label="DIVISION NAME" v-model="term3DivisionSelected" variant="solo-filled" item-title="label"
            item-value="value" density="comfortable" persistent-hint hint="Select the name given to each period" 
          />
          <v-text-field class="input-field" v-if="academicYearSelected" v-model="startDate" label="ACADEMIC YEAR START DATE" type="date" variant="solo-filled" density="comfortable" persistent-hint
            disabled
          />
          <v-text-field class="input-field" v-if="academicYearSelected" v-model="endDate" label="ACADEMIC YEAR END DATE"
            type="date" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the date the academic year ends" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 2" v-model="term1EndDate"
            label="SEMESTER 1 END DATE" type="date" variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date semester 1 ends`" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 2" v-model="term2StartDate"
            label="SEMESTER 2 START DATE" type="date" variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date semester 2 starts`" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 2" v-model="term2EndDate"
            label="SEMESTER 2 END DATE" type="date" variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date semester 2 ends`" />

          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 3 && term3DivisionSelected"
            v-model="term1EndDate" :label="`${term3DivisionSelected} 1 END DATE`" type="date" variant="solo-filled"
            density="comfortable" persistent-hint :hint="`Select the date ${term3DivisionSelected} 1 ends`" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 3 && term3DivisionSelected"
            v-model="term2StartDate" :label="`${term3DivisionSelected.toUpperCase()} 2 START DATE`" type="date"
            variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date ${term3DivisionSelected} 2 starts`" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 3 && term3DivisionSelected"
            v-model="term2EndDate" :label="`${term3DivisionSelected.toUpperCase()} 2 END DATE`" type="date"
            variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date ${term3DivisionSelected} 2 ends`" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 3 && term3DivisionSelected"
            v-model="term3StartDate" :label="`${term3DivisionSelected.toUpperCase()} 3 START DATE`" type="date"
            variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date ${term3DivisionSelected} 3 starts`" />
          <v-text-field class="input-field" v-if="academicYearPeriodDivisionSelected === 3 && term3DivisionSelected"
            v-model="term3EndDate" :label="`${term3DivisionSelected.toUpperCase()} 3 END DATE`" type="date"
            variant="solo-filled" density="comfortable" persistent-hint
            :hint="`Select the date ${term3DivisionSelected} 3 ends`" />
          <v-text-field class="input-field" v-if="academicYearSelected" v-model="graduationDate"
            label="GRADUATION DATE(OPTIONAL)" type="date" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the date students will graduate" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createAcademicYear()" :disabled="checkInput" :ripple="false" variant="flat" type="submit"
            color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header" v-if="userAuthStore.adminData.academicYears">
      <v-btn class="ma-1" color="blue" @click="showOverlay('AdminAddAcademicYearOverlay')"
        :size="elementsStore.btnSize1">
        ADD ACADEMIC YEAR
      </v-btn>
    </div>
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
          <th class="table-head">ACTION</th>
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
          <td class="table-data">
            <v-btn v-if="index == 0 && academicYearsData.length > 1" @click="elementsStore.ShowDeletionOverlay(()=>deleteAcademicYear(), 'Are you sure you want to delete the current academic year?')" icon="mdi-delete" color="red" size="x-small"/>
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

.overlay-card-info-container {
  margin-top: 3rem;
}

</style>
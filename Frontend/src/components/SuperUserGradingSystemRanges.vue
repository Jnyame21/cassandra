<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const gradingSystemRangeLabel = ref('')
const gradingSystemRangeUperLimit = ref<number | null>(null)
const gradingSystemRangeLowerLimit = ref<number | null>(null)
const gradingSystemRangeRemark = ref('')

const gradingSystemRanges = computed(() => {
  return userAuthStore.superUserData.gradingSystemRanges
})

const createGradingSystemRange = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('label', gradingSystemRangeLabel.value);
  formData.append('upperLimit', gradingSystemRangeUperLimit.value?.toString() || '');
  formData.append('lowerLimit', gradingSystemRangeLowerLimit.value?.toString() || '');
  formData.append('remark', gradingSystemRangeRemark.value);

  try {
    const response = await axiosInstance.post('superuser/grading_system_ranges', formData)
    userAuthStore.superUserData.gradingSystemRanges.unshift(response.data)
    elementsStore.HideLoadingOverlay()
    gradingSystemRangeLabel.value = ''
    gradingSystemRangeUperLimit.value = null
    gradingSystemRangeLowerLimit.value = null
    gradingSystemRangeRemark.value = ''
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

const deleteGradingSystemRange = async (index: number, grading_system_range_id: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', grading_system_range_id);

  try {
    await axiosInstance.post('superuser/grading_system_ranges', formData)
    userAuthStore.superUserData.gradingSystemRanges.splice(index, 1)
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
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserGradingSystemRanges'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserGradingSystemRanges' }">
    
    <!-- gradingSystemRange creation overlay -->
    <div id="SuperUserCreateGradingSystemRangeOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateGradingSystemRangeOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="gradingSystemRangeLabel" label="LABEL" clearable />
          <v-text-field class="input-field" v-model="gradingSystemRangeUperLimit" label="UPPER LIMIT" clearable />
          <v-text-field class="input-field" v-model="gradingSystemRangeLowerLimit" label="LOWER LIMIT" clearable />
          <v-text-field class="input-field" v-model="gradingSystemRangeRemark" label="REMARK" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createGradingSystemRange()"
            :disabled="!(gradingSystemRangeLabel && gradingSystemRangeUperLimit && gradingSystemRangeLowerLimit && gradingSystemRangeRemark)"
            :ripple="false" variant="flat" type="submit" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateGradingSystemRangeOverlay')" color="blue"
        :size="elementsStore.btnSize1">
        CREATE GRADING SYSTEM RANGE
      </v-btn>
    </div>
    <div class="no-data" v-if="gradingSystemRanges.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="gradingSystemRanges.length > 0">
      <thead>
        <tr>
          <th class="table-head">ID</th>
          <th class="table-head">LABEL</th>
          <th class="table-head">UPPER LIMIT</th>
          <th class="table-head">LOWER LIMIT</th>
          <th class="table-head">REMARK</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(gradingSystemRange, index) in gradingSystemRanges" :key="index">
          <td class="table-data">{{ gradingSystemRange.id }}</td>
          <td class="table-data">{{ gradingSystemRange.label }}</td>
          <td class="table-data">{{ gradingSystemRange.upper_limit }}</td>
          <td class="table-data">{{ gradingSystemRange.lower_limit }}</td>
          <td class="table-data">{{ gradingSystemRange.remark }}</td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ gradingSystemRange.identifier }}</v-chip>
          </td>
          <td class="table-data">
            <v-btn class="ma-2"
              @click="elementsStore.ShowDeletionOverlay(() => deleteGradingSystemRange(index, gradingSystemRange.id.toString()), 'Are you sure you want to delete this grading system range. The process cannot be reversed')"
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
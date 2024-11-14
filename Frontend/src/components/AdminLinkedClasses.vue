<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import TheLoader from '@/components/TheLoader.vue'
import { useElementsStore } from '@/stores/elementsStore'
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';


const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const deleteLinkedClass = async (index:number, from_class:string, to_class:string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('fromClass', from_class);
  formData.append('toClass', to_class);

  try {
    await axiosInstance.post('school-admin/linked-class', formData)
    userAuthStore.adminData.linkedClasses.splice(index, 1)
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



</script>

<template>
    <div class="content-wrapper" v-show="elementsStore.activePage === 'AdminLinkedClases'" :class="{ 'is-active-page': elementsStore.activePage === 'AdminLinkedClases' }">
      <div class="no-data" v-if="userAuthStore.adminData.linkedClasses?.length === 0">
        <p>YOU HAVE NOT LINKED ANY CLASSES</p>b
      </div>
      <TheLoader :func="userAuthStore.getAdminData" v-if="!userAuthStore.adminData.linkedClasses" />
      <v-table fixed-header class="table" v-if="userAuthStore.adminData.linkedClasses?.length >0">
        <thead>
        <tr>
          <th class="table-head">FROM</th>
          <th class="table-head">TO</th>
          <th class="table-head">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(_class, index) in userAuthStore.adminData.linkedClasses" :key="index">
          <td class="table-data">{{ _class['from_class']}}</td>
          <td class="table-data">{{_class['to_class']}}</td>
          <td class="table-data">
            <v-btn color="red" size="x-small" variant="flat" @click="elementsStore.ShowDeletionOverlay(()=>deleteLinkedClass(index, _class['from_class'], _class['to_class']), 'Are you sure you want to delete?')">
              DELETE
            </v-btn>
          </td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

.table{
  min-height: 100% !important;
}
.overlay-card{
  max-width: 600px !important;
}
.overlay-card-info-container{
  margin-top: 3rem;
}


</style>
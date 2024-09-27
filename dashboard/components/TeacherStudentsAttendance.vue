<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const loading = ref(false)
const formErrorMessage = ref('')
const date = ref('')
const studentsClass = ref('')
const currentAttendanceIndex:any = ref(null)

const hidOverlay = ()=>{
  const overlay = document.getElementById('deleteStudentsAttendanceOverlay')
  overlay ? overlay.style.display = "none" : null
}

const continueDeletion = async()=>{
  const formData = new FormData
  formData.append('className', studentsClass.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('date', date.value)
  formData.append('type', 'delete')
  formData.append('term', userAuthStore.activeTerm.toString())
  hidOverlay()
  elementsStore.ShowLoadingOverlay()
  try {
    await axiosInstance.post('teacher/students/attendance', formData)
    userAuthStore.teacherData.studentsattendance.splice(currentAttendanceIndex.value, 1)
    elementsStore.HideLoadingOverlay()
  }
  catch(error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError){
      error.response?.status === 400 && error.response.data.message ? elementsStore.ShowOverlay(error.response.data.message, 'red', null, null) : elementsStore.ShowOverlay("Something went wrong. Check your internet connection and try again", 'red', null, null)
    }
  }
}

const deleteStudentAttendance = async(studentsClassName: string, dateItem: string, index:Number)=>{
  const overlay = document.getElementById('deleteStudentsAttendanceOverlay')
  date.value = dateItem
  studentsClass.value = studentsClassName
  currentAttendanceIndex.value = index
  overlay ? overlay.style.display = 'flex' : null
}


</script>

<template>
  <div class="content-wrapper">
      <div id="deleteStudentsAttendanceOverlay" class="overlay">
        <v-card class="d-flex flex-column align-center">
          <v-card-text style="font-size: .8rem; font-family: sans-serif; text-align: left; line-height: 1.2; font-weight: bold">
            <p>Continue to delete ?</p>
            <p v-if="formErrorMessage" class="mt-5" style="color: red">{{ formErrorMessage }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn :loading="loading" class="mr-5" color="red" size="small" variant="flat" @click="continueDeletion">YES</v-btn>
            <v-btn :disabled="loading" class="ml-5" color="black" size="small" variant="flat" @click="hidOverlay">NO</v-btn>
          </v-card-actions>
        </v-card>
      </div>
      <TheLoader v-if="!userAuthStore.teacherData.studentsattendance" />
      <h4 class="no-data" v-if="userAuthStore.teacherData.studentsattendance?.length === 0">
        <p>You have not uploaded any student attendance for the {{userAuthStore.activeAcademicYear}} academic year {{userAuthStore.userData['academic_year']['period_division']['name']}} {{ userAuthStore.activeTerm }} yet</p>
      </h4>
      <div class="info-wrapper" v-if="userAuthStore.teacherData.studentsattendance?.length > 0">
        {{ userAuthStore.activeAcademicYear}} {{ userAuthStore.userData['academic_year']['period_division']['name'] }} {{ userAuthStore.activeTerm }} STUDENTS ATTENDANCE
      </div>
      <v-table class="table" fixed-header v-if="userAuthStore.teacherData.studentsattendance?.length > 0">
        <thead>
        <tr>
          <th class="table-head">CLASS</th>
          <th class="table-head">DATE</th>
          <th class="table-head">STUDENTS PRESENT</th>
          <th class="table-head">STUDENTS ABSENT</th>
          <th class="table-head">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(attendance, i) in userAuthStore.teacherData.studentsattendance" :key="i">
          <td class="table-data">{{attendance['students_class']['name']}}</td>
          <td class="table-data">{{attendance['date']}}</td>
            <td style=" padding: 0">
                <v-list class="pa-0">
                  <v-list-group>
                    <template v-slot:activator="{ props }">
                      <v-list-item class="title" v-bind="props">
                        <v-icon icon="mdi-account-circle" />{{attendance['students_present'].length}} STUDENTS
                      </v-list-item>
                    </template>
                      <v-virtual-scroll class="v-scroll" height="22vh" :items="attendance['students_present']">
                        <template v-slot:default="{ item }" >
                          <v-list-item style="position: relative">
                            <v-list-item-title>
                              <p class="user-name">{{ item['user']['first_name'] }} {{item['user']['last_name']}}</p>
                            </v-list-item-title>
                            <v-list-item-subtitle>
                              <p class="user-name">{{item['st_id']}}</p>
                            </v-list-item-subtitle>
                          </v-list-item>
                        </template>
                      </v-virtual-scroll>
                  </v-list-group>
                </v-list>
            </td>
            <td style=" padding: 0">
                <v-list class="pa-0">
                  <v-list-group>
                    <template v-slot:activator="{ props }">
                      <v-list-item class="title" v-bind="props">
                        <v-icon icon="mdi-account-circle" />{{attendance['students_absent'].length}} STUDENTS
                      </v-list-item>
                    </template>
                      <v-virtual-scroll class="v-scroll" height="22vh" :items="attendance['students_absent']">
                        <template v-slot:default="{ item }" >
                          <v-list-item style="position: relative">
                            <v-list-item-title>
                              <p class="user-name">{{ item['user']['first_name'] }} {{item['user']['last_name']}}</p>
                            </v-list-item-title>
                            <v-list-item-subtitle>
                              <p class="user-name">{{item['st_id']}}</p>
                            </v-list-item-subtitle>
                          </v-list-item>
                        </template>
                      </v-virtual-scroll>
                  </v-list-group>
                </v-list>
            </td>
            <td>
              <v-icon @click="deleteStudentAttendance(attendance['students_class']['name'], attendance['date'], i)" icon="mdi-delete" size="small" color="red"/>
            </td>
        </tr>
        </tbody>
      </v-table>
  </div>
</template>

<style scoped>

.info-wrapper, .table{
  max-width: 1000px !important;
}
.overlay{
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.7);
  align-items: center;
  justify-content: center;
  z-index: 10 !important;
}


</style>


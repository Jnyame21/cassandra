<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '../utils/axiosInstance';

const userAuthStore = useUserAuthStore()
const loading = ref(false)
const formErrorMessage = ref('')
const subject = ref('')
const date = ref('')
const studentsClass = ref('')

interface Props {
  index: number;
  attendance: any;
}

const { index, attendance } = defineProps<Props>()

const hidOverlay = ()=>{
  const overlay = document.getElementById(`deleteAttendance${index}`)
  overlay ? overlay.style.display = "none" : null
  formErrorMessage.value = ''
  subject.value = ''
  studentsClass.value = ''
  date.value = ''

}

const continueDeletion = async()=>{
  loading.value = true
  const formData = new FormData
  formData.append('subject', subject.value)
  formData.append('className', studentsClass.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('date', date.value)
  formData.append('type', 'delete')
  formData.append('term', userAuthStore.activeTerm.toString())
  
  try {
    const response = await axiosInstance.post('teacher/students/attendance', formData)
    if (response.status===200){
      const subjectAttendance = userAuthStore.teacherStudentsAttendance.find(c => c['subject']===subject.value && c['class_name']===studentsClass.value)
      if (subjectAttendance){
        const index = userAuthStore.teacherStudentsAttendance.indexOf(subjectAttendance)
        const attendanceItem = userAuthStore.teacherStudentsAttendance[index]['attendance'].find(attendance_item => attendance_item['date'] === date.value)
        if (attendanceItem){
            const attendance_index = userAuthStore.teacherStudentsAttendance[index]['attendance'].indexOf(attendanceItem)
            userAuthStore.teacherStudentsAttendance[index]['attendance'].splice(attendance_index, 1)
        }
      }
      hidOverlay()
      loading.value = false
    }
  }

  catch(e) {
    formErrorMessage.value = "Oops! something went wrong. Check your internet connection and try again"
    loading.value = false
  }
}


const deletesubjectAssignment = async(subjectName: string, studentsClassName: string, dateItem: string)=>{
  const overlay = document.getElementById(`deleteAttendance${index}`)
  subject.value = subjectName
  date.value = dateItem
  studentsClass.value = studentsClassName
  overlay ? overlay.style.display = 'flex' : null

}


</script>

<template>
  <div :id="`deleteAttendance${index}`" class="overlay">
    <v-card class="d-flex flex-column align-center">
      <v-card-text style="font-size: .8rem; font-family: sans-serif; text-align: left; line-height: 1.2; font-weight: bold">
        <p>Continue to delete ?</p>
        <p v-if="formErrorMessage" class="mt-5" style="color: red">{{ formErrorMessage }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn :loading="loading" class="overlay-btn mr-5" elevation="4" @click="continueDeletion">YES</v-btn>
        <v-btn :disabled="loading" class="overlay-btn ml-5" elevation="4" @click="hidOverlay">NO</v-btn>
      </v-card-actions>
    </v-card>
  </div>
    <div style="width: 100%; position: relative; height: 100%">
      <v-table fixed-header v-if="attendance && attendance.length > 0">
        <thead>
        <tr>
          <th class="table-head">DATE</th>
          <th class="table-head">STUDENTS PRESENT</th>
          <th class="table-head">STUDENTS ABSENT</th>
          <th class="table-head">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(atten, i) in attendance" :key="i">
            <td class="table-data">{{atten['date']}}</td>
            <td style=" padding: 0">
                <v-list class="pa-0">
                  <v-list-group>
                    <template v-slot:activator="{ props }">
                      <v-list-item class="title" v-bind="props">
                        <v-icon icon="mdi-account-circle" />{{atten['students_present'].length}} STUDENTS
                      </v-list-item>
                    </template>
                      <v-virtual-scroll class="v-scroll" height="22vh" :items="atten['students_present']">
                        <template v-slot:default="{ item }" >
                          <v-list-item style="position: relative">
                            <v-list-item-title>
                              <p class="user-name">{{item['user']['first_name']+' '+item['user']['last_name']}}</p>
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
                        <v-icon icon="mdi-account-circle" />{{atten['students_absent'].length}} STUDENTS
                      </v-list-item>
                    </template>
                      <v-virtual-scroll class="v-scroll" height="22vh" :items="atten['students_absent']">
                        <template v-slot:default="{ item }" >
                          <v-list-item style="position: relative">
                            <v-list-item-title>
                              <p class="user-name">{{item['user']['first_name']+' '+item['user']['last_name']}}</p>
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
            <td><v-btn @click="deletesubjectAssignment(atten['subject']['name'], atten['students_class']['name'], atten['date'])" size="small" color="red">Delete</v-btn></td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


.overlay{
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.7);
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.overlay-btn{
  background-color: lightseagreen;
  color: yellow;
  font-family: Verdana, "sans-serif";
  font-size: .7rem;
  margin-right: 2em;
  margin-left: 2em;

}
.overlay-btn:hover{
  background-color: mediumseagreen;
}

</style>


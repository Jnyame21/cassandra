
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';

import { ref } from 'vue';

interface Props {
    classYear: any;
}

const { classYear } = defineProps<Props>()

const userAuthStore = useUserAuthStore()
const deleteLoading = ref(false)
const formErrorMessage = ref('')
const deleteType = ref('')
const className = ref('')
const subjectName = ref('')
const studentId = ref('')
const overlayMessage = ref('')

const deleteSubject = async(clasName: any, subject: any)=>{
    const formData = new FormData()
    formData.append('className', clasName)
    formData.append('subject', subject)
    formData.append('type', 'delete-subject')

    await axiosInstance.post('sch-admin/students', formData)
    .then(response =>{
        const data = response.data
        const year = data['year'];
        const clas = userAuthStore.adminClasses[year].find(classItem => classItem['name']===data['class_name']);
        if (clas){
            const clas_index = userAuthStore.adminClasses[year].indexOf(clas);
            const subjectArray = userAuthStore.adminClasses[year][clas_index]['subjects'].filter(sub => sub['name'] !== subject)
            userAuthStore.adminClasses[year][clas_index]['subjects'] = subjectArray;
        }
    })
    .catch(e =>{
        return Promise.reject(e)
    })
}

const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
  }, 15000)
}

const deleteStudent = async(clasName: any, stId: any)=>{
    const formData = new FormData()
    formData.append('className', clasName)
    formData.append('stId', stId)
    formData.append('type', 'delete-student')

    await axiosInstance.post('sch-admin/students', formData)
    .then(response =>{
        const data = response.data
        const year = data['year'];
        const clas = userAuthStore.adminClasses[year].find(classItem => classItem['name']===data['class_name']);
        if (clas){
            const clas_index = userAuthStore.adminClasses[year].indexOf(clas);
            const studentArray = userAuthStore.adminClasses[year][clas_index]['students'].filter(st => st['st_id'] !== stId)
            userAuthStore.adminClasses[year][clas_index]['students'] = studentArray;
        }
    })
    .catch(e =>{
        return Promise.reject(e)
    })
}

const showOverlay = (type:string, clasName:string, stId:string, subject:string)=>{
  deleteType.value = type
  className.value = clasName
  studentId.value = stId
  subjectName.value = subject

  if (type === 'deleteStudent'){
    overlayMessage.value = `Are you sure you want to delete student with ID ${studentId.value} from the class`
  }else if (type === 'deleteClass'){
    overlayMessage.value = `Are you sure you want to delete the ${className.value} class`
  }else if (type === 'deleteSubject'){
    overlayMessage.value = `Are you sure you want to delete ${subjectName.value} from the ${className.value} class subjects`
  }

  const overlay = document.getElementById('deleteClassSubjectStudentOverlay')
  overlay ? overlay.style.display = 'flex' : null
}

const hidOverlay = ()=>{
  const overlay = document.getElementById('deleteClassSubjectStudentOverlay')
  overlay ? overlay.style.display = 'none' : null
}

const deleteClass = async(clasName: any)=>{
    const formData = new FormData()
    formData.append('className', clasName)
    formData.append('type', 'delete-class')

    await axiosInstance.post('sch-admin/students', formData)
    .then(response =>{
        const clas = userAuthStore.adminClasses.yearOne.find(classItem => classItem['name']===clasName);
        if (clas){
            const clas_index = userAuthStore.adminClasses.yearOne.indexOf(clas);
            userAuthStore.adminClasses.yearOne.splice(clas_index, 1);
            const newClassNames = userAuthStore.adminClasses.names.filter(classItem => classItem !== `${clasName} FORM-1`)
            newClassNames ? userAuthStore.adminClasses.names = newClassNames : null
        }
    })
    .catch(e =>{
        return Promise.reject(e)
    })
}

const deleteClassSubjectStudent = async()=>{
  deleteLoading.value = true
  if (deleteType.value === 'deleteStudent') {
    await deleteStudent(className.value, studentId.value)
    .then(response =>{
      hidOverlay()
    })
    .catch(e =>{
      clearMessage();
    })
  } else if (deleteType.value === 'deleteSubject') {
    await deleteSubject(className.value, subjectName.value)
    .then(response =>{
      hidOverlay()
    })
    .catch(e =>{
      clearMessage();
    })
  } else if (deleteType.value === 'deleteClass') {
    await deleteClass(className.value)
    .then(response =>{
      hidOverlay()
    })
    .catch(e =>{
      clearMessage();
    })
  }
  deleteLoading.value = false
  clearMessage()
}



</script>

<template>
    <div id="deleteClassSubjectStudentOverlay" class=overlay>
      <v-card class="overlay-card">
        <p class="mb-5 error-message">{{formErrorMessage}}</p>
        <p class="mb-10">{{overlayMessage}}</p>
        <div>
          <v-btn class="mr-5" color="red" @click="deleteClassSubjectStudent" :loading="deleteLoading">YES</v-btn>
          <v-btn @click="hidOverlay" color="blue" class="ml-5" :disabled="deleteLoading">NO</v-btn>
        </div>
      </v-card>
    </div>
    <div style="width: 100%; position: relative" >
      
      <TheLoader class="no-data flex-all" v-if="!classYear" />
      <NoData v-if="classYear && classYear.length ===0 " :message="'No data yet'"/>
        <v-table fixed-header class="table-2" v-if="classYear && classYear.length >0">
        <thead>
        <tr>
          <th class="table-head">CLASS</th>
          <th class="table-head">DATE ENROLLED</th>
          <th class="table-head">EXPECTED COMPLETION DATE</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">STUDENTS</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['delete_class']">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(clas, i) in classYear" :key="i">
          <td class="table-data">{{clas['name']}}</td>
          <td class="table-data">{{clas['date_enrolled']}}</td>
          <td class="table-data">{{clas['completion_date']}}</td>
          <td style=" padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-lightbulb-on" />{{clas['subjects'].length}} SUBJECTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="clas['subjects']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <div class="student-info-container">
                          <p>{{ item['name'] }}</p>
                          <div class="flex-all pa-2"  v-if="clas['students_year']===1 && userAuthStore.userData['school']['delete_class']">
                            <v-btn @click="showOverlay('deleteSubject' ,clas['name'], '', item['name'])" size="x-small" class="edit-btn remove">delete</v-btn>
                          </div>
                        </div>
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
                    <v-icon icon="mdi-account-circle" />{{clas['students'].length}} STUDENTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="clas['students']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <div class="student-info-container">
                          <img class="profile-img" :src="item['img']">
                          <div class="flex-all-c">
                            <p class="user-name">{{item['user']['first_name']}} {{item['user']['last_name']}} [ {{ item['gender'] }} ]</p>
                            <p class="user-name">{{item['st_id']}} [ {{ item['user']['username'] }} ] [ {{ item['dob'] }} ]</p>
                          </div>
                          <div class="flex-all pa-2" v-if="clas['students_year']===1 && userAuthStore.userData['school']['delete_class']">
                            <v-btn @click="showOverlay('deleteStudent' ,clas['name'], item['st_id'], '')" size="x-small" class="edit-btn remove">delete</v-btn>
                          </div>
                        </div>
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
              </v-list-group>
            </v-list>
          </td>
          <td class="table-data" v-if="clas['students_year']===1 && userAuthStore.userData['school']['delete_class']">
            <div class="flex-all pa-2">
              <v-btn @click="showOverlay('deleteClass' ,clas['name'], '', '')" size="x-small" class="edit-btn remove">delete</v-btn>
            </div>
          </td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.overlay-card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  align-items: center;
  padding: 0.5em 1em;
  color: blue;
}
.error-message{
  color: red;
}

.edit-btn{
    font-size: .7rem;
    padding: .1em .5em
}

.remove{
    font-size: .5rem;
    background-color: red;
    color: white;
    margin-left: 2em;
}
.remove:hover{
    color: yellow;
    background-color: seagreen;
}
.no-data{
    margin-top: 5em;
}


</style>
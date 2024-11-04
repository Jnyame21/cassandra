<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';

const userAuthStore = useUserAuthStore()

const showOverlay = ()=>{
  const overlay = document.getElementById('teacherInfoOverlay')
  if (overlay){
    overlay.style.display = 'flex'
  }
}

const closeBtn = ()=>{
  const overlay = document.getElementById('teacherInfoOverlay')
  if (overlay){
    overlay.style.display = 'none'
  }
}

</script>

<template>
  <div class="content-wrapper">
    <div id="teacherInfoOverlay" class="overlay" v-if="userAuthStore.studentData.classData">
      <div class="info-container">
        <v-btn @click="closeBtn" color="red" size="small" class="close-btn">X</v-btn>
        <div class="flex-all-c ma-5 mt-15">
          <div class="teacher-info">
            <h4  class="title">CLASS HEAD TEACHER INFORMATION</h4>
            <p class="title">NAME: <strong>{{ userAuthStore.studentData.classData['head_teacher']['user']['first_name'] }} {{ userAuthStore.studentData.classData['head_teacher']['user']['last_name'] }}</strong></p>
            <p class="title">GENDER: <strong>{{ userAuthStore.studentData.classData['head_teacher']['gender'] }}</strong></p>
            <p class="title" v-if="userAuthStore.studentData.classData['head_teacher']['department'] !=='none' ">DEPARTMENT: <strong>{{ userAuthStore.studentData.classData['head_teacher']['department']['name'] }}</strong></p>
            <p class="title" v-if="userAuthStore.studentData.classData['head_teacher']['contact']">PHONE NO: <strong>{{ userAuthStore.studentData.classData['head_teacher']['contact']}}</strong></p>
            <p class="title" v-if="userAuthStore.studentData.classData['head_teacher']['user']['email']">EMAIL: <strong>{{ userAuthStore.studentData.classData['head_teacher']['user']['email']}}</strong></p>
            <p class="title"><img class="teacher-img" :src="userAuthStore.studentData.classData['head_teacher']['img']"></p>
          </div>
        </div>
      </div>
    </div>
    <TheLoader v-if="!userAuthStore.studentData.classData" />
    <div class="content-header" v-if="userAuthStore.studentData.classData && userAuthStore.studentData.classData['head_teacher'] !=='none' ">
      <v-btn size="small" @click="showOverlay()">HEAD TEACHER</v-btn>
    </div>
    <div class="content-header" v-if="userAuthStore.studentData.classData && userAuthStore.studentData.classData['students'].length >0 ">
      TOTAL NUMBER OF STUDENTS 
      <h4>{{ userAuthStore.studentData.classData['students'].length }}</h4>
    </div>
    <v-table fixed-header class="table" v-if="userAuthStore.studentData.classData && userAuthStore.studentData.classData['students'].length >0 ">
      <thead>
      <tr>
        <th class="table-head">NAME</th>
        <th class="table-head">GENDER</th>
        <th class="table-head">IMAGE</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(st, i) in userAuthStore.studentData.classData['students']" :key="i">
        <td class="table-data">{{st['user']['first_name']}} {{st['user']['last_name']}}</td>
        <td class="table-data">{{st['gender']}}</td>
        <td class="table-data"><img class="profile-img" :src="st['img']"></td>
      </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.table{
  height: 80% !important;
}
.info-container{
  position: relative;
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  border-radius: .3em;
  max-width: 500px;
}
.teacher-info h4{
  font-size: .8rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: red;
  border: 2px solid black;
}
.title{
  font-size: .8rem;
  margin-top: .5em;
  text-align: center;
  font-weight: bold;
}
.title strong{
  color: seagreen;
}
.teacher-img{
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.overlay{
  position: absolute;
  background: rgba(0, 0, 0, .5);
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: 10 !important;
  align-items: center;
  justify-content: center;
  display: none;
}



</style>
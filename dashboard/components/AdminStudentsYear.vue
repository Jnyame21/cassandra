
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';

import { ref } from 'vue';

interface Props {
    classYear: any;
}

const { classYear } = defineProps<Props>()

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const deleteLoading = ref(1000)


const deleteStudent = async(clasName: any, stId: any, index: number)=>{
    deleteLoading.value = index
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
        deleteLoading.value = 1000
    })
    .catch(e =>{
        deleteLoading.value = 1000
        return Promise.reject(e)
    })

}


</script>

<template>

    <div style="width: 100%; position: relative; height: 100%">
      
      <TheLoader class="no-data flex-all" v-if="!classYear || classYear && classYear.length ===0 " />
      
        <v-table fixed-header class="table-1" v-if="classYear && classYear.length >0">
        <thead>
        <tr>
          <th class="table-head">CLASS</th>
          <th class="table-head">STUDENTS</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(clas, i) in classYear" :key="i">
          <td class="table-data">{{clas['name']}}</td>
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
                          <img class="student-img" :src="elementsStore.getBaseUrl + item['img']">
                          <div class="flex-all-c">
                            <p class="user-name">{{item['user']['first_name']}} {{item['user']['last_name']}}</p>
                            <p class="user-name">{{item['st_id']}}</p>
                          </div>
                          <div class="flex-all pa-2">
                            <v-btn :loading="deleteLoading===clas['students'].indexOf(item)" @click="deleteStudent(clas['name'], item['st_id'], clas['students'].indexOf(item))" size="x-small" class="edit-btn remove">delete</v-btn>
                          </div>
                        </div>
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
              </v-list-group>
            </v-list>
          </td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

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
}
.no-data{
    margin-top: 5em;
}


</style>
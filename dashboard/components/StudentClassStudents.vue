<script setup lang="ts">
import TheLoader from '@/components/TheLoader.vue'

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()



</script>

<template>
    <div style="width: 100%; position: relatve; height: 100%">
      <TheLoader v-if="!userAuthStore.studentData.classData" />
      <v-table fixed-header class="table-1" v-if="userAuthStore.studentData.classData && userAuthStore.studentData.classData.length >0 ">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">ID</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">IMAGE</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(st, i) in userAuthStore.studentData.classData" :key="i">
          <td class="table-data">{{st['user']['first_name']}} {{st['user']['last_name']}}</td>
          <td class="table-data">{{st['st_id']}}</td>
          <td class="table-data">{{st['gender']}}</td>
          <td class="table-data"><img class="student-img" :src="elementsStore.getBaseUrl + st['img']"></td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

</style>
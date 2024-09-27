<script setup lang="ts">

const userAuthStore = useUserAuthStore()



</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!userAuthStore.studentData.studentApplications" />
      <NoData :message="'You have not applied to any university yet'" v-if="userAuthStore.studentData.studentApplications && userAuthStore.studentData.studentApplications.lenght===0"/>
      <v-table fixed-header height="55dvh" v-if="userAuthStore.studentData.studentApplications && userAuthStore.studentData.studentApplications.length > 0">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">DATE</th>
          <th class="table-head">STATUS</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(application, index) in userAuthStore.studentData.studentApplications" :key="index">
          <td class="table-data">{{ application['name']}}</td>
          <td class="table-data">{{application['date']}}</td>
          <td class="table-data">{{application['status']}}</td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


</style>
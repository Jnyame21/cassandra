<script setup lang="ts">

const userAuthStore = useUserAuthStore()



</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!userAuthStore.adminStaff.academicYears" />
        <!-- semesters -->
      <v-table fixed-header height="55dvh" v-if="userAuthStore.userData['school']['semesters'] && userAuthStore.adminStaff.academicYears">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">START DATE</th>
          <th class="table-head">END DATE</th>
          <th class="table-head">SEM 1 END DATE</th>
          <th class="table-head">SEM 2 START DATE</th>
          <th class="table-head">SEM 2 END DATE</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(year, index) in userAuthStore.adminStaff.academicYears" :key="index">
          <td class="table-data">{{ year['name']}}</td>
          <td class="table-data">{{year['start_date']}}</td>
          <td class="table-data">{{year['end_date']}}</td>
          <td class="table-data">{{year['term_1_end_date']}}</td>
          <td class="table-data">{{year['term_2_start_date']}}</td>
          <td class="table-data">{{year['term_2_end_date']}}</td>
        </tr>
        </tbody>
      </v-table>

      <!-- semesters -->
      <v-table fixed-header height="55dvh" v-if="!userAuthStore.userData['school']['semesters'] && userAuthStore.adminStaff.academicYears">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">START DATE</th>
          <th class="table-head">END DATE</th>
          <th class="table-head">TRIM 1 END DATE</th>
          <th class="table-head">TRIM 2 START DATE</th>
          <th class="table-head">TRIM 2 END DATE</th>
          <th class="table-head">TRIM 3 START DATE</th>
          <th class="table-head">TRIM 3 END DATE</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(year, index) in userAuthStore.adminStaff.academicYears" :key="index">
          <td class="table-data">{{ year['name']}}</td>
          <td class="table-data">{{year['start_date']}}</td>
          <td class="table-data">{{year['end_date']}}</td>
          <td class="table-data">{{year['term_1_end_date']}}</td>
          <td class="table-data">{{year['term_2_start_date']}}</td>
          <td class="table-data">{{year['term_2_end_date']}}</td>
          <td class="table-data" >{{year['term_3_start_date']}}</td>
          <td class="table-data" >{{year['term_3_end_date']}}</td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


</style>
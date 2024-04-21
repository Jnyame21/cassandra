<script setup lang="ts">

const userAuthStore = useUserAuthStore()



</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!userAuthStore.studentData.results['termOne'] && !userAuthStore.studentData.results['termTwo'] && !userAuthStore.studentData.results['termThree']"/>
      <h4 class="no-data flex-all" v-if="userAuthStore.studentData.results['termOne']?.length ===0 && userAuthStore.studentData.results['termTwo']?.length === 0 && userAuthStore.studentData.results['termThree']?.length ===0">
        <p>No data yet</p>
      </h4>
      <v-table fixed-header 
      v-if="userAuthStore.studentData.results['termThree'] && userAuthStore.studentData.results['termThree'].length > 0 || userAuthStore.studentData.results['termTwo'] && userAuthStore.studentData.results['termTwo'].length > 0 || userAuthStore.studentData.results['termOne'] && userAuthStore.studentData.results['termOne'].length > 0"
      >
        <thead>
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">SCORE</th>
        </tr>
        </thead>

        <!-- trimesters -->
        <tbody v-if="!userAuthStore.userData && userAuthStore.userData['school']['semesters']">
        <tr v-if="userAuthStore.studentData.results['termThree'] && userAuthStore.studentData.results['termThree'].length > 0" class="table-title-container" style="position: relative">
            <td>Justice</td>
            <td class="table-title">TRIMESTER 3</td>
        </tr>
        <tr v-for="(result, i) in userAuthStore.studentData.results['termThree']" :key="i">
          <td class="table-data">{{result['subject']['name']}}</td>
          <td class="table-data">{{result['score']}}</td>
        </tr>
        <tr v-if="userAuthStore.studentData.results['termTwo'] && userAuthStore.studentData.results['termTwo'].length > 0" class="table-title-container" style="position: relative">
          <td>Justice</td>
          <td class="table-title">TRIMESTER 2</td>
        </tr>
        <tr v-for="(result, i) in userAuthStore.studentData.results['termTwo']" :key="i">
          <td class="table-data">{{result['subject']['name']}}</td>
          <td class="table-data">{{result['score']}}</td>
        </tr>
        <tr v-if="userAuthStore.studentData.results['termOne'] && userAuthStore.studentData.results['termOne'].length > 0" class="table-title-container" style="position: relative">
          <td>Justice</td>
          <td class="table-title">TRIMESTER 1</td>
        </tr>
          <tr v-for="(result, i) in userAuthStore.studentData.results['termOne']" :key="i">
            <td class="table-data">{{result['subject']['name']}}</td>
            <td class="table-data">{{result['score']}}</td>
          </tr>
        </tbody>

        <!-- semesters -->
        <tbody v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">
        <tr v-if="userAuthStore.studentData.results['termTwo'] && userAuthStore.studentData.results['termTwo'].length > 0" class="table-title-container" style="position: relative">
          <td>Justice</td>
          <td class="table-title">SEMESTER 2</td>
        </tr>
        <tr v-for="(result, i) in userAuthStore.studentData.results['termTwo']" :key="i">
          <td class="table-data">{{result['subject']['name']}}</td>
          <td class="table-data">{{result['score']}}</td>
        </tr>
        <tr v-if="userAuthStore.studentData.results['termOne'] && userAuthStore.studentData.results['termOne'].length > 0" class="table-title-container" style="position: relative">
          <td>Justice</td>
          <td class="table-title">SEMESTER 1</td>
        </tr>
        <tr v-for="(result, i) in userAuthStore.studentData.results['termOne']" :key="i">
          <td class="table-data">{{result['subject']['name']}}</td>
          <td class="table-data">{{result['score']}}</td>
        </tr>
          </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


</style>
<script setup lang="ts">

interface Props {
    term: string;
    termNumber: number;
}

const { term } = defineProps<Props>()
const userAuthStore = useUserAuthStore()

</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!userAuthStore.studentData.results[term]" />
      <h4 class="no-data flex-all" v-if="userAuthStore.studentData.results[term] && userAuthStore.studentData.results[term].length === 0">
        <p v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">No results for semester {{ termNumber }} yet</p>
        <p v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">No results for trimester {{ termNumber }} yet</p>
      </h4>
      <v-table fixed-header height="60dvh" v-if="userAuthStore.studentData.results[term] && userAuthStore.studentData.results[term].length > 0">
        <thead>
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">SCORE</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(result, i) in userAuthStore.studentData.results[term]" :key="i">
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
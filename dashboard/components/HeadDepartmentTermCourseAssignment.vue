<script setup lang="ts">


interface Props {
  term: any[];
}

const { term } = defineProps<Props>()


</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!term || term.length ===0 " />
      <v-table fixed-header height="45dvh" v-if="term && term.length >0" >
        <thead>
        <tr>
            <th class="table-head">TEACHER</th>
            <th class="table-head">STAFF ID</th>
            <th class="table-head">SUBJECT</th>
            <th class="table-head">CLASS</th>
            <th class="table-head">FORM</th>
          
        </tr>
        </thead>
        <tbody>
        <tr v-for="(assign, i) in term" :key="i" >
            <td class="table-data">{{assign['teacher']['user']['first_name']}} {{assign['teacher']['user']['last_name']}}</td>
            <td class="table-data">{{assign['teacher']['staff_id']}}</td>
            <td class="table-data">{{assign['subject']['name']}}</td>
            <td class="table-data">{{assign['students_class']['name']}}</td>
            <td class="table-data">{{assign['students_class']['students_year']}}</td>
        </tr>
        <tr class="empty-row">Justice</tr>
        </tbody>
      </v-table>
    </div>
</template>


<style scoped>

@import url('../assets/css/tables.css');

</style>
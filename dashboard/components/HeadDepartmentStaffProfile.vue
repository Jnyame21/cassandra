<script setup lang="ts">

const props = defineProps({
  staff: null,
})

const elementsStore = useElementsStore()


</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!props.staff" />
      <v-table fixed-header height="55dvh" v-if="props.staff">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">STAFF ID</th>
          <th class="table-head">SUBJECT(S)</th>
          <th class="table-head">IMAGE</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(staff, i) in props.staff" :key="i">
          <td class="table-data">
            {{staff['user']['first_name']}} {{staff['user']['last_name']}}
            <span style="color: seagreen;" v-if="staff['role'] === 'hod'">[HOD]</span>
          </td>
          <td class="table-data">{{staff['staff_id']}}</td>
          <td class="table-data">
            <p v-for="(subject, i) in staff['subjects']" :key="i">{{subject['name']}}</p>
          </td>
          <td class="table-data">
            <img class="student-img" :src="elementsStore.getBaseUrl + staff['img']">
          </td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

</style>
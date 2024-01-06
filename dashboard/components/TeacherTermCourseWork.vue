<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

interface Props {
  term: string;
  termNumber: number;
}

const { term, termNumber } = defineProps<Props>()


</script>

<template>
    <div style="width: 100%; position: relatve; height: 100%">
      <TheLoader v-if="!userAuthStore.staffSubjectAssignment[term]" />
      <h4 class="no-data flex-all" v-if="userAuthStore.staffSubjectAssignment[term] && userAuthStore.staffSubjectAssignment[term].length === 0">
        <p>No coursework for semester {{ termNumber }} yet</p>
      </h4>
      <v-table fixed-header class="table-1" v-if="userAuthStore.staffSubjectAssignment[term] && userAuthStore.staffSubjectAssignment[term].length > 0">
        <thead>
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">FORM</th>
          <th class="table-head">STUDENTS</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(assign, i) in userAuthStore.staffSubjectAssignment[term]" :key="i">
          <td class="table-data">{{assign['subject']['name']}}</td>
          <td class="table-data">{{assign['students_class']['name']}}</td>
          <td class="table-data">{{assign['students_class']['students_year']}}</td>
          <td style=" padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-account-circle" />{{assign['students_class']['students'].length}} STUDENTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="assign['students_class']['students']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <div class="student-info-container">
                          <img class="student-img" :src="elementsStore.getBaseUrl + item['img']">
                          <div class="flex-all-c">
                            <p class="user-name">{{item['user']['first_name']+' '+item['user']['last_name']}}</p>
                            <p class="user-name">{{item['st_id']}}</p>
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

</style>
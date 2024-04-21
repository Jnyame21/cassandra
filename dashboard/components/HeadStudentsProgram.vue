<script setup lang="ts">

const elementsStore = useElementsStore()

interface Props {
    program: any;
}

const { program } = defineProps<Props>()


</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <v-table fixed-header height="300px">
        <thead>
        <tr>
          <th class="table-head">CLASS</th>
          <th class="table-head">FORM</th>
          <th class="table-head">STUDENTS</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(clas, i) in program['classes']" :key="i">
          <td class="table-data">{{clas['name']}}</td>
          <td class="table-data">{{clas['students_year']}}</td>
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
                          <img class="profile-img" :src="item['img']">
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
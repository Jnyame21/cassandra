<script setup lang="ts">
import { computed } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from './TheLoader.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const staff = computed(() => {
  return userAuthStore.headData.staff
})

const maleStaff = computed(() => {
  return staff.value?.filter(item => item['gender'].toLowerCase() === 'male').length || 0
})

const femaleStaff = computed(() => {
  return staff.value?.filter(item => item['gender'].toLowerCase() === 'female').length || 0
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStaff`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStaff` }">

    <div class="content-header" v-if="staff">
      <div class="content-header-text">
        TOTAL NUMBER OF STAFF:
        <span class="content-header-text-value">
          {{ staff.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STAFF:
        <span class="content-header-text-value">
          {{ maleStaff }} <span v-if="staff.length > 0">[{{ ((maleStaff / staff.length) * 100).toFixed(1) }}%]</span>
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STAFF:
        <span class="content-header-text-value">
          {{ femaleStaff }} <span v-if="staff.length > 0">[{{ ((femaleStaff / staff.length) * 100).toFixed(1)}}%]</span>
        </span>
      </div>
    </div>
    <TheLoader v-if="!staff" :func="userAuthStore.getHeadData" />
    <v-table fixed-header class="table" v-if="staff">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">ROLES</th>
          <th class="table-head">DEPARTMENTS</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">DATE EMPLOYED</th>
          <th class="table-head">RELIGION</th>
          <th class="table-head">HOME CITY/TOWN</th>
          <th class="table-head">REGION/STATE</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">ALT CONTACT</th>
          <th class="table-head">RESIDENTIAL ADDRESS</th>
          <th class="table-head">EMAIL</th>
          <th class="table-head">IMAGE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_staff, index) in staff" :key="index">
          <td class="table-data">
            <v-btn class="mr-1" size="x-small" v-if="_staff.staff_id === userAuthStore.userData['staff_id']" color="black">YOU</v-btn>{{ _staff['user'] }}
            <v-list-item-subtitle>
              {{ _staff['staff_id'] }}
            </v-list-item-subtitle>
          </td>
          <td class="table-data">
            {{ _staff['gender'].toUpperCase() }}
          </td>
          <td class="table-data">
            <v-chip class="ma-2" v-for="(role, ind) in _staff.roles" :key="ind" :text="`${role.split('|')[1]} ${role.split('|')[0]}`" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip v-for="(department, ind) in _staff.departments" :key="ind" :text="`${department.split('|')[0]} [${department.split('|')[1]}]`" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip v-for="(_subj, ind) in _staff.subjects" :key="ind" :text="`${_subj.split('|')[0]}(${_subj.split('|')[1]})`" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            {{ _staff['dob'] }}
          </td>
          <td class="table-data">
            {{ _staff['date_enrolled'] }}
          </td>
          <td class="table-data">
            {{ _staff['religion'] }}
          </td>
          <td class="table-data">
            {{ _staff['pob'] }}
          </td>
          <td class="table-data">
            {{ _staff['region'] }}
          </td>
          <td class="table-data">
            {{ _staff['nationality'] }}
          </td>
          <td class="table-data">
            {{ _staff['contact'] }}
          </td>
          <td class="table-data">
            {{ _staff['alt_contact'] }}
          </td>
          <td class="table-data">
            {{ _staff['address'] }}
          </td>
          <td class="table-data">
            {{ _staff['email'] }}
          </td>
          <td class="table-data">
            <img class="profile-img" :src="_staff['img']">
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 20% !important;
}


</style>
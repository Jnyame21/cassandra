<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import TheLoader from '@/components/TheLoader.vue'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const teacherSubjects = ref<string[]>([])


const staff = computed(() => {
  return userAuthStore.otherRolesData.staff
})

const maleStaff = computed(() => {
  return staff.value?.filter((item: any) => item['gender'].toLocaleLowerCase() === 'male').length || 0
})

const femaleStaff = computed(() => {
  return staff.value?.filter((item: any) => item['gender'].toLocaleLowerCase() === 'female').length || 0
})

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string, teacher_subjects:string[]) => {
  teacherSubjects.value = teacher_subjects
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'OtherRolesStaff'" :class="{ 'is-active-page': elementsStore.activePage === 'OtherRolesStaff' }">

    <!-- teacher subjects overlay -->
    <div id="TeacherTeachersSubjectsOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('TeacherTeachersSubjectsOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subject, index) in teacherSubjects" :key=index>{{subject.split('|')[0]}}( {{ subject.split('|')[1]}} )</p>
        </div>
      </div>
    </div>
    
    <TheLoader :func="userAuthStore.getTeacherData" v-if="!staff"/>
    <div class="content-header stats" v-if="staff">
      <div class="content-header-text">
        TOTAL NUMBER OF STAFF:
        <span class="content-header-text-value">
          {{ staff.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STAFF:
        <span class="content-header-text-value">
          {{ maleStaff }} [{{ ((maleStaff / staff.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STAFF:
        <span class="content-header-text-value">
          {{ femaleStaff }} [{{ ((femaleStaff / staff.length) * 100).toFixed(1) }}%]
        </span>
      </div>
    </div>
    <v-table fixed-header class="table" v-if="staff">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">ROLES</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">DEPARTMENTS</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">ALT CONTACT</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">ADDRESS</th>
          <th class="table-head">EMAIL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_staff, index) in staff" :key="index">
          <td class="table-data">
            <v-btn class="mr-1" size="x-small" v-if="_staff.staff_id === userAuthStore.userData['staff_id']" color="black">YOU</v-btn>{{ _staff.user }}
            <v-list-item-subtitle>{{ _staff.staff_id }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            {{ _staff.gender }}
          </td>
          <td class="table-data">
            <v-chip v-for="(role, ind) in _staff.roles" :key="ind" :size="elementsStore.btnSize1" >{{ role.split('|')[1] }} {{ role.split('|')[0] }}</v-chip>
          </td>
          <td class="table-data">
            <v-btn @click="showOverlay('TeacherTeachersSubjectsOverlay', _staff.subjects)" color="blue" :size="elementsStore.btnSize1">
              VIEW SUBJECTS
            </v-btn>
          </td>
          <td class="table-data">
            <v-chip v-for="(department, ind) in _staff.departments" :key="ind" :size="elementsStore.btnSize1">{{ department.split('|')[0] }}({{ department.split('|')[1] }})</v-chip>
          </td>
          <td class="table-data">
            {{ _staff.contact }}
          </td>
          <td class="table-data">
            {{ _staff.alt_contact }}
          </td>
          <td class="table-data">
            {{ _staff.nationality }}
          </td>
          <td class="table-data">
            <img class="profile-img" :src="_staff.img">
          </td>
          <td class="table-data">
            {{ _staff.address }}
          </td>
          <td class="table-data">
            {{ _staff.email }}
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header{
  height: 15% !important;
}

.overlay-card {
  max-width: 600px !important;
} 
.overlay-card-info-container {
  margin-top: 3em !important;
}

@media screen and (min-width: 400px) {
  .content-header-text {
    font-size: .75rem !important;
  }
}

@media screen and (min-width: 576px) {

  .content-header-text {
    font-size: .8rem !important;
  }
}

@media screen and (min-width: 767px) {
  .content-header-text {
    font-size: .85rem !important;
  }
}

@media screen and (min-width: 1000px) {
  .content-header-text {
    font-size: .9rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .content-header-text {
    font-size: 1rem !important;
  }
}


</style>
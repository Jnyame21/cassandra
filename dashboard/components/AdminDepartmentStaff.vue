<script setup lang="ts">

const props = defineProps({
  staff: null,
  overlayIndex: null,
})


const userAuthStore = useUserAuthStore()
const loading = ref(false)
const formErrorMessage = ref('')
const stfId = ref('')


const hidOverlay = ()=>{
  const overlay = document.getElementById(`deleteStaff${props.overlayIndex}`)
  overlay ? overlay.style.display = "none" : null
  formErrorMessage.value = ''
  stfId.value = ''
}

const deleteStaff = async()=>{
  loading.value = true
  const formData = new FormData()
  formData.append('staffId', stfId.value)
  formData.append('type', 'delete-staff')

  await axiosInstance.post('sch-admin/staff', formData)
  .then(response =>{
      const data = response.data
      const department = userAuthStore.adminStaff.departments.find(departmentItem => departmentItem['name']===data['department_name']);
      if (department){
          const department_index = userAuthStore.adminStaff.departments.indexOf(department);
          const staffArray = userAuthStore.adminStaff.departments[department_index]['teachers'].filter(stf => stf['staff_id'] !== stfId.value)
          userAuthStore.adminStaff.departments[department_index]['teachers'] = staffArray;
      }
      hidOverlay()
      loading.value = false
  })
  .catch(e =>{
    formErrorMessage.value = 'Oops! something went wrong. Check your internet connection and try again'
    loading.value = false
  })

}

const showOverlay = (staffId: any)=>{
  stfId.value = staffId
  const overlay = document.getElementById(`deleteStaff${props.overlayIndex}`)
  overlay ? overlay.style.display = 'flex' : null
}


</script>

<template>
  <div :id="`deleteStaff${props.overlayIndex}`" class="overlay" v-if="userAuthStore.userData['school']['delete_staff']">
    <v-card class="d-flex flex-column align-center">
      <v-card-text style="font-size: .8rem; font-family: sans-serif; text-align: left; line-height: 1.2; font-weight: bold">
        <p>Continue to delete ?</p>
        <p v-if="formErrorMessage" class="mt-5" style="color: red">{{ formErrorMessage }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn :loading="loading" color="red" class="mr-5" elevation="4" @click="deleteStaff">YES</v-btn>
        <v-btn :disabled="loading" color="blue" class="ml-5" elevation="4" @click="hidOverlay">NO</v-btn>
      </v-card-actions>
    </v-card>
  </div>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!props.staff || props.staff.length ===0 " />
      <v-table fixed-header height="50dvh" v-if="props.staff && props.staff.length > 0">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">USERNAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">STAFF ID</th>
          <th class="table-head">SUBJECT(S)</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['delete_staff']">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(staff, index) in props.staff" :key="index">
          <td class="table-data">
            {{staff['user']['first_name']}} {{staff['user']['last_name']}}
            <span style="color: seagreen;" v-if="staff['role'] === 'hod'">[HOD]</span>
          </td>
          <td class="table-data username">{{staff['user']['username']}}</td>
          <td class="table-data username">{{staff['gender']}}</td>
          <td class="table-data">{{staff['staff_id']}}</td>
          <td class="table-data">
            <p v-for="(subject, i) in staff['subjects']" :key="i">{{subject['name']}}</p>
          </td>
          <td class="table-data username">{{staff['dob']}}</td>
          <td class="table-data">
            <img class="profile-img" :src="staff['img']">
          </td>
          <td class="table-data"  v-if="userAuthStore.userData['school']['delete_staff']">
            <v-btn @click="showOverlay(staff['staff_id'])" color="red" size="x-small">delete</v-btn>
          </td>            
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


.username{
  text-transform: none;
}



.overlay{
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  display: none;
  background-color: rgba(0,0,0,0.7);
  align-items: center;
  justify-content: center;
  z-index: 10;
}


</style>
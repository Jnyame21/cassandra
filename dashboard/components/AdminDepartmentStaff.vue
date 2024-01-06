<script setup lang="ts">

const props = defineProps({
  staff: null,
})

const elementsStore = useElementsStore()
const userAuthStore = useUserAuthStore()
const deleteLoading = ref(1000)

const deleteStaff = async(staffId: any, index: number)=>{
    deleteLoading.value = index
    const formData = new FormData()
    formData.append('staffId', staffId)
    formData.append('type', 'delete-staff')

    await axiosInstance.post('sch-admin/staff', formData)
    .then(response =>{
        const data = response.data
        const department = userAuthStore.adminStaff.departments.find(departmentItem => departmentItem['name']===data['department_name']);
        if (department){
            const department_index = userAuthStore.adminStaff.departments.indexOf(department);
            const staffArray = userAuthStore.adminStaff.departments[department_index]['teachers'].filter(stf => stf['staff_id'] !== staffId)
            userAuthStore.adminStaff.departments[department_index]['teachers'] = staffArray;
        }
        deleteLoading.value = 1000
    })
    .catch(e =>{
        deleteLoading.value = 1000
        return Promise.reject(e)
    })

}

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
          <th class="table-head">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(staff, index) in props.staff" :key="index">
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
          <td class="table-data">
            <v-btn :loading="deleteLoading===index" @click="deleteStaff(staff['staff_id'], index)" size="x-small" class="edit-btn remove">delete</v-btn>
          </td>            
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.edit-btn{
  font-size: .7rem;
  padding: .1em .5em;
}

.remove{
  font-size: .5rem;
  background-color: red;
  color: white;
  margin-left: 2em;
}
.remove:hover{
  color: yellow;
}


</style>
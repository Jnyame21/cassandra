<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const loading = ref(false)
const formErrorMessage = ref('')
const headId = ref('')


const hidOverlay = ()=>{
  const overlay = document.getElementById('deleteHead')
  overlay ? overlay.style.display = "none" : null
  formErrorMessage.value = ''
  headId.value = ''
}

const deleteHead = async()=>{
  loading.value = true
  formErrorMessage.value = ''
  const formData = new FormData()
  formData.append('headId', headId.value)
  formData.append('type', 'delete-head')

  await axiosInstance.post('sch-admin/head', formData)
  .then(response =>{
      const data = response.data
      const head = userAuthStore.adminHeads.find(headItem => headItem['head_id']===headId.value);
      if (head){
          const head_index = userAuthStore.adminHeads.indexOf(head);
          userAuthStore.adminHeads.splice(head_index, 1);
      }
      hidOverlay()
      loading.value = false
  })
  .catch(e =>{
    formErrorMessage.value = 'Oops! something went wrong. Check your internet connection and try again'
    loading.value = false
  })

}

const showOverlay = (head_id: any)=>{
  headId.value = head_id
  const overlay = document.getElementById("deleteHead")
  overlay ? overlay.style.display = 'flex' : null
}


</script>

<template>
  <div id="deleteHead" class="overlay" v-if="userAuthStore.userData['school']['delete_staff']">
    <v-card class="d-flex flex-column align-center">
      <v-card-text style="font-size: .8rem; font-family: sans-serif; text-align: left; line-height: 1.2; font-weight: bold">
        <p>Continue to delete ?</p>
        <p v-if="formErrorMessage" class="mt-5" style="color: red">{{ formErrorMessage }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn :loading="loading" class="overlay-btn mr-5" elevation="4" @click="deleteHead">YES</v-btn>
        <v-btn :disabled="loading" class="overlay-btn ml-5" elevation="4" @click="hidOverlay">NO</v-btn>
      </v-card-actions>
    </v-card>
  </div>
    <div style="width: 100%; position: relative; height: 100%">
      <TheLoader v-if="!userAuthStore.adminHeads" />
      <NoData :message="'No data yet'"  v-if="userAuthStore.adminHeads && userAuthStore.adminHeads.length === 0 "/>
      <v-table fixed-header height="55dvh"  v-if="userAuthStore.adminHeads && userAuthStore.adminHeads.length > 0 ">
        <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">USERNAME</th>
          <th class="table-head">STAFF ID</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['delete_staff']">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(head, index) in userAuthStore.adminHeads" :key="index">
          <td class="table-data">
            {{head['user']['first_name']}} {{head['user']['last_name']}}
            <span style="color: seagreen;">[ {{head['role']}} ]</span>
          </td>
          <td class="table-data username">{{head['user']['username']}}</td>
          <td class="table-data">{{head['head_id']}}</td>
          <td class="table-data">
           {{ head['gender'] }}
          </td>
          <td class="table-data">{{head['dob']}}</td>
          <td class="table-data">
            <img class="profile-img" :src="head['img']">
          </td>
          <td class="table-data"  v-if="userAuthStore.userData['school']['delete_staff']">
            <v-btn @click="showOverlay(head['head_id'])" size="x-small" class="edit-btn remove">delete</v-btn>
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

.username{
  text-transform: none;
}
.remove{
  font-size: .5rem;
  background-color: red;
  color: white;
  margin-left: 2em;
}
.remove:hover{
  color: yellow;
  background-color: seagreen;
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

.overlay-btn{
  background-color: lightseagreen;
  color: yellow;
  font-family: Verdana, "sans-serif";
  font-size: .7rem;
  margin-right: 2em;
  margin-left: 2em;

}
.overlay-btn:hover{
  background-color: mediumseagreen;
}


</style>
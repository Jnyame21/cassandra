<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const showMessage = ()=>{
  const overlay = document.getElementById('staffMessage')
  overlay ? overlay.style.display = 'flex' : null
}

const showOverlay = ()=>{
  const overlay = document.getElementById('logout')
    if (overlay){
      elementsStore.overlayPath = '/'
      overlay.style.display = 'flex'
    }
}


</script>

<template>
    <header class="header flex-all-c" v-if="userAuthStore.userData">
        <StaffDrawer v-if="userAuthStore.userData['role']==='staff' || userAuthStore.userData['role']==='head' " />
        <StudentsDrawer v-if="userAuthStore.userData['role']==='student' " />
        <p class="last-login" v-if="userAuthStore.userData && userAuthStore.userData['last_login']">Last Login: {{userAuthStore.userData['last_login']}}</p>
        <div class="info-container">
          <div class="profile-container">
            <img @click.stop="elementsStore.drawer =!elementsStore.drawer" class="user-img" :src="elementsStore.getBaseUrl+userAuthStore.userData['img']">
            <div class="name-container">
              <p class="user-name">{{userAuthStore.userData['first_name']}} {{userAuthStore.userData['last_name']}}</p>
              <p class="user-username">{{ userAuthStore.userData['username'] }}</p>
            </div>
          </div>
          <div class="flex-all">
            <p class="year-info">ACADEMIC CALENDAR: {{userAuthStore.activeAcademicYear}} SEMESTER: {{userAuthStore.activeTerm}}</p>
          </div>
          <div v-if="userAuthStore.userData['role']=== 'staff' || userAuthStore.userData['role']=== 'head' " class="flex-all">
            <v-icon @click="showMessage" class="message" color="yellow" icon="mdi-bell"/>
            <StaffMessage id="staffMessage" />
          </div>
          <button @click="showOverlay()" class="logout-btn page-btn">LOGOUT<v-icon icon="mdi-logout"/></button>
        </div>
      </header>
</template>

<style scoped>

.year-info{
  font-size: .5rem;
  margin: .5em;
  color: yellow;
  font-family: monospace;
}
.message{
    box-shadow: 0px 0px 2px black;
    border-radius: .1em;
    cursor: pointer;
    padding: .1em .2em;
    width: 40px
  }
  .message:hover{
    box-shadow: 1px 1px 4px black;
  }
  
  #staffMessage{
    display: none;
  }
  
.header{
    height: 10vh; 
    height: 10dvh; 
    margin-top: 0 !important; 
    background-color: seagreen; 
    width: 100%
}

.last-login{
    font-size: .6rem;
    width: 100%;
    text-transform: uppercase;
    text-align: center;
    font-family: monospace;
    color: yellow;
}

.info-container{
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.profile-container{
    width: max-content;
    display: flex;
    padding: .2em;
    margin-left: 1em;
}

.user-img{
    width: 30px;
    height: 30px;
    border-radius: 50%;
}

.user-img:hover{
    box-shadow: 0px 0px 10px black;
    cursor: pointer;
}

.name-container{
    display: flex;
    flex-direction: column;
    width: max-content;
}

.user-name{
    font-size: .7rem;
    color: yellow;
}

.user-username{
    font-size: .7rem;
    color: yellow;
}

.logout-btn{
    font-size: .7rem;
    padding: .2em .5em;
    margin-right: 1em;
    margin-top: .8em;
}

@media screen and (min-width: 576px) {
    .last-login{
        font-size: .7rem;
    }
    .year-info{
      font-size: .7rem;
    }
   
}

</style>
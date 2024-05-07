<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const showMessage = ()=>{
  const overlay = document.getElementById('Notification')
  overlay ? overlay.style.display = 'flex' : console.log('no overlay')
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
            <img @click.stop="elementsStore.drawer =!elementsStore.drawer" class="user-img" :src="userAuthStore.userData['img']">
            <div class="name-container">
              <p class="user-name">{{userAuthStore.userData['first_name']}} {{userAuthStore.userData['last_name']}}</p>
              <p class="user-username">{{ userAuthStore.userData['username'] }}</p>
            </div>
          </div>
          <div class="flex-all">
            <p v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']" class="year-info">ACADEMIC CALENDAR: {{userAuthStore.activeAcademicYear}} SEMESTER: {{userAuthStore.activeTerm}}</p>
            <p v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']" class="year-info">ACADEMIC CALENDAR: {{userAuthStore.activeAcademicYear}} TRIMESTER: {{userAuthStore.activeTerm}}</p>
          </div>
          <div class="flex-all">
            <v-icon @click="showMessage" class="notice" color="yellow" icon="mdi-bell"/>
            <NoticeOverlay id="Notification" />
          </div>
          <button @click="showOverlay()" class="logout-btn">LOGOUT<v-icon icon="mdi-logout"/></button>
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
.notice{
    box-shadow: 0px 0px 2px black;
    border-radius: .1em;
    cursor: pointer;
    padding: .1em .2em;
    width: 40px
  }
  .message:hover{
    box-shadow: 1px 1px 4px black;
  }
  
  #Notification{
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
  background-color: lightseagreen;
  box-shadow: 1px 1px 5px black;
  font-size: .7rem;
  padding: .2em .5em;
  margin-left: .5em;
  margin-right: .5em;
  border-radius: .2em;
  color: white;
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
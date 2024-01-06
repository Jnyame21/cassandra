<script setup lang="ts">

const userAuthStore = useUserAuthStore()


</script>

<template>
    <footer class="footer" v-if="userAuthStore.userData">
        <p class="footer-text">© 2024 EduAAP</p>
      </footer>
</template>

<style scoped>

.footer{
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 5vh;
    height: 5dvh;
    align-items: center;
    background-color: seagreen;
}

.footer-text{
    font-size: .6rem;
    color: yellow;
}

</style>
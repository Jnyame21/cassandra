<script setup lang="ts">
import { onMounted, ref } from 'vue'

const stillLoading = ref(true)


onMounted(()=>{
    setTimeout(()=>{
        stillLoading.value = false
    }, 15000)
})


</script>


<template>
<div class="loaderOverlay flex-all-c">
    <v-progress-circular v-if="stillLoading" indeterminate></v-progress-circular>
    <h4 v-if="!stillLoading" class="no-data">
        <p>No Data Yet</p>
    </h4>
</div>
</template>

<style scoped>

.loaderOverlay{
    width: 100%;
    height: 100%;
    background-color: white;
}


</style>
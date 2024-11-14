<script setup lang="ts">
import { onMounted, ref } from 'vue'

const loading = ref(true)
const errorMessage = ref('Failed to load data')
interface Props {
    func?: any
}
const props = defineProps<Props>()
const func = props.func || null
const startLoading = ()=>{
    loading.value = true
    setTimeout(()=>{
        loading.value = false
    }, 60*1000)
}

onMounted(()=>{
    startLoading()
})

const reloadData = async()=>{
    startLoading()
    await func()
    .then(()=>{
        loading.value = false
    })
    .catch(()=>{
        loading.value = false
        errorMessage.value = 'An error occurred while fetching data'
    })
}



</script>


<template>
<div class="loaderOverlay flex-all-c">
    <v-progress-circular v-if="loading" indeterminate></v-progress-circular>
    <p v-if="!loading" style="color: red">{{ errorMessage }}</p>
    <v-btn v-if="!loading && func" @click="reloadData" size="small" color="black">Reload</v-btn>
</div>
</template>

<style scoped>

.loaderOverlay{
    width: 100% !important;
    height: 100% !important;
    background-color: white !important;
}


</style>
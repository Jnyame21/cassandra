<script setup lang="ts">

interface Props {
    message: any;
}

const { message } = defineProps<Props>()


</script>


<template>
<div class="w-100 h-100 flex-all-c">
    <h4 class="no-data">
        <p v-if="message">{{ message }}</p>
        <p v-if="!message">No Data Yet</p>
    </h4>
</div>
</template>

<style scoped>



</style>
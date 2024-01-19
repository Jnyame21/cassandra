<script setup lang="ts">

interface Props {
    message: any;
}

const { message } = defineProps<Props>()


</script>


<template>
<div class="w-100 h-100 flex-all-c">
    <h4 class="no-data">
        <p>{{ message }}</p>
    </h4>
</div>
</template>

<style scoped>

.no-data{
    margin-top: 7em;
}


</style>
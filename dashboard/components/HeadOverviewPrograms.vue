<script setup lang="ts">
import { ref } from 'vue';


interface Props {
    program: {
        name: string;
        classes: any;
    };
}

const { program } = defineProps<Props>()


const userAuthStore = useUserAuthStore()
const totalStudents: any = ref([]);
const totalMales: any = ref([])
const totalFemales: any = ref([])
const yearOneStudents: any = ref([]);
const yearOneMales: any = ref([])
const yearOneFemales: any = ref([])
const yearTwoStudents: any = ref([]);
const yearTwoMales: any = ref([])
const yearTwoFemales: any = ref([])
const yearThreeStudents: any = ref([]);
const yearThreeMales: any = ref([])
const yearThreeFemales: any = ref([])


program.classes.forEach((clas: any) => {
    if (clas && clas['students']) {
        clas['students'].forEach((st: any) => {
            totalStudents.value.push(st)
            st['gender'] && st['gender']=== 'MALE' || st['gender']=== 'M' ? totalMales.value.push(st) : totalFemales.value.push(st)
            if (st['current_year'] && st['current_year'] === 1) {
                yearOneStudents.value.push(st);
                st['gender'] && st['gender']=== 'MALE' || st['gender']=== 'M' ? yearOneMales.value.push(st) : yearOneFemales.value.push(st)
            } 
            else if (st['current_year'] && st['current_year'] === 2) {
                yearTwoStudents.value.push(st);
                st['gender'] && st['gender']=== 'MALE' || st['gender']=== 'M' ? yearTwoMales.value.push(st) : yearTwoFemales.value.push(st)
            } 
            else if (st['current_year'] && st['current_year'] === 3){
                yearThreeStudents.value.push(st);
                st['gender'] && st['gender']=== 'MALE' || st['gender']=== 'M' ? yearThreeMales.value.push(st) : yearThreeFemales.value.push(st)
            }
        });
    }
});
 

</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
      <v-table class="mt-5" height="300px" v-if="totalStudents.length > 0">
        <tbody>
        <tr class="table-title-container" style="position: relative">
            <td>Justice</td>
            <td class="subtitle">{{ program.name }}</td>
        </tr>
        <tr>
            <td class="table-data">Total</td>
            <td class="table-data-value">
                {{totalStudents.length}} 
                <span class="table-data" v-if="totalStudents && totalStudents.length >0 && totalStudents[0]['gender']">
                    [ M: {{ totalMales.length }}({{ parseFloat(((totalMales.length/totalStudents.length)*100).toFixed(1)) }})%]
                    [ F: {{ totalFemales.length }}({{ parseFloat(((totalFemales.length/totalStudents.length)*100).toFixed(1)) }})%]
                </span>
            </td>
        </tr>
        <tr>
            <td class="table-data">form one</td>
            <td class="table-data-value">
                {{yearOneStudents.length}} 
                <span class="table-data" v-if="yearOneStudents && yearOneStudents.length >0 && yearOneStudents[0]['gender']">
                    [ M: {{ yearOneMales.length }}({{ parseFloat(((yearOneMales.length/yearOneStudents.length)*100).toFixed(1)) }})%]
                    [ F: {{ yearOneFemales.length }}({{ parseFloat(((yearOneFemales.length/yearOneStudents.length)*100).toFixed(1)) }})%]
                </span>
            </td>
        </tr>
        <tr>
            <td class="table-data">form two</td>
            <td class="table-data-value">
                {{yearTwoStudents.length}} 
                <span class="table-data" v-if="yearTwoStudents && yearTwoStudents.length >0 && yearTwoStudents[0]['gender']">
                    [ M: {{ yearTwoMales.length }}({{ parseFloat(((yearTwoMales.length/yearTwoStudents.length)*100).toFixed(1)) }})%]
                    [ F: {{ yearTwoFemales.length }}({{ parseFloat(((yearTwoFemales.length/yearTwoStudents.length)*100).toFixed(1)) }})%]
                </span>
            </td>
        </tr>
        <tr>
            <td class="table-data">form three</td>
            <td class="table-data-value">
                {{yearThreeStudents.length}} 
                <span class="table-data" v-if="yearThreeStudents && yearThreeStudents.length >0 && yearThreeStudents[0]['gender']">
                    [ M: {{ yearThreeMales.length }}({{ parseFloat(((yearThreeMales.length/yearThreeStudents.length)*100).toFixed(1)) }})%]
                    [ F: {{ yearThreeFemales.length }}({{ parseFloat(((yearThreeFemales.length/yearThreeStudents.length)*100).toFixed(1)) }})%]
                </span>
            </td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


</style>
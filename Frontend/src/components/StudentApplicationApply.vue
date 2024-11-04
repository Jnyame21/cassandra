<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const steps = ref(1)
const selectedUni = ref(null)
const selectedPrograms = ref<string[]>([])
const items = ref([
    'UNIVERSITY', 'PROGRAM', 'E-VOUCHER'
])

const removeItem = (program:string)=>{
    const itemIndex = selectedPrograms.value.indexOf(program)
    itemIndex !== -1 ? selectedPrograms.value.splice(itemIndex, 1) : null
    
}

const addRemoveProgram = (program: string)=>{
    const program_index = selectedPrograms.value.indexOf(program)
    if (selectedPrograms.value.length <4){
        program_index !== -1 ? selectedPrograms.value.splice(program_index, 1) : selectedPrograms.value.push(program)
    }else{
        program_index !== -1 ? selectedPrograms.value.splice(program_index, 1) : null
    }
}

const toggleSlip = ()=>{
    const slip = document.getElementById('programSlip')
    if (slip){
        slip.style.display === 'flex' ? slip.style.display = 'none' : slip.style.display = 'flex'
    }
}

const isSelectedProgram = (program:any)=>{
    return selectedPrograms.value.includes(program)
}

const clearSelectedPrograms = ()=>{
    selectedPrograms.value = []
}

</script>

<template>
    <div style="width: 100%; position: relative; height: 100%">
        <TheLoader v-if="!userAuthStore.studentData.universities"/>
        <NoData :message="'Something went wrong'" v-if="userAuthStore.studentData.universities && userAuthStore.studentData.universities.length === 0"/>
      <v-stepper class="apply-stepper" alt-labels v-model="steps" :items="items" v-if="userAuthStore.studentData.universities && userAuthStore.studentData.universities.length > 0">
        <template v-slot:item.1>
            <v-sheet>
                <v-select v-model="selectedUni" :onchange="clearSelectedPrograms()" label="UNIVERSITY" :items="userAuthStore.studentData.universities" item-title="name" hint="Select the university you want to apply to" persistent-hint variant="outlined" />
            </v-sheet>
        </template>
        <template v-slot:item.2 style="position: relative">
            <p v-if="selectedUni" class="notice mb-10">Select your program of choice in order</p>
            <p v-if="!selectedUni" class="notice mb-10">You didn't select any university. Click on the "PREVIOURS" button to go back</p>
            <v-card id="programSlip" class="flex-all-c" v-if="selectedPrograms.length > 0">
                <v-card-title>
                    <v-btn @click="toggleSlip()" color="red" size="small">X</v-btn>
                </v-card-title>
                <v-list >
                    <v-list-item v-for="(item, index) in selectedPrograms" :key="index" >
                        <template v-slot:prepend>
                            [{{ index+1 }}]
                        </template>
                        <p class="ml-2 slip-item-label">{{ item }}</p>
                        <template v-slot:append>
                            <v-icon @click="removeItem(item)" color="red" icon="mdi-close-circle" />
                        </template>
                    </v-list-item>
                </v-list>
            </v-card>
            <h1 class="program-slip-icon" @click="toggleSlip()" >
                {{ selectedPrograms.length }}
            </h1>

            <v-sheet class="programs-container" v-for="(uni, index) in userAuthStore.studentData.universities" :key="index">
                
                <!-- KNUST -->
                <v-table v-if="selectedUni === 'KWAME NKRUMAH UNIVERSITY OF SCIENCE AND TECHNOLOGY - KNUST' && uni['name'] === 'KWAME NKRUMAH UNIVERSITY OF SCIENCE AND TECHNOLOGY - KNUST'" >
                    <thead>
                        <th class="table-data" >PROGRAM</th>
                        <th class="table-data" >CUT-OFF POINT</th>
                    </thead>
                    <tbody>
                        <tr class="program-row table-data-value" @click="addRemoveProgram(`${program['name']} - ${program['cut_off_point']}`)" v-for="(program, index) in uni['programs']" :key="index" :class="{'active': isSelectedProgram(`${program['name']} - ${program['cut_off_point']}`)}" >
                            <td class="pa-0" >{{program['name']}}</td>
                            <td class="pa-0" >{{program['cut_off_point']}}</td>
                        </tr>
                    </tbody>
                </v-table>

                <!-- UG -->
                <v-table v-if="selectedUni === 'UNIVERSITY OF GHANA - UG(LEGON)' && uni['name'] === 'UNIVERSITY OF GHANA - UG(LEGON)'" >
                    <thead>
                        <th class="table-data" >PROGRAM</th>
                        <th class="table-data" >CUT-OFF POINT(1st CHOICE)</th>
                        <th class="table-data" >CUT-OFF POINT(2nd CHOICE)</th>
                        <th class="table-data" >SUBJECT REQUIREMENT</th>
                    </thead>
                    <tbody>
                        <tr class="program-row table-data-value"  @click="addRemoveProgram(program['name'])" v-for="(program, index) in uni['programs']" :key="index"  :class="{'active': isSelectedProgram(program['name'])}">
                            <td class="pa-0" >{{program['name']}}</td>
                            <td class="pa-0" >{{program['cut_off_point_choice_1']}}</td>
                            <td class="pa-0">{{program['cut_off_point_choice_2']}}</td>
                            <td class="pa-0" >{{program['subject_requirement']}}</td>
                        </tr>
                    </tbody>
                </v-table>
                
                <!-- UCC -->
                <v-table v-if="selectedUni === 'UNIVERSITY OF CAPE COAST - UCC' && uni['name'] === 'UNIVERSITY OF CAPE COAST - UCC' ">
                    <thead>
                        <th class="table-data" >PROGRAM</th>
                        <th class="table-data" >CUT-OFF POINT(MALES)</th>
                        <th class="table-data" >CUT-OFF POINT(FEMALES)</th>
                    </thead>
                    <tbody>
                        <tr class="program-row table-data-value"  @click="addRemoveProgram(`${program['name']} - Males[${program['cut_off_point_male']}] - Females[${program['cut_off_point_female']}]`)" v-for="(program, index) in uni['programs']" :key="index"  :class="{'active': isSelectedProgram(`${program['name']} - Males[${program['cut_off_point_male']}] - Females[${program['cut_off_point_female']}]`)}">
                            <td class="pa-0" >{{program['name']}}</td>
                            <td class="pa-0" >{{program['cut_off_point_male']}}</td>
                            <td class="pa-0" >{{program['cut_off_point_female']}}</td>
                        </tr>
                    </tbody>
                </v-table>
            </v-sheet>
        </template>
      </v-stepper>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.programs-container{
    max-width: 1200px;
}

#programSlip{
    position: fixed;
    width: 100%;
    max-width: 700px !important;
    display: none;
    top: 40%;
    right: 0;
    z-index: 20;
}

.program-slip-icon{
    background-color: aqua;
    width: fit-content;
    position: fixed;
    padding: 0 .5em;
    top: 60%;
    left: 0;
    z-index: 15;
    border-radius: 1em;
}

.program-slip-icon:hover{
    cursor: pointer;
    background-color: black;
    color: white;
}

.slip-item-label{
    font-size: .6rem;
}

.table{
    padding: 0 !important;
    margin: 0 !important;
}

.program-row:hover{
    background-color: whitesmoke;
    cursor: pointer;
}

.apply-stepper{
    max-width: 2000px;
}

.notice{
    text-align: center;
    color: red;
}

.active{
    background-color: whitesmoke;
}

.table-data-value{
    color: green;
}

@media screen and (min-width: 400px) {
    .slip-item-label{
        font-size: .7rem;
    }
}

@media screen and (min-width: 576px) {
    .slip-item-label{
        font-size: .8rem;
    }
}



</style>
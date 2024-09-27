import { resolve } from "chart.js/helpers"

export const sleep = (ms:number)=>{
    return new Promise(resolve => setTimeout(resolve, ms));
}

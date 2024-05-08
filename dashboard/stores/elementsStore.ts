import { defineStore } from "pinia";


interface states {
    overlayMessage: string;
    overlayMessageColor: any;
    overlayPath: any;
    logout: any;
    isLoading: boolean;
    drawer: boolean;
    activePage: string;
}

export const useElementsStore = defineStore('elementsStore', {
    state: (): states =>{
        return{
            overlayMessage: '',
            overlayMessageColor: null,
            overlayPath: null,
            logout: null,
            isLoading: true,
            drawer: false,
            activePage: 'page1',
        }
    },

    getters: {
        getBaseUrl: ()=>{
            if (process.env.NODE_ENV=== 'production'){
                return "https://cassandra.onrender.com"
            }else{
                return 'http://localhost:8000'
            }
        },
    },

    actions: {

        ShowOverlay(message: string, messageColor: any, path: any, logout: any){
            const overlay = document.getElementById('session-alert')
            if (overlay){
                this.overlayMessage = message
                this.overlayPath = path
                this.logout = logout
                this.overlayMessageColor = messageColor
                overlay.style.display = 'flex'
            }
        }
    }
})


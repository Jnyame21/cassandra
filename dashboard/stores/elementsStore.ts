import { defineStore } from "pinia";


interface states {
    overlayMessage: string;
    overlayMessageColor: any;
    overlayPath: any;
    logout: any;
    isLoading: boolean;
    drawer: boolean;
    navDrawer: boolean;
    activePage: string;
    errorMessage: boolean;
    deleteFunction: any;
    deleteOverlayMessage: string;
    btnSize1: string;
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
            navDrawer: false,
            activePage: 'page1',
            errorMessage: false,
            deleteFunction: null,
            deleteOverlayMessage: '',
            btnSize1: 'x-small',
        }
    },

    getters: {
        getBaseUrl: ()=>{
            if (process.env.NODE_ENV=== 'production'){
                return "https://cassandra-o5ft.onrender.com"
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
        },

        ShowLoadingOverlay(){
            const overlay = document.getElementById('LoadingOverlay')
            overlay ? overlay.style.display = 'flex' : null
        },

        HideLoadingOverlay(){
            const overlay = document.getElementById('LoadingOverlay')
            overlay ? overlay.style.display = 'none' : null
        },

        ShowDeletionOverlay(func:any, message:string){
            const overlay = document.getElementById('deleteOverlay')
            this.deleteFunction = func
            this.deleteOverlayMessage = message
            overlay ? overlay.style.display = 'flex' : null
        },
    }
})


import { defineStore } from "pinia";


interface states {
    overlayMessage: string;
    overlayMessageColor: any;
    isLoading: boolean;
    drawer: boolean;
    navDrawer: boolean;
    onDesk: boolean;
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
            isLoading: true,
            drawer: false,
            navDrawer: false,
            onDesk: false,
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
            }
            else{
                return 'http://localhost:8000'
            }
        },
    },

    actions: {

        ShowOverlay(message: string, messageColor: any){
            const overlay = document.getElementById('AlertOverlay')
            if (overlay){
                this.overlayMessage = message
                this.overlayMessageColor = messageColor
                overlay.style.display = 'flex'
            }
        },

        ShowLoadingOverlay(){
            const overlay = document.getElementById('LoadingOverlay')
            if (overlay){
                overlay.style.display = 'flex'
            }
        },

        HideLoadingOverlay(){
            const overlay = document.getElementById('LoadingOverlay')
            if (overlay){
                overlay.style.display = 'none'
            }
        },

        ShowDeletionOverlay(func:any, message:string){
            const overlay = document.getElementById('deleteOverlay')
            this.deleteFunction = func
            this.deleteOverlayMessage = message
            if (overlay){
                overlay.style.display = 'flex'
            }
        },
    }
})


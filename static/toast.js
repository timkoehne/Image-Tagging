class Toast {
    constructor(message) {
        this.message = message
        this.toast = document.createElement("div")
        this.toast.id = "toast"
        this.toast.innerHTML = `<p>${this.message}</p>`
        document.body.appendChild(this.toast)
    }
    show() {
        this.toast.classList.add("show")
        setTimeout(() => {
            this.toast.classList.remove("show")
        }, 1500)
    }
}
const myToast = new Toast("This is a toast notification!")

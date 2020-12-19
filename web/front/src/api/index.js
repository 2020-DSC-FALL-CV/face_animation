import Axios from "axios"

const api = Axios.create({
    baseURL: "https://api.sshz.kr/",
    headers: {
        Accept: '*'
    }
    // baseURL:"http://127.0.0.1:8080"
})

export default api;
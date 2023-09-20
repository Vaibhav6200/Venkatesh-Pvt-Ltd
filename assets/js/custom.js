
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function select_date(pressed_button){
    const appointment_date = document.getElementById('appointment_date')
    const date_slotBtn = appointment_date.querySelectorAll('.slot_btn')
    date_slotBtn.forEach(button => button.classList.remove('slot_btn_active'));
    pressed_button.classList.add('slot_btn_active')
}

function select_time(pressed_button){
    const appointment_time = document.getElementById('appointment_time')
    const time_slotBtn = appointment_time.querySelectorAll('.slot_btn')
    time_slotBtn.forEach(button => button.classList.remove('slot_btn_active'));
    pressed_button.classList.add('slot_btn_active')
}

function addToCart(e){

    let sub_service_id = e.value
    let url = "/cart/add_to_cart/"
    let data= {
        sub_service_id:sub_service_id,
    }
    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
}
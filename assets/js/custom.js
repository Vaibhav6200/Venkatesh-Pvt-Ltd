var date_selected = null
var time_selected = null
var selected_service = null



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
    const date_slotBtn = document.querySelectorAll('.date_slot_btn')
    date_slotBtn.forEach(button=>button.classList.remove('slot_btn_active', 'selected-date'));
    pressed_button.classList.add('slot_btn_active', 'selected-date')
    date_selected = pressed_button
}

function select_time(pressed_button){
    const time_slotBtn = document.querySelectorAll('.time_slot_btn')
    time_slotBtn.forEach(button => button.classList.remove('slot_btn_active', 'selected-time'));
    pressed_button.classList.add('slot_btn_active', 'selected-time')
    time_selected = pressed_button
}


function addToCart(){
    if(date_selected && time_selected){
        let date_slot = date_selected.querySelector('div>div + div').textContent
        let time_slot = time_selected.textContent

        console.log(date_slot)
        console.log(time_slot)

        $("#timeSlotModal").modal("hide");

        document.querySelectorAll('.date_slot_btn').forEach(button=>button.classList.remove('slot_btn_active', 'selected-date'));
        document.querySelectorAll('.time_slot_btn').forEach(button => button.classList.remove('slot_btn_active', 'selected-time'));

        let url = "/cart/add_to_cart/"
        let data= {
            sub_service_id:selected_service,
            date_slot: date_slot,
            time_slot: time_slot,
        }
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
            body: JSON.stringify(data)
        })
        .then(res=>res.json())
        .then(data=>{
            document.getElementById('num_of_items').innerHTML = data
        })
        .catch(error=>{
            console.log(error)
        })

        date_selected = null
        time_selected = null
        selected_service = null
    }
    else{
        alert('please select date and time properly')
    }
}


booking_modal = document.getElementById('bookAppointmentModal');

function bookService(sub_service_id){
    selected_service = sub_service_id
    let appointment_date = document.getElementById('appointment_date')
    // let selected_date = appointment_date.querySelector('.selected-date')
    document.querySelectorAll('.date_slot_btn').forEach(button=>{button.classList.remove('disabled')})
    document.querySelectorAll('.time_slot_btn').forEach(button=>{button.classList.remove('disabled')})


    let url = "/cart/get_available_dates/"
    let data= {
        sub_service_id:sub_service_id,
    }
    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(available_dates_map=>{
        let date_buttons = document.querySelectorAll('.date_slot_btn')
        date_buttons.forEach(button => {
            const buttonDateValue = button.getAttribute('value')

            if(available_dates_map[buttonDateValue]){
                button.classList.add('disabled')
            }
        })
    })
    .catch(error=>{
        console.log(error)
    })
}


function handleSelectedDate(){
    let date_slot = date_selected.value

    let url = "/cart/get_available_time_slots/"
    let data= {
        sub_service_id:selected_service,
        date_slot:date_slot,
    }
    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(available_time_map=>{
        let time_buttons = document.querySelectorAll('.time_slot_btn')
        time_buttons.forEach(button => {
            const buttonDateValue = button.getAttribute('value')
            if(available_time_map[buttonDateValue]){
                button.classList.add('disabled')
            }
        })
    })
    .catch(error=>{
        console.log(error)
    })
}
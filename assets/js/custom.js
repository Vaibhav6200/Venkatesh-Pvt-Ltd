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
    // document.getElementById('bookAppointmentModal').setAttribute("data-bs-dismiss", "modal");
}

function select_time(pressed_button){
    const time_slotBtn = document.querySelectorAll('.time_slot_btn')
    time_slotBtn.forEach(button => button.classList.remove('slot_btn_active', 'selected-time'));
    pressed_button.classList.add('slot_btn_active', 'selected-time')
    time_selected = pressed_button
}



function addToCart(cart_btn){
    if(date_selected && time_selected){
        let date_slot = date_selected.querySelector('div>div + div').textContent
        let time_slot = time_selected.textContent

        $("#bookAppointmentModal").modal("hide");

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


// *** QUANTITY SPINNER JAVASCRIPT OF INDIVIDUAL SERVICE PAGE ***
// function increment_total_cost(quantity, service_cost_id, total_cost_id){
//     service_cost = document.getElementById(service_cost_id)
//     total_cost = document.getElementById(total_cost_id)

//     total_cost.innerHTML = parseFloat(quantity)*parseFloat(service_cost.innerHTML)

// }
// function decrement_total_cost(quantity, service_cost_id, total_cost_id){
//     service_cost = document.getElementById(service_cost_id)
//     total_cost = document.getElementById(total_cost_id)
//     total_cost.innerHTML = parseFloat(total_cost.innerHTML) - parseFloat(service_cost.innerHTML)
// }
// function plusFunc(button, service_cost_id, total_cost_id) {
//     let input = button.previousSibling.previousElementSibling;
//     let quantity = parseInt(input.value)
//     quantity = parseInt(quantity)
//     quantity += 1
//     button.previousSibling.previousElementSibling.value = quantity

//     increment_total_cost(quantity, service_cost_id, total_cost_id)
// }
// function minusFunc(button, service_cost_id, total_cost_id) {
//     let input = button.nextSibling.nextElementSibling;
//     let quantity = parseInt(input.value)
//     quantity -= 1
//     if (quantity < 0) quantity = 0
//     button.nextSibling.nextElementSibling.value = quantity

//     if(quantity>0)
//         decrement_total_cost(quantity, service_cost_id, total_cost_id)
//     else
//         document.getElementById(total_cost_id).innerHTML = 0
// }



booking_modal = document.getElementById('bookAppointmentModal')
function bookService(btn, sub_service_id){
    let appointment_date = document.getElementById('appointment_date')
    let selected_date = appointment_date.querySelector('.selected-date')
    selected_service = sub_service_id
}
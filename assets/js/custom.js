
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

function select_date(pressed_button, sub_service_id){
    const appointment_date = document.getElementById('appointment_date')
    const date_slotBtn = appointment_date.querySelectorAll('.slot_btn')
    date_slotBtn.forEach((button)=>{
        button.classList.remove('slot_btn_active')
        button.classList.remove('selected-date')
    } );
    pressed_button.classList.add('slot_btn_active', 'selected-date')

    // var selectedDate = document.querySelector('.selected-date');
    // var selectedQuantity = parseInt(document.getElementById("subservice_" + sub_service_id).querySelector('.in-num').value);
}

function select_time(pressed_button){
    const appointment_time = document.getElementById('appointment_time')
    const time_slotBtn = appointment_time.querySelectorAll('.slot_btn')
    time_slotBtn.forEach(button => button.classList.remove('slot_btn_active'));
    pressed_button.classList.add('slot_btn_active')
}

function addToCart(cart_btn){
    let sub_service_id = cart_btn.value
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
        document.getElementById('num_of_items').innerHTML = data
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
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


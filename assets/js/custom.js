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
    document.getElementById('date_selected_next_button').classList.remove('disabled')
    const date_slotBtn = document.querySelectorAll('.date_slot_btn')
    date_slotBtn.forEach(button=>button.classList.remove('slot_btn_active', 'selected-date'));
    pressed_button.classList.add('slot_btn_active', 'selected-date')
    date_selected = pressed_button
}

function select_time(pressed_button){
    document.getElementById('time_selected_next_button').classList.remove('disabled')
    const time_slotBtn = document.querySelectorAll('.time_slot_btn')
    time_slotBtn.forEach(button => button.classList.remove('slot_btn_active', 'selected-time'));
    pressed_button.classList.add('slot_btn_active', 'selected-time')
    time_selected = pressed_button
}


function addToCart(){
    if(date_selected && time_selected){
        $("#timeSlotModal").modal("hide");

        document.querySelectorAll('.date_slot_btn').forEach(button=>button.classList.remove('slot_btn_active', 'selected-date'));
        document.querySelectorAll('.time_slot_btn').forEach(button => button.classList.remove('slot_btn_active', 'selected-time'));

        let url = "/cart/add_to_cart/"
        let data= {
            sub_service_id:selected_service,
            date_slot: date_selected.value,
            time_slot: time_selected.value,
        }
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
            body: JSON.stringify(data)
        })
        .then(res=>res.json())
        .then(data=>{
            document.getElementById('date_selected_next_button').classList.add('disabled')

            var elements = document.getElementsByClassName('num_of_items');
            for (var i = 0; i < elements.length; i++) {
                elements[i].innerHTML = data;
            }
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
    if(date_selected == null){
        document.getElementById('date_selected_next_button').classList.add('disabled')
    }
    else{

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
}


function handleCartItemRemoval(item_id, cart_id){
    let url = "/cart/remove_cart_item/"
    let data= {
        cart_item_id:item_id,
        cart_id: cart_id
    }
    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById('cart_item_' + item_id).style.display = 'none'

        var elements = document.getElementsByClassName('num_of_items');
        for (var i = 0; i < elements.length; i++) {
            elements[i].innerHTML = data['num_of_items'];
        }

        let grand_total = document.getElementById('grand_total')
        grand_total.innerHTML = data['cart_cost']
        let remove_coupon = data['remove_coupon']
        if(remove_coupon == true){
            document.getElementById('coupon_name').classList.add('d-none')
            document.getElementById('coupon_savings').classList.add('d-none')
        }

        if(data['num_of_items'] == 0){
            location.reload();
        }
    })
    .catch(error=>{
        console.log(error)
    })
}



// ********** PROFILE PAGE JAVASCRIPT **********
function openBio(){
    document.getElementById('my_bio').classList.remove('d-none');
    document.getElementById('my_address').classList.add('d-none')
    document.getElementById('my_profile').classList.add('d-none')
    document.getElementById('my_password').classList.add('d-none')
}
function openAddress(){
    document.getElementById('my_bio').classList.add('d-none');
    document.getElementById('my_address').classList.remove('d-none')
    document.getElementById('my_profile').classList.add('d-none')
    document.getElementById('my_password').classList.add('d-none')
}
function openProfile(){
    document.getElementById('my_bio').classList.add('d-none');
    document.getElementById('my_address').classList.add('d-none')
    document.getElementById('my_profile').classList.remove('d-none')
    document.getElementById('my_password').classList.add('d-none')
}
function openPassword(){
    document.getElementById('my_bio').classList.add('d-none');
    document.getElementById('my_address').classList.add('d-none')
    document.getElementById('my_profile').classList.add('d-none')
    document.getElementById('my_password').classList.remove('d-none')
}
function enableEditing(){
    document.getElementById('first_name').removeAttribute('readonly')
    document.getElementById('last_name').removeAttribute('readonly')
    document.getElementById('email').removeAttribute('readonly')
    document.getElementById('phone').removeAttribute('readonly')
    document.getElementById('bio').removeAttribute('readonly')
    document.getElementById('billing_address').removeAttribute('readonly')
    document.getElementById('new_password').removeAttribute('readonly')
    document.getElementById('confirm_new_password').removeAttribute('readonly')
    document.getElementById('profile_image').removeAttribute('disabled')
    document.getElementById('save_btn').classList.remove('d-none')
}



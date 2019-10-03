function registration_form() {
    el = document.querySelector('.registration_form');
    register_btn = document.querySelector('.registration_btn');

    if (el.style.display == 'none') {
        el.style.display = 'block';
        register_btn.style.display = 'none';
    }
}



function login_form() {
    el = document.querySelector('.login_form');
    login_btn = document.querySelector('.login_btn');

    if (el.style.display == 'none') {
        el.style.display = 'block';
        login_btn.style.display = 'none';
    }
}


function org_form() {
    alert("Org form");
}

function project_form() {
    alert("Project form");
}
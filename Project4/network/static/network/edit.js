document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('#edit').forEach(button => {
        button.addEventListener('click', () => edit_post(button));
    });

    document.querySelectorAll('#save').forEach(button => {
        button.addEventListener('click', () => save_edition(button));
    });

    document.querySelectorAll('#like').forEach(button => {
        button.addEventListener('click', () => like_post(button));
    });

});

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

function edit_post(editbutton) {

    div = editbutton.parentElement;
    content = div.querySelector('#content');
    textarea = div.querySelector('#textarea');
    savebutton = div.querySelector('#save');

    textarea.value = content.textContent;
    
    content.style.display = 'none';
    textarea.style.display = 'block';
    editbutton.style.display = 'none';
    savebutton.style.display = 'block';

}

function save_edition(savebutton) {

    div = savebutton.parentElement;
    content = div.querySelector('#content');
    textarea = div.querySelector('#textarea');
    editbutton = div.querySelector('#edit');

    const text = textarea.value;

    content.textContent = text;

    content.style.display = 'block';
    textarea.style.display = 'none';
    editbutton.style.display = 'block';
    savebutton.style.display = 'none';
    
    const csrftoken = getCookie('csrftoken');

    fetch(`/save/${div.id.substr(4)}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: text
        }),
        headers: {"X-CSRFToken": csrftoken}
    })

}

function like_post(likebutton) {

    console.log("ACA");

    div = likebutton.parentElement;
    likes = div.querySelector('#likes');
    numberoflikes = parseInt(likes.textContent.substr(7)) + 1;
    likes.textContent = "Likes: " + numberoflikes;
    
    const csrftoken = getCookie('csrftoken');

    fetch(`/like/${div.id.substr(4)}`, {
        method: 'PUT',
        headers: {"X-CSRFToken": csrftoken}
    })

}
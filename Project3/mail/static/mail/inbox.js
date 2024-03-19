document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('form').addEventListener('submit', send_email);
    //document.querySelector('#send-email').addEventListener('click', send_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

}

function reply_email(content) {
    
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = content.sender;
    document.querySelector('#compose-subject').value = `Re: ${content.subject}`;
    document.querySelector('#compose-body').value = `\n\nOn ${content.timestamp} ${content.sender} wrote:\n${content.body}`;
}

function add_mail_sent(content) {
    const mail = document.createElement('div');
    mail.style = "cursor: pointer;";
    mail.className = content.read ? 'readmail' : 'unreadmail';
    const recipients = document.createElement('p');
    let recipientsHTML = `<b>To:</b> ${content.recipients[0]}`;
    for (let i = 1; i < content.recipients.length; i++) {
        recipientsHTML += `, ${content.recipients[i]}`;
    }
    recipients.innerHTML = recipientsHTML;
    mail.appendChild(recipients);
    appendChildP(mail, 'Subject', content.subject);
    appendChildP(mail, 'Date', content.timestamp);
    mail.addEventListener('click', function () {
        open_email_sent(content.id);
    });
    document.querySelector('#emails-view').append(mail);
}

function appendChildP(parent, text, info) {
    const element = document.createElement('p');
    element.innerHTML = `<b>${text}:</b> ${info}`;
    parent.append(element);
}

function add_mail_received(content) {
    const mail = document.createElement('div');
    mail.style = "cursor: pointer;";
    mail.className = content.read ? 'readmail' : 'unreadmail';
    appendChildP(mail, 'From', content.sender);
    appendChildP(mail, 'Subject', content.subject);
    appendChildP(mail, 'Date', content.timestamp);
    mail.addEventListener('click', function () {
        open_email_received(content.id);
    });
    document.querySelector('#emails-view').append(mail);
}

function show_email(content) {
    const mail = document.createElement('div');
    mail.className = 'readmail';
    const recipients = document.createElement('p');
    let recipientsHTML = `<b>To:</b> ${content.recipients[0]}`;
    for (let i = 1; i < content.recipients.length; i++) {
        recipientsHTML += `, ${content.recipients[i]}`;
    }
    recipients.innerHTML = recipientsHTML;
    appendChildP(mail, 'From', content.sender);
    mail.appendChild(recipients);
    appendChildP(mail, 'Subject', content.subject);
    appendChildP(mail, 'Date', content.timestamp);
    appendChildP(mail, 'Body', content.body);
    document.querySelector('#email-view').append(mail);
    const reply = document.createElement('button');
    reply.class = "btn btn-primary";
    reply.textContent = "Reply";
    reply.addEventListener('click', function () {
        reply_email(content);
    });
    document.querySelector('#email-view').append(reply);
}

function archive_email(id) {
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    })
    .then(() => load_mailbox('inbox'));
}

function unarchive_email(id) {
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
    })
    .then(() => load_mailbox('inbox'));
}

function open_email_received(id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').innerHTML = '';

    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(content => {
            show_email(content);
            const archive = document.createElement('button');
            archive.class = "btn btn-primary";
            if (content.archived) {
                archive.textContent = "Unarchive";
                archive.addEventListener('click', function () {
                    unarchive_email(content.id);
                });
            } else {
                archive.textContent = "Archive";
                archive.addEventListener('click', function () {
                    archive_email(content.id);
                });
            }
            document.querySelector('#email-view').append(archive);
        });
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
}

function open_email_sent(id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').innerHTML = '';

    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(content => {
            show_email(content);
        });
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {
            // Print emails
            if (mailbox === 'sent') {
                emails.forEach(add_mail_sent);
            } else {
                emails.forEach(add_mail_received);
            }

            // ... do something else with emails ...
        });
}

function send_email(event) {
    event.preventDefault();
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
    })
        .then(response => response.json())
        .then(result => {
            if (result["error"]) {
                alert(result["error"]);
            } else {
                load_mailbox('sent');
            }
        })
    return false;
}

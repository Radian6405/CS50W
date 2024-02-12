document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click',() => compose_email('','',''));

  // By default, load the inbox
  load_mailbox('inbox');

  //sending mail
  document.querySelector('#compose-form').onsubmit = send_mail;

  //opening mail
  document.addEventListener('click', event => open_mail(event));

  //archive mail
  document.querySelector('#archiveButton').onclick = archive_mail;

  //reply mail
  document.querySelector('#replyButton').onclick = reply_mail;
  
});

function reply_mail() {
  fetch(`/emails/${parseInt(this.value)}`)
  .then(response => response.json())
  .then(email => {
    compose_email(email.sender, 
      email.subject.slice(0,3) === 'Re:' ? email.subject : `Re:${email.subject}`, 
      `On ${email.timestamp} ${email.sender} wrote:\n ${email.body}\n\n`);
  });
}

function archive_mail() {
  const archived = (this.innerHTML === 'Archive');
  console.log(archived)
  fetch(`/emails/${parseInt(this.value)}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archived
    })
  })

  location.reload();
}

function open_mail(event) {
  let element = event.target;
  if (!element) {
    return false;
  }
  if (element.parentElement.className === 'list-group-item') {
    element = element.parentElement;
  }
  if (element.className === 'list-group-item'){
    fetch(`/emails/${parseInt(element.id)}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      console.log(email);
      
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#mail-view').style.display = 'block';
      
      document.querySelector('#mailFrom').innerHTML = `<span style="font-weight: bold;">From:</span> ${email.sender}`
      document.querySelector('#mailTo').innerHTML = `<span style="font-weight: bold;">To:</span> ${email.recipients}`
      document.querySelector('#mailTime').innerHTML = `${email.timestamp}`
      document.querySelector('#mailSubject').innerHTML = `${email.subject}`
      document.querySelector('#mailBody').innerHTML = `${email.body.replace(/\r?\n/g, '<br />')}`

      document.querySelector('#replyButton').value = element.id;

      if(!email.read) {
        fetch(`/emails/${parseInt(element.id)}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }

      const archiveButton = document.querySelector('#archiveButton');
      if (document.querySelector('#userEmail').innerHTML === email.sender) {
        archiveButton.style.display = 'none';
      }
      else {
        archiveButton.style.display = 'inline';
        archiveButton.value = email.id;
        if(email.archived) {
          archiveButton.innerHTML = 'Unarchive';
        }
        else {
          archiveButton.innerHTML = 'Archive';
        }
      }
    });
  }
}

function send_mail() {
  const toEmail = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: toEmail,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
  
  return false
}

function compose_email(recipientsText, subjectText, bodyText) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipientsText;
  document.querySelector('#compose-subject').value = subjectText;
  document.querySelector('#compose-body').value = bodyText;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //fetching emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      //creating unordered list
      const mailList = document.createElement('ul');
      mailList.setAttribute('id', 'email-list');
      mailList.setAttribute('class', 'list-group');
      document.querySelector('#emails-view').append(mailList)

      //creating list element for each mail
      emails.forEach(element => {
        const mail = document.createElement('li');
        mail.classList.add("list-group-item");
        mail.setAttribute('id', element.id);
        if (element.read) {
          mail.style.backgroundColor = 'rgb(230,230,230)';
        }

        //mail info
        const nameDiv = document.createElement('div');
        nameDiv.classList.add('nameDiv');
        nameDiv.innerHTML = element.sender;
        mail.append(nameDiv);
        
        const subjectDiv = document.createElement('div');
        subjectDiv.classList.add('subjectDiv');
        subjectDiv.innerHTML = element.subject;
        mail.append(subjectDiv);

        const timeDiv = document.createElement('div');
        timeDiv.classList.add('timeDiv');
        timeDiv.innerHTML = element.timestamp;
        mail.append(timeDiv);

        
        
        mailList.append(mail);
      });
  });
}
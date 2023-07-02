function sendEmail(){
    const serid="service_2ceb68m";
    const templateid="template_oppxk9i";
    emailjs.send(serid,templateid).then((res) => {
        alert("Chek your password");
    }).catch((err) => console.log(err));
}

function mail(){window.location.href='https://mail.google.com/mail/u/0/#inbox?compose=CllgCHrhVJZrbxlQSwhBTJSxSCQmbpxLstjCgQfCqddNvLzrGtBdXWZDpTrLJDSswWXJwlfzddq';}
function facebook(){window.location.href="https://www.facebook.com/mahfoudh.bslimen";}
function linkedIn(){window.location.href="";}


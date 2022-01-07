window.onload = (event) => {
};

// show menu 
const navMenu = document.getElementById('nav-menu'), 
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

// validate if variable exists
if(navToggle){
    navToggle.addEventListener('click', (z) => {
        navMenu.classList.add('show-menu')
    })
}

if(navClose){
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

//remove nav-mobile menu 
const navLink = document.querySelectorAll('.nav_link')

function linkAction() {
    const navMenu = document.getElementById('nav-menu')
    // if each link on nav is clicked, remove show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

//accordion

const skillsContent = document.getElementsByClassName('skills_content'),
        skillsHeader = document.querySelectorAll('.skills_header');

function toggleSkills(){
    let itemClass = this.parentNode.className

    for(i = 0; i < skillsContent.length; i++){
        skillsContent[i].className = 'skills_content skills_close'
    }
    if(itemClass === 'skills_content skills_close'){
        this.parentNode.className = 'skills_content skills_open'
    }
}

skillsHeader.forEach((el) =>{
    el.addEventListener('click', toggleSkills)
})

let swiper = new Swiper(".portfolio_container", {
    cssMode: true,
    loop: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
    },
    mousewheel: true,
    keyboard: true,
  });
  

//   Scroll Active Links
const sections = document.querySelectorAll('section[id]')
function scrollActive(){
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight
        const sectionTop = current.offsetTop - 30;
        sectionId = current.getAttribute('id')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            document.querySelector('.nav_menu a[href*=' + sectionId + ']').classList.add('active_link')
        }else{
            document.querySelector('.nav_menu a[href*=' + sectionId + ']').classList.remove('active_link')
        }
    })
}
window.addEventListener('scroll', scrollActive)

// change header background
function scrollHeader(){
    const nav = document.getElementById('header')
    if(this.scrollY >= 80){
        nav.classList.add('scroll-header')
    }else{
        nav.classList.remove('scroll-header')
    }
}
window.addEventListener('scroll', scrollHeader)

//show scroll top button
function scrollUp(){
    const scrollUp = document.getElementById('scroll-up')

    if(this.scrollY >= 600){
        scrollUp.classList.add('scroll-header')
    }else{
        scrollUp.classList.remove('scroll-header')
    }
}
window.addEventListener('scroll', scrollUp)

// Dark Light Theme
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'uil-sun'

// load session if user selected from last access
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun'

if(selectedTheme){
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove' ](darkTheme)
    themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme)
}

//activate or deactive the theme with the button
themeButton.addEventListener('click', () => {
    // add or remove theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)

    // save session 
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})

// this makes csrf token for ajax calls spec posts
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

const contactForm = document.getElementById('contact-submit');
if(contactForm){
    contactForm.addEventListener("submit", handleContactForm)
    // contactForm.addEventListener("touch", handleContactForm)
}

function handleContactForm(e){
     // prevent page reload
     e.preventDefault();
     // get values from form
     const contactUrl = document.getElementById('contact-form-url').value;
     const FormData = {
         name: contactForm.elements["contact_form_name"].value,
         subject: contactForm.elements["contact_form_subject"].value,
         email: contactForm.elements["contact_form_email"].value,
         message: contactForm.elements["contact_form_message"].value,
     }
 
     if(!contactForm.classList.contains('form-timeout')) {
         submitContact(contactUrl, FormData)
         // adding timeout on contact submit
         formTimeout(contactForm)
         setTimeout(() => {
             contactForm.classList.remove('form-timeout')
         }, 60*1000);
     }else{
         swal({
             title: "Take a break",
             text: "Please take a minute to send another message.",
             icon: "error",
             button: "Close",
           });
     }
     
     contactForm.reset()
}


function formTimeout(formButton){
    formButton.classList.add('form-timeout')
}

function submitContact(url, payload) {
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
        'Content-Type': 'application/json',
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({payload: payload}),
    })
    .then(response => response.json())
    .then(data => {
        // console.log('Success:', data);
        swal("Thanks.", "Message sent.", "success");
        })
}

// Like Button

const postLike = document.getElementById('post-like-submit');
if(postLike){
    postLike.addEventListener("submit", (e) => {
        // prevent page reload
        e.preventDefault();
    
        const postLikeUrl = document.getElementById('post-like-url').value;
        // get values from form
        const FormData = {
            post_id: postLike.elements["post-id"].value,
        }
        // console.log(FormData)
        postAddLike(postLikeUrl, FormData)
        postLike.reset()
    })
}


function postAddLike(url, payload){
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
        'Content-Type': 'application/json',
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({payload: payload}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)

        const likeButton = document.getElementById('post-like-btn'); 
        if(data['isLiked']){
            likeButton.innerHTML = '<i class="uil uil-thumbs-down "></i>&nbsp; Unlike';
        }else{
            likeButton.innerHTML = '<i class="uil uil-thumbs-up "></i>&nbsp; Like';
        }
        
        const totalLike = document.getElementById('total-likes');
        totalLike.textContent = data['total_likes'] + ' Like' + pluralize(data['total_likes'])
    })
}

let userCommentCount = localStorage.getItem('userCommentCount'); // 0
if(!userCommentCount){
    userCommentCount = 0
}
const postComment = document.getElementById('form-add-comment');
if(postComment){
    postComment.addEventListener("submit", (e)=>{
        e.preventDefault();

        const postCommentUrl = document.getElementById('post-comment-url').value;
        // get values from form
        const FormData = {
            post_id: postComment.elements["post-id"].value,
            post_comment: postComment.elements["post-comment"].value,
        }

        // timeout if commented 5 times
        // console.log(userCommentCount)
        if(userCommentCount < 5){
            postAddComment(postCommentUrl, FormData)
        }
        else{
            swal({
                title: "Slow Down.",
                text: "Please take a minute to add another comment",
                icon: "error",
                button: "Close",
              });
            
              setTimeout(() => {
                userCommentCount = 0;
                localStorage.setItem('userCommentCount', userCommentCount)
            }, 60*1000);
        }
        postComment.reset()
    })
}

const commentWrapper = document.getElementById('comments-wrapper');
function postAddComment(url, payload){
    // console.log(payload)
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
        'Content-Type': 'application/json',
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({payload: payload}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)

        // parent first child
        let firstItem = commentWrapper.firstChild
        const commentItem = document.createElement("div");
        commentItem.className = "comment_item";
        commentItem.innerHTML = '<p class="comment_author">' + 
            data['author'] + ' <span class="comment_timestamp">on' + data['date'] + 
            '</span></p>' +
            '<p class="comment_detail">' + data['body'] + '</p>';
        commentWrapper.insertBefore(commentItem, firstItem);
        userCommentCount++;
        localStorage.setItem('userCommentCount', userCommentCount)

        const totalComment = document.getElementById('total-comments');
        totalComment.textContent = data['total_comments'] + ' Comment' + pluralize(data['total_comments'])
    })
}

function pluralize(num){
    console.log(num)
    if(parseInt(num) > 1)
        return 's'
    
    return ''
}

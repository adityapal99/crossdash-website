const navSlide = () => {
    const menu = document.querySelector('.menu');
    const nav = document.querySelector('.navlinks');    

    menu.addEventListener('click', ()=>{
        nav.classList.toggle('nav-active');
    })
}

navSlide();
document.addEventListener('DOMContentLoaded', function() {
    console.log('Bartershop application loaded!');
    
    // Подсветка активной страницы в меню
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Обработчик для формы записи (если она есть на странице)
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            alert('Спасибо за заявку! Мы свяжемся с вами в ближайшее время.');
            window.location.href = '/thanks/';
        });
    }
});
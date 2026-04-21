// Mobile Navigation Toggle
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');

    burger.addEventListener('click', () => {
        // Toggle Nav
        nav.classList.toggle('nav-active');

        // Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });

        // Burger Animation
        burger.classList.toggle('toggle');
    });
};

navSlide();

// Smooth Scrolling for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });

            // Close mobile menu if open
            const nav = document.querySelector('.nav-links');
            if (nav.classList.contains('nav-active')) {
                nav.classList.remove('nav-active');
                const navLinks = document.querySelectorAll('.nav-links li');
                navLinks.forEach(link => {
                    link.style.animation = '';
                });
            }
        }
    });
});

// Form Submission Handler
const bookingForm = document.getElementById('bookingForm');
if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form values
        const formData = new FormData(bookingForm);
        const name = bookingForm.querySelector('input[type="text"]').value;
        const phone = bookingForm.querySelector('input[type="tel"]').value;
        const service = bookingForm.querySelector('select').value;
        const comment = bookingForm.querySelector('textarea').value;

        // In a real application, you would send this data to a server
        // For now, we'll just show an alert
        alert(`Спасибо за заявку, ${name}! \n\nМы свяжемся с вами по телефону ${phone} в ближайшее время для подтверждения записи на услугу: ${service || 'не выбрана'}.`);
        
        // Reset form
        bookingForm.reset();
    });
}

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
        header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
    } else {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
});

// Intersection Observer for Animation on Scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe service cards, portfolio items, and review cards
document.querySelectorAll('.service-card, .portfolio-item, .review-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

console.log('Сайт мастера по наращиванию ресниц загружен успешно!');

// Public Calendar Functions
let publicCurrentDate = new Date();
let publicScheduleData = {};

const timeSlots = [
    '09:00', '10:00', '11:00', '12:00', '13:00', '14:00',
    '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'
];

function changePublicMonth(delta) {
    publicCurrentDate.setMonth(publicCurrentDate.getMonth() + delta);
    renderPublicCalendar();
    loadPublicSchedule();
}

function renderPublicCalendar() {
    const year = publicCurrentDate.getFullYear();
    const month = publicCurrentDate.getMonth();
    
    const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                      'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    document.getElementById('publicCurrentMonth').textContent = `${monthNames[month]} ${year}`;

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDay = (firstDay.getDay() + 6) % 7; // Понедельник = 0
    const totalDays = lastDay.getDate();

    const calendarDays = document.getElementById('publicCalendarDays');
    calendarDays.innerHTML = '';

    // Пустые ячейки до первого дня месяца
    for (let i = 0; i < startDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'public-day-cell empty';
        calendarDays.appendChild(emptyCell);
    }

    // Дни месяца
    const today = new Date();
    for (let day = 1; day <= totalDays; day++) {
        const cell = document.createElement('div');
        cell.className = 'public-day-cell';
        
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        if (dateStr === today.toISOString().split('T')[0]) {
            cell.classList.add('today');
        }

        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        cell.appendChild(dayNumber);

        // Проверяем занятость на этот день
        if (publicScheduleData[dateStr]) {
            const dayApps = publicScheduleData[dateStr];
            const busyCount = dayApps.filter(a => a.is_busy).length;
            const freeCount = timeSlots.length - busyCount;
            
            if (busyCount > 0) {
                cell.classList.add('all-busy');
            }
            if (freeCount > 0) {
                cell.classList.add('has-free');
            }

            // Показываем статусы времени
            const shownTimes = dayApps.slice(0, 3);
            shownTimes.forEach(app => {
                const badge = document.createElement('span');
                badge.className = `status-badge ${app.is_busy ? 'busy' : 'free'}`;
                badge.textContent = `${app.time} ${app.is_busy ? 'Занято' : 'Свободно'}`;
                cell.appendChild(badge);
            });

            if (dayApps.length > 3) {
                const more = document.createElement('span');
                more.className = 'status-badge';
                more.style.background = '#e5e7eb';
                more.style.color = '#374151';
                more.textContent = `+${dayApps.length - 3} еще`;
                cell.appendChild(more);
            }
        } else {
            // День полностью свободен
            cell.classList.add('has-free');
            const badge = document.createElement('span');
            badge.className = 'status-badge free';
            badge.textContent = 'Свободно';
            cell.appendChild(badge);
        }

        calendarDays.appendChild(cell);
    }
}

async function loadPublicSchedule() {
    const year = publicCurrentDate.getFullYear();
    const month = publicCurrentDate.getMonth() + 1;
    
    try {
        const response = await fetch(`/api/schedule/${year}/${month}`);
        if (response.ok) {
            publicScheduleData = await response.json();
            renderPublicCalendar();
        }
    } catch (error) {
        console.error('Ошибка загрузки расписания:', error);
    }
}

// Инициализация публичного календаря
if (document.getElementById('publicCalendar')) {
    renderPublicCalendar();
    loadPublicSchedule();
}

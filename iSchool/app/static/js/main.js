document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('section');
    createCounterObserver();

    // Smooth Scrolling
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            // Smooth scroll with animation
            targetSection.scrollIntoView({
                behavior: 'smooth'
            });

            // Mobile menu close
            const mobileMenu = document.getElementById('mobileMenu');
            const menuBtn = document.getElementById('menuBtn');
            mobileMenu.classList.add('hidden');
        });
    });

    // Mobile Menu Toggle
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    menuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    // Active Menu Highlighting
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            const sectionId = entry.target.id;
            const correspondingNavLink = document.querySelector(`nav a[href="#${sectionId}"]`);
            
            if (entry.isIntersecting) {
                // Remove active state from all links
                navLinks.forEach(link => {
                    link.classList.remove('text-blue-900');
                });
                
                // Add active state to current section's link
                if (correspondingNavLink !== null) {
                    correspondingNavLink.classList.add('text-blue-900');
                }
            }
        });
    };

    const sectionObserver = new IntersectionObserver(observerCallback, observerOptions);

    // Observe all sections
    sections.forEach(section => {
        sectionObserver.observe(section);
    });
    // Animated Counter Function
    function animateCounter(elementId, start, end, duration) {
        const element = document.getElementById(elementId);
        let startTimestamp = null;
        
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            // Use ease-out quadratic function for more natural acceleration
            const easeOutQuad = progress * (2 - progress);
            
            element.textContent = Math.floor(easeOutQuad * (end - start) + start);
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                element.textContent = end;
            }
        };
        
        window.requestAnimationFrame(step);
    }

    // Responsive Menu
    // const menuBtn = document.getElementById('menuBtn');
    // const mobileMenu = document.getElementById('mobileMenu');

    menuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
        menuBtn.innerHTML = mobileMenu.classList.contains('hidden') 
            ? '<i class="fas fa-bars text-2xl"></i>' 
            : '<i class="fas fa-times text-2xl"></i>';
    });

    // Intersection Observer to trigger animation when element comes into view
    function createCounterObserver() {
        const observers = [
            {
                element: document.getElementById('studentsCounter'),
                start: 0,
                end: 1018,
                duration: 2000
            },
            {
                element: document.getElementById('teachersCounter'),
                start: 0,
                end: 28,
                duration: 2000
            }
        ];

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const config = observers.find(obs => obs.element === entry.target);
                    if (config && !entry.target.dataset.animated) {
                        animateCounter(
                            entry.target.id, 
                            config.start, 
                            config.end, 
                            config.duration
                        );
                        entry.target.dataset.animated = 'true';
                        observer.unobserve(entry.target);
                    }
                }
            });
        }, {
            threshold: 0.1 // Trigger when at least 10% of the element is visible
        });

        observers.forEach(obs => observer.observe(obs.element));
    }
});


// // Initialize the counter observer when the DOM is fully loaded
// document.addEventListener('DOMContentLoaded', createCounterObserver);

document.addEventListener('DOMContentLoaded', function() {
  // Variables
  const header = document.querySelector('.header');
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const heroSlides = document.querySelectorAll('.hero-slide');
  const indicators = document.querySelectorAll('.indicator');
  const contactForm = document.getElementById('contactForm');
  const toast = document.getElementById('toast');
  const toastClose = document.querySelector('.toast-close');
  const currentYearEl = document.getElementById('currentYear');

  // Set current year in footer
  if (currentYearEl) {
    currentYearEl.textContent = new Date().getFullYear();
  }

  // Header scroll effect
  function handleScroll() {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  // Mobile menu toggle
  function toggleMobileMenu() {
    mobileMenu.classList.toggle('open');
    
    // Toggle hamburger animation
    const spans = mobileMenuBtn.querySelectorAll('span');
    if (mobileMenu.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    }
  }

  // Slideshow functionality
  let currentSlide = 0;
  
  function showSlide(index) {
    // Hide all slides
    heroSlides.forEach(slide => {
      slide.classList.remove('active');
    });
    
    // Remove active class from all indicators
    indicators.forEach(dot => {
      dot.classList.remove('active');
    });
    
    // Show the current slide and set indicator
    heroSlides[index].classList.add('active');
    indicators[index].classList.add('active');
  }
  
  function nextSlide() {
    currentSlide = (currentSlide + 1) % heroSlides.length;
    showSlide(currentSlide);
  }
  
  // Contact form submission
  function handleFormSubmit(e) {
    e.preventDefault();
    
    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const message = document.getElementById('message').value;
    
    // Log form data (in a real application you would send this to a server)
    console.log({
      name,
      email,
      phone,
      message
    });
    
    // Show success toast
    showToast('Demande envoyée', 'Nous vous contacterons dans les plus brefs délais.');
    
    // Reset form
    contactForm.reset();
  }
  
  // Toast notifications
  function showToast(title, message, duration = 5000) {
    const toastTitle = document.querySelector('.toast-title');
    const toastMessage = document.querySelector('.toast-message');
    
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    toast.classList.add('show');
    
    // Auto hide after duration
    setTimeout(() => {
      hideToast();
    }, duration);
  }
  
  function hideToast() {
    toast.classList.remove('show');
  }
  
  // Add scroll animations
  function addScrollAnimations() {
    const elements = document.querySelectorAll('.section-header, .properties-grid, .about-grid, .contact-grid');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    
    elements.forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(20px)';
      element.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
      observer.observe(element);
    });
  }
  
  // Event listeners
  window.addEventListener('scroll', handleScroll);
  
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', toggleMobileMenu);
  }
  
  // Initialize slideshow if on homepage
  if (heroSlides.length > 0) {
    // Set up slideshow
    showSlide(0);
    
    // Set up auto slideshow
    setInterval(nextSlide, 6000);
    
    // Indicator click events
    indicators.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        currentSlide = index;
        showSlide(currentSlide);
      });
    });
  }
  
  // Handle contact form submission
  if (contactForm) {
    contactForm.addEventListener('submit', handleFormSubmit);
  }
  
  // Toast close button
  if (toastClose) {
    toastClose.addEventListener('click', hideToast);
  }
  
  // Initialize scroll animations
  addScrollAnimations();
  
  // Call scroll handler on page load (to set initial header state)
  handleScroll();
});

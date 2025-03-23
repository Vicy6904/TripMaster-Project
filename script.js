// header transparent bg

document.addEventListener("DOMContentLoaded", () => {
    const header = document.getElementById("main-header");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });
});



// section scrolling animation

document.addEventListener("DOMContentLoaded", () => {
    const exploreSection = document.querySelector(".explore-packages");
    const travelSection = document.querySelector(".travel-management");
    const whySection = document.querySelector(".why-choose");
    const testimonialsSection = document.querySelector(".testimonials");
    const aboutSection = document.querySelector(".about-us");
    const newsletterSection = document.querySelector(".newsletter");
    const observerOptions = {
        root: null, // Viewport
        threshold: 0.4, // Trigger when 20% of the section is visible
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Add the animation class when the section enters the viewport
                entry.target.classList.add("animate");
            } else {
                // Remove the animation class when the section leaves the viewport
                entry.target.classList.remove("animate");
            }
        });
    }, observerOptions);

    if (exploreSection) {
        observer.observe(exploreSection);
    }

    if (travelSection) {
        observer.observe(travelSection);
    }

    if (whySection) {
        observer.observe(whySection);
    }

    if (testimonialsSection) {
        observer.observe(testimonialsSection);
    }

    if (aboutSection) {
        observer.observe(aboutSection);
    }

    if (newsletterSection) {
        observer.observe(newsletterSection);
    }

});

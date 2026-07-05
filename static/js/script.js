document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initScrollAnimations();
    initCounters();
    initPortfolioFilters();
    initLightbox();
    initFormValidation();
    initLazyLoading();
});

/* ==========================================================================
   1. Control de Navegación y Menú Móvil
   ========================================================================== */
function initNavigation() {
    const header = document.querySelector(".main-header");
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");
    const navLinks = document.querySelectorAll(".nav-link");

    // Efecto de Header en Scroll
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
        updateActiveLink();
    });

    // Menú Móvil Hamburguesa
    menuToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active");
        menuToggle.classList.toggle("open");
    });

    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            navMenu.classList.remove("active");
        });
    });

    function updateActiveLink() {
        let fromTop = window.scrollY + 120;
        navLinks.forEach(link => {
            const section = document.querySelector(link.hash);
            if (section.offsetTop <= fromTop && section.offsetTop + section.offsetHeight > fromTop) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    }
}

/* ==========================================================================
   2. Animaciones al Aparecer (Intersection Observer)
   ========================================================================== */
function initScrollAnimations() {
    const targetElements = document.querySelectorAll(".reveal");
    const observerOptions = { threshold: 0.1, rootMargin: "0px 0px -50px 0px" };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    targetElements.forEach(el => observer.observe(el));
}

/* ==========================================================================
   3. Contadores Animados Numéricos
   ========================================================================== */
function initCounters() {
    const counterBoxes = document.querySelectorAll(".counter-number");
    const observerOptions = { threshold: 0.5 };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute("data-target"), 10);
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    counterBoxes.forEach(box => observer.observe(box));

    function animateCounter(element, target) {
        let count = 0;
        const duration = 2000; 
        const increment = target / (duration / 16); 

        function updateCount() {
            count += increment;
            if (count < target) {
                element.innerText = Math.floor(count);
                requestAnimationFrame(updateCount);
            } else {
                element.innerText = target;
            }
        }
        updateCount();
    }
}

/* ==========================================================================
   4. Galería Filtrable Dinámica
   ========================================================================== */
function initPortfolioFilters() {
    const filterButtons = document.querySelectorAll(".filter-btn");
    const portfolioItems = document.querySelectorAll(".portfolio-item");

    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            filterButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            const filterValue = button.getAttribute("data-filter");

            portfolioItems.forEach(item => {
                if (filterValue === "all" || item.getAttribute("data-category") === filterValue) {
                    item.style.display = "block";
                    setTimeout(() => item.style.opacity = "1", 50);
                } else {
                    item.style.opacity = "0";
                    setTimeout(() => item.style.display = "none", 400);
                }
            });
        });
    });
}

/* ==========================================================================
   5. Lightbox Cinemática Multimedia (Videos e Imágenes)
   ========================================================================== */
function initLightbox() {
    const lightbox = document.getElementById("videoLightbox");
    const lightboxIframe = document.getElementById("lightboxIframe");
    const lightboxImg = document.getElementById("lightboxImg");
    const closeBtn = document.querySelector(".lightbox-close");
    const triggerBtns = document.querySelectorAll(".view-project-btn");

    triggerBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const mediaUrl = btn.getAttribute("href");

            if (btn.classList.contains("type-img")) {
                lightboxImg.setAttribute("src", mediaUrl);
                lightboxImg.style.display = "block";
                lightboxIframe.style.display = "none";
            } else {
                lightboxIframe.setAttribute("src", mediaUrl + "?autoplay=1");
                lightboxIframe.style.display = "block";
                lightboxImg.style.display = "none";
            }
            lightbox.classList.add("active");
        });
    });

    closeBtn.addEventListener("click", closeLightbox);
    lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    function closeLightbox() {
        lightbox.classList.remove("active");
        setTimeout(() => {
            lightboxIframe.setAttribute("src", "");
            lightboxImg.setAttribute("src", "");
        }, 400);
    }
}

/* ==========================================================================
   6. Validación y Envío de Formulario Asíncrono (AJAX)
   ========================================================================== */
function initFormValidation() {
    const form = document.getElementById("contactForm");
    const emailInput = document.getElementById("formCorreo");
    const responseMsg = document.getElementById("formResponse");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        // Validación Básica Regex de Correo Corporativo o Común
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(emailInput.value)) {
            emailInput.parentElement.classList.add("invalid");
            return;
        } else {
            emailInput.parentElement.classList.remove("invalid");
        }

        responseMsg.style.color = "var(--gold)";
        responseMsg.innerText = "Procesando propuesta de producción...";

        // Recolección e inyección mediante FormData a la API Flask
        const formData = new FormData(form);

        try {
            const response = await fetch("/api/contacto", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.status === 200) {
                responseMsg.style.color = "#25D366";
                responseMsg.innerText = result.message;
                form.reset();
            } else {
                responseMsg.style.color = "#ff4d4d";
                responseMsg.innerText = result.message;
            }
        } catch (error) {
            responseMsg.style.color = "#ff4d4d";
            responseMsg.innerText = "Error de conexión. Intente por WhatsApp de forma directa.";
        }
    });
}

/* ==========================================================================
   7. Lazy Loading para Optimización Core Web Vitals
   ========================================================================== */
function initLazyLoading() {
    const lazyImages = document.querySelectorAll(".lazy-img");

    if ("IntersectionObserver" in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.getAttribute("data-src");
                    image.classList.remove("lazy-img");
                    imageObserver.unobserve(image);
                }
            });
        });

        lazyImages.forEach(image => imageObserver.observe(image));
    } else {
        // Fallback para navegadores antiguos
        lazyImages.forEach(image => image.src = image.getAttribute("data-src"));
    }
}
document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initScrollAnimations();
    initCounters();
    initPortfolioFilters();
    initLightbox();
    initFormValidation();
    initHeroBackgroundCarousel();
    initHeroCarousel();
    initClientCarousel();
    initPrizeWheel();
    initParkGame();
    initSocialForm();
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

function initHeroCarousel() {
    const slides = document.querySelectorAll('.hero-carousel .carousel-slide');
    let current = 0;
    const interval = 6000;

    if (!slides.length) return;

    const showSlide = (index) => {
        slides.forEach((slide, idx) => {
            slide.classList.toggle('active', idx === index);
        });
    };

    showSlide(current);
    setInterval(() => {
        current = (current + 1) % slides.length;
        showSlide(current);
    }, interval);
}

function initClientCarousel() {
    const cards = document.querySelectorAll('.client-carousel .client-card');
    const prevBtn = document.querySelector('.carousel-control.prev');
    const nextBtn = document.querySelector('.carousel-control.next');
    let current = 0;

    if (!cards.length) return;

    const setActiveCard = (index) => {
        current = (index + cards.length) % cards.length;
        cards.forEach((card, idx) => {
            card.classList.toggle('active', idx === current);
        });
        cards[current].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    };

    cards.forEach((card, index) => {
        card.addEventListener('click', () => setActiveCard(index));
    });

    prevBtn?.addEventListener('click', () => setActiveCard(current - 1));
    nextBtn?.addEventListener('click', () => setActiveCard(current + 1));
    setActiveCard(current);
}

function initSocialForm() {
    const socialComment = document.getElementById('socialComment');
    const socialSubmitBtn = document.getElementById('socialSubmitBtn');
    const socialNotice = document.getElementById('socialNotice');

    if (!socialComment || !socialSubmitBtn || !socialNotice) return;

    socialSubmitBtn.addEventListener('click', () => {
        const message = socialComment.value.trim();
        if (!message) {
            socialNotice.style.color = '#ff4d4d';
            socialNotice.textContent = 'Por favor escribe tu comentario antes de enviar.';
            return;
        }

        const whatsappUrl = `https://wa.me/51924130007?text=${encodeURIComponent('Hola 4KM Producciones, quiero publicar lo siguiente en redes: ' + message)}`;
        window.open(whatsappUrl, '_blank');
        socialNotice.style.color = '#25D366';
        socialNotice.textContent = 'Abriendo WhatsApp para enviar tu comentario...';
    });
}

function initHeroBackgroundCarousel() {
    const slides = document.querySelectorAll('.hero-bg-carousel .hero-bg-slide');
    let current = 0;
    const interval = 7000;

    if (!slides.length) return;

    const showSlide = (index) => {
        slides.forEach((slide, idx) => {
            slide.classList.toggle('active', idx === index);
        });
    };

    showSlide(current);
    setInterval(() => {
        current = (current + 1) % slides.length;
        showSlide(current);
    }, interval);
}

function initPrizeWheel() {
    const wheel = document.getElementById('prizeWheel');
    const spinBtn = document.getElementById('spinWheelBtn');
    const wheelResult = document.getElementById('wheelResult');
    const codeInput = document.getElementById('wheelCodeInput');
    const verifyCodeBtn = document.getElementById('verifyCodeBtn');
    const codeMessage = document.getElementById('wheelCodeMessage');
    const options = [
        '¡Ganaste una gorra 4KM! Envíanos un mensaje para coordinar la entrega.',
        '¡Felicidades! 10% de descuento en servicios de filmación desde S/500.',
        '¡Polo oficial 4KM! Contacta por WhatsApp para reclamarlo.',
        'Premio sorpresa: descuento especial para tu próxima producción.',
        'No ganas nada esta vez, sigue intentando y usa otro código.',
        '¡Buena! Descuento adicional de S/150 en tu paquete de filmación.'
    ];
    let spinning = false;
    let wheelUnlocked = false;

    if (!codeInput || !verifyCodeBtn || !codeMessage) return;
    if (!wheel || !spinBtn || !wheelResult) return;

    window.validWheelCodes = window.validWheelCodes || ['4KMSERVICE', '4KMCLIENTE'];

    const showMessage = (text, valid = true) => {
        codeMessage.textContent = text;
        codeMessage.style.color = valid ? '#25D366' : '#ff4d4d';
    };

    const unlockWheel = () => {
        wheelUnlocked = true;
        spinBtn.disabled = false;
        showMessage('Código válido. La ruleta está desbloqueada.', true);
    };

    verifyCodeBtn.addEventListener('click', () => {
        const code = codeInput.value.trim().toUpperCase();
        if (!code) {
            showMessage('Ingresa un código para desbloquear la ruleta.', false);
            return;
        }
        if (window.validWheelCodes.includes(code)) {
            unlockWheel();
        } else {
            showMessage('Código inválido. Revisa el mensaje o tu compra.', false);
        }
    });

    spinBtn.disabled = true;
    spinBtn.addEventListener('click', () => {
        if (spinning || !wheelUnlocked) return;
        spinning = true;
        wheelResult.textContent = 'Girando...';
        const index = Math.floor(Math.random() * options.length);
        const turns = 7;
        const angle = 360 * turns + index * (360 / options.length) + 30;

        wheel.style.transform = `rotate(${angle}deg)`;
        spinBtn.disabled = true;

        setTimeout(() => {
            const microDiscount = (Math.random() * 0.1 + 0.1).toFixed(2);
            const randomCashPrize = Math.random() < 0.45;
            if (index === 4) {
                wheelResult.textContent = `No ganas nada esta vez, pero sigue buscando nuevos códigos.`;
            } else if (randomCashPrize) {
                wheelResult.textContent = `¡Ganaste S/${microDiscount} de descuento para tu próximo servicio! Aplica en compras válidas.`;
            } else {
                wheelResult.textContent = options[index];
            }
            wheelUnlocked = false;
            spinBtn.disabled = true;
            spinning = false;
            showMessage('Ingresa otro código o completa otro juego para girar de nuevo.', false);
        }, 4200);
    });
}

function initParkGame() {
    const board = document.getElementById('parkBoard');
    const startBtn = document.getElementById('startGameBtn');
    const resetBtn = document.getElementById('resetGameBtn');
    const resultEl = document.getElementById('gameStatus');
    const foundEl = document.getElementById('chargersFound');
    const movesEl = document.getElementById('movesCount');
    const controls = document.querySelectorAll('.arrow-btn');

    if (!board || !startBtn || !resetBtn || !resultEl || !foundEl || !movesEl) return;

    const rows = 6;
    const cols = 10;
    const totalChargers = 5;
    let cells = [];
    let player = { row: rows - 1, col: 0 };
    let chargers = new Set();
    let found = 0;
    let moves = 0;
    let active = false;

    const directions = {
        up: { row: -1, col: 0 },
        down: { row: 1, col: 0 },
        left: { row: 0, col: -1 },
        right: { row: 0, col: 1 }
    };

    // Ensure UI elements for code validation and prize summary are present
    function ensureParkUI() {
        let container = document.getElementById('parkGameUI');
        if (container) return container;
        container = document.createElement('div');
        container.id = 'parkGameUI';
        container.style.position = 'fixed';
        container.style.top = '16px';
        container.style.right = '16px';
        container.style.zIndex = '9999';
        container.style.width = '260px';
        container.style.fontFamily = 'Inter, sans-serif';

        container.innerHTML = `
            <div id="parkCodeBox" style="background:#0b0b0b;color:#fff;padding:12px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.4);margin-bottom:8px;font-size:14px;">
                <label style="display:block;font-weight:600;margin-bottom:6px;">Código único para jugar</label>
                <div style="display:flex;gap:6px;">
                    <input id="parkGameCodeInput" placeholder="Ingresa tu código" style="flex:1;padding:8px;border-radius:4px;border:1px solid #333;background:#111;color:#fff" />
                    <button id="parkVerifyBtn" style="padding:8px 10px;border-radius:4px;background:#D4AF37;border:none;color:#000;font-weight:700;">Verificar</button>
                </div>
                <div id="parkCodeMessage" style="margin-top:8px;font-size:13px;color:#ccc"></div>
            </div>
            <div id="parkPrizeBox" style="background:#fff;color:#111;padding:12px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.12);font-size:14px;text-align:center;">
                <div style="font-weight:700;margin-bottom:6px">Premio / Promoción</div>
                <div id="parkPrizeText">Sin premio aún</div>
            </div>
        `;

        document.body.appendChild(container);

        const verifyBtn = document.getElementById('parkVerifyBtn');
        verifyBtn.addEventListener('click', async () => {
            const code = document.getElementById('parkGameCodeInput').value.trim().toUpperCase();
            const msgEl = document.getElementById('parkCodeMessage');
            if (!code) { msgEl.textContent = 'Ingresa un código proporcionado.'; msgEl.style.color = '#ff4d4d'; return; }
            msgEl.textContent = 'Validando código...'; msgEl.style.color = '#D4AF37';
            try {
                const form = new FormData(); form.append('code', code);
                const res = await fetch('/api/validate_code', { method: 'POST', body: form });
                const data = await res.json();
                if (res.status === 200 && data.status === 'ok') {
                    msgEl.textContent = 'Código válido. Ya puedes iniciar el juego.'; msgEl.style.color = '#25D366';
                    startBtn.disabled = false;
                    startBtn.dataset.validCode = code;
                } else {
                    msgEl.textContent = data.message || 'Código inválido.'; msgEl.style.color = '#ff4d4d';
                    startBtn.disabled = true;
                }
            } catch (err) { msgEl.textContent = 'Error validando código.'; msgEl.style.color = '#ff4d4d'; }
        });

        return container;
    }

    ensureParkUI();

    function buildBoard() {
        board.innerHTML = '';
        board.style.gridTemplateColumns = `repeat(${cols}, minmax(0, 1fr))`;
        cells = [];
        chargers.clear();

        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const cell = document.createElement('div');
                cell.classList.add('park-cell');
                cell.dataset.row = row;
                cell.dataset.col = col;
                board.appendChild(cell);
                cells.push(cell);
            }
        }

        placeChargers();
        placeObstacles();
        player = { row: rows - 1, col: 0 };
        found = 0;
        moves = 0;
        updateScore();
        updateBoard();
        resultEl.textContent = 'Presiona Iniciar para buscar cargadores en el parque.';
        active = false;
    }

    function randomCell(includeEdge = true) {
        const row = Math.floor(Math.random() * rows);
        const col = Math.floor(Math.random() * cols);
        if (!includeEdge && (row === rows - 1 && col === 0)) return randomCell(includeEdge);
        return { row, col };
    }

    function buildKey(row, col) {
        return `${row}:${col}`;
    }

    function placeChargers() {
        while (chargers.size < totalChargers) {
            const { row, col } = randomCell(false);
            const key = buildKey(row, col);
            if (key === buildKey(rows - 1, 0)) continue;
            chargers.add(key);
        }
    }

    function placeObstacles() {
        cells.forEach(cell => cell.classList.remove('obstacle'));
        const obstacleCount = 8;
        let placed = 0;
        while (placed < obstacleCount) {
            const { row, col } = randomCell(false);
            const key = buildKey(row, col);
            if (chargers.has(key) || key === buildKey(rows - 1, 0)) continue;
            const cell = getCell(row, col);
            if (!cell.classList.contains('obstacle')) {
                cell.classList.add('obstacle');
                placed++;
            }
        }
    }

    function getCell(row, col) {
        return cells[row * cols + col];
    }

    function updateBoard() {
        cells.forEach(cell => {
            cell.classList.remove('player', 'charger');
            const row = parseInt(cell.dataset.row, 10);
            const col = parseInt(cell.dataset.col, 10);
            const key = buildKey(row, col);
            if (chargers.has(key)) cell.classList.add('charger');
        });
        getCell(player.row, player.col).classList.add('player');
    }

    function updateScore() {
        foundEl.textContent = String(found);
        movesEl.textContent = String(moves);
    }

    function movePlayer(direction) {
        if (!active) return;
        const next = {
            row: player.row + direction.row,
            col: player.col + direction.col
        };
        if (next.row < 0 || next.row >= rows || next.col < 0 || next.col >= cols) return;

        const targetCell = getCell(next.row, next.col);
        if (targetCell.classList.contains('obstacle')) {
            resultEl.textContent = 'Hay un obstáculo en el camino. Usa otra dirección.';
            return;
        }

        player = next;
        moves += 1;
        const key = buildKey(player.row, player.col);
        if (chargers.has(key)) {
            chargers.delete(key);
            found += 1;
            const microDiscount = (Math.random() * 0.1 + 0.1).toFixed(2);
            resultEl.textContent = `Encontraste un cargador. ¡Sigue buscando! Descuento en efectivo disponible: S/${microDiscount}.`;
        } else {
            resultEl.textContent = 'Sigue buscando. Encuentra más cargadores para aumentar tus premios.';
        }

        updateBoard();
        updateScore();

        if (found === totalChargers) {
            active = false;
            const chance = Math.random();
            const unlockCode = '4KMPLAY';
            window.validWheelCodes = window.validWheelCodes || ['4KMSERVICE', '4KMCLIENTE'];
            if (!window.validWheelCodes.includes(unlockCode)) {
                window.validWheelCodes.push(unlockCode);
            }
            const codeLabel = document.getElementById('generatedGameCode');
            if (codeLabel) codeLabel.textContent = unlockCode;
            let prizeText = '';
            if (chance < 0.75) {
                prizeText = `10% de descuento en servicios de filmación (aplica desde S/500).`;
                resultEl.textContent = `¡Increíble! Reuniste todos los cargadores y ganaste ${prizeText}`;
            } else {
                const micro = (Math.random() * 0.1 + 0.1).toFixed(2);
                prizeText = `S/${micro} de descuento adicional en tu próxima compra.`;
                resultEl.textContent = `¡Excelente! Reuniste todos los cargadores y ganaste ${prizeText}`;
            }

            // Mostrar premio en la caja superior
            const prizeBox = document.getElementById('parkPrizeText');
            if (prizeBox) prizeBox.textContent = prizeText;

            // Registrar ganador solicitando datos básicos
            setTimeout(async () => {
                const code = startBtn.dataset.validCode || '';
                const nombre = prompt('Felicidades! Ingresa tu nombre para registrar el premio:');
                if (!nombre) return alert('Registro cancelado: nombre requerido.');
                const correo = prompt('Ingresa tu correo (opcional):');
                const telefono = prompt('Ingresa tu teléfono (opcional):');
                try {
                    const form = new FormData();
                    form.append('nombre', nombre);
                    if (correo) form.append('correo', correo);
                    if (telefono) form.append('telefono', telefono);
                    if (code) form.append('code', code);
                    form.append('prize', prizeText);
                    const packageName = document.querySelector('.category-hero h1')?.textContent || '';
                    if (packageName) form.append('package', packageName);
                    const res = await fetch('/api/game_result', { method: 'POST', body: form });
                    const data = await res.json();
                    if (res.status === 200 && data.status === 'ok') {
                        alert('Registro exitoso. ¡Gracias!');
                        const msgEl = document.getElementById('parkCodeMessage');
                        if (msgEl) { msgEl.textContent = 'Premio registrado. Pronto nos comunicaremos.'; msgEl.style.color = '#25D366'; }
                    } else {
                        alert('Error registrando: ' + (data.message || ''));
                    }
                } catch (err) {
                    alert('Error al enviar registro.');
                }
            }, 300);
        }
    }

    function onControlClick(event) {
        const dir = event.currentTarget.dataset.dir;
        if (!dir) return;
        movePlayer(directions[dir]);
    }

    function handleKey(event) {
        if (!active) return;
        const mapping = {
            ArrowUp: 'up',
            ArrowDown: 'down',
            ArrowLeft: 'left',
            ArrowRight: 'right',
            w: 'up',
            s: 'down',
            a: 'left',
            d: 'right'
        };
        const dir = mapping[event.key];
        if (dir) {
            event.preventDefault();
            movePlayer(directions[dir]);
        }
    }

    controls.forEach(button => button.addEventListener('click', onControlClick));
    window.addEventListener('keydown', handleKey);

    startBtn.addEventListener('click', () => {
        // Require validated code prior to starting
        const validated = startBtn.dataset.validCode;
        if (!validated) {
            const msgEl = document.getElementById('parkCodeMessage');
            if (msgEl) { msgEl.textContent = 'Debes ingresar y validar tu código antes de jugar.'; msgEl.style.color = '#ff4d4d'; }
            return;
        }
        active = true;
        resultEl.textContent = 'Juego iniciado. Usa las teclas de flecha o los botones para moverte.';
    });

    resetBtn.addEventListener('click', buildBoard);

    buildBoard();
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
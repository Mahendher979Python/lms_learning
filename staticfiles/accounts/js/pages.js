document.addEventListener('DOMContentLoaded', () => {
    // --------------------------------------------------------------------------
    // 1. COURSES PAGE FILTERING & SEARCH ENGINE
    // --------------------------------------------------------------------------
    const filterButtons = document.querySelectorAll('.filter-btn');
    const courseCards = document.querySelectorAll('.premium-course-card');
    const coursesSearchInput = document.getElementById('coursesSearchInput');

    function filterCourses() {
        const activeFilter = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
        const searchQuery = coursesSearchInput ? coursesSearchInput.value.toLowerCase().trim() : '';

        courseCards.forEach(card => {
            const category = card.dataset.category || '';
            const title = card.querySelector('h3')?.textContent.toLowerCase() || '';
            const desc = card.querySelector('p')?.textContent.toLowerCase() || '';

            const matchesCategory = (activeFilter === 'all' || category === activeFilter);
            const matchesSearch = (title.includes(searchQuery) || desc.includes(searchQuery));

            if (matchesCategory && matchesSearch) {
                card.style.display = 'flex';
                card.style.animation = 'fadeIn 0.4s ease forwards';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // Category Tabs Event Listeners
    if (filterButtons.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                filterCourses();
            });
        });
    }

    // Live Text Search Event Listener
    if (coursesSearchInput) {
        coursesSearchInput.addEventListener('input', filterCourses);
    }

    // --------------------------------------------------------------------------
    // 2. FAQ PAGE ACCORDION AND LIVE FAQ SEARCH
    // --------------------------------------------------------------------------
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    const faqSearchInput = document.getElementById('faqSearch');
    const accordionItems = document.querySelectorAll('.accordion-item');
    const categoryTitles = document.querySelectorAll('.faq-category-title');

    // Toggle Expandable Accordion
    if (accordionHeaders.length > 0) {
        accordionHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const item = header.parentElement;
                const collapse = item.querySelector('.accordion-collapse');
                const isOpen = item.classList.contains('active');

                // Close other accordions in the same list
                const siblingGroup = item.closest('.faq-accordion-group');
                if (siblingGroup) {
                    siblingGroup.querySelectorAll('.accordion-item').forEach(sibling => {
                        if (sibling !== item) {
                            sibling.classList.remove('active');
                            const sibCollapse = sibling.querySelector('.accordion-collapse');
                            if (sibCollapse) sibCollapse.style.maxHeight = null;
                        }
                    });
                }

                // Toggle target item
                if (isOpen) {
                    item.classList.remove('active');
                    if (collapse) collapse.style.maxHeight = null;
                } else {
                    item.classList.add('active');
                    if (collapse) {
                        // Using scrollHeight for smooth height transition
                        collapse.style.maxHeight = collapse.scrollHeight + 'px';
                    }
                }
            });
        });
    }

    // Real-time FAQ Search Engine
    if (faqSearchInput) {
        faqSearchInput.addEventListener('input', () => {
            const query = faqSearchInput.value.toLowerCase().trim();

            accordionItems.forEach(item => {
                const question = item.querySelector('.accordion-header h3')?.textContent.toLowerCase() || '';
                const answer = item.querySelector('.accordion-body')?.textContent.toLowerCase() || '';

                if (question.includes(query) || answer.includes(query)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });

            // Hide section category titles if no matching questions exist in that category
            categoryTitles.forEach(title => {
                const nextGroup = title.nextElementSibling;
                if (nextGroup && nextGroup.classList.contains('faq-accordion-group')) {
                    const visibleItems = nextGroup.querySelectorAll('.accordion-item[style="display: block;"]').length;
                    const totalItems = nextGroup.querySelectorAll('.accordion-item').length;
                    const hiddenItems = nextGroup.querySelectorAll('.accordion-item[style="display: none;"]').length;
                    
                    if (hiddenItems === totalItems) {
                        title.style.display = 'none';
                        nextGroup.style.display = 'none';
                    } else {
                        title.style.display = 'block';
                        nextGroup.style.display = 'grid';
                    }
                }
            });
        });
    }

    // --------------------------------------------------------------------------
    // 3. CONTACT FORM INPUT VALIDATION & TOAST ALERT SYSTEM
    // --------------------------------------------------------------------------
    const contactForm = document.getElementById('premiumContactForm');
    const toast = document.getElementById('contactSuccessToast');

    if (contactForm) {
        const inputs = contactForm.querySelectorAll('input[required], textarea[required]');
        const submitBtn = contactForm.querySelector('button[type="submit"]');

        function validateEmail(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(String(email).toLowerCase());
        }

        function checkFormValidity() {
            let isValid = true;
            
            inputs.forEach(input => {
                const errorMsg = input.parentElement.parentElement.querySelector('.input-error-msg');
                let inputValid = true;

                if (!input.value.trim()) {
                    inputValid = false;
                } else if (input.type === 'email' && !validateEmail(input.value)) {
                    inputValid = false;
                }

                if (inputValid) {
                    if (errorMsg) errorMsg.style.display = 'none';
                    input.style.borderColor = '';
                } else {
                    isValid = false;
                }
            });

            return isValid;
        }

        // Live inputs validation checks
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                const errorMsg = input.parentElement.parentElement.querySelector('.input-error-msg');
                if (input.value.trim()) {
                    if (input.type === 'email') {
                        if (validateEmail(input.value)) {
                            if (errorMsg) errorMsg.style.display = 'none';
                            input.style.borderColor = '#cbd5e1';
                        } else {
                            if (errorMsg) {
                                errorMsg.textContent = 'Please enter a valid email address';
                                errorMsg.style.display = 'block';
                            }
                            input.style.borderColor = '#ef4444';
                        }
                    } else {
                        if (errorMsg) errorMsg.style.display = 'none';
                        input.style.borderColor = '#cbd5e1';
                    }
                }
            });

            input.addEventListener('blur', () => {
                const errorMsg = input.parentElement.parentElement.querySelector('.input-error-msg');
                if (!input.value.trim()) {
                    if (errorMsg) {
                        errorMsg.textContent = 'This field is required';
                        errorMsg.style.display = 'block';
                    }
                    input.style.borderColor = '#ef4444';
                }
            });
        });

        // Form Submit Handler
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            if (checkFormValidity()) {
                // Disable submit button and show loading state
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending message...';
                }

                // Simulate API call delay (1.2s)
                setTimeout(() => {
                    // Reset Form
                    contactForm.reset();

                    // Re-enable submit button
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = 'Send Message <i class="fas fa-paper-plane"></i>';
                    }

                    // Show success toast notification
                    if (toast) {
                        toast.classList.add('show');
                        setTimeout(() => {
                            toast.classList.remove('show');
                        }, 5000); // Hide after 5 seconds
                    }
                }, 1200);
            } else {
                // Show errors for empty fields
                inputs.forEach(input => {
                    if (!input.value.trim()) {
                        const errorMsg = input.parentElement.parentElement.querySelector('.input-error-msg');
                        if (errorMsg) {
                            errorMsg.textContent = 'This field is required';
                            errorMsg.style.display = 'block';
                        }
                        input.style.borderColor = '#ef4444';
                    }
                });
            }
        });
    }
});

// Simple CSS @keyframes injector for fadeIn animation
const styleSheet = document.createElement("style");
styleSheet.innerText = `
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
`;
document.head.appendChild(styleSheet);

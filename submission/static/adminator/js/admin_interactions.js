/* Minimal JS for Adminator interactions */

document.addEventListener('DOMContentLoaded', function () {
    // Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function (e) {
            e.preventDefault();

            if (window.innerWidth < 992) {
                // Mobile
                sidebar.classList.toggle('is-active');
            } else {
                // Desktop - collapse sidebar (optional implementation)
                // For now we just focus on mobile toggle which is critical

                // If we want desktop collapse:
                // document.body.classList.toggle('is-collapsed');
            }
        });
    }

    // Dropdown Menus
    const dropdowns = document.querySelectorAll('.sidebar-menu .dropdown-toggle');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function (e) {
            e.preventDefault();
            // Toggle current
            const parent = this.parentElement;
            parent.classList.toggle('open');

            // Optional: Close others? For "Expanded View" usually we allow multiple open.
            // Keeping multiple open allows user to see more structure.
        });
    });

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', function (e) {
        if (window.innerWidth < 992 &&
            sidebar.classList.contains('is-active') &&
            !sidebar.contains(e.target) &&
            !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('is-active');
        }
    });

    // Handle Active State based on URL
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.sidebar-link');

    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            // If inside dropdown, open it
            const parentLi = link.closest('li');
            const parentUl = parentLi.closest('ul');
            if (parentUl && parentUl.classList.contains('dropdown-menu')) {
                parentUl.closest('li').classList.add('open');
            }
        }
    });
});

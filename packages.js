document.addEventListener('DOMContentLoaded', () => {
    const packageGrid = document.getElementById('package-grid');
    const searchInput = document.getElementById('search');
    const sortSelect = document.getElementById('sort');
    const filterSelect = document.getElementById('filter');
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const customPackageForm = document.getElementById('custom-package-form');

    // Fetch packages from the server
    async function fetchPackages() {
        try {
            const response = await fetch('/get_packages');
            const data = await response.json();
            if (data.success) {
                renderPackages(data.packages);
            } else {
                console.error("Failed to fetch packages:", data.message);
            }
        } catch (error) {
            console.error("Error fetching packages:", error);
        }
    }

    // Function to render packages on the page
    function renderPackages(packages) {
        packageGrid.innerHTML = packages.map(pkg => `
            <div class="package-card">
                <img src="${pkg.image}" alt="${pkg.name}">
                <div class="package-card-content">
                    <h3>${pkg.name}</h3>
                    <p>${pkg.type}</p>
                    <div class="package-info">
                        <i data-lucide="map-pin"></i>
                        <span>${pkg.location}</span>
                    </div>
                    <div class="package-info">
                        <i data-lucide="clock"></i>
                        <span>${pkg.duration} days</span>
                    </div>
                    <div class="package-info">
                        <i data-lucide="calendar"></i>
                        <span>Available year-round</span>
                    </div>
                </div>
                <div class="package-footer">
                    <span class="price">$${pkg.price}</span>
                    <button onclick="bookPackage(${pkg.id})">Book Now</button>
                </div>
            </div>
        `).join('');
        lucide.createIcons();
    }

    function filterAndSortPackages() {
        const searchTerm = searchInput.value.toLowerCase();
        const sortBy = sortSelect.value;
        const filterType = filterSelect.value;

        let filteredPackages = predefinedPackages.filter(pkg => 
            pkg.name.toLowerCase().includes(searchTerm) &&
            (filterType === 'All' || pkg.type === filterType)
        );

        filteredPackages.sort((a, b) => {
            if (sortBy === 'price') return a.price - b.price;
            if (sortBy === 'duration') return a.duration - b.duration;
            return 0;
        });

        renderPackages(filteredPackages);
    }

    searchInput.addEventListener('input', filterAndSortPackages);
    sortSelect.addEventListener('change', filterAndSortPackages);
    filterSelect.addEventListener('change', filterAndSortPackages);

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            button.classList.add('active');
            document.getElementById(button.dataset.tab).classList.add('active');
        });
    });

    // customPackageForm.addEventListener('submit', (e) => {
    //     e.preventDefault();
    //     alert('Custom package request submitted! We will contact you soon with a personalized offer.');
    // });

    // Fetch and render packages on page load
    fetchPackages();
});

function bookPackage(packageId) {
    alert(`Booking package ${packageId}. This feature is not yet implemented.`);
}

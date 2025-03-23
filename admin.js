document.addEventListener("DOMContentLoaded", () => {
    // Sidebar Navigation
    document.querySelectorAll(".sidebar a").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelectorAll(".page").forEach(page => page.classList.remove("active"));
            document.querySelectorAll(".sidebar a").forEach(l => l.classList.remove("active"));

            document.getElementById(this.getAttribute("href").substring(1)).classList.add("active");
            this.classList.add("active");
        });
    });

    // Show/Hide Forms
    document.querySelectorAll(".show-form-btn").forEach(button => {
        button.addEventListener("click", function () {
            const form = document.getElementById(this.dataset.target);
            form.style.display = form.style.display === "block" ? "none" : "block";
        });
    });

    // Form Submission via AJAX (Includes File Upload)
    const forms = {
        "package-form": "package-list",
        "bus-form": "bus-list",
        "route-form": "route-list"
    };


    // Animated Dashboard Count Effect
    

    // Validate Image Upload
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener("change", function () {
            const file = this.files[0];
            const feedback = document.getElementById("form-feedback");

            if (file && file.size > 2 * 1024 * 1024) {  // Max file size: 2MB
                feedback.textContent = "File is too large. Maximum size is 2MB.";
                this.value = "";  // Clear the file input
            } else {
                feedback.textContent = "";  // Clear error message if valid
            }
        });
    });

    // Handle Form Submission Feedback (Optional)
    document.getElementById('package-form').addEventListener('submit', function(event) {
        const feedback = document.getElementById("form-feedback");
        feedback.textContent = "";  // Clear feedback on form submission
    });

    // Fetch initial packages data
    fetchPackages();
});

// Fetch and display packages
function fetchPackages() {
    fetch("/get_packages")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayPackages(data.packages);
            } else {
                console.error("Error fetching packages:", data.message);
            }
        })
        .catch(error => console.error("Fetch error:", error));
}

// Display the list of packages in the table format
function displayPackages(packages) {
    const packageList = document.getElementById("package-list");
    packageList.innerHTML = ""; // Clear the previous content

    // Creating the table header if it doesn't exist
    if (packageList.children.length === 0) {
        const table = document.createElement("table");
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Package Name</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Duration</th>
                    <th>Type</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="package-body">
            </tbody>
        `;
        packageList.appendChild(table);
    }

    const packageBody = document.getElementById("package-body");

    packages.forEach(pkg => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${pkg.name}</td>
            <td>${pkg.description}</td>
            <td>$${pkg.price}</td>
            <td>${pkg.duration} days</td>
            <td>${pkg.type}</td>
            <td><button onclick="deletePackage(${pkg.id})">Delete</button></td>
        `;

        packageBody.appendChild(row);
    });
}

// Handle package deletion
function deletePackage(packageId) {
    if (confirm("Are you sure you want to delete this package?")) {
        fetch(`/delete_package/${packageId}`, {
            method: "DELETE"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Package deleted successfully.");
                fetchPackages(); // Refresh the package list
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the package.");
        });
    }
}


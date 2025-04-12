// Define interfaces for your data models
interface Pet {
    _id: string;
    name: string;
    species: string;
    breed: string;
    age: number;
    weight: number;
    owner_id?: string;
}

interface Appointment {
    _id: string;
    pet_id: string;
    pet_name: string;
    date: string;
    time: string;
    service_type: string;
    notes?: string;
}

// DOM Element Selectors with proper typing
const petForm = document.getElementById('pet-form') as HTMLFormElement | null;
const appointmentForm = document.getElementById('appointment-form') as HTMLFormElement | null;
const deleteButtons = document.querySelectorAll('.delete-btn') as NodeListOf<HTMLButtonElement>;
const datePicker = document.getElementById('date') as HTMLInputElement | null;
const timePicker = document.getElementById('time') as HTMLInputElement | null;

// Initialize date picker if element exists
if (datePicker) {
    // Add date picker initialization
    // If using a library like flatpickr or datepicker, you'd need to add type definitions
    // Example with flatpickr (would require @types/flatpickr to be installed)
    // flatpickr(datePicker, { minDate: 'today' });
}

// Initialize time picker if element exists
if (timePicker) {
    // Add time picker initialization
}

// Add event listener to pet form with validation
if (petForm) {
    petForm.addEventListener('submit', (e: Event) => {
        const nameInput = document.getElementById('name') as HTMLInputElement;
        const speciesInput = document.getElementById('species') as HTMLInputElement;
        
        if (!nameInput.value.trim() || !speciesInput.value.trim()) {
            e.preventDefault();
            showAlert('Please fill in all required fields', 'danger');
        }
    });
}

// Add event listener to appointment form with validation
if (appointmentForm) {
    appointmentForm.addEventListener('submit', (e: Event) => {
        const petSelect = document.getElementById('pet_id') as HTMLSelectElement;
        const dateInput = document.getElementById('date') as HTMLInputElement;
        const timeInput = document.getElementById('time') as HTMLInputElement;
        
        if (!petSelect.value || !dateInput.value || !timeInput.value) {
            e.preventDefault();
            showAlert('Please fill in all required fields', 'danger');
        }
    });
}

// Set up delete confirmation for delete buttons
deleteButtons.forEach(button => {
    button.addEventListener('click', (e: Event) => {
        if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
});

// Define function to display alert messages
function showAlert(message: string, type: 'success' | 'info' | 'warning' | 'danger'): void {
    const alertContainer = document.getElementById('alert-container');
    
    if (!alertContainer) {
        console.error('Alert container not found');
        return;
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode === alertContainer) {
            alertContainer.removeChild(alert);
        }
    }, 5000);
}

// Function to handle fetching pet details for appointment form
function loadPetDetails(petId: string): void {
    if (!petId) return;
    
    fetch(`/api/pets/${petId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch pet details');
            }
            return response.json();
        })
        .then((pet: Pet) => {
            const petInfoElement = document.getElementById('pet-info');
            if (petInfoElement) {
                petInfoElement.innerHTML = `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${pet.name}</h5>
                            <p class="card-text">
                                <strong>Species:</strong> ${pet.species}<br>
                                <strong>Breed:</strong> ${pet.breed || 'N/A'}<br>
                                <strong>Age:</strong> ${pet.age || 'N/A'}<br>
                            </p>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Initialize pet select change handler
const petSelect = document.getElementById('pet_id') as HTMLSelectElement | null;
if (petSelect) {
    petSelect.addEventListener('change', (e: Event) => {
        const target = e.target as HTMLSelectElement;
        loadPetDetails(target.value);
    });
    
    // Load details for initially selected pet
    if (petSelect.value) {
        loadPetDetails(petSelect.value);
    }
}

// Document ready function
document.addEventListener('DOMContentLoaded', () => {
    // Initialize any Bootstrap components like tooltips or popovers
    const tooltipElements = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        // If using Bootstrap 4/5, you might need to initialize tooltips
        // $(element).tooltip(); // jQuery way
        // or new bootstrap.Tooltip(element); // Bootstrap 5 way
    });
    
    // Handle flash messages auto-dismiss
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 5000);
    });
});
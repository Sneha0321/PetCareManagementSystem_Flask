// Custom JavaScript for PetCare Management System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            // Create a Bootstrap alert instance and hide it
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize date pickers
    const datePickers = document.querySelectorAll('input[type="date"]');
    datePickers.forEach(function(picker) {
        picker.valueAsDate = picker.valueAsDate || new Date();
    });

    // Species-dependent breed suggestions
    const speciesSelect = document.getElementById('species');
    const breedInput = document.getElementById('breed');
    
    if (speciesSelect && breedInput) {
        // Dog breeds
        const dogBreeds = [
            'Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'Bulldog',
            'Beagle', 'Poodle', 'Rottweiler', 'Yorkshire Terrier', 'Boxer', 'Dachshund'
        ];
        
        // Cat breeds
        const catBreeds = [
            'Persian', 'Maine Coon', 'Siamese', 'Ragdoll', 'British Shorthair',
            'Bengal', 'Sphynx', 'Abyssinian', 'Scottish Fold', 'Norwegian Forest Cat'
        ];
        
        // Add datalist for breed suggestions
        const datalist = document.createElement('datalist');
        datalist.id = 'breed-suggestions';
        document.body.appendChild(datalist);
        breedInput.setAttribute('list', 'breed-suggestions');
        
        speciesSelect.addEventListener('change', function() {
            // Clear existing options
            datalist.innerHTML = '';
            
            // Add new breed suggestions based on selected species
            let breedOptions = [];
            if (this.value === 'dog') {
                breedOptions = dogBreeds;
            } else if (this.value === 'cat') {
                breedOptions = catBreeds;
            }
            
            breedOptions.forEach(function(breed) {
                const option = document.createElement('option');
                option.value = breed;
                datalist.appendChild(option);
            });
        });
        
        // Trigger change to load initial breeds
        if (speciesSelect.value) {
            speciesSelect.dispatchEvent(new Event('change'));
        }
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});
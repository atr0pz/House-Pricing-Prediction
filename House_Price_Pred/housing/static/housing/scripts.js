document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('prediction-form');
  const resultDiv = document.getElementById('result');
  const addressSelect = document.getElementById('address');

  // Fetch all addresses and populate the dropdown
  fetch('/api/addresses/')
    .then((response) => response.json())
    .then((data) => {
      data.forEach((address) => {
        const option = document.createElement('option');
        option.value = address;
        option.textContent = address;
        addressSelect.appendChild(option);
      });

      // Initialize searchable dropdown with Tom Select
      new TomSelect('#address', {
        create: false,
        sortField: { field: 'text', direction: 'asc' },
        placeholder: 'Select or search address...',
      });
    })
    .catch((error) => {
      console.error('Error loading addresses:', error);
    });

  // Handle form submission
  form.addEventListener('submit', async function (event) {
    event.preventDefault();

    const data = {
      area: parseFloat(document.getElementById('area').value),
      room: parseInt(document.getElementById('room').value),
      parking: parseInt(document.getElementById('parking').value),
      warehouse: parseInt(document.getElementById('warehouse').value),
      elevator: parseInt(document.getElementById('elevator').value),
      address: document.getElementById('address').value,
    };

    try {
      const response = await fetch('/api/predict/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);
      const result = await response.json();

      resultDiv.textContent = `(USD): $${result.predicted_price_usd.toFixed(2)}
(TOMAN): ${Math.floor(result.predicted_price_usd * 108000).toLocaleString()}`;
    } catch (err) {
      console.error(err);
      resultDiv.textContent =
        'Error: Could not fetch prediction. Make sure to fill the address input.';
    }
  });
});

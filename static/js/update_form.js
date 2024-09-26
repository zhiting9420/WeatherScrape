document.getElementById('update').addEventListener('submit', function(e) {
            e.preventDefault();

            const year = document.getElementById('year').value;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const resultDiv = document.getElementById('result');
            const loadingDiv = document.getElementById('loading');

            resultDiv.className = '';
            resultDiv.textContent = '';
            loadingDiv.style.display = 'block';

            fetch('/update-form/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({year: year})
            })
            .then(response => response.json())
            .then(data => {
                loadingDiv.style.display = 'none';
                resultDiv.textContent = data.message;
                resultDiv.className = data.status === 'success' ? 'success' : 'error';
            })
            .catch(error => {
                loadingDiv.style.display = 'none';
                resultDiv.textContent = '发生错误：' + error;
                resultDiv.className = 'error';
            });
        });
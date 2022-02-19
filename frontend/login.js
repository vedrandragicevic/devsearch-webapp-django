let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()
    
    let formData = {
        'username': form.username.value,
        'password': form.password.value
    }
    
    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body:JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data: ', data.access)
        if (data.access){
            localStorage.setItem('token', data.access)
            // Redirect the user to projects
            window.location = 'file:///E:/Users/Vedran/VS%20Code/django_project/devsearch/frontend/projects-list.html'
        }
        else{
            alert('Username or password did not work!')
        }
    })
})
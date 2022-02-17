
let projectsUrl = 'http://127.0.0.1:8000/api/projects/'

let getProjects = () => {
    fetch(projectsUrl, {
        headers: {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MjEzNjY5LCJpYXQiOjE2NDUxMjcyNjksImp0aSI6ImFhZDEzN2U3N2IyYzRjZGQ4NjM5YWZlM2Q5MjFjNzUyIiwidXNlcl9pZCI6MX0.RHiDxwqRqze0_UJwZ76B-qwyDkwRiQgld8bKyWe3XfI'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        buildProjects(data)
    })
}


let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects--wrapper')

    for(let i=0; projects.length > i; i++){
        let project = projects[i]
        
        let projectCard = `
            <div class="project--card"> 
                <img src="http://127.0.0.1:8000${project.featured_image}" />
                
                <div> 
                    <div class="card--header"> 
                        <h3>${project.title}</h3>
                        <strong class="vote--option">&#43;</strong>
                        <strong class="vote--option">&#8722;</strong>
                    </div>
                    <i>${project.vote_ration}% Positive feedback </i>
                    <p>${project.description.substring(0,150)}</p>
                </div>
            </div>
        `
        projectsWrapper.innerHTML += projectCard
    }
}

getProjects()
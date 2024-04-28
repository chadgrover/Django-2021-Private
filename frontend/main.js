const backendUrl = "http://localhost:8000/api/";
const token = JSON.parse(localStorage.getItem("accessToken"));
const loginButton = document.getElementById("login--button");
const logoutButton = document.getElementById("logout--button");
const loginPage = "login.html";

if (!token) {
  window.location.href = loginPage;
  logoutButton.remove();
}

if (token) {
  loginButton.remove();
}

logoutButton.addEventListener("click", (event) => {
  event.preventDefault();
  localStorage.removeItem("accessToken");
  window.location.href = loginPage;
});

const buildProjects = (projects) => {
  const projectsWrapper = document.getElementById("projects--wrapper");

  for (const project of projects) {
    const projectCard = `
    <div class="project--card">
        <img src="http://localhost:8000/${project.featured_image}" alt="${
      project.title
    }" />
        <div>
            <div class="card--header">
                <h1>${project.title}</h1>
                <strong class="vote--option" data-vote="up" data-project="${
                  project.id
                }" >&#43;</strong>
                <strong class="vote--option" data-vote="down" data-project="${
                  project.id
                }" >&#8722;</strong>
            </div>
            <i>${project.vote_ratio}% Positive Feedback</i>
            <p>${project.description.substring(0, 150)}</p>
        </div>
    </div>`;

    projectsWrapper.innerHTML += projectCard;
  }
};

const getProjects = async () => {
  const data = await fetch(`${backendUrl}projects/`);
  const parsedData = await data.json();
  buildProjects(parsedData);
  addVoteEventListeners();
};

const addVoteEventListeners = () => {
  const voteButtons = document.getElementsByClassName("vote--option");

  for (const button of voteButtons) {
    button.addEventListener("click", async (event) => {
      const typeOfVote = event.target.dataset.vote;
      const projectId = event.target.dataset.project;

      const response = await fetch(`${backendUrl}projects/${projectId}/vote/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          value: typeOfVote,
        }),
      });

      const data = await response.json();

      return data;
    });
  }
};

getProjects();

const backendUrl = "http://localhost:8000/api/";
const form = document.getElementById("login--form");

const getToken = async (formData) => {
  const response = await fetch(`${backendUrl}users/token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const token = await response.json();

  return token;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = {
    username: form.username.value,
    password: form.password.value,
  };

  const token = await getToken(formData);

  if (token.access) {
    await localStorage.setItem("accessToken", JSON.stringify(token.access));

    // You can access relative paths by using window.location.href and no slash at the beginning
    window.location.href = "projects-list.html";
  } else {
    alert("Invalid credentials");
  }
});
